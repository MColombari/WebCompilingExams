import yaml


class ExamInformation:
    def __init__(self, path):
        yaml.warnings({'YAMLLoadWarning': False})
        with open(str(path)) as f:
            self.config = yaml.load(f)

    def load_generic_information(self):
        if int(self.config['General']['Duration']) == 0:
            return {"Durata": "Nessun limite di tempo",
                    "Numero di domande": str(self.config['General']['NumberOfQuestion']),
                    }

        return {"Durata": str(self.config['General']['Duration']) + " minuti",
                "Numero di domande": str(self.config['General']['NumberOfQuestion']),
                }

    def load_duration(self):
        return int(self.config['General']['Duration'])

    def load_questions_data(self):
        return self.config['Questions']

    def load_admin_information(self):
        return {"Username": str(self.config['AdminCredential']['Username']),
                "Password": str(self.config['AdminCredential']['Password']),
                }
