import cv2
import numpy as np

def segment_digits(image):
    """
    Segments an image containing multiple digits into individual digits.
    Returns a list of 8x8 flattened arrays and a list of bounds (x, y, w, h).
    """
    if len(image.shape) == 3:
        if image.shape[2] == 4: # Handle RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()
        
    border_pixels = np.concatenate([gray[0,:], gray[-1,:], gray[:,0], gray[:,-1]])
    if np.mean(border_pixels) > 127:
        gray = cv2.bitwise_not(gray)

    # Adaptive Thresholding & morphological ops to thicken digits (sklearn digits are very thick/pixelated)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Sklearn digits are thick (8x8 grid). We need to dilate our high-res lines so they don't vanish or get confusing during downscale.
    kernel = np.ones((10, 10), np.uint8)  
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_rects = []
    min_area = (image.shape[0] * image.shape[1]) * 0.001 
    
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        # Relax aspect ratio filter entirely or keep it very wide to allow generic handwriting
        if area > min_area and h > 10: 
            valid_rects.append((x, y, w, h))
            
    valid_rects = sorted(valid_rects, key=lambda b: b[0])
    
    processed_digits = []
    bounding_boxes = []
    
    for (x, y, w, h) in valid_rects:
        # Increase padding slightly so it sits safely in the 8x8 frame center natively
        pad = int(max(w, h) * 0.35)
        
        side_len = max(w, h) + 2*pad
        
        center_x = x + w//2
        center_y = y + h//2
        
        x_start = max(0, center_x - side_len//2)
        y_start = max(0, center_y - side_len//2)
        x_end = min(gray.shape[1], center_x + side_len//2)
        y_end = min(gray.shape[0], center_y + side_len//2)
        
        roi = thresh[y_start:y_end, x_start:x_end]
        
        # We need a perfectly square image before downscaling
        square_roi = np.zeros((side_len, side_len), dtype=np.uint8)
        
        actual_h, actual_w = roi.shape
        start_y = (side_len - actual_h) // 2
        start_x = (side_len - actual_w) // 2
        
        if actual_h > 0 and actual_w > 0:
            square_roi[start_y:start_y+actual_h, start_x:start_x+actual_w] = roi

        # OpenCV Area works well for compression
        roi_resized = cv2.resize(square_roi, (8, 8), interpolation=cv2.INTER_AREA)
        
        # Scale 0-255 -> 0-16
        roi_scaled = (roi_resized / 255.0) * 16.0
        
        processed_digits.append(roi_scaled.flatten())
        bounding_boxes.append((x, y, w, h))
        
    return processed_digits, bounding_boxes

def preprocess_single_image(image):
    """
    Standardizes a single drawn or uploaded digit.
    Pads it squarely, thickens the ink natively, resizes to 8x8, and scales to 0-16.
    """
    if len(image.shape) == 3:
        if image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()
        
    # Check background lightness
    border_pixels = np.concatenate([gray[0,:], gray[-1,:], gray[:,0], gray[:,-1]])
    if np.mean(border_pixels) > 127:
        gray = cv2.bitwise_not(gray)
        
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Sklearn images are VERY thick. We need to dilate.
    # The canvas is 200x200 usually, so a nice big kernel makes drawn lines fat.
    kernel = np.ones((15, 15), np.uint8)  
    thresh = cv2.dilate(thresh, kernel, iterations=1)
        
    coords = cv2.findNonZero(thresh)
    if coords is None:
        return np.zeros(64), np.zeros((8, 8))
        
    x, y, w, h = cv2.boundingRect(coords)
    
    pad_len = max(w, h)
    # Huge padding forces the number to be small in the center, mimicking Sklearn perfectly
    pad = int(pad_len * 0.40) 
    
    roi = thresh[y:y+h, x:x+w]
    
    side_len = pad_len + 2*pad
    square_img = np.zeros((side_len, side_len), dtype=np.uint8)
    
    start_x = pad + (pad_len - w)//2
    start_y = pad + (pad_len - h)//2
    
    square_img[start_y:start_y+h, start_x:start_x+w] = roi
    
    img_resized = cv2.resize(square_img, (8, 8), interpolation=cv2.INTER_AREA)
    img_scaled = (img_resized / 255.0) * 16.0
    
    return img_scaled.flatten(), img_resized
