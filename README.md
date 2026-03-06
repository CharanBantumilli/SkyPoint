# ☁️ SkyPoint
### Gesture-Based Virtual Mouse Using Computer Vision

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

SkyPoint is a **gesture-controlled virtual mouse** that allows users to control their computer **without touching a physical mouse or trackpad**.

Using **computer vision and real-time hand tracking**, SkyPoint detects hand gestures from a webcam and converts them into **mouse actions** such as cursor movement, clicking, dragging, and right-clicking.

This project demonstrates **touchless human–computer interaction (HCI)** using **Python, OpenCV, and MediaPipe**.

---

# 🚀 Features

### 🖐 Real-Time Hand Tracking
Detects **21 hand landmarks** using MediaPipe for accurate gesture recognition.

### 🖱 Gesture-Based Mouse Control

| Gesture | Action |
|-------|-------|
| ☝️ Move Index Finger | Move Cursor |
| 🤏 Thumb + Index Pinch | Left Click |
| 🤏 Hold Pinch | Drag |
| ✋ Pinky Up + Fist | Right Click |

### ⚡ Smooth Cursor Movement
Uses an **adaptive smoothing algorithm** to reduce cursor jitter and improve precision.

### 🎯 Accurate Screen Mapping
Maps camera coordinates to the entire screen resolution.

### 🧠 Intelligent Gesture Detection
Supports detection for:

- Tap gestures  
- Hold gestures  
- Drag gestures  
- Right-click gestures  

### 📊 Visual Feedback
The system displays:

- Virtual cursor marker
- Gesture instructions
- Pinch distance indicator

---

# 🧠 How It Works

SkyPoint processes webcam input through the following pipeline:

### 1️⃣ Camera Capture
Frames are captured from the webcam using **OpenCV**.

### 2️⃣ Hand Landmark Detection
**MediaPipe Hands** detects and tracks **21 hand landmarks**.

### 3️⃣ Gesture Recognition
Distances between landmarks determine gestures.

Example:

```python
pinch_dist = get_normalized_distance(hand, 4, 8)
