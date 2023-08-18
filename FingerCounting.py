import cv2
import HandTracking as ht

cap = cv2.VideoCapture(0)
detector = ht.HandDetector()
finger_tips = {8: "Index", 12: "Middle", 16: "Ring", 20: "Pinky"}

while True:
    success, img = cap.read()
    image = cv2.flip(img, 1)
    img = detector.find_hands(image, draw=False)
    lm_lists = [[], []]
    fingers_open = [[], []]
    lm_lists[0], lm_lists[1], hand_side = detector.find_position(image, draw=False)
    for i in range(2):
        if len(lm_lists[i]) != 0:
            if lm_lists[i][0][3] == "Left":
                # Thumb
                if lm_lists[i][4][1] > lm_lists[i][3][1]:
                    fingers_open[i].append("Thumb")

            elif lm_lists[i][0][3] == "Right":
                # Thumb
                if lm_lists[i][4][1] < lm_lists[i][3][1]:
                    fingers_open[i].append("Thumb")

            # Fingers
            for finger_tip in finger_tips.keys():
                if lm_lists[i][finger_tip][2] < lm_lists[i][finger_tip - 2][2]:
                    fingers_open[i].append(finger_tips[finger_tip])

    cv2.putText(image, f"{hand_side} Hand Fingers Open: {len(fingers_open[0]) + len(fingers_open[1])}", (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", image)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
