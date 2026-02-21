
import cv2
import mediapipe as mp
import pyautogui
import math
import time

# --- Configuration & Global Settings ---
SCREEN_W, SCREEN_H = pyautogui.size()
SMOOTHING_FACTOR = 0.15  # Lower = smoother/slower, Higher = snappier (0.05 to 0.9)
PINCH_THRESHOLD = 0.045  # Distance (normalized 0-1) between Thumb and Index to trigger click
DRAG_THRESHOLD = 0.06    # Distance to trigger "Hold Mode"
CLICK_COOLDOWN = 0.4     # Seconds between clicks to prevent machine-gunning

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_draw_styles = mp.solutions.drawing_styles

# State Management Variables
class MouseController:
    def __init__(self):
        self.prev_x, self.prev_y = 0, 0
        self.is_pinching = False
        self.is_dragging = False
        self.pinch_start_time = 0
        self.last_click_time = 0
        self.last_right_click_time = 0
        
        # For velocity calculation (acceleration smoothing)
        self.velocity_history = []

controller = MouseController()

# --- Advanced Smoothing Function (EMA with Velocity Check & Spatial Calibration) ---
def smooth_move(current_x, current_y, width, height):

    margin = 0.1  # 10% crop
    norm_x = (current_x / width - margin) / (1 - 2 * margin)
    norm_y = (current_y / height - margin) / (1 - 2 * margin)

    norm_x = max(0, min(1, norm_x))
    norm_y = max(0, min(1, norm_y))

    # Map to full screen
    screen_x = norm_x * SCREEN_W
    screen_y = norm_y * SCREEN_H

    dist_moved = math.sqrt((screen_x - controller.prev_x)**2 +
                           (screen_y - controller.prev_y)**2)

    if dist_moved > 80:
        adaptive_alpha = 0.8
    else:
        adaptive_alpha = SMOOTHING_FACTOR

    final_x = controller.prev_x + (screen_x - controller.prev_x) * adaptive_alpha
    final_y = controller.prev_y + (screen_y - controller.prev_y) * adaptive_alpha

    # Clamp to screen edges
    final_x = max(0, min(SCREEN_W - 1, final_x))
    final_y = max(0, min(SCREEN_H - 1, final_y))

    controller.prev_x, controller.prev_y = final_x, final_y
    return int(final_x), int(final_y)

# --- Distance Calculation (Normalized) ---
def get_normalized_distance(landmarks, idx1, idx2):
    p1 = landmarks.landmark[idx1]
    p2 = landmarks.landmark[idx2]
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# --- Main Application ---
def main():
    cap = cv2.VideoCapture(0)
    # High resolution for better tracking accuracy
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    with mp_hands.Hands(
        static_image_mode=False,
        model_complexity=1,       # Medium complexity for balance of speed/accuracy
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
        max_num_hands=1
    ) as hands:
        
        print("Initializing... Hold hand still for 1 second to calibrate center.")
        calibration_active = True
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            # Pre-processing: Flip and Convert
            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process
            results = hands.process(image_rgb)
            
            # Convert back for drawing
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            h, w, _ = image.shape

            # UI Overlay
            cv2.rectangle(image, (0, 0), (w, 60), (0, 0, 0), -1)
            cv2.putText(image, "Index: Move | Pinch: Click/Hold | Pinky: Right Click", 
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                
                # 1. DRAW HAND
                mp_draw.draw_landmarks(
                    image, hand, mp_hands.HAND_CONNECTIONS,
                    mp_draw_styles.get_default_hand_landmarks_style(),
                    mp_draw_styles.get_default_hand_connections_style())

                # 2. EXTRACT PIXEL DATA
                # Convert normalized coords to pixels for screen mapping
                index_tip = hand.landmark[8]
                thumb_tip = hand.landmark[4]
                
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)
                tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

                # 3. SMOOTH MOUSE MOVEMENT
                smooth_x, smooth_y = smooth_move(ix, iy, w, h)
                pyautogui.moveTo(smooth_x, smooth_y)

                # Draw "Virtual Cursor" on screen
                cv2.circle(image, (ix, iy), 15, (255, 0, 255), -1)
                cv2.circle(image, (ix, iy), 5, (255, 255, 255), -1)

                # 4. PINCH DETECTION (Click Logic)
                pinch_dist = get_normalized_distance(hand, 4, 8)
                
                # Visual Feedback for Pinch Distance
                cv2.line(image, (ix, iy), (tx, ty), (255, 255, 255), 2)
                cv2.putText(image, f"Pinch Dist: {pinch_dist:.3f}", (10, h-20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                current_time = time.time()

                # --- SCENARIO A: START PINCH (Click) ---
                if pinch_dist < PINCH_THRESHOLD and not controller.is_pinching:
                    controller.is_pinching = True
                    controller.pinch_start_time = current_time
                    
                    # Small delay to distinguish between a "tap" and a "hold"
                    # We execute the click immediately, but set the state for dragging
                    if current_time - controller.last_click_time > CLICK_COOLDOWN:
                        pyautogui.click()
                        controller.last_click_time = current_time
                        print("Action: Left Click (Tap)")

                # --- SCENARIO B: MAINTAIN PINCH (Drag) ---
                elif pinch_dist < PINCH_THRESHOLD and controller.is_pinching:
                    # If held for > 0.5 seconds, switch to drag mode
                    if (current_time - controller.pinch_start_time > 0.5) and not controller.is_dragging:
                        controller.is_dragging = True
                        pyautogui.mouseDown() # Start Drag
                        print("Action: Drag Started")

                # --- SCENARIO C: RELEASE PINCH (Stop Drag) ---
                elif pinch_dist >= PINCH_THRESHOLD and controller.is_pinching:
                    if controller.is_dragging:
                        pyautogui.mouseUp() # Stop Drag
                        controller.is_dragging = False
                        print("Action: Drag Released")
                    controller.is_pinching = False

                # --- SCENARIO D: RIGHT CLICK (Middle Finger Up) ---
                middle_tip = hand.landmark[12]
                middle_pip = hand.landmark[11] # PIP joint
                
                # If Middle Tip is higher (smaller Y) than PIP
                if middle_tip.y < middle_pip.y:
                     # Check if thumb is NOT pinching (so we don't right click while trying to left click)
                     if pinch_dist >= PINCH_THRESHOLD:
                         if current_time - controller.last_right_click_time > 1.0: # Longer cooldown for Right Click
                             pyautogui.rightClick()
                             controller.last_right_click_time = current_time # Ensure you define this in __init__
                             cv2.putText(image, "RIGHT CLICK", (w//2 - 100, h//2), 
                                         cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
                             print("Action: Right Click")

            else:
                # Reset state if hand is lost
                controller.is_pinching = False
                controller.is_dragging = False

            cv2.imshow("Advanced Hand Controller", image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

