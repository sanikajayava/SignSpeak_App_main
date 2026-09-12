# 🚀 QUICK START GUIDE

## EIS Project: Real-Time Sign Language Recognition System

### Prerequisites
- Python 3.8 or higher
- Webcam
- GPU (optional but recommended)
- Dataset at: `D:\Real time Sign Language\dataset`

---

## OPTION 1: Automated Setup (Recommended)

### Step 1: Run Setup Script
```bash
python setup.py
```

This will:
- ✓ Create necessary folders (model, logs, predictions)
- ✓ Install all dependencies
- ✓ Verify dataset location

### Step 2: Train the Model
```bash
python train.py
```

**Expected time:**
- GPU: 30-60 minutes
- CPU: 2-4 hours

**Watch for:**
- Training progress output
- Validation accuracy > 90% (target)
- Best model saved to `model/mobilenet_model.h5`

### Step 3: Run the App
```bash
streamlit run app.py
```

Open browser to: http://localhost:8501

---

## OPTION 2: Manual Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Model Folder
```bash
mkdir model
```

### Step 3: Train Model
```bash
python train.py
```

### Step 4: Run App
```bash
streamlit run app.py
```

---

## Using the Application

1. **Click "▶️ Start Camera"** button
2. **Position hand** in front of webcam
3. **Watch prediction** update in real-time
4. **Prediction stabilizes** after ~1-2 seconds
5. **Click "⏹️ Stop Camera"** to end

---

## Key Features Enabled

✅ Real-time hand detection (0, 1, or 2 hands)  
✅ Smart prediction filtering (hand count based)  
✅ Prediction stabilization (majority voting)  
✅ Live confidence scores  
✅ Prediction history tracking  
✅ Adjustable confidence threshold  
✅ Single and dual-hand gesture support  

---

## Gesture Reference

### Single-Hand (1 hand only)
```
C  I  L  O  U  V
```

### Dual-Hand (2 hands only)
```
A  B  D  E  F  G  H  J  K  M
N  P  Q  R  S  T  W  X  Y  Z
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Model not found" | Run `python train.py` first |
| "Cannot access webcam" | Check webcam permissions |
| "Low accuracy" | Improve lighting, hold gesture steady |
| "GPU not used" | Install CUDA toolkit |
| "Dependencies error" | Run `pip install --upgrade pip` first |

---

## Performance Tips

- **Better lighting** = Better detection
- **Clear hand visibility** = More accurate predictions
- **Steady gestures** = Stable predictions
- **Correct hand count** = Proper filtering
- **GPU enabled** = Faster inference

---

## Expected Results

- ✓ Model Accuracy: >90%
- ✓ Inference Speed: 50-100ms (GPU)
- ✓ Hand Detection: Real-time (30 FPS)
- ✓ Prediction Stabilization: 5 frames
- ✓ Supported Gestures: 26 (A-Z)

---

## Project Structure

```
D:\ESI MODEL\
├── train.py              ← Run this first
├── app.py                ← Run this second  
├── setup.py              ← Optional setup
├── requirements.txt      ← Dependencies
├── README.md             ← Full documentation
├── QUICKSTART.md         ← This file
└── model/                ← Generated models
    ├── mobilenet_model.h5
    ├── mobilenet_model_final.h5
    └── training_history.png
```

---

## Commands Summary

```bash
# Setup (optional)
python setup.py

# Train model
python train.py

# Run application
streamlit run app.py

# Install dependencies (if not using setup.py)
pip install -r requirements.txt
```

---

## Need Help?

1. Check **README.md** for detailed information
2. Review code comments in **train.py** and **app.py**
3. Check **Troubleshooting** section above
4. Verify dataset location: `D:\Real time Sign Language\dataset`

---

**Status**: Ready to Deploy ✅


