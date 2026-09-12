# ⚙️ CONFIGURATION GUIDE
## ESI Project: Real-Time Sign Language Recognition System

This guide explains all configurable parameters in the system.

---

## 🎯 train.py Configuration

### Dataset Paths
```python
# Line ~60
DATASET_PATH = r"D:\Real time Sign Language\dataset"
TRAIN_PATH = os.path.join(DATASET_PATH, "train")
VALIDATION_PATH = os.path.join(DATASET_PATH, "validation")
```
**Change if**: Dataset is located elsewhere

---

### Image Processing
```python
# Line ~70
IMG_SIZE = 224          # Target image size (default: 224)
BATCH_SIZE = 32         # Training batch size (default: 32)
```
**Adjust for**:
- `IMG_SIZE`: Must match model input (224 recommended for MobileNetV2)
- `BATCH_SIZE`: Larger = faster training but more memory (GPU: 32-64, CPU: 8-16)

---

### Data Augmentation
```python
# Lines ~89-96
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,      # ±20 degrees
    zoom_range=0.2,         # ±20% zoom
    shear_range=0.2,        # ±20% shear
    horizontal_flip=True,
    fill_mode='nearest'
)
```
**Customize**:
- `rotation_range`: 0-40 degrees (more = more augmentation)
- `zoom_range`: 0-0.5 (more = more variation)
- `shear_range`: 0-0.4 (geometric transformation)
- `horizontal_flip`: True/False (mirror images)

**Note**: More augmentation = better generalization but slower training

---

### Model Architecture
```python
# Lines ~130-140
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# Custom head
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)  # Change 128 for different capacity
x = Dropout(0.5)(x)                   # Change 0.5 for different dropout rate
output_layer = Dense(NUM_CLASSES, activation='softmax')(x)
```
**Customize**:
- `Dense(128)`: Number of neurons in hidden layer
  - Smaller (64): Faster, less parameters
  - Larger (256): More capacity but risk of overfitting
- `Dropout(0.5)`: Dropout rate
  - Higher (0.7): More regularization
  - Lower (0.3): Less regularization

---

### Optimization
```python
# Lines ~149-150
optimizer = Adam(learning_rate=0.001)
```
**Customize**:
- `learning_rate`: 0.001 (default)
  - 0.0001: Slower convergence, more stable
  - 0.01: Faster convergence, may overshoot

---

### Training Parameters
```python
# Line ~176
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=50,          # Number of training epochs
    callbacks=callbacks,
    verbose=1
)
```
**Customize**:
- `epochs`: 50 (default)
  - Lower (20): Faster, but may underfit
  - Higher (100): Better accuracy, but slower and risk of overfitting

---

### Early Stopping
```python
# Lines ~159-164
EarlyStopping(
    monitor='val_loss',
    patience=5,                    # Stop after 5 epochs without improvement
    restore_best_weights=True,
    verbose=1
)
```
**Customize**:
- `patience`: 5 (default)
  - Lower (2-3): Stops earlier
  - Higher (10): Trains longer

---

### Learning Rate Reduction
```python
# Lines ~168-173
ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,         # Reduce LR by 50%
    patience=3,         # Wait 3 epochs before reducing
    min_lr=1e-7,        # Minimum learning rate
    verbose=1
)
```
**Customize**:
- `factor`: 0.5 (reduce to 50%)
  - Higher (0.9): Smaller reduction
  - Lower (0.1): Larger reduction
- `patience`: 3 (wait epochs before reducing)

---

## 🎨 app.py Configuration

### Hand Detection
```python
# Lines ~50-60
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,                    # Maximum hands to detect
    min_detection_confidence=0.7,        # Detection threshold
    min_tracking_confidence=0.5
)
```
**Customize**:
- `max_num_hands`: 1-2 (default: 2)
  - Lower: Faster, but limits dual-hand gestures
  - Higher: Slower
- `min_detection_confidence`: 0.0-1.0 (default: 0.7)
  - Higher: Only detect confident hands (fewer false positives)
  - Lower: Detect more hands (more false positives)
- `min_tracking_confidence`: 0.0-1.0 (default: 0.5)
  - Higher: Better tracking stability
  - Lower: More responsive but jittery

---

### Prediction Stabilization
```python
# Line ~200
self.prediction_history = deque(maxlen=window_size)

# Usage
stabilizer = PredictionStabilizer(window_size=5)
```
**Customize**:
- `window_size`: 5 (default)
  - Lower (2-3): Faster response, less stable
  - Higher (7-10): More stable, slower response

---

### Streamlit UI Configuration
```python
# Lines ~224-240
st.set_page_config(
    page_title="Sign Language Translator",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)
```
**Customize**:
- `page_title`: Browser tab title
- `page_icon`: Browser tab emoji
- `layout`: "wide" or "centered"
- `initial_sidebar_state`: "expanded" or "collapsed"

---

