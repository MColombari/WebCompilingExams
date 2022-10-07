import json
import os
import random

from flask import url_for

from webcompilingexams import CHARACTER_SEPARATOR
from webcompilingexams.models import Question


class DebugLoadQuestion:
    def __init__(self, user):
        self.user = user

    def load(self):
        return [
            Question(user_id=self.user.id, number=0, type=2, text='Domanda 1',
                     options="/app/questions/Java/Basic/Es1.java",
                     answer='', compiler_output='',
                     test_output='',
                     test_output_summary='Nessun test eseguito',
                     test_output_icon=url_for('static', filename="icon/question-mark-64.png")),
            Question(user_id=self.user.id, number=1, type=3, text='Domanda 2',
                     options="/app/questions/Python/Basic/Es1.py",
                     answer='', compiler_output='',
                     test_output='',
                     test_output_summary='Nessun test eseguito',
                     test_output_icon=url_for('static', filename="icon/question-mark-64.png")),
            Question(user_id=self.user.id, number=2, type=1, text='Domanda 3', options="a\nb\nc\nd",
                     answer='', correct_answer='0', compiler_output='',
                     test_output='',
                     test_output_summary='Nessuna risposta fornita',
                     test_output_icon=url_for('static', filename="icon/cross-mark-48.png")),
            Question(user_id=self.user.id, number=3, type=1, text='Domanda 3.1', options="a",
                     answer='', correct_answer='0', compiler_output='',
                     test_output='',
                     test_output_summary='Nessuna risposta fornita',
                     test_output_icon=url_for('static', filename="icon/cross-mark-48.png")),
            Question(user_id=self.user.id, number=4, type=1, text='Domanda 3.2', options="a\nb\nc\nd\n1\n2\n3\n4\n5\n6",
                     answer='', correct_answer='3\n5\n0', compiler_output='',
                     test_output='',
                     test_output_summary='Nessuna risposta fornita',
                     test_output_icon=url_for('static', filename="icon/cross-mark-48.png")),
            Question(user_id=self.user.id, number=5, type=0, text='Domanda 4', options="",
                     answer='', compiler_output='',
                     test_output='',
                     test_output_summary='Nessuna risposta fornita',
                     test_output_icon=url_for('static', filename="icon/cross-mark-48.png")),
        ]


class OptionContainer:
    def __init__(self, text):
        self.text = text
        self.option = []

    def __repr__(self):
        return f'Text: {self.text}\nOptions: {self.option}'


class LoadQuestion:
    def __init__(self, user, exam_information):
        self.user = user
        self.question_data = exam_information.load_questions_data()

    def parse_question(self, q_dict):
        ret_options = q_dict["options"]
        ret_correct_answer = q_dict["correct_answer"]

        if q_dict["type"] == 1:
            options = []
            correct_options_index = q_dict["correct_answer"].split(CHARACTER_SEPARATOR)
            index = 0
            for o in q_dict["options"].split(CHARACTER_SEPARATOR):
                if str(index) in correct_options_index:
                    options.append((o, True))
                else:
                    options.append((o, False))
                index += 1

            random.shuffle(options)

            ret_options = []
            ret_correct_answer = []
            index = 0
            for o in options:
                ret_options.append(str(o[0]))
                if o[1]:
                    ret_correct_answer.append(str(index))
                index += 1

            ret_options = CHARACTER_SEPARATOR.join(ret_options)
            ret_correct_answer = CHARACTER_SEPARATOR.join(ret_correct_answer)

        return Question(user_id=self.user.id,
                        type=q_dict["type"],
                        text=q_dict["text"],
                        options=ret_options,
                        answer="",
                        correct_answer=ret_correct_answer,
                        question_weight=q_dict["time_expected"],
                        test_output_summary= "Nessuna risposta fornita" if q_dict["type"] < 2 else "Nessun test eseguito",
                        test_output_icon=url_for('static', filename="icon/cross-mark-48.png") if q_dict["type"] < 2 else url_for('static', filename="icon/question-mark-64.png"))

    def load(self):
        out_question = []
        PATH = '/app/questions/'

        for type_key in self.question_data.keys():
            if os.path.isdir(PATH + type_key):
                current_type_question = []
                for path, currentDirectory, files in os.walk(PATH + type_key):
                    for file in files:
                        if file.endswith('.json'):
                            with open(os.path.join(path, file), "r") as f:
                                content = f.read()
                                content_parsed = json.loads(content)
                                if isinstance(content_parsed, list):
                                    for q_dict in content_parsed:
                                        current_type_question.append(self.parse_question(q_dict))
                                elif isinstance(content_parsed, dict):
                                    current_type_question.append(self.parse_question(content_parsed))

                starting_index = len(out_question)
                random.shuffle(current_type_question)
                for i in range(self.question_data[type_key]):
                    if len(current_type_question) > 0:
                        q = current_type_question.pop()
                        q.number = starting_index + i
                        out_question.append(q)

        return out_question
