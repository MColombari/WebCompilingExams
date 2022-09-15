import os
import random

from flask import url_for

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


class LoadQuestion:
    def __init__(self, user, exam_information):
        self.user = user
        self.question_data = exam_information.load_questions_data()

    def load(self):
        out_question = []
        PATH = '/app/questions/OpenQuestion/'
        # PATH = '/Users/mattiacolombari/Desktop/ProgettoBicocchi/WebCompilingExams/questions/OpenQuestion/'

        open_question_data = self.question_data['OpenQuestion']
        for k in open_question_data.keys():
            if (os.path.isdir(PATH + k) and
                    os.path.isfile(PATH + k + '/OpenQuestion.txt')):
                file_path = PATH + k + '/OpenQuestion.txt'

                tmp_load = {}
                tmp_weight = {}
                with open(file_path, 'r') as f:
                    tag = None
                    for line in f.read().split('\n'):
                        if '--' in line:
                            tag = line.split('"')[1]
                            weight = line.split("'")[1]
                            tmp_load[tag] = []
                            tmp_weight[tag] = int(weight)
                        elif '"' in line:
                            if tag:
                                tmp_load[tag].append(line.split('"')[1])

                for tmp_k in tmp_load.keys():
                    random.shuffle(tmp_load[tmp_k])

                # number need to be changed.
                for difficulty_key in open_question_data[k].keys():
                    if difficulty_key in tmp_load.keys():
                        for i in range(int(open_question_data[k][difficulty_key])):
                            if len(tmp_load[difficulty_key]) > 0:
                                q_text = tmp_load[difficulty_key].pop()
                                q_tmp = Question(user_id=self.user.id, number=5, type=0, text=q_text,
                                                 question_weight=tmp_weight[difficulty_key],
                                                 test_output_summary='Nessuna risposta fornita',
                                                 test_output_icon=url_for('static', filename="icon/cross-mark-48.png"))
                                out_question.append(q_tmp)

        random.shuffle(out_question)

        i = 0
        for q in out_question:
            q.number = i
            i += 1

        return out_question
