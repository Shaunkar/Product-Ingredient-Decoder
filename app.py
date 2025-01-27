import streamlit as st 
import os 
from PIL import Image
from io import BytesIO
from tempfile import NamedTemporaryFile
from phi.agent import Agent 
from phi.model.google import Gemini 
from phi.tools.tavily import TavilyTools
from constants import SYSTEM_PROMPT, INSTRUCTIONS

# Configure environment variables from Streamlit secrets
os.environ['TAVILY_API_KEY'] = st.secrets['TAVILY_KEY']
os.environ['GOOGLE_API_KEY'] = st.secrets['GEMINI_KEY']

# Constants
MAX_IMAGE_WIDTH = 350

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton button {
        width: 100%;
    }
    .analysis-container {
        border: 1px solid #f0f0f0;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def resize_image_for_display(image_file):
    """Resize image for display while maintaining aspect ratio"""
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
    """Initialize and cache the Gemini agent"""
    return Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        tools=[TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))],
        markdown=True,
    )

def analyze_image(image_path):
    """Analyze image using the Gemini agent"""
    agent = get_agent()
    with st.spinner('🔍 Analyzing product details...'):
        try:
            response = agent.run(
                "Analyze the given image in detail, focusing on ingredients, nutrition, and safety information.",
                images=[image_path],
            )
            with st.container():
                st.markdown("### 📊 Analysis Results")
                st.markdown(response.content)
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary location"""
    try:
        with NamedTemporaryFile(dir='.', suffix='.jpg', delete=False) as f:
            f.write(uploaded_file.getbuffer())
            return f.name
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None

def create_example_card(name, path, col):
    """Create a card for example products"""
    with col:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        if st.button(name, use_container_width=True):
            st.session_state.selected_example = path
            st.session_state.analyze_clicked = False
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.title("🔍 Product Components Analyzer")
    st.markdown("### Analyze ingredients and components of various products")
    
    # Initialize session state
    if 'selected_example' not in st.session_state:
        st.session_state.selected_example = None
    if 'analyze_clicked' not in st.session_state:
        st.session_state.analyze_clicked = False
    
    # Create tabs
    tab_examples, tab_upload, tab_camera = st.tabs([
        "📚 Example Products", 
        "📤 Upload Image", 
        "📸 Take Photo"
    ])
    
    # Example Products Tab
    with tab_examples:
        st.markdown("### Select a sample product to analyze")
        example_images = {
            "🍫 Chocolate Bar": "images/chocolate_bar.jpg",
            "🥤 Energy Drink": "images/Amul Pro.jpg",
            "🥔 Potato Chips": "images/potato chips.jpg",
            "🧴 Shampoo": "images/shampoo.jpg"
        }
        
        cols = st.columns(4)
        for idx, (name, path) in enumerate(example_images.items()):
            create_example_card(name, path, cols[idx])
    
    # Upload Image Tab
    with tab_upload:
        st.markdown("### Upload a product image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the product's ingredient list or label"
        )
        
        if uploaded_file:
            try:
                resized_image = resize_image_for_display(uploaded_file)
                st.image(resized_image, caption="Uploaded Image", use_container_width=False, width=MAX_IMAGE_WIDTH)
                if st.button("🔍 Analyze Uploaded Image", key="analyze_upload", type="primary"):
                    temp_path = save_uploaded_file(uploaded_file)
                    if temp_path:
                        analyze_image(temp_path)
                        os.unlink(temp_path)
            except Exception as e:
                st.error(f"Error processing uploaded image: {str(e)}")
    
    # Camera Input Tab
    with tab_camera:
        st.markdown("### Take a photo of the product")
        camera_photo = st.camera_input(
            "Take a picture",
            help="Position the product label clearly in the frame"
        )
        
        if camera_photo:
            try:
                resized_image = resize_image_for_display(camera_photo)
                st.image(resized_image, caption="Captured Photo", use_container_width=False, width=MAX_IMAGE_WIDTH)
                if st.button("🔍 Analyze Captured Photo", key="analyze_camera", type="primary"):
                    temp_path = save_uploaded_file(camera_photo)
                    if temp_path:
                        analyze_image(temp_path)
                        os.unlink(temp_path)
            except Exception as e:
                st.error(f"Error processing captured photo: {str(e)}")
    
    # Display selected example
    if st.session_state.selected_example:
        st.divider()
        with st.container():
            st.subheader("Selected Product")
            try:
                resized_image = resize_image_for_display(st.session_state.selected_example)
                st.image(resized_image, caption="Selected Example", use_container_width=False, width=MAX_IMAGE_WIDTH)
                
                if st.button("🔍 Analyze Example", key="analyze_example", type="primary") and not st.session_state.analyze_clicked:
                    st.session_state.analyze_clicked = True
                    analyze_image(st.session_state.selected_example)
            except Exception as e:
                st.error(f"Error processing example image: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>📸 For best results, ensure product labels are clearly visible in images</p>
            <p>⚠️ This tool provides general information only. Always verify with the actual product packaging.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Product Components Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()