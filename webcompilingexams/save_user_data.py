import os

from webcompilingexams import QUESTION_TYPE, CHARACTER_SEPARATOR
from webcompilingexams import DIR_DATE


class SaveUserData:
    def __init__(self, user):
        self.user = user

    def save(self):
        DIR_PATH = f'/app/exam/exam_{str(DIR_DATE)}'
        USER_DIR_PATH = DIR_PATH + f'/u{self.user.id:06}'

        if not self.user.exam_started:
            if not os.path.isdir(DIR_PATH):
                os.mkdir(DIR_PATH)
            if not os.path.isdir(USER_DIR_PATH):
                os.mkdir(USER_DIR_PATH)

            with open(USER_DIR_PATH + '/user_results', 'w') as f:
                f.write('L\'utente non ha neanche iniziato l\'esame')

            with open(USER_DIR_PATH + '/raw_result_data', 'w') as f:
                f.write(f'{self.user}')

            return

        out = []

        single_out = ["Dati utente:\n",
                      f'Matricola: {self.user.id:06}',
                      f'Nome: {self.user.name}',
                      f'Congnome: {self.user.surname}',
                      f'Email: {self.user.email}']

        out.append("\n".join(single_out))

        single_out = ["Domande:\n"]
        for question in self.user.questions:
            single_out.append(f'{question.number}: "{question.text}" [{QUESTION_TYPE[question.type]}]')
            if question.type == 0:
                single_out.append(f'Risposta\n"\n{question.answer}\n"\n')
            elif question.type == 1:
                single_out.append("Opzioni:")
                options = question.options.split(CHARACTER_SEPARATOR)
                for op_index in range(len(options)):
                    if str(op_index) in question.answer:
                        single_out.append(f'\t+ {options[op_index]}.')
                    else:
                        single_out.append(f'\t- {options[op_index]}.')
                single_out.append("")
            else:
                single_out.append(f'Risposta:\n"\n{question.answer}\n"\n')

        out.append("\n".join(single_out))

        with open(USER_DIR_PATH + '/user_results', 'w') as f:
            f.write('\n\n'.join(out))

        with open(USER_DIR_PATH + '/raw_result_data', 'w') as f:
            out = [f'{self.user}']
            for question in self.user.questions:
                out.append(f'{question}')

            f.write('\n\n'.join(out))
