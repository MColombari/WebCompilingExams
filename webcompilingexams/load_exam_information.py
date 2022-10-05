import yaml


class ExamInformation:
    def __init__(self, path):
        yaml.warnings({'YAMLLoadWarning': False})
        with open(str(path)) as f:
            self.config = yaml.load(f)

    def load_title(self):
        return str(self.config['Title'])

    def load_generic_information(self):
        open_question_count = sum(
            [sum([int(val) for val in self.config['Questions']['OpenQuestion'][k].values()]) for k in
             self.config['Questions']['OpenQuestion'].keys()]
        )
        option_question_count = sum(
            [sum([int(val) for val in self.config['Questions']['MultipleOptionQuestion'][k].values()]) for k in
             self.config['Questions']['MultipleOptionQuestion'].keys()]
        )
        java_question_count = sum(
            [sum([int(val) for val in self.config['Questions']['Java'][k].values()]) for k in
             self.config['Questions']['Java'].keys()]
        )
        python_question_count = sum(
            [sum([int(val) for val in self.config['Questions']['Python'][k].values()]) for k in
             self.config['Questions']['Python'].keys()]
        )

        total_count = open_question_count + option_question_count + java_question_count + python_question_count
        duration = "Nessun limite di tempo"

        if int(self.config['General']['Duration']) != 0:
            duration = str(self.config['General']['Duration']) + " minuti"

        return {"Durata": duration,
                "Numero totale di domande": total_count,
                "Domande di programmazione su java": java_question_count,
                "Domande di programmazione su python": python_question_count,
                "Domande a risposta multipla": option_question_count,
                "Domande a risposta aperta": open_question_count,
                "Penalità in caso di errore domande a risposta multipla": str(self.load_penalty())
                }

    def load_duration(self):
        return int(self.config['General']['Duration'])

    def load_penalty(self):
        return float(self.config['General']['WrongOptionQuestionPenalty'])

    def load_questions_data(self):
        return self.config['Questions']

    def load_admin_information(self):
        return {"Username": str(self.config['AdminCredential']['Username']),
                "Password": str(self.config['AdminCredential']['Password']),
                }
