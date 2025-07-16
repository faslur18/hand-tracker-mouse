
# Faslu's Hand-Tracker-AI Gesture Mouse 🖐️🖱️

A Python application that allows you to control your computer's mouse using hand gestures via your webcam. This tool uses computer vision to track hand movements and translate them into mouse actions like moving, clicking, scrolling, and dragging.

## Features

* **Pointer Control:** Move the mouse pointer by moving your index finger.
* **Variable-Speed Scrolling:** Bring your index and middle fingers together and move your hand up or down to scroll. The scroll speed adapts to your hand's movement speed.
* **Left-Click & Drag-and-Drop:** Pinch your thumb and index finger together to press and hold the left mouse button. Move your hand to drag and release the pinch to drop.
* **Right-Click:** Pinch your thumb and middle finger together to perform a right-click.

---

## Technology Stack

* **Python 3**
* **OpenCV:** For capturing video from the webcam.
* **MediaPipe:** For real-time hand tracking and landmark detection.
* **PyAutoGUI:** For programmatically controlling the mouse.
* **NumPy:** For efficient numerical operations and coordinate mapping.

---

## Setup and Installation

1.  Ensure you have Python 3 installed on your system.
2.  Install the required libraries by running the following command in your terminal:

    ```bash
    pip install opencv-python mediapipe pyautogui numpy
    ```

---

## How to Run

1.  Save the project code as a Python file (e.g., `hand_tracker_mouse.py`).
2.  Execute the script from your terminal:

    ```bash
    python hand_tracker_mouse.py
    ```
3.  A window showing your webcam feed will appear. The tool is now active.
4.  To stop the program, make the webcam window active and press the **'q'** key.

---

## Gesture Controls

* **Move Pointer:** Point with your **index finger**.
* **Scroll:** Bring your **index and middle fingers** together.
* **Left-Click / Drag:** Pinch your **thumb and index finger**.
* **Right-Click:** Pinch your **thumb and middle finger**.

---

## Customization

You can fine-tune the performance by adjusting the configuration variables at the top of the script:

* **`smoothing`**: A lower value (e.g., `2`) makes the pointer faster and more responsive, while a higher value (e.g., `7`) makes it smoother but slower.
* **`frameR`**: This "Frame Reduction" value sets a border. A larger value (e.g., `100`) makes the pointer more sensitive, as smaller hand movements cover the entire screen.
* **Scroll Multiplier**: In the `pyautogui.scroll()` line, you can change the multiplier (`* 4`) to increase or decrease scrolling sensitivity.
