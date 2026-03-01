import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from digit_recognition_notebook import DigitRecognitionModel
from utils.cv_segmentation import segment_digits, preprocess_single_image
from streamlit_drawable_canvas import st_canvas

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DigitAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CACHING ---
@st.cache_resource(show_spinner="Loading and Training Model...")
def load_and_train_model(model_name, test_size):
    """
    Initializes, loads data, and either loads from disk or trains the model.
    Cached to prevent retraining on every prediction.
    """
    model = DigitRecognitionModel(model_type=model_name, test_size=test_size)
    model.load_data()
    
    # Try to load existing local model if settings match, else train 
    # (Since we change test_size, we enforce retraining if not matching, 
    # but for simplicity we'll just train once per (model_name, test_size) combination)
    model.train() # Always retrain for the specific session configuration, it is fast on MNIST 8x8
    return model

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .prediction-card {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #333;
        margin-bottom: 10px;
    }
    .big-digit {
        font-size: 4rem;
        font-weight: 800;
        color: #4da6ff;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("🤖 DigitAI")
st.sidebar.markdown("Professional Handwritten Digit Recognition Platform.")

st.sidebar.markdown("### ⚙️ Model Configuration")
selected_model = st.sidebar.selectbox(
    "Select Model Architecture:",
    ["Support Vector Machine (SVM)", "Random Forest", "KMeans++"]
)

# Map UI name to Class name
model_map = {
    "Support Vector Machine (SVM)": "SVM",
    "Random Forest": "Random Forest",
    "KMeans++": "KMeans++"
}
active_model_name = model_map[selected_model]

test_split = st.sidebar.slider(
    "Train/Test Split:",
    min_value=0.70,
    max_value=0.90,
    value=0.80,
    step=0.05,
    help="Define the percentage of data used for training vs testing."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 About this Model")
if active_model_name == "SVM":
    st.sidebar.info("**SVM (RBF Kernel)**\n\nHigh-accuracy supervised model. Standardized inputs to maximize margin representation. Recommended for primary use. Expected Accuracy: >95%")
elif active_model_name == "Random Forest":
    st.sidebar.info("**Random Forest**\n\nEnsemble learning method operating by constructing multiple decision trees. Highly stable. Expected Accuracy: 94-97%")
else:
    st.sidebar.info("**KMeans++**\n\nUnsupervised clustering algorithm. Groups data into 10 clusters dynamically. Expected Accuracy: 75-85%")
    
st.sidebar.markdown("---")
st.sidebar.caption("v2.0 - Final Execution")

# Load model using the cached function
active_model = load_and_train_model(active_model_name, round(1.0 - test_split, 2))

# --- MAIN CONTENT ---
st.title("🔢 Digit Analysis Terminal")

tab1, tab2, tab3 = st.tabs(["✍️ Single Digit", "📸 Multi-Digit", "📊 Model Analytics"])

# ---------- TAB 1: SINGLE DIGIT ----------
with tab1:
    st.markdown("### Predict a Single Digit")
    st.markdown("Upload a clear image of a single digit, or draw one on the canvas.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        input_type = st.radio("Input Method:", ["Draw Digit", "Upload Image"], horizontal=True)
        
        image_to_predict = None
        
        if input_type == "Upload Image":
            uploaded_file = st.file_uploader("Choose a digit image (PNG, JPG)", type=["png", "jpg", "jpeg"])
            if uploaded_file:
                # Read as standard Image
                image_pil = Image.open(uploaded_file).convert('L')
                st.image(image_pil, caption="Uploaded Image", width=150)
                image_to_predict = np.array(image_pil)
                
                # Invert if the background is light
                if np.mean(image_to_predict) > 127:
                    image_to_predict = cv2.bitwise_not(image_to_predict)
                
        else:
            st.markdown("Draw inside the box:")
            canvas_result = st_canvas(
                fill_color="black",
                stroke_width=15,
                stroke_color="white",
                background_color="black",
                height=200,
                width=200,
                drawing_mode="freedraw",
                key="canvas",
            )
            if canvas_result.image_data is not None:
                # Convert RGBA to Grayscale
                image_to_predict = cv2.cvtColor(canvas_result.image_data, cv2.COLOR_RGBA2GRAY)
                # Only predict if canvas actually has drawings
                if np.sum(image_to_predict) == 0:
                    image_to_predict = None

    with col2:
        if image_to_predict is not None:
            # Preprocess the single image for Sklearn constraints
            img_scaled, img_resized = preprocess_single_image(image_to_predict)
            
            st.markdown("### Processed Input (8x8)")
            st.image(img_resized, width=150)
            
            # Predict only if we found contours (not entirely blank)
            if np.sum(img_scaled) == 0:
                st.warning("Please draw a clear digit.")
            elif st.button("Predict 🚀", type="primary", use_container_width=True):
                predicted_digit, confidence, top_3 = active_model.predict(img_scaled)
                
                st.markdown(f"""
                <div class="prediction-card">
                    <p style="margin:0; color:#888;">Detected Digit</p>
                    <p class="big-digit">{predicted_digit}</p>
                    <p style="margin:0; color:#ccc;">Confidence: <strong>{confidence*100:.1f}%</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                if top_3:
                    st.markdown("#### Top 3 Predictions")
                    for i, t in enumerate(top_3):
                        st.progress(float(t['probability']), text=f"Digit {t['digit']} ({t['probability']*100:.1f}%)")


# ---------- TAB 2: MULTI-DIGIT ----------
with tab2:
    st.markdown("### Multi-Digit Extraction Pipeline")
    st.markdown("Upload a photo containing a sequence of handwritten digits spaced apart (e.g. `1 2 3`). The system will segment and evaluate each digit.")
    
    multi_file = st.file_uploader("Choose an image with multiple digits", type=["png", "jpg", "jpeg"], key="multi_upload")
    
    if multi_file:
        file_bytes = np.asarray(bytearray(multi_file.read()), dtype=np.uint8)
        image_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Segment digits
        extracted_digits, bboxes = segment_digits(image_cv)
        
        st.markdown("---")
        
        if len(extracted_digits) == 0:
            st.error("No clear digits detected. Try again with a clearer image or darker ink.")
        else:
            colA, colB = st.columns([1.5, 1])
            
            with colA:
                st.markdown("#### 1. Segmentation Visualized")
                # Draw boxes
                vis_img = image_cv.copy()
                
                # Draw individual boxes in light green
                for (x, y, w, h) in bboxes:
                    cv2.rectangle(vis_img, (x, y), (x+w, y+h), (100, 255, 100), 2)
                    
                # Draw the main frame around all detected digits
                if len(bboxes) > 0:
                    min_x = min(b[0] for b in bboxes)
                    min_y = min(b[1] for b in bboxes)
                    max_x = max(b[0] + b[2] for b in bboxes)
                    max_y = max(b[1] + b[3] for b in bboxes)
                    
                    # Draw sequence bounding frame in thick Red
                    cv2.rectangle(vis_img, (min_x-5, min_y-5), (max_x+5, max_y+5), (0, 0, 255), 4)
                    cv2.putText(vis_img, "Detected Sequence", (min_x, max(0, min_y-10)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                vis_rgb = cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB)
                st.image(vis_rgb, caption=f"Found {len(bboxes)} elements", use_container_width=True)
                
            with colB:
                st.markdown("#### 2. Model Evaluation")
                
                final_sequence = ""
                
                for idx, digit_flat in enumerate(extracted_digits):
                    pred, conf, _ = active_model.predict(digit_flat)
                    final_sequence += str(pred)
                    
                    st.markdown(f"**Box {idx+1}:** `Digit {pred}` _({conf*100:.1f}%)_")
                
                st.markdown("---")
                st.success(f"### Detected Sequence:\n# {final_sequence}")


# ---------- TAB 3: ANALYTICS ----------
with tab3:
    st.markdown("### Global Model Analytics")
    
    acc, conf_matrix = active_model.evaluate()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Accuracy", f"{acc*100:.2f}%")
    col2.metric("Dataset Size", f"{len(active_model.X_train)} train / {len(active_model.X_test)} test")
    col3.metric("Input Dimensions", "8x8 normalized")
    
    st.markdown("---")
    
    if conf_matrix is not None:
        st.markdown("#### Confusion Matrix")
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Display Heatmap
        cax = ax.matshow(conf_matrix, cmap=plt.cm.Blues)
        fig.colorbar(cax)
        
        for i in range(10):
            for j in range(10):
                c = conf_matrix[j, i]
                ax.text(i, j, str(c), va='center', ha='center', color='white' if c > conf_matrix.max()/2 else 'black')
                
        ax.set_xlabel('Predicted Digit')
        ax.set_ylabel('True Digit')
        ax.set_xticks(range(10))
        ax.set_yticks(range(10))
        
        # Streamlit implicitly supports Matplotlib figs
        st.pyplot(fig)
        
    st.markdown("#### Test Pipeline Overview")
    st.info("The digits dataset contains 1,797 samples. We dynamically split this into Training and Testing datasets based on the sidebar slider. Performance metrics shown here reflect evaluation against the unseen test subset in the current session.")
