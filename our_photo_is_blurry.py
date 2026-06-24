import cv2
from mediapipe.python.solutions import hands as mp_hands

# Initialize MediaPipe Hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Function to overlay transparent PNG onto the frame
def overlay_sticker(background_img, sticker_img, x, y, size):
    if sticker_img is None:
        return background_img

    sticker = cv2.resize(sticker_img, size, interpolation=cv2.INTER_AREA)
    h_s, w_s, c_s = sticker.shape

    if x < 0 or y < 0 or y + h_s > background_img.shape[0] or x + w_s > background_img.shape[1]:
        return background_img

    if c_s == 4:
        bgr = sticker[:, :, 0:3]
        mask = sticker[:, :, 3]
        mask_inv = cv2.bitwise_not(mask)

        roi = background_img[y:y+h_s, x:x+w_s]
        bg_black = cv2.bitwise_and(roi, roi, mask=mask_inv)
        fg_sticker = cv2.bitwise_and(bgr, bgr, mask=mask)

        dst = cv2.add(bg_black, fg_sticker)
        background_img[y:y+h_s, x:x+w_s] = dst
    else:
        background_img[y:y+h_s, x:x+w_s] = sticker[:, :, 0:3]

    return background_img

# Load mascot image
img_mascot = cv2.imread('mascot.png', cv2.IMREAD_UNCHANGED)

# Initialize Camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    success, frame = camera.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    trigger_blur = False

    if result.multi_hand_landmarks: # type: ignore
        for hand_landmarks in result.multi_hand_landmarks: # type: ignore
            fingers_open = []

            pinky_is_right = hand_landmarks.landmark[17].x > hand_landmarks.landmark[5].x
            if pinky_is_right:
                fingers_open.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)
            else:
                fingers_open.append(1 if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else 0)

            tips_ids = [8, 12, 16, 20]
            pip_ids = [6, 10, 14, 18]
            for tip, pip in zip(tips_ids, pip_ids):
                fingers_open.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y else 0)

            finger_count = fingers_open.count(1)

            # Trigger blur only when 2 fingers are raised
            if finger_count == 2:
                trigger_blur = True

    if trigger_blur:
        frame = cv2.GaussianBlur(frame, (55, 55), 0)

    mascot_height = int(h * 0.5)
    mascot_width = mascot_height

    pos_x = 10
    pos_y = h - mascot_height

    # Overlay mascot at the Bottom-Right corner smoothly
    frame = overlay_sticker(frame, img_mascot, pos_x, pos_y, size=(mascot_width, mascot_height))

    cv2.imshow("Cute Maskot Window", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
print("Done")
