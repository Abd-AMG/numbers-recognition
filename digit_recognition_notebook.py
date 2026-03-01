import os
import joblib
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import warnings

warnings.filterwarnings('ignore')

class DigitRecognitionModel:
    """
    Modular class for handling Digit Recognition ML Models.
    Supports KMeans++, SVM, and Random Forest.
    """
    def __init__(self, model_type="SVM", test_size=0.2):
        self.model_type = model_type
        self.test_size = test_size
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Datasets
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        # Only used for clustering models
        self.cluster_labels = {}
        
    def load_data(self):
        """Loads the MNIST 8x8 dataset from sklearn and applies train/test split."""
        digits = load_digits()
        X = digits.data
        y = digits.target
        
        # Apply scaling
        X_scaled = self.scaler.fit_transform(X)
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_scaled, y, test_size=self.test_size, random_state=42, stratify=y
        )
        return self.X_train, self.X_test, self.y_train, self.y_test

    def get_model_file_name(self):
        return f"saved_model_{self.model_type}.pkl"
    
    def train(self):
        """Trains the selected model architecture."""
        if self.model_type == "KMeans++":
            self.model = KMeans(n_clusters=10, init="k-means++", n_init=10, random_state=42)
            self.model.fit(self.X_train)
            self._map_clusters_to_digits()
        
        elif self.model_type == "SVM":
            self.model = SVC(kernel="rbf", probability=True, random_state=42)
            self.model.fit(self.X_train, self.y_train)
            
        elif self.model_type == "Random Forest":
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(self.X_train, self.y_train)
            
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
            
        self.is_trained = True
        
        # Save model locally
        try:
            joblib.dump({"model": self.model, "scaler": self.scaler, "clusters": self.cluster_labels}, self.get_model_file_name())
        except Exception as e:
            print(f"Warning: Could not save model to disk: {e}")

    def load_saved_model(self):
        """Attempts to load a previously trained model from disk."""
        filename = self.get_model_file_name()
        if os.path.exists(filename):
            data = joblib.load(filename)
            self.model = data["model"]
            self.scaler = data["scaler"]
            self.cluster_labels = data.get("clusters", {})
            self.is_trained = True
            return True
        return False
        
    def _map_clusters_to_digits(self):
        """Maps KMeans clusters to actual digits using training labels."""
        predictions = self.model.labels_
        cluster_to_digit = {}
        
        for cluster_id in range(10):
            mask = predictions == cluster_id
            if mask.sum() > 0:
                most_common_digit = np.bincount(self.y_train[mask]).argmax()
                cluster_to_digit[cluster_id] = most_common_digit
                
        self.cluster_labels = cluster_to_digit

    def evaluate(self):
        """Evaluates the model on test data and returns accuracy and confusion matrix."""
        if not self.is_trained:
            return 0.0, None
            
        if self.model_type == "KMeans++":
            raw_predictions = self.model.predict(self.X_test)
            y_pred = np.array([self.cluster_labels.get(pred, -1) for pred in raw_predictions])
        else:
            y_pred = self.model.predict(self.X_test)
            
        accuracy = accuracy_score(self.y_test, y_pred)
        conf_matrix = confusion_matrix(self.y_test, y_pred)
        
        return accuracy, conf_matrix

    def predict(self, image_array):
        """
        Predicts a single digit.
        Expects an 8x8 flattened image array (shape: (1, 64) or (64,)).
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet.")
            
        image_flat = image_array.flatten().reshape(1, -1)
        image_scaled = self.scaler.transform(image_flat)
        
        top_3 = []
        
        if self.model_type == "KMeans++":
            cluster_id = self.model.predict(image_scaled)[0]
            predicted_digit = self.cluster_labels.get(cluster_id, -1)
            
            # Distance-based confidence
            distance = np.linalg.norm(image_scaled[0] - self.model.cluster_centers_[cluster_id])
            confidence = 1 / (1 + distance) 
            
            # Calculate distances to all centers to get top 3
            distances = []
            for i, center in enumerate(self.model.cluster_centers_):
                dist = np.linalg.norm(image_scaled[0] - center)
                dist_conf = 1 / (1 + dist)
                mapped_digit = self.cluster_labels.get(i, -1)
                distances.append((mapped_digit, dist_conf))
                
            # Sort by confidence
            distances.sort(key=lambda x: x[1], reverse=True)
            
            # Deduplicate mapped digits while keeping highest confidence
            seen_digits = set()
            for d, c in distances:
                if d not in seen_digits and d != -1:
                    seen_digits.add(d)
                    top_3.append({'digit': d, 'probability': c})
                    if len(top_3) == 3:
                        break
                        
            # Normalize pseudo-probabilities for display
            total_score = sum(item['probability'] for item in top_3)
            if total_score > 0:
                for item in top_3:
                    item['probability'] = item['probability'] / total_score
            
            # Override confidence with normalized value
            if top_3:
                confidence = top_3[0]['probability']
                predicted_digit = top_3[0]['digit']

        else:
            predicted_digit = self.model.predict(image_scaled)[0]
            probabilities = self.model.predict_proba(image_scaled)[0]
            confidence = probabilities[predicted_digit]
            
            # Get Top 3
            top_3_indices = np.argsort(probabilities)[-3:][::-1]
            for idx in top_3_indices:
                top_3.append({'digit': int(idx), 'probability': probabilities[idx]})
                
        return predicted_digit, confidence, top_3
