import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self):
        self.results = None
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)

        return image

    def find_position(self, image, hand_number=0, draw=True):
        lm_list_1 = []
        lm_list_2 = []
        hand_side = ""
        if self.results.multi_hand_landmarks:
            hand1 = self.results.multi_hand_landmarks[hand_number]
            hand_side = self.results.multi_handedness[hand_number].classification[0].label

            for id, lm in enumerate(hand1.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list_1.append([id, cx, cy, hand_side])
                if draw:
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

            if len(self.results.multi_hand_landmarks) > 1:
                hand2 = self.results.multi_hand_landmarks[hand_number + 1]
                hand_side = "Both"
                for id, lm in enumerate(hand2.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list_2.append(
                        [id, cx, cy, self.results.multi_handedness[hand_number + 1].classification[0].label])
                    if draw:
                        cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

        return lm_list_1, lm_list_2, hand_side


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        image = cv2.flip(img, 1)
        image = detector.find_hands(image)
        left_pos, right_pos, hand_side = detector.find_position(image)

        if len(left_pos) != 0:
            print(hand_side, left_pos[4])

        if len(right_pos) != 0:
            print(hand_side, right_pos[4])

        cv2.imshow("Image", image)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()
