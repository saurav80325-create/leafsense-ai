# LeafSense AI 🌿

An AI-powered plant health and disease detection system that uses deep learning
to identify plant diseases from leaf images.

LeafSense AI integrates two image classification models — a Custom CNN and
MobileNetV2 — into a Flask web application for interactive plant disease
prediction.

## 👥 Team

This project was collaboratively developed as a college minor project.

- Saurav Yadav
- Adnan

Both contributors worked across dataset preparation, data augmentation,
model development, training, evaluation, and web application development.

## ✨ Features

- 🌱 Plant disease detection from leaf images
- 🧠 Custom CNN model
- 📱 MobileNetV2 transfer-learning model
- 🔄 Model selection through the web interface
- 📊 Top-3 predictions with confidence scores
- 🩺 Disease cause information
- 💊 Treatment recommendations
- 🖼️ Image upload and preprocessing
- 🌐 Flask-based web interface

## 🛠️ Tech Stack

### Machine Learning
- Python
- TensorFlow
- Keras
- NumPy
- Convolutional Neural Networks (CNN)
- MobileNetV2
- Transfer Learning

### Web Application
- Flask
- HTML
- CSS
- Bootstrap

### Tools
- Git
- GitHub
- VS Code

## 🧠 Models

LeafSense AI provides two models for prediction:

### 1. Custom CNN

A custom convolutional neural network trained for plant disease
classification.

### 2. MobileNetV2

A MobileNetV2-based transfer-learning model used for plant disease
classification.

Users can select either model from the web interface and compare their
predictions.

## 📊 Prediction Output

For a given leaf image, the application provides:

- Predicted plant/disease class
- Confidence score
- Top-3 predictions
- Disease cause
- Recommended treatment

## 📁 Project Structure

```text
leafsense-ai/
│
├── app.py
├── models/
│   ├── class_names.txt
│   ├── plant_health_cnn_model.keras
│   └── plant_health_mobilenetv2_model.keras
│
├── static/
├── templates/
├── uploadimages/
├── plant_disease.json
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE