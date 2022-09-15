import yaml


class ExamInformation:
    def __init__(self, path):
        yaml.warnings({'YAMLLoadWarning': False})
        with open(str(path)) as f:
            self.config = yaml.load(f)

    def load_generic_information(self):
        return {"Durata": str(self.config['General']['Duration']) + " minuti",
                "Numero di domande": str(self.config['General']['NumberOfQuestion']),
                }

    def load_questions_data(self):
        return self.config['Questions']

    def load_admin_information(self):
        return {"Username": str(self.config['AdminCredential']['Username']),
                "Password": str(self.config['AdminCredential']['Password']),
                }
