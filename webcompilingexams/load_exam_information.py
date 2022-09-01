import configparser


class DebugExamInformation:
    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.read(str(path))

    def load_generic_information(self):
        return {"Durata": self.config['General']['Duration'] + " minuti",
                "Numero di domande": str(self.config['General']['NumberOfQuestion']),
                }

    def load_admin_information(self):
        return {"Username": str(self.config['AdminCredential']['Username']),
                "Password": str(self.config['AdminCredential']['Password']),
                }
