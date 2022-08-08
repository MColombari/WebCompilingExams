from webcompilingexams import QUESTION_TYPE, CHARACTER_SEPARATOR


class SaveUserData:
    def __init__(self, user):
        self.user = user

    def save(self):
        out = []

        single_out = ["Dati utente:\n",
                      f'Matricola: {self.user.id}',
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

        with open(f'/app/student_exam/u{self.user.id}/user_results', 'w') as f:
            f.write('\n\n'.join(out))

        with open(f'/app/student_exam/u{self.user.id}/raw_result_data', 'w') as f:
            out = [f'{self.user}']
            for question in self.user.questions:
                out.append(f'{question}')

            f.write('\n\n'.join(out))