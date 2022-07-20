from webcompilingexams.models import Question


class DebugLoadQuestion:
    def __init__(self, user):
        self.user = user

    def load(self):
        return [
            Question(user_id=self.user.id, number=0, type=0, text='Domanda 1', answer='Inserisci la risposta quì.',
                     compiler_output='Output Compilatore 1', test_output='Output Test 1'),
            Question(user_id=self.user.id, number=1, type=5, text='Domanda 2', answer='Inserisci la risposta quì.',
                     compiler_output='Output Compilatore 2', test_output='Output Test 2'),
            Question(user_id=self.user.id, number=2, type=6, text='Domanda 3', answer='Inserisci la risposta quì.',
                     compiler_output='Output Compilatore 3', test_output='Output Test 3'),
            Question(user_id=self.user.id, number=3, type=8, text='Domanda 4', answer='Inserisci la risposta quì.',
                     compiler_output='Output Compilatore 4', test_output='Output Test 4'),
        ]
