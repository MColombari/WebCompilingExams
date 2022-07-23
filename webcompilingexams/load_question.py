from webcompilingexams.models import Question


class DebugLoadQuestion:
    def __init__(self, user):
        self.user = user

    def load(self):
        return [
            Question(user_id=self.user.id, number=0, type=0, text='Domanda 1', options="",
                     answer='Inserisci la risposta quì.',
                     compiler_output='Output Compilatore 1', test_output='Output Test 1'),
            Question(user_id=self.user.id, number=1, type=1, text='Domanda 2', options="",
                     answer='Inserisci la risposta quì.',
                     compiler_output='Output Compilatore 2', test_output='Output Test 2'),
            Question(user_id=self.user.id, number=2, type=2, text='Domanda 3', options="a\nb\nc\nd",
                     answer='', compiler_output='Output Compilatore 3', test_output='Output Test 3'),
            Question(user_id=self.user.id, number=3, type=3, text='Domanda 4', options="",
                     answer='Inserisci la risposta quì.',
                     compiler_output='Output Compilatore 4', test_output='Output Test 4'),
        ]
