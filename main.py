import cv2
import time
import finger_counting as fc
import math_questions as mq

cap = cv2.VideoCapture(0)
math = mq.MathQuestions()
detector = fc.FingerCounting()
menu = True
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    h, w, c = img.shape
    image = cv2.flip(img, 1)
    image = detector.find_hands(image, draw=False)
    # start page with instructions
    if menu:
        cv2.putText(image, "Math Quiz", (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)
        # game instructions
        cv2.putText(image, "Instructions:", (10, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(image, "Hold up 5 fingers on your left hand to play game", (10, 200), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 255), 2)
        cv2.putText(image, "Hold up 5 fingers on your right hand to quit game", (10, 250), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 255), 2)
        cv2.putText(image, "You have 15 seconds to answer each question", (10, 300), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 255), 2)
        cv2.putText(image, "You can use both hands to show your answer to the question", (10, 350), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 255), 2)
        cv2.putText(image, "There are hints at the bottom of the screen to help if you're stuck", (10, 400), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(image, "Press 'q' to quit at any time", (10, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        if detector.count_fingers(image) == 5 and detector.hand_side == "Left":
            math = mq.MathQuestions()
            math.start()
            menu = False
        elif detector.count_fingers(image) == 5 and detector.hand_side == "Right":
            break

    if not math.game_over and not menu:
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
        answer_color = (0, 0, 255)  # red
        if math.user_answer == math.current_answer:
            answer_color = (0, 255, 0)  # green
            cv2.putText(image, "Correct!", (w - 400, 150), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)
        cv2.putText(image, math.user_answer, (w - 100, 70), cv2.FONT_HERSHEY_PLAIN, 5, answer_color, 5)
        cv2.rectangle(image, (0, h - 75), (w, h - 175), (0, 0, 0), cv2.FILLED)
        # display fact about answer on multiple lines
        for i, line in enumerate(math.number_fact.split("\n")):
            cv2.putText(image, ("Hint: " if i == 0 else "") + line, (10, h - (150 - (25 * (i + 1)))),
                        cv2.FONT_HERSHEY_PLAIN, 1.8, (255, 255, 255), 2)
    elif not menu and math.game_over:
        cv2.putText(image, "Score: " + str(math.correct_answers / math.total_questions * 100) + "%", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN,
                    5, (255, 0, 255), 5)
        # instructions for hold up 5 fingers on left hand to play again or 5 fingers on right hand to quit
        cv2.putText(image, "Hold up 5 fingers on your left hand to play again", (10, 150), cv2.FONT_HERSHEY_PLAIN,
                    2, (255, 0, 255), 2)
        cv2.putText(image, "Hold up 5 fingers on your right hand to quit", (10, 200), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 255), 2)
        if detector.count_fingers(image) == 5 and detector.hand_side == "Left":
            math = mq.MathQuestions()
            math.start()
        elif detector.count_fingers(image) == 5 and detector.hand_side == "Right":
            math.join()
            break

    cv2.imshow("Output", image)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        math.game_over = True
        if not menu:
            math.join()
        break

cap.release()
cv2.destroyAllWindows()
