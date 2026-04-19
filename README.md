# 🖱️ SkyPoint
### Gesture-Based Virtual Mouse Using Computer Vision

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

SkyPoint is a **gesture-controlled virtual mouse** that allows users to control their computer **without touching a physical mouse or trackpad**.

Using **computer vision and real-time hand tracking**, SkyPoint detects hand gestures from a webcam and converts them into **mouse actions** such as cursor movement, clicking, dragging, and right-clicking.

This project demonstrates **touchless human–computer interaction (HCI)** using **Python, OpenCV, and MediaPipe**.


## 🚧 Project Status

SkyPoint is currently in a **demo / beta stage**.  

This version focuses on demonstrating the **core concept of gesture-based mouse control using hand tracking**.

The project will continue evolving as improvements and refinements are made over time.


# 🚀 Features

### Real-Time Hand Tracking
Detects **21 hand landmarks** using MediaPipe for accurate gesture recognition.

### Gesture-Based Mouse Control

| Gesture | Action |
|-------|-------|
| Move Index Finger | Move Cursor |
| Thumb + Index Pinch | Left Click |
| Hold Pinch | Drag |
| Pinky Up + Fist | Right Click |

### Smooth Cursor Movement
Uses an **adaptive smoothing algorithm** to reduce cursor jitter and improve precision.

### Accurate Screen Mapping
Maps camera coordinates to the entire screen resolution.

### Intelligent Gesture Detection
Supports detection for:

- Tap gestures  
- Hold gestures  
- Drag gestures  
- Right-click gestures  

### Visual Feedback
The system displays:

- Virtual cursor marker
- Gesture instructions
- Pinch distance indicator


# 🧠 How It Works

SkyPoint processes webcam input through the following pipeline:

### Camera Capture
Frames are captured from the webcam using **OpenCV**.

### Hand Landmark Detection
**MediaPipe Hands** detects and tracks **21 hand landmarks**.

### Gesture Recognition
Distances between landmarks determine gestures.

```python
pinch_dist = get_normalized_distance(hand, 4, 8)
```
### Cursor Mapping
The index fingertip coordinates are mapped to the screen coordinates so that hand movement directly controls the mouse pointer.

This converts the **camera position of the index finger** into the **actual screen cursor position**.

### Cursor Smoothing
An **Exponential Moving Average (EMA)** smoothing algorithm is used to make cursor movement natural and reduce jitter.


# 🛠 Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python | Core programming |
| OpenCV | Webcam processing |
| MediaPipe | Hand landmark detection |
| PyAutoGUI | Mouse automation |
| Math | Distance calculations |


# 📦 Installation

### Clone the Repository

```
git clone https://github.com/yourusername/skypoint.git  
cd skypoint
```
### Install Dependencies
```
pip install opencv-python mediapipe pyautogui
```
Or install from requirements file:
```
pip install -r requirements.txt
```

# ▶️ Run the Project
```
python SkyPoint.py
```
Your webcam will start and SkyPoint will begin detecting gestures.


# 🎮 Gesture Controls

| Gesture | Action |
|------|------|
| Move Index Finger | Move Cursor |
| Thumb + Index Pinch | Left Click |
| Hold Pinch (>0.5s) | Drag |
| Pinky Up + Closed Fingers | Right Click |


# ⚙ Configuration

You can adjust gesture sensitivity in the source code.

| Parameter | Description |
|-----------|-------------|
| SMOOTHING FACTOR | Controls cursor smoothness |
| PINCH THRESHOLD | Pinch detection sensitivity |
| DRAG THRESHOLD | Drag activation sensitivity |
| CLICK COOLDOWN | Prevents rapid repeated clicks |


# 📂 Project Structure
```
SkyPoint  
│  
├── skypoint.py  
├── README.md  
├── requirements.txt  
```

# 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork the repository  
2. Create a new branch  
3. Make your changes  
4. Submit a pull request  


# 📜 License

This project is licensed under the **MIT License**.

# 👨‍💻 Author

Developed by **Charan Bantumilli**



