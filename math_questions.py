import threading
import random
import time
import fact_api as facts


class MathQuestions(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.score = 0
        # dictionary with answer keys and question values for each operation
        self.answers_and_questions = {
            "1": ["What is 176^0"],
            "2": ["What is log9(81)?"],
            "3": ["What is 2 x 1.5?"],
            "4": ["What is 3.07 x 1.3?"],
            "5": ["What is 3.33% of 150?"],
            "6": ["What is 84 / 14?"],
            "7": ["What is 56 / 7?"],
            "8": ["What is 64 / 8?"],
            "9": ["What is 3^2?"],
            "10": ["What is log2(1024)?"]
        }
        self.current_question = ""
        self.current_answer = ""
        self.total_questions = sum([len(self.answers_and_questions[key]) for key in self.answers_and_questions.keys()])
        self.correct_answers = 0
        self.user_answer = ""
        self.game_over = False
        self.current_time = 0
        self.max_time = 15
        self.question_number = 1
        self.number_fact = ""
        self.fact_api = facts.FactAPI()

    def set_question(self):
        number_of_questions = 0
        while number_of_questions == 0:
            random_answer = random.randint(0, len(self.answers_and_questions.keys()) - 1)
            self.current_answer = list(self.answers_and_questions.keys())[random_answer]
            if self.current_answer in self.answers_and_questions.keys():
                number_of_questions = len(self.answers_and_questions[self.current_answer])
        random_question = random.randint(0, number_of_questions - 1)
        self.current_question = self.answers_and_questions[self.current_answer][random_question]
        del self.answers_and_questions[self.current_answer][random_question]
        if not self.answers_and_questions[self.current_answer]:
            del self.answers_and_questions[self.current_answer]

    def split_fact(self):
        # split fact into multiple lines at spaces if possible
        for char in range(1, len(self.number_fact)):
            if char % 60 == 0:
                while self.number_fact[char] != " ":
                    char -= 1
                self.number_fact = self.number_fact[:char] + "\n" + self.number_fact[char:]

    def run(self):
        while not self.game_over:
            if self.answers_and_questions == {}:
                break
            self.set_question()
            self.current_time = time.time()
            self.number_fact = self.fact_api.get_fact(self.current_answer)
            self.split_fact()
            while self.user_answer != self.current_answer:
                if time.time() - self.current_time > self.max_time:
                    break
            if self.user_answer == self.current_answer:
                self.correct_answers += 1
            self.question_number += 1
            time.sleep(0.5)
        self.score = self.correct_answers / self.total_questions * 100
        self.game_over = True
