import cv2
import hand_tracking as ht


class FingerCounting(ht.HandDetector):
    def __init__(self):
        super().__init__()
        self.finger_tips = {8: "Index", 12: "Middle", 16: "Ring", 20: "Pinky"}
        self.hand_side = ""

    def count_fingers(self, image):
        lm_lists = [[], []]
        fingers_open = [[], []]
        lm_lists[0], lm_lists[1], self.hand_side = self.find_position(image, draw=False)
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
                for finger_tip in self.finger_tips.keys():
                    if lm_lists[i][finger_tip][2] < lm_lists[i][finger_tip - 2][2]:
                        fingers_open[i].append(self.finger_tips[finger_tip])

        return len(fingers_open[0]) + len(fingers_open[1])


def main():
    cap = cv2.VideoCapture(0)
    detector = FingerCounting()
    while True:
        success, img = cap.read()
        image = cv2.flip(img, 1)
        image = detector.find_hands(image, draw=False)
        cv2.putText(image, detector.hand_side + ": " + str(detector.count_fingers(image)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)
        cv2.imshow("Output", image)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()
