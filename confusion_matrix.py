import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# =========================
# PATHS (UPDATED FOR YOU)
# =========================
MODEL_PATH = "model/mobilenet_model.h5"

# Windows path (IMPORTANT: use r"" or double \\)
VAL_DIR = r"D:\Real time Sign Language\dataset\validation"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

# =========================
# LOAD MODEL
# =========================
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "model/mobilenet_model_final.h5"

model = load_model(MODEL_PATH)
print(f"✅ Loaded model from: {MODEL_PATH}")

# =========================
# LOAD VALIDATION DATA
# =========================
val_datagen = ImageDataGenerator(rescale=1./255)

val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False   # IMPORTANT for confusion matrix
)

# =========================
# PREDICTIONS
# =========================
pred_probs = model.predict(val_generator, verbose=1)
y_pred = np.argmax(pred_probs, axis=1)
y_true = val_generator.classes

# =========================
# CLASS LABELS
# =========================
class_labels = list(val_generator.class_indices.keys())

# =========================
# ACCURACY
# =========================
acc = accuracy_score(y_true, y_pred)
print(f"\n✅ Validation Accuracy: {acc * 100:.2f}%")

# =========================
# CLASSIFICATION REPORT
# =========================
print("\n📊 Classification Report:\n")
print(classification_report(y_true, y_pred, target_names=class_labels))

# =========================
# CONFUSION MATRIX
# =========================
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(14, 12))
sns.heatmap(cm, annot=False, cmap='Blues',
            xticklabels=class_labels,
            yticklabels=class_labels)

plt.title("Confusion Matrix (A-Z)")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.xticks(rotation=90)
plt.yticks(rotation=0)

plt.tight_layout()

# SAVE IMAGE FOR PPT 🔥
plt.savefig("confusion_matrix.png", dpi=300)

plt.show()