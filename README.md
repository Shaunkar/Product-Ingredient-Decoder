# Product Ingredient Agent 🔍

A **Multimodal Agentic Workflow** powered by **Phidata**.  
This is a **Streamlit application** that analyzes product ingredients using **Gemini AI**, providing insights about food and personal care products.

---

## 🌟 Features
- **Example Products**: Pre-loaded examples of common products.
- **Image Upload**: Upload your own product images for analysis.
- **Camera Capture**: Take photos directly through the app.
- **AI Analysis**: Powered by **Google's Gemini 2.0 Flash** and **Tavily Search**.
- **Ingredient Insights**: Receive detailed ingredient analysis and implications.

---

## 🚀 Installation

### Clone the repository:
```bash
git clone https://github.com/yourusername/Product-Ingredient-Agent.git
cd Product-Ingredient-Agent
```

### Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

1. Create a `.env` file in the project root and add the following keys:
   ```plaintext
   TAVILY_API_KEY = your_tavily_api_key
   GOOGLE_API_KEY = your_gemini_api_key
   ```
2. Add your example images in the `images/` directory:
   ```plaintext
   images/
   ├── chocolate_bar.jpg
   ├── Amul Pro.jpg
   ├── potato chips.jpg
   └── shampoo.jpg
   ```

---

## 💡 Usage

### Run the Streamlit app:
```bash
streamlit run app.py
```

### Access the app:
- Open your browser and navigate to: **[http://localhost:8501](http://localhost:8501)**

### Analyze a product:
1. Select from example products.
2. Upload your own image.
3. Take a photo using your camera.

---

## 📁 Project Structure
```plaintext
product-ingredient-analyzer/
├── app.py                 # Main Streamlit application
├── constants.py           # System prompts and constants
├── requirements.txt       # Project dependencies
├── images/                # Example product images
└── README.md              # Project documentation
```

---

## 📚 Dependencies
- `streamlit`
- `phidata`
- `pillow`
- `tavily-python`
- `google-generativeai`

---

## 🤝 Contributing
⭐️ **STAR the Phidata repository**: [https://github.com/phidatahq/phidata](https://github.com/phidatahq/phidata)

---

## 📄 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👏 Acknowledgments
- **Phidata** for building the Multimodal Agent.
- **Google Gemini AI** for powering the analysis.
- **Streamlit** for the web interface.
- **Tavily** for search capabilities.
