from flask import url_for

from webcompilingexams.models import Question


class DebugLoadQuestion:
    def __init__(self, user):
        self.user = user

    def load(self):
        return [
            Question(user_id=self.user.id, number=0, type=2, text='Domanda 1', options="",
                     answer='', compiler_output='',
                     test_output='',
                     test_output_summary='Nessun test eseguito',
                     test_output_icon=url_for('static', filename="icon/question-mark-64.png")),
            Question(user_id=self.user.id, number=1, type=3, text='Domanda 2', options="",
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
