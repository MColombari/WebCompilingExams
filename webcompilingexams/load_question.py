from flask import url_for

from webcompilingexams.models import Question


class DebugLoadQuestion:
    def __init__(self, user):
        self.user = user

    def load(self):
        return [
            Question(user_id=self.user.id, number=0, type=2, text='Domanda 1', options="",
                     answer='Inserisci la risposta quì.', compiler_output='Output Compilatore 1',
                     test_output='NaN',
                     test_output_summary='Nessun test eseguito',
                     test_output_icon=url_for('static', filename="icon/question-mark-64.png")),
            Question(user_id=self.user.id, number=1, type=3, text='Domanda 2', options="",
                     answer='Inserisci la risposta quì.', compiler_output='Output Compilatore 2',
                     test_output='NaN',
                     test_output_summary='Nessun test eseguito',
                     test_output_icon=url_for('static', filename="icon/question-mark-64.png")),
            Question(user_id=self.user.id, number=2, type=1, text='Domanda 3', options="a\nb\nc\nd",
                     answer='', compiler_output='Output Compilatore 3',
                     test_output='NaN',
                     test_output_summary='Nessun test eseguito',
                     test_output_icon=url_for('static', filename="icon/question-mark-64.png")),
            Question(user_id=self.user.id, number=3, type=1, text='Domanda 3.1', options="a",
                     answer='', compiler_output='Output Compilatore 3.1',
                     test_output='NaN',
                     test_output_summary='Nessun test eseguito',
                     test_output_icon=url_for('static', filename="icon/question-mark-64.png")),
            Question(user_id=self.user.id, number=4, type=1, text='Domanda 3.2', options="a\nb\nc\nd\n1\n2\n3\n4\n5\n6",
                     answer='', compiler_output='Output Compilatore 3.2',
                     test_output='NaN',
                     test_output_summary='Nessun test eseguito',
                     test_output_icon=url_for('static', filename="icon/question-mark-64.png")),
            Question(user_id=self.user.id, number=5, type=0, text='Domanda 4', options="",
                     answer='Inserisci la risposta quì.', compiler_output='Output Compilatore 4',
                     test_output='NaN',
                     test_output_summary='Nessun test eseguito',
                     test_output_icon=url_for('static', filename="icon/question-mark-64.png")),
        ]
