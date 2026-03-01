Digit & Text Recognition Application
====================================

A professional application that combines handwritten digit classification and multilingual text recognition with a clean and user-friendly interface.

Overview
--------

This project was developed as part of a laboratory continuation project in Image Processing. It integrates image preprocessing, unsupervised learning, and interactive web deployment using Streamlit.

The application includes:

*   Handwritten digit classification using K-means clustering
    
*   Image binarization with adjustable thresholding
    
*   Text recognition and analysis in multiple languages
    
*   Interactive web interface for experimentation and demonstration
    

Main Features
-------------

### 1\. Digit Classification

*   Uses K-means clustering with 10 clusters
    
*   Applies image binarization before training and prediction
    
*   Includes data normalization using StandardScaler
    
*   Provides prediction confidence estimation
    

Input methods:

*   Upload handwritten digit image
    
*   Draw digit directly in the application
    
*   Select a sample from the MNIST dataset
    

Output information:

*   Predicted digit
    
*   Cluster ID
    
*   Confidence score
    

### 2\. Text Recognition and Analysis

Supports:

*   Arabic
    
*   French
    
*   English
    

Input methods:

*   Direct text input
    
*   Upload image containing text
    

Text analysis includes:

*   Character count
    
*   Word count
    
*   Unique word count
    
*   Average word length
    

### 3\. Model Information Section

Displays:

*   Model details
    
*   Training process explanation
    
*   Performance statistics
    
*   Mapping between clusters and real digits
    

Project Structure
-----------------

`   digit_text_app/├── streamlit_app.py├── digit_recognition_notebook.py├── requirements.txt├── README.md└── advanced_notebook.ipynb   `

Libraries Used
--------------

*   Streamlit 1.28.1 – Web interface
    
*   Scikit-learn 1.3.0 – Machine learning and clustering
    
*   OpenCV 4.8.0 – Image processing
    
*   NumPy 1.24.3 – Numerical operations
    
*   Matplotlib 3.7.2 – Visualization
    
*   Pillow 10.0.0 – Image handling
    

Installation
------------

Requirements:

*   Python 3.8 or higher
    
*   pip
    

Steps:

1.  Navigate to the project folder:
    
`   cd digit_text_app   `

1.  Install required libraries:
    
`   pip install -r requirements.txt   `

1.  Run the application:
    
`   streamlit run streamlit_app.py   `

1.  Open in browser:
    

`   http://localhost:8501   `

Classification Pipeline
-----------------------

Raw Data↓Image Binarization↓Data Normalization (StandardScaler)↓K-means Training (10 clusters)↓Cluster-to-digit mapping↓Prediction

Image Binarization
------------------

Each image is converted into a binary image using a threshold:

`   binary_image = (image > threshold).astype(np.uint8)   `

Benefits:

*   Noise reduction
    
*   Simpler feature representation
    
*   Improved clustering stability
    

K-means Clustering
------------------

Model initialization:

`   kmeans = KMeans(n_clusters=10, random_state=42)kmeans.fit(X_scaled)   `

Process:

1.  Initialize 10 cluster centers
    
2.  Assign each data point to the nearest center
    
3.  Update cluster centers
    
4.  Repeat until convergence
    

Confidence Calculation
----------------------

Confidence is computed using the distance between the input image and the cluster center:

`   distance = ||image - cluster_center||confidence = 1 / (1 + distance)   `

Smaller distance results in higher confidence.

Performance
-----------

*   Accuracy: approximately 85–90% on MNIST dataset
    
*   Single digit prediction time: less than 100 ms
    
*   Text analysis time: less than 50 ms
    
*   Model loading time: 2–3 seconds
    

Performance depends on input image quality.

Possible Improvements
---------------------

Model improvements:

*   Replace K-means with SVM or Neural Networks
    
*   Use pre-trained deep learning models
    

Preprocessing improvements:

*   Advanced image enhancement techniques
    
*   Data augmentation
    

Parameter tuning:

*   Optimize binarization threshold
    
*   Adjust number of clusters
    

Additional features:

*   Save results to CSV or JSON
    
*   Add confusion matrix visualization
    
*   Support additional languages
    

Troubleshooting
---------------

Application is slow:

*   Check installed dependencies
    
*   Restart the app
    
*   Verify CPU and RAM availability
    

Incorrect digit prediction:

*   Ensure image clarity
    
*   Use similar resolution to training data (8x8)
    
*   Adjust binarization threshold
    

Library import error:

`   pip install --upgrade -r requirements.txt   `

Educational Value
-----------------

This project demonstrates:

*   Image preprocessing techniques
    
*   Binary image transformation
    
*   Unsupervised learning with K-means
    
*   Cluster-to-label mapping
    
*   Confidence estimation
    
*   Interactive web application development using Streamlit
    
*   Basic text analysis
    

License
-------

This project is open-source and free to use.

Version
-------

Version: 1.0.0Year: 2026
