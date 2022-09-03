import os
import shutil
import subprocess
import threading

from flask import flash

from webcompilingexams import db


class RunManager:
    def __init__(self, user, question):
        self.user = user
        self.question = question
        self.stderr = None
        self.stdout = None
        self.flash = None
        self.flash_type = None

    @staticmethod
    def create_directory(user_id):
        if not os.path.isdir(f'/app/student_exam/u{user_id:06}'):
            os.mkdir(f'/app/student_exam/u{user_id:06}')

    def compile(self):
        PATH = f'/app/student_exam/u{self.user.id:06}'

        if self.question.type == 2:
            words = self.question.answer.split()
            class_index = [out[0] for out in enumerate(words) if out[1].lower() == 'class']
            if len(class_index) > 0 and (class_index[0] + 1) <= (len(words) - 1):
                class_name = words[class_index[0] + 1].replace("{", "")
            else:
                flash('Nessuna classe trovata', 'warning')
                return

            with open(PATH + f'/{class_name}.java', 'w') as f:
                f.write(self.question.answer)
            # '-proc:only' suppress .class file generation.
            # '-Xlint:none' suppress warning due to a warning generated using '-proc:only'.
            t = CommandRun(['javac', '-proc:only', '-Xlint:none', PATH + f'/{class_name}.java'], self)
            t.start()
            t.join()

        elif self.question.type == 3:
            with open(PATH + '/RunningFile.py', 'w') as f:
                f.write(self.question.answer)

            t = CommandRun(['python3', PATH + '/RunningFile.py'], self)
            t.start()
            t.join()

        if self.stderr == '':
            self.question.compiler_output = 'Il compilatore non ha trovato nessun errore.'
        else:
            self.question.compiler_output = self.stderr

        if self.flash and self.flash_type:
            flash(self.flash, self.flash_type)

        db.session.commit()

    def test(self):
        PATH = f'/app/student_exam/u{self.user.id:06}'
        TEST_PATH = str(self.question.options)

        if self.question.type == 2:
            pass
        elif self.question.type == 3:
            with open(PATH + '/RunningFile.py', 'w') as f:
                f.write(self.question.answer)

            if not os.path.isfile(TEST_PATH):
                self.question.compiler_output = ''
                self.question.test_output = 'Errore, test non trovato!'
                flash('Errore esecuzione', 'danger')
                db.session.commit()
                return

            test_name = TEST_PATH.split('/')[-1]
            shutil.copyfile(TEST_PATH, PATH + '/' + test_name)

            t = CommandRun(['python3', PATH + '/' + test_name], self)
            t.start()
            t.join()

            result = str(self.stderr).split('\n')[0]
            count_success = result.count(".")
            count_failed = result.count("F")

            self.question.test_output = f'''Test passati: {count_success}
                                            Test falliti: {count_failed}'''

            result = str(self.stderr).split('----------------------------------------------------------------------')
            out = []
            for i in range(count_failed):
                if len(result) > i + 1:
                    out.append(result[i + 1]
                               .split("======================================================================")[0])

            self.question.compiler_output = ''.join(out)

            db.session.commit()

        if self.flash and self.flash_type:
            flash(self.flash, self.flash_type)

        db.session.commit()


class CommandRun(threading.Thread):
    def __init__(self, command, run_manager):
        threading.Thread.__init__(self)
        self.command = command
        self.run_manager = run_manager

    def run(self):
        flash_type = 'success'
        try:
            process = subprocess.run(self.command, capture_output=True, encoding="utf-8",
                                     timeout=5)
            self.run_manager.stdout = process.stdout
            self.run_manager.stderr = process.stderr

        except subprocess.TimeoutExpired as e:
            self.run_manager.terminal_output = f'La compilazione ha richiesto più di 5 secondi\n{e}'
            flash_type = 'warning'
        finally:
            self.run_manager.flash = 'Compilazione completata'
            self.run_manager.flash_type = flash_type
