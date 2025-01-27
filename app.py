import streamlit as st 
import os 
from PIL import Image
from io import BytesIO
from tempfile import NamedTemporaryFile
from phi.agent import Agent 
from phi.model.google import Gemini 
from phi.tools.tavily import TavilyTools
from constants import SYSTEM_PROMPT, INSTRUCTIONS

# Set page config first before any other Streamlit commands
st.set_page_config(
    page_title="Product Components Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add some basic styling
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #e0e4ea;
    }
    .upload-box {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .analyze-button {
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

os.environ['TAVILY_API_KEY'] = st.secrets['TAVILY_KEY']
os.environ['GOOGLE_API_KEY'] = st.secrets['GEMINI_KEY']
 
MAX_IMAGE_WIDTH = 350

def resize_image_for_display(image_file):
    """Resize image for display only, returns bytes"""
    if isinstance(image_file, str):
        img = Image.open(image_file)
    else:
        img = Image.open(image_file)
        image_file.seek(0)
    
    aspect_ratio = img.height / img.width
    new_height = int(MAX_IMAGE_WIDTH * aspect_ratio)
    img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

@st.cache_resource
def get_agent():
    return Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        tools=[TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))],
        markdown=True,
    )

def analyze_image(image_path):
    agent = get_agent()
    with st.spinner('🔍 Analyzing ingredients...'):
        response = agent.run(
            "Analyze the given image",
            images=[image_path],
        )
        st.markdown(response.content)

def save_uploaded_file(uploaded_file):
    with NamedTemporaryFile(dir='.', suffix='.jpg', delete=False) as f:
        f.write(uploaded_file.getbuffer())
        return f.name
    
def main():
    st.title("🔍 Product Components Analyzer")
    st.markdown("### Discover what's in your products")
    
    if 'selected_example' not in st.session_state:
        st.session_state.selected_example = None
    if 'analyze_clicked' not in st.session_state:
        st.session_state.analyze_clicked = False
    
    tab_examples, tab_upload, tab_camera = st.tabs([
        "📚 Example Products", 
        "📤 Upload Image", 
        "📸 Take Photo"
    ])
    
    with tab_examples:
        example_images = {
            "🍫 Chocolate Bar": "images/chocolate_bar.jpg",
            "🥤 Energy Drink": "images/Amul Pro.jpg",
            "🥔 Potato Chips": "images/potato chips.jpg",
            "🧴 Shampoo": "images/shampoo.jpg"
        }
        
        cols = st.columns(4)
        for idx, (name, path) in enumerate(example_images.items()):
            with cols[idx]:
                if st.button(name, use_container_width=True):
                    st.session_state.selected_example = path
                    st.session_state.analyze_clicked = False
    
    with tab_upload:
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload product image", 
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the product's ingredient list"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file:
            resized_image = resize_image_for_display(uploaded_file)
            st.image(resized_image, caption="Uploaded Image", use_container_width=False, width=MAX_IMAGE_WIDTH)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("🔍 Analyze Uploaded Image", key="analyze_upload", type="primary", use_container_width=True):
                    temp_path = save_uploaded_file(uploaded_file)
                    analyze_image(temp_path)
                    os.unlink(temp_path) 
    
    with tab_camera:
        camera_photo = st.camera_input("Take a picture of the product")
        if camera_photo:
            resized_image = resize_image_for_display(camera_photo)
            st.image(resized_image, caption="Captured Photo", use_container_width=False, width=MAX_IMAGE_WIDTH)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("🔍 Analyze Captured Photo", key="analyze_camera", type="primary", use_container_width=True):
                    temp_path = save_uploaded_file(camera_photo)
                    analyze_image(temp_path)
                    os.unlink(temp_path) 
    
    if st.session_state.selected_example:
        st.divider()
        st.subheader("Selected Product")
        resized_image = resize_image_for_display(st.session_state.selected_example)
        st.image(resized_image, caption="Selected Example", use_container_width=False, width=MAX_IMAGE_WIDTH)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🔍 Analyze Example", key="analyze_example", type="primary", use_container_width=True) and not st.session_state.analyze_clicked:
                st.session_state.analyze_clicked = True
                analyze_image(st.session_state.selected_example)

if __name__ == "__main__":
    main()