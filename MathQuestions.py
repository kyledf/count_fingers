import threading
import random
import time
import cv2
import FingerCounting as count
import FactAPI as facts


class MathQuestions(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.score = 0
        # # dictionary with answer keys and question values for each operation
        self.answers_and_questions = {
            "1": ["What is 0 + 1?", "What is 3 - 2?", "What is 1 x 1?", "What is 2 / 2?"],
            "2": ["What is 1 + 1?", "What is 5 - 3?", "What is 2 x 1?", "What is 4 / 2?"],
            "3": ["What is 1 + 2?", "What is 7 - 4?", "What is 3 x 1?", "What is 9 / 3?"],
            "4": ["What is 2 + 2?", "What is 9 - 5?", "What is 2 x 2?", "What is 24 / 6?"],
            "5": ["What is 2 + 3?", "What is 11 - 6?", "What is 5 x 1?", "What is 15 / 3?"],
            "6": ["What is 3 + 3?", "What is 13 - 7?", "What is 2 x 3?", "What is 54 / 9?"],
            "7": ["What is 5 + 2?", "What is 16 - 9?", "What is 7 x 1?", "What is 56 / 8?"],
            "8": ["What is 4 + 4?", "What is 19 - 11?", "What is 2 x 4?", "What is 32 / 4?"],
            "9": ["What is 5 + 4?", "What is 21 - 12?", "What is 3 x 3?", "What is 81 / 9?"],
            "10": ["What is 5 + 5?", "What is 25 - 15?", "What is 2 x 5?", "What is 100 / 10?"],
        }
        self.current_question = ""
        self.current_answer = ""
        self.total_questions = 40
        self.correct_answers = 0
        self.user_answer = ""
        self.game_over = False
        self.current_time = 0
        self.max_time = 15
        self.question_number = 0
        self.number_fact = ""

    def run(self):
        for i in range(self.total_questions):
            self.question_number = i + 1
            if self.answers_and_questions == {}:
                break
            number_of_questions = 0
            while number_of_questions == 0:
                random_answer = random.randint(1, 10)
                self.current_answer = str(random_answer)
                if self.current_answer in self.answers_and_questions.keys():
                    number_of_questions = len(self.answers_and_questions[self.current_answer])
            random_question = random.randint(0, number_of_questions - 1)
            self.current_question = self.answers_and_questions[self.current_answer][random_question]
            del self.answers_and_questions[self.current_answer][random_question]
            if not self.answers_and_questions[self.current_answer]:
                del self.answers_and_questions[self.current_answer]
            self.current_time = time.time()
            self.number_fact = facts.FactAPI(self.current_answer).get_fact()
            # split fact into multiple lines at spaces if possible
            for char in range(1, len(self.number_fact)):
                if char % 60 == 0:
                    while self.number_fact[char] != " ":
                        char -= 1
                    self.number_fact = self.number_fact[:char] + "\n" + self.number_fact[char:]
            while self.user_answer != self.current_answer:
                if time.time() - self.current_time > self.max_time:
                    break
            if self.user_answer == self.current_answer:
                self.correct_answers += 1
            time.sleep(0.5)
        self.score = self.correct_answers / self.total_questions * 100
        self.game_over = True


def main():
    cap = cv2.VideoCapture(0)
    math = MathQuestions()
    detector = count.FingerCounting()
    math.start()
    while True:
        success, img = cap.read()
        h, w, c = img.shape
        image = cv2.flip(img, 1)
        image = detector.find_hands(image, draw=False)
        if not math.game_over:
            # change color of progress bar as time goes down
            color = (0, 255, 0)  # green
            if time.time() - math.current_time > math.max_time / 3:
                color = (0, 255, 255)  # yellow
            if time.time() - math.current_time > math.max_time * 2 / 3:
                color = (0, 0, 255)  # red
            # create progress bar that goes down as time goes down
            cv2.rectangle(image, (0, h - 10), (int(w * (1 - (time.time() - math.current_time) / math.max_time)), h),
                          color, cv2.FILLED)
            # display question and answer
            cv2.putText(image, str(math.question_number) + ") " + math.current_question, (10, 70),
                        cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)
            math.user_answer = str(detector.count_fingers(image))
            cv2.putText(image, math.user_answer, (900, 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)
            cv2.rectangle(image, (0, h - 75), (w, h - 175), (0, 0, 0), cv2.FILLED)
            # display fact about answer on multiple lines
            for i, line in enumerate(math.number_fact.split("\n")):
                cv2.putText(image, ("Hint: " if i == 0 else "") + line, (10, h - (150 - (25 * (i + 1)))), cv2.FONT_HERSHEY_PLAIN, 1.8, (255, 255, 255), 2)
            if math.user_answer == math.current_answer:
                cv2.putText(image, "Correct!", (10, 150), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)
        else:
            cv2.putText(image, "Score: " + str(math.correct_answers / math.total_questions * 100) + "%", (10, 70),
                        cv2.FONT_HERSHEY_PLAIN,
                        5, (255, 0, 255), 5)
        cv2.imshow("Output", image)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()
