# ESI PROJECT: Advanced Real-Time Sign Language Recognition System

## 📋 Project Overview

This is a comprehensive **Embedded System with Intelligence (ESI)** project that recognizes Indian Sign Language (ISL) alphabets (A-Z) in real-time using:

- **Deep Learning**: MobileNetV2 pre-trained model
- **Hand Detection**: MediaPipe for robust hand keypoint detection
- **Smart Filtering**: Intelligent prediction filtering based on detected hand count
- **Real-time Processing**: Optimized for webcam input
- **Professional UI**: Streamlit-based interactive application

## 🎯 Key Features

### 1. **High Accuracy Model**
- MobileNetV2 architecture with custom head
- Transfer learning from ImageNet pre-trained weights
- Batch normalization and dropout for regularization
- Target validation accuracy: >90%

### 2. **Hand Detection (0, 1, or 2 Hands)**
- MediaPipe Hands for robust detection
- 21-point hand skeleton keypoint detection
- Real-time processing at camera frame rate

### 3. **Smart Prediction Filtering**
- **Single-Hand Gestures** (1 hand required): C, I, L, O, U, V
- **Dual-Hand Gestures** (2 hands required): A, B, D, E, F, G, H, J, K, M, N, P, Q, R, S, T, W, X, Y, Z
- Predictions filtered based on detected hand count to eliminate false positives

### 4. **Prediction Stabilization**
- Majority voting over last 5 predictions
- Prevents flickering in real-time display
- Smooth user experience

### 5. **Professional Streamlit UI**
- Live webcam feed with hand landmarks visualization
- Real-time prediction display with confidence score
- Prediction history tracking
- Settings for confidence threshold adjustment
- Comprehensive instructions and gesture guide

## 📁 Project Structure

```
D:\ESI MODEL\
├── train.py                    # Training script
├── app.py                      # Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── model/
    ├── mobilenet_model.h5      # Best trained model (generated)
    ├── mobilenet_model_final.h5 # Final model (generated)
    └── training_history.png    # Training plot (generated)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Webcam (for real-time prediction)
- GPU support (optional but recommended for faster training)
- Dataset at `D:\Real time Sign Language\dataset` with train/validation folders

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Train the Model

```bash
python train.py
```

**What happens during training:**
- Loads training data from `D:\Real time Sign Language\dataset\train`
- Loads validation data from `D:\Real time Sign Language\dataset\validation`
- Creates and trains MobileNetV2 model
- Applies data augmentation (rotation, zoom, shear, flip)
- Uses callbacks: EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
- Saves best model to `model/mobilenet_model.h5`
- Displays training history plot

**Expected output:**
```
Number of GPUs available: 1
✓ GPU memory growth enabled
✓ Dataset folders verified
✓ Training data loaded with augmentation
  - Rotation: 20°
  - Zoom: 20%
  - Shear: 20%
  - Horizontal flip: enabled

Training samples: XXXX
Validation samples: XXXX
Classes: 26

STARTING TRAINING...
[Training progress...]

Final Training Accuracy: 0.XXXX
Final Training Loss: X.XXXX
Final Validation Accuracy: 0.XXXX
Final Validation Loss: X.XXXX

✓ TARGET ACHIEVED: Validation accuracy > 90%
✓ Best model saved to: model/mobilenet_model.h5
```

### Step 3: Run the Streamlit Application

```bash
streamlit run app.py
```

**What the app does:**
- Loads the trained model
- Initializes MediaPipe Hands detector
- Opens webcam feed
- Displays real-time predictions
- Shows hand count and confidence score
- Maintains prediction history

## 🎮 Using the Application

### Interface Elements

**Sidebar:**
- Instructions for using the system
- Single-hand gesture reference (C, I, L, O, U, V)
- Dual-hand gesture reference (remaining alphabets)
- Confidence threshold slider
- Tips for better accuracy

**Main Area:**
- **Live Feed**: Real-time webcam video with hand landmarks
- **Prediction**: Current predicted letter
- **Confidence**: Prediction confidence score (0-100%)
- **Hand Count**: Number of detected hands (0, 1, or 2)
- **Prediction History**: Recent 10 predictions

### How to Get Best Results

1. **Lighting**: Ensure good, uniform lighting
2. **Hand Position**: Keep hands clearly visible in frame
3. **Gesture Clarity**: Make distinct, clear gestures
4. **Hold Steady**: Hold gesture for ~1-2 seconds for stable prediction
5. **Hand Count**: Use correct number of hands for gesture
   - Single-hand gestures: Use 1 hand only
   - Dual-hand gestures: Use both hands

## 📊 Model Architecture

```
Input: 224x224x3 Image
  ↓
