import cv2
import time
import FingerCounting as fc

class MathQuestions():
    def __init__(self):
        self.finger_counting = fc.FingerCounting()
        self.question = ""
        self.answer = 0
        self.question_number = 0
        self.correct_answers = 0
        self.total_questions = 0
        self.start_time = 0
        self.end_time = 0
        self.time_taken = 0
        self.accuracy = 0
        #make a dictionary where key is the answers and value is the questions
        self.questions = {
            1: ["1 + 0", "2 - 1", "1 * 1", "2 / 2"],
            2: ["1 + 1", "2 - 0", "1 * 2", "4 / 2"],
            3: ["1 + 2", "3 - 1", "3 * 1", "9 / 3"],
            4: ["1 + 3", "10 - 6", "2 * 2", "24 / 6"],
            5: ["1 + 4", "5 - 0", "2 * 3", "15 / 3"],
            6: ["1 + 5", "6 - 1", "3 * 2", "18 / 3"],
            7: ["1 + 6", "7 - 0", "3 * 3", "21 / 3"],
            8: ["1 + 7", "8 - 1", "4 * 2", "8 / 1"],
            9: ["1 + 8", "9 - 0", "4 * 3", "12 / 3"],
            10: ["1 + 9", "11 - 1", "5 * 2", "20 / 2"]
        }

    def generate_question(self):
        self.question_number += 1
        self.question = self.questions[self.question_number][0]
        self.answer = eval(self.questions[self.question_number][0])
        self.total_questions = len(self.questions)
        self.start_time = time.time()

    def check_answer(self, image):
        if self.finger_counting.count_fingers(image) == self.answer:
            self.correct_answers += 1
            return True
        else:
            return False


    def get_accuracy(self):
        self.end_time = time.time()
        self.time_taken = self.end_time - self.start_time
        self.accuracy = round((self.correct_answers / self.total_questions) * 100, 2)
        return self.accuracy

def main():
    cap = cv2.VideoCapture(0)
    math_questions = MathQuestions()
    while True:
        success, img = cap.read()
        image = cv2.flip(img, 1)
        image = math_questions.finger_counting.find_hands(image, draw=False)
        if math_questions.check_answer(image):
            math_questions.generate_question()
        cv2.putText(image, math_questions.question, (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)
        cv2.putText(image, "Accuracy: " + str(math_questions.get_accuracy()) + "%", (10, 450), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)
        cv2.imshow("Output", image)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()