### Confidence Threshold Slider
```python
# Line ~299
confidence_threshold = st.slider(
    "Confidence Threshold",
    0.0,    # Min
    1.0,    # Max
    0.7,    # Default
    0.05    # Step
)
```
**Customize**:
- Default (3rd parameter): Starting threshold
- Step (4th parameter): Adjustment increment

---

## 🎓 Gesture Configuration

### Single-Hand Gestures
```python
# Line ~34
SINGLE_HAND_ALPHABETS = {'C', 'I', 'L', 'O', 'U', 'V'}
```
**Change if**: Different hand count requirements

### Dual-Hand Gestures
```python
# Lines ~37-39
DUAL_HAND_ALPHABETS = {
    'A', 'B', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 
    'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z'
}
```
**Change if**: Different hand count requirements

---

## 🚀 Performance Tuning

### For Faster Training
```python
# In train.py
BATCH_SIZE = 64         # Increase batch size
epochs = 30             # Reduce epochs
IMG_SIZE = 224          # Keep as is
rotation_range = 10     # Reduce augmentation
```

### For Better Accuracy
```python
# In train.py
BATCH_SIZE = 32         # Standard batch size
epochs = 100            # More epochs
rotation_range = 30     # More augmentation
Dense(256)              # More neurons in custom head
```

### For Better Real-Time Performance
```python
# In app.py
min_detection_confidence = 0.8      # Higher threshold
window_size = 3                      # Smaller window
```

### For Lower GPU Memory Usage
```python
# In train.py
BATCH_SIZE = 16         # Smaller batch
IMG_SIZE = 224          # Standard size

# In app.py (avoid streaming large frames)
# Reduce frame resolution if needed
```

---

## 📊 Recommended Configurations

### Quick Training (Low-End GPU/CPU)
```python
IMG_SIZE = 224
BATCH_SIZE = 16
epochs = 30
rotation_range = 10
Dense(64)  # Smaller head
```
**Training Time**: ~15 minutes (GPU)
**Expected Accuracy**: 85-88%

### Balanced (Standard Setup)
```python
IMG_SIZE = 224
BATCH_SIZE = 32
epochs = 50
rotation_range = 20
Dense(128)  # Default head
```
**Training Time**: ~45 minutes (GPU)
**Expected Accuracy**: 90-93%

### High Accuracy (High-End GPU)
```python
IMG_SIZE = 256
BATCH_SIZE = 64
epochs = 100
rotation_range = 30
Dense(256)  # Larger head
```
**Training Time**: ~2-3 hours (GPU)
**Expected Accuracy**: 93-96%

---

## 🔍 Debugging Configuration

### Verbose Output
```python
# In train.py
model.fit(..., verbose=1)  # Detailed progress

# In app.py - Add debug prints:
print(f"Detected hands: {num_hands}")
print(f"Raw prediction: {predictions}")
print(f"Filtered prediction: {filtered_predictions}")
print(f"Confidence: {confidence}")
```

### Validation During Training
```python
# In train.py
model.validate_on_batch(batch_x, batch_y)
```

### Save Model Checkpoints
```python
# In train.py - Already configured via ModelCheckpoint callback
ModelCheckpoint(
    'model/mobilenet_model.h5',
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)
```

---

## 🔐 Safety Thresholds

### Minimum Recommended Thresholds
- `Hand detection confidence`: ≥ 0.5
- `Prediction confidence`: ≥ 0.6
- `Validation accuracy`: ≥ 0.85

### Maximum Recommended Settings
- `Rotation range`: ≤ 45°
- `Zoom range`: ≤ 0.3
- `Epochs`: ≤ 200
- `Batch size`: ≤ 128

---

## 📝 Configuration Checklist

Before running, verify:
- [ ] Dataset path is correct
- [ ] `IMG_SIZE` matches model input
- [ ] `BATCH_SIZE` fits in GPU/CPU memory
- [ ] Hand gesture mapping is appropriate
- [ ] Confidence thresholds are reasonable
- [ ] Stabilization window size is suitable

---

## 💡 Tips for Configuration

1. **Start with defaults**: Provided configs are well-tested
2. **Change one parameter at a time**: Easier to identify impact
3. **Monitor validation metrics**: Check if changes help or hurt
4. **Consider hardware**: Adjust batch size based on your GPU/CPU
5. **Balance speed vs accuracy**: Higher settings = slower but better accuracy
6. **Save good models**: Keep track of configurations that work well

---

## 🆘 Configuration Issues

| Problem | Solution |
|---------|----------|
| Out of memory | Reduce `BATCH_SIZE` |
| Training too slow | Reduce `rotation_range`, epochs |
| Low accuracy | Increase augmentation, epochs |
| High false positives | Increase `min_detection_confidence` |
| Flickering predictions | Increase `window_size` |
| Model not converging | Reduce `learning_rate` |

---

**Remember**: Start with default configs, then fine-tune based on your needs!