MobileNetV2 (Pretrained on ImageNet)
  ↓
GlobalAveragePooling2D
  ↓
Dense(128, activation='relu')
  ↓
Dropout(0.5)
  ↓
Dense(26, activation='softmax')
  ↓
Output: 26 classes (A-Z)
```

## 🧠 Smart Prediction Filtering Logic

```python
# DOMAIN LOGIC: Based on detected hand count

if num_hands == 1:
    # Allow ONLY: C, I, L, O, U, V
    # Zero out all other predictions
    
elif num_hands == 2:
    # Allow ONLY: A, B, D, E, F, G, H, J, K, M, N, P, Q, R, S, T, W, X, Y, Z
    # Zero out single-hand predictions
    
else:  # num_hands == 0 or other
    # Invalid: Return no prediction
    # Inform user to show hand
```

## 🔧 Configuration Options

### In `train.py`:
- `IMG_SIZE`: Target image size (default: 224)
- `BATCH_SIZE`: Training batch size (default: 32)
- `epochs`: Number of training epochs (default: 50)
- Augmentation parameters: rotation, zoom, shear ranges

### In `app.py`:
- Hand detection confidence: Adjustable in sidebar
- Stabilization window: Number of frames for majority voting (default: 5)
- Confidence threshold: Slider in sidebar (0.0 - 1.0, default: 0.7)

## 🚨 Troubleshooting

### "Model not found" Error
- Run `train.py` first to generate the model
- Ensure model files are saved in `model/` folder

### "Cannot access webcam" Error
- Check webcam permissions
- Ensure webcam is not being used by other applications
- Try restarting the app

### Low Prediction Accuracy
- Improve lighting conditions
- Ensure clear hand visibility
- Hold gesture steady for 1-2 seconds
- Check that you're using the correct hand count for gesture

### GPU Not Being Used
- Install CUDA toolkit and cuDNN
- Reinstall TensorFlow: `pip install tensorflow[and-cuda]`
- Verify with GPU detection output in training script

### Slow Inference
- Close other applications to free up resources
- For CPU-only machines, inference is naturally slower
- Consider using GPU for better performance

## 📈 Performance Metrics

**Model Performance:**
- Parameters: ~3.5M (MobileNetV2)
- Training time: ~30-60 minutes (GPU) / 2-4 hours (CPU)
- Inference time: ~50-100ms per frame (GPU) / 200-500ms (CPU)
- Expected accuracy: >90% on validation set

**Hand Detection:**
- Detection confidence: 0.7 (adjustable)
- Tracking frames: ~5-10 frames
- Supports up to 2 hands simultaneously

## 🎓 Embedded Intelligence System (EIS) Concepts Implementation

### **E – Embedded**

- Webcam used as an input device
- Real-time continuous video capture
- Frame-by-frame data acquisition

### **I – Intelligence**

- Deep learning model (MobileNetV2) for gesture recognition
- Hand landmark detection using MediaPipe
- Intelligent prediction filtering and stabilization

### **S – System**

- Real-time Indian Sign Language recognition system
- Continuous processing and translation pipeline
- Smooth and stable output generation

### **Optimization**

- Lightweight MobileNetV2 for efficient inference
- TensorFlow memory optimization
- Reuse of loaded model and detector
- Prediction filtering to improve accuracy

## 📝 License

This project is created for educational purposes as part of an advanced embedded systems course.

## ✅ Checklist for Submission

- [x] Model training script (train.py)
- [x] Real-time application (app.py)
- [x] Hand detection integration
- [x] Smart prediction filtering
- [x] Professional Streamlit UI
- [x] Prediction stabilization
- [x] ESI concept comments
- [x] Comprehensive documentation
- [x] Requirements.txt with dependencies
- [ ] Trained model (generate by running train.py)

## 🎯 Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Prepare dataset at specified location
3. Run training: `python train.py`
4. Wait for model training to complete (check for >90% accuracy)
5. Launch app: `streamlit run app.py`
6. Test with real sign language gestures

---

**Project Status**: Ready for Deployment ✓

For questions or issues, please refer to the troubleshooting section or review the code comments for detailed implementation details.
