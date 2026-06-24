# "Foto Kita Blur" - Gesture Controlled Camera App

An interactive computer vision project inspired by the viral social media trend **"Foto kita blur"**. This app uses your webcam to track your hand gestures in real-time. When you strike the signature pose (exactly 2 fingers raised), it automatically triggers a smooth blur effect over your camera feed.

This project was created as a practical learning journey into Python, real-time image processing, and responsive user interface design.

## How It Works
The application continuously captures frames from your webcam and processes them through a pipeline:
1. **Hand Landmarks Tracking:** Detects hand structures using MediaPipe.
2. **Gesture Condition:** Checks if exactly 2 fingers are raised.
3. **Gaussian Blur:** If the condition is met, it applies a real-time blur to the background.
4. **Mascot Overlay:** Places a `mascot.png` sticker at 1/3 of the screen height, anchored perfectly to the bottom-left corner so it stays visible even when the camera blurs.

## Features
- **16:9 HD Resolution:** Forced standard widescreen layout (1280x720) for a clean modern look.
- **Dynamic UI:** No matter your webcam size, the mascot scales and aligns proportionally.
- **Standalone Ready:** Bundled setup instructions to convert the script into a `.exe` file.

## Prerequisites
Make sure you have Python installed, then install the required libraries:
```bash
pip install opencv-python mediapipe
