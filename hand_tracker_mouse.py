import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time # Import the time module for right-click cooldown

# Disable PyAutoGUI's failsafe to allow moving the mouse to the screen corners
pyautogui.FAILSAFE = False

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize OpenCV Video Capture
cap = cv2.VideoCapture(0)

# --- Configuration Variables ---
frameR = 100 # Frame Reduction for mapping (makes pointer faster)
smoothing = 3 # Smoothing factor (lower is faster, more jittery)

# --- State Variables ---
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
is_mouse_down = False # Variable to track drag state
last_right_click_time = 0 # Variable for right-click cooldown

print("🚀 AI Mouse Control Activated.")
print("   - Index Finger: Move Pointer")
print("   - Index + Middle Finger together: Scroll")
print("   - Thumb + Index Pinch: Drag & Drop (Left Click)")
print("   - Thumb + Middle Pinch: Right Click")
print("Press 'q' in the video window to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Get coordinates for key landmarks
        h, w, c = frame.shape
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

        # Convert normalized coordinates to pixel coordinates
        ix, iy = int(index_tip.x * w), int(index_tip.y * h)
        mx, my = int(middle_tip.x * w), int(middle_tip.y * h)
        tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

        # Map hand coordinates to screen coordinates
        screen_x = np.interp(ix, (frameR, w - frameR), (0, screen_width))
        screen_y = np.interp(iy, (frameR, h - frameR), (0, screen_height))
        
        # Smooth the movement
        curr_x = prev_x + (screen_x - prev_x) / smoothing
        curr_y = prev_y + (screen_y - prev_y) / smoothing

        # --- GESTURE DETECTION ---
        # Calculate distances between finger tips
        scroll_dist = ((ix - mx)**2 + (iy - my)**2)**0.5
        left_click_dist = ((ix - tx)**2 + (iy - ty)**2)**0.5
        right_click_dist = ((mx - tx)**2 + (my - ty)**2)**0.5

        # 1. Scroll Mode
        if scroll_dist < 40:
            cv2.putText(frame, "Scroll Mode", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            scroll_amount = int((prev_y - curr_y) * 4) # Determine scroll amount and direction
            pyautogui.scroll(scroll_amount)
        
        # 2. Pointer Movement & Clicks
        else:
            pyautogui.moveTo(curr_x, curr_y) # Move the mouse
            cv2.circle(frame, (ix, iy), 10, (0, 255, 0), cv2.FILLED) # Green circle on index tip

            # 2a. Right Click Gesture (Thumb + Middle)
            if right_click_dist < 40:
                current_time = time.time()
                if current_time - last_right_click_time > 1.0: # 1-second cooldown
                    pyautogui.rightClick()
                    last_right_click_time = current_time
                    cv2.circle(frame, (tx, ty), 15, (0, 255, 255), cv2.FILLED) # Yellow circle for right click

            # 2b. Drag & Drop / Left Click (Thumb + Index)
            if left_click_dist < 40:
                if not is_mouse_down:
                    pyautogui.mouseDown()
                    is_mouse_down = True
                    cv2.circle(frame, (ix, iy), 15, (0, 0, 255), cv2.FILLED) # Red circle for drag
            else:
                if is_mouse_down:
                    pyautogui.mouseUp()
                    is_mouse_down = False

        # Update previous coordinates for the next frame
        prev_x, prev_y = curr_x, curr_y

    cv2.imshow("Faslu's AI Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
print("✅ Program terminated.")