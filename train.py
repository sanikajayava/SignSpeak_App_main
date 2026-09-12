"""
EIS PROJECT: Real-Time Sign Language Recognition System
TASK 1 & 2: Model Training with GPU Support

Embedded System Input: Camera feed captured for training
Intelligent System: Deep Learning with MobileNetV2 transfer learning
Optimization: Uses MobileNetV2 for efficient real-time inference

This script trains a high-accuracy model to recognize A-Z sign language alphabets.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import (
    GlobalAveragePooling2D, Dense, Dropout, Input
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)
import matplotlib.pyplot as plt


# ============================================================================
# TASK 2: GPU SUPPORT - Detect and enable GPU
# ============================================================================

print("\n" + "="*80)
print("TASK 2: GPU SUPPORT DETECTION")
print("="*80)

# List available GPUs
gpus = tf.config.list_physical_devices('GPU')
print(f"\nNumber of GPUs available: {len(gpus)}")

if gpus:
    try:
        # Enable memory growth to prevent OOM errors
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("✓ GPU memory growth enabled")
        print(f"✓ Using GPU: {gpus[0].name}")
    except RuntimeError as e:
        print(f"Error enabling GPU memory growth: {e}")
else:
    print("⚠ No GPU detected. Training will use CPU (slower)")

# Verify TensorFlow GPU usage
print(f"\nTensorFlow version: {tf.__version__}")
print(f"Built with CUDA: {tf.test.is_built_with_cuda()}")


# ============================================================================
# TASK 1: MODEL TRAINING - Data Preparation
# ============================================================================

print("\n" + "="*80)
print("TASK 1: MODEL TRAINING - DATA PREPARATION")
print("="*80)

# Dataset paths
DATASET_PATH = r"D:\Real time Sign Language\dataset"
TRAIN_PATH = os.path.join(DATASET_PATH, "train")
VALIDATION_PATH = os.path.join(DATASET_PATH, "validation")

print(f"\nDataset path: {DATASET_PATH}")
print(f"Train path: {TRAIN_PATH}")
print(f"Validation path: {VALIDATION_PATH}")

# Verify dataset exists
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

if not os.path.exists(TRAIN_PATH):
    raise FileNotFoundError(f"Train folder not found at {TRAIN_PATH}")

if not os.path.exists(VALIDATION_PATH):
    raise FileNotFoundError(f"Validation folder not found at {VALIDATION_PATH}")

print("✓ Dataset folders verified")

# Image parameters
IMG_SIZE = 224
BATCH_SIZE = 16  # ← Reduced from 32 for faster CPU training

# ============================================================================
# TASK 5: PREPROCESSING - ImageDataGenerator with Augmentation
# ============================================================================

print("\n" + "="*80)
print("TASK 5: PREPROCESSING - DATA AUGMENTATION")
print("="*80)

# Training data generator with augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,      # ← Reduced from 20 for faster CPU
    zoom_range=0.1,         # ← Reduced from 0.2 for faster CPU
    shear_range=0.1,        # ← Reduced from 0.2 for faster CPU
    horizontal_flip=True,
    fill_mode='nearest'
)

# Validation data generator (no augmentation, only rescaling)
validation_datagen = ImageDataGenerator(rescale=1./255)

# Load training data
train_generator = train_datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

# Load validation data
validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

print("✓ Training data loaded with augmentation")
print(f"  - Rotation: 10° (reduced for CPU)")
print(f"  - Zoom: 10% (reduced for CPU)")
print(f"  - Shear: 10% (reduced for CPU)")
print(f"  - Horizontal flip: enabled")
print(f"\nTraining samples: {train_generator.samples}")
print(f"Validation samples: {validation_generator.samples}")
print(f"Classes: {train_generator.num_classes}")
print(f"Classes mapping: {train_generator.class_indices}")

# Get number of classes
NUM_CLASSES = train_generator.num_classes


# ============================================================================
# TASK 1: MODEL TRAINING - Build MobileNetV2 Model
# ============================================================================

print("\n" + "="*80)
print("TASK 1: MODEL TRAINING - MODEL ARCHITECTURE")
print("="*80)

# Load pretrained MobileNetV2 (without top layers)
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze base model weights (transfer learning)
base_model.trainable = False

# Build custom head
input_layer = Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base_model(input_layer, training=False)
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output_layer = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=input_layer, outputs=output_layer)

print("✓ MobileNetV2 model built successfully")
print("\nModel Architecture:")
print(f"  - Base: MobileNetV2 (pretrained on ImageNet)")
print(f"  - Input: {IMG_SIZE}x{IMG_SIZE}x3")
print(f"  - GlobalAveragePooling2D")
print(f"  - Dense: 128 units, ReLU activation")
print(f"  - Dropout: 0.5")
print(f"  - Output: {NUM_CLASSES} units, Softmax")

# Compile model
optimizer = Adam(learning_rate=0.001)
model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\n✓ Model compiled")
print(f"  - Optimizer: Adam (learning_rate=0.001)")
print(f"  - Loss: Categorical Crossentropy")
print(f"  - Metrics: Accuracy")


# ============================================================================
# TASK 1: MODEL TRAINING - Training with Callbacks
# ============================================================================

print("\n" + "="*80)
print("TASK 1: MODEL TRAINING - TRAINING PROCESS")
print("="*80)

# Create model directory
os.makedirs('model', exist_ok=True)

# Define callbacks
callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    ModelCheckpoint(
        'model/mobilenet_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
]

print("\nCallbacks enabled:")
print("  - EarlyStopping (patience=5 on val_loss)")
print("  - ModelCheckpoint (save best on val_accuracy)")
print("  - ReduceLROnPlateau (factor=0.5, patience=3)")

print("\n" + "="*80)
print("STARTING TRAINING...")
print("="*80)

# Train model
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=25,  # ← Reduced from 50 for CPU (EarlyStopping may stop earlier)
    callbacks=callbacks,
    verbose=1
)

print("\n" + "="*80)
print("TRAINING COMPLETED")
print("="*80)


# ============================================================================
# TASK 1: MODEL TRAINING - Save Model
# ============================================================================

print("\nTASK 1: SAVING MODEL")

# Save final model
model.save('model/mobilenet_model_final.h5')
print("✓ Final model saved to: model/mobilenet_model_final.h5")
print("✓ Best model saved to: model/mobilenet_model.h5")

# Training summary
print("\n" + "="*80)
print("TRAINING SUMMARY")
print("="*80)

final_train_accuracy = history.history['accuracy'][-1]
final_train_loss = history.history['loss'][-1]
final_val_accuracy = history.history['val_accuracy'][-1]
final_val_loss = history.history['val_loss'][-1]

print(f"\nFinal Training Accuracy: {final_train_accuracy:.4f}")
print(f"Final Training Loss: {final_train_loss:.4f}")
print(f"Final Validation Accuracy: {final_val_accuracy:.4f}")
print(f"Final Validation Loss: {final_val_loss:.4f}")

if final_val_accuracy > 0.90:
    print("\n✓ TARGET ACHIEVED: Validation accuracy > 90%")
else:
    print(f"\n⚠ Target accuracy not yet achieved. Current: {final_val_accuracy:.4f}")


# ============================================================================
# Plot Training History
# ============================================================================

print("\nGenerating training history plots...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy plot
axes[0].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
axes[0].set_xlabel('Epoch', fontsize=12)
axes[0].set_ylabel('Accuracy', fontsize=12)
axes[0].set_title('Model Accuracy Over Epochs', fontsize=14, fontweight='bold')
axes[0].legend(fontsize=10)
axes[0].grid(True, alpha=0.3)

# Loss plot
axes[1].plot(history.history['loss'], label='Training Loss', linewidth=2)
axes[1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
axes[1].set_xlabel('Epoch', fontsize=12)
axes[1].set_ylabel('Loss', fontsize=12)
axes[1].set_title('Model Loss Over Epochs', fontsize=14, fontweight='bold')
axes[1].legend(fontsize=10)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('model/training_history.png', dpi=300, bbox_inches='tight')
print("✓ Training history plot saved to: model/training_history.png")

print("\n" + "="*80)
print("TRAINING COMPLETE - MODEL READY FOR DEPLOYMENT")
print("="*80)
