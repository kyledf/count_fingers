import threading
import random
import time
import FingerCounting as fc
import cv2

class MathQuestions(threading.Thread):
    def __init__(self, name, score):
        threading.Thread.__init__(self)
        self.name = name
        self.score = score
        self.questions = ["What is 1 + 1?", "What is 2 + 2?", "What is 3 + 3?", "What is 4 + 4?", "What is 5 + 5?"]
        self.answers = ["2", "4", "6", "8", "10"]
        self.question = ""
        self.answer = ""
        self.total = 0
        self.correct = 0
        self.userAnswer = ""
        self.gameOver = False

    def run(self):
        self.total = len(self.questions)
        for i in range(self.total):
            self.question = self.questions[i]
            self.answer = self.answers[i]
            while self.userAnswer != self.answer:
                time.sleep(0.5)
            self.correct += 1
            time.sleep(0.5)
        self.score = self.correct / self.total * 100
        self.gameOver = True

    def getScore(self):
        return self.score

    def getCorrect(self):
        return self.correct

    def getTotal(self):
        return self.total

    def getQuestion(self):
        return self.question

    def getAnswer(self):
        return self.answer

    def getQuestions(self):
        return self.questions

    def getAnswers(self):
        return self.answers


def main():
    cap = cv2.VideoCapture(0)

    score = 0
    math = MathQuestions("Math", score)
    detector = fc.FingerCounting()
    math.start()
    while True:
        success, img = cap.read()
        image = cv2.flip(img, 1)
        image = detector.find_hands(image, draw=False)
        if not math.gameOver:
            cv2.putText(image, math.getQuestion(), (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)
            math.userAnswer = str(detector.count_fingers(image))
            cv2.putText(image, math.userAnswer, (800, 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)
            if math.userAnswer == math.getAnswer():
                cv2.putText(image, "Correct!", (10, 150), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)
        else:
            cv2.putText(image, "Score: " + str(math.correct / math.total * 100) + "%", (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)
        cv2.imshow("Output", image)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()