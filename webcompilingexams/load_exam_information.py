import yaml


class ExamInformation:
    def __init__(self, path):
        yaml.warnings({'YAMLLoadWarning': False})
        with open(str(path)) as f:
            self.config = yaml.load(f)

    def load_title(self):
        return str(self.config['Title'])

    def load_generic_information(self):
        ret_dict = {}
        info_dict = self.config['Questions']
        total_count = 0

        duration = "Nessun limite di tempo"
        if int(self.config['General']['Duration']) != 0:
            duration = str(self.config['General']['Duration']) + " minuti"

        for key in info_dict.keys():
            total_count += int(info_dict[key])

        ret_dict["Durata"] = duration
        ret_dict["Numero totale di domande"] = total_count

        for key in info_dict.keys():
            ret_dict[key] = info_dict[key]

        ret_dict["Penalità in caso di errore domande a risposta multipla"] = str(self.load_penalty())

        return ret_dict

    def load_duration(self):
        return int(self.config['General']['Duration'])

    def load_penalty(self):
        return float(self.config['General']['WrongOptionQuestionPenalty'])

    def load_difficulty(self):
        return str(self.config["Difficulty"])

    def load_questions_data(self):
        return self.config['Questions']

    def load_admin_information(self):
        return {"Username": str(self.config['AdminCredential']['Username']),
                "Password": str(self.config['AdminCredential']['Password']),
                }
