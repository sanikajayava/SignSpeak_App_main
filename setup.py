"""
Setup script for EIS Project: Real-Time Sign Language Recognition System
"""

import os
import subprocess
import sys

def create_directories():
    """Create necessary directories."""
    directories = [
        'model',
        'logs',
        'predictions'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies."""
    print("\n" + "="*80)
    print("INSTALLING DEPENDENCIES")
    print("="*80)
    
    subprocess.check_call([
        sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
    ])
    
    subprocess.check_call([
        sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
    ])
    
    print("\n✓ All dependencies installed successfully")

def verify_dataset():
    """Verify dataset exists."""
    print("\n" + "="*80)
    print("VERIFYING DATASET")
    print("="*80)
    
    dataset_path = r"D:\Real time Sign Language\dataset"
    train_path = os.path.join(dataset_path, "train")
    validation_path = os.path.join(dataset_path, "validation")
    
    if os.path.exists(dataset_path):
        print(f"✓ Dataset found at: {dataset_path}")
        
        if os.path.exists(train_path):
            train_classes = len(os.listdir(train_path))
            print(f"  - Train folder: {train_classes} classes")
        else:
            print(f"  ⚠ Train folder not found at: {train_path}")
        
        if os.path.exists(validation_path):
            val_classes = len(os.listdir(validation_path))
            print(f"  - Validation folder: {val_classes} classes")
        else:
            print(f"  ⚠ Validation folder not found at: {validation_path}")
    else:
        print(f"⚠ Dataset not found at: {dataset_path}")
        print("  Please ensure dataset is placed at the correct location")

def main():
    """Main setup function."""
    print("\n" + "="*80)
    print("ESI PROJECT SETUP")
    print("Real-Time Sign Language Recognition System")
    print("="*80)
    
    try:
        # Create directories
        create_directories()
        
        # Install dependencies
        install_dependencies()
        
        # Verify dataset
        verify_dataset()
        
        print("\n" + "="*80)
        print("SETUP COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nNext steps:")
        print("1. Verify dataset is at: D:\\Real time Sign Language\\dataset")
        print("2. Run training: python train.py")
        print("3. After training completes, run: streamlit run app.py")
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
