from webcompilingexams.models import Question

class DebugLoadQuestion:
    def __init__(self, user):
        self.user = user

    def load(self):
        return [
            Question(user_id=self.user.id, number=1, type=0, text='Domanda 1', answer='Risposta 1',
                     compiler_output='Output Compilatore 1', test_output='Output Test 1'),
            Question(user_id=self.user.id, number=2, type=5, text='Domanda 2', answer='Risposta 2',
                     compiler_output='Output Compilatore 2', test_output='Output Test 2'),
        ]