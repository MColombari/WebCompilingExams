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


class OptionContainer:
    def __init__(self, text):
        self.text = text
        self.option = []

    def __repr__(self):
        return f'Text: {self.text}\nRight_op: {self.right_option}\nWrong_op: {self.wrong_option}'


class LoadQuestion:
    def __init__(self, user, exam_information):
        self.user = user
        self.question_data = exam_information.load_questions_data()

    def load(self):
        out_question = []
        PATH = '/app/questions/'
        # PATH = '/Users/mattiacolombari/Desktop/ProgettoBicocchi/WebCompilingExams/questions/'

        # Load Java Questions
        pass

        # Load Python Questions
        pass

        # Load Multiple Option Questions
        multiple_option_data = self.question_data['MultipleOptionQuestion']
        multiple_option_ret = []
        for k in multiple_option_data.keys():
            if (os.path.isdir(PATH + 'MultipleOptionQuestion/' + k) and
                    os.path.isfile(PATH + 'MultipleOptionQuestion/' + k + '/MultipleChoiceQuestion.txt')):
                file_path = PATH + 'MultipleOptionQuestion/' + k + '/MultipleChoiceQuestion.txt'

                tmp_question = {}
                tmp_weight = {}
                with open(file_path, 'r') as f:
                    tag = None
                    for line in f.read().split('\n'):
                        if '--' in line:
                            tag = line.split('"')[1]
                            weight = line.split("'")[1]
                            tmp_question[tag] = []
                            tmp_weight[tag] = int(weight)
                        elif '-"' in line:
                            if tag:
                                tmp_question[tag][-1].option.append((False, line.split('"')[1]))
                        elif '+"' in line:
                            if tag:
                                tmp_question[tag][-1].option.append((True, line.split('"')[1]))
                        elif '"' in line:
                            if tag:
                                tmp_question[tag].append(OptionContainer(line.split('"')[1]))

                for tmp_k in tmp_question.keys():
                    random.shuffle(tmp_question[tmp_k])

                for difficulty_key in multiple_option_data[k].keys():
                    if difficulty_key in tmp_question.keys():
                        for i in range(int(multiple_option_data[k][difficulty_key])):
                            if len(tmp_question[difficulty_key]) > 0:
                                q = tmp_question[difficulty_key].pop()
                                all_options = q.option

                                random.shuffle(all_options)

                                option_text = []
                                right_option = []
                                index = 0
                                for op in all_options:
                                    option_text.append(op[1])
                                    if op[0]:
                                        right_option.append(str(index))
                                    index += 1

                                # print(f'{all_options} - {right_option}')

                                multiple_option_ret.append(Question(user_id=self.user.id, number=0, type=1, text=q.text,
                                                                    options='\n'.join(option_text),
                                                                    correct_answer='\n'.join(right_option),
                                                                    test_output_summary='Nessuna risposta fornita',
                                                                    test_output_icon=url_for('static',
                                                                                             filename="icon/cross-mark-48.png")))
        random.shuffle(multiple_option_ret)

        for q_i in multiple_option_ret:
            q_i.number = len(out_question)
            out_question.append(q_i)

        # Load Open Questions
        open_question_data = self.question_data['OpenQuestion']
        open_question_ret = []
        for k in open_question_data.keys():
            if (os.path.isdir(PATH + 'OpenQuestion/' + k) and
                    os.path.isfile(PATH + 'OpenQuestion/' + k + '/OpenQuestion.txt')):
                file_path = PATH + 'OpenQuestion/' + k + '/OpenQuestion.txt'

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

                for difficulty_key in open_question_data[k].keys():
                    if difficulty_key in tmp_load.keys():
                        for i in range(int(open_question_data[k][difficulty_key])):
                            if len(tmp_load[difficulty_key]) > 0:
                                q_text = tmp_load[difficulty_key].pop()
                                open_question_ret.append(Question(user_id=self.user.id, type=0, text=q_text,
                                                                  number=0,
                                                                  question_weight=tmp_weight[difficulty_key],
                                                                  test_output_summary='Nessuna risposta fornita',
                                                                  test_output_icon=url_for('static',
                                                                                           filename="icon/cross-mark-48.png")))
        random.shuffle(open_question_ret)

        for q_i in open_question_ret:
            q_i.number = len(out_question)
            out_question.append(q_i)

        return out_question
