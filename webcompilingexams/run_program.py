import os
import shutil
import subprocess
import threading

from flask import flash, url_for

from webcompilingexams import db
from webcompilingexams import DIR_DATE


class RunManager:
    def __init__(self, user, question):
        self.user = user
        self.question = question
        self.stderr = None
        self.stdout = None

    @staticmethod
    def create_directory(user_id):
        DIR_PATH = f'/app/exam/exam_{str(DIR_DATE)}'
        USER_DIR_PATH = DIR_PATH + f'/u{user_id:06}'

        if not os.path.isdir(DIR_PATH):
            os.mkdir(DIR_PATH)
        if not os.path.isdir(USER_DIR_PATH):
            os.mkdir(USER_DIR_PATH)

    def compile(self):
        PATH = f'/app/exam/exam_{str(DIR_DATE)}/u{self.user.id:06}'

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

        db.session.commit()

    def test(self):
        PATH = f'/app/exam/exam_{str(DIR_DATE)}/u{self.user.id:06}'
        TEST_CONTENT = str(self.question.options)
        LOCAL_PATH = f'exam/exam_{str(DIR_DATE)}/u{self.user.id:06}'

        if self.question.type == 2:
            words = self.question.answer.split()
            class_index = [out[0] for out in enumerate(words) if out[1].lower() == 'class']
            if len(class_index) > 0 and (class_index[0] + 1) <= (len(words) - 1):
                class_name = words[class_index[0] + 1].replace("{", "")
            else:
                flash('Nessuna classe trovata', 'warning')
                return

            with open(PATH + f'/{class_name}.java', 'w') as f:
                f.write(f'package exam.exam_{str(DIR_DATE)}.u{self.user.id:06};\n')
                f.write(self.question.answer)

            words = TEST_CONTENT.split()
            test_class_index = [out[0] for out in enumerate(words) if out[1].lower() == 'class']
            test_class_name = words[test_class_index[0] + 1].replace("{", "")

            test_name = test_class_name + ".java"
            with open(PATH + '/' + test_name, 'w') as f_out:
                f_out.write(f'package exam.exam_{str(DIR_DATE)}.u{self.user.id:06};\n')
                f_out.write(TEST_CONTENT)

            t = CommandRun(['javac', LOCAL_PATH + '/' + test_name, LOCAL_PATH + f'/{class_name}.java'], self)
            t.start()
            t.join()

            if (self.stderr != '') or (self.stdout != ''):
                self.question.test_output = ''
                self.question.compiler_output = self.stdout + '\n' + self.stderr
                self.question.test_output_summary = 'Errore compilatione'
                self.question.test_output_icon = url_for('static', filename="icon/cross-mark-48.png")
                flash('Errore compilazione', 'warning')
                db.session.commit()
                return

            t = CommandRun(['java', LOCAL_PATH + '/' + test_name.split('.java')[0]], self)
            t.start()
            t.join()

            if 'La compilazione ha richiesto più di 5 secondi' in self.stdout:
                self.question.test_output = ''
                self.question.compiler_output = self.stdout
                self.question.test_output_summary = 'Errore test'
                self.question.test_output_icon = url_for('static', filename="icon/cross-mark-48.png")
                flash('Errore test', 'warning')
                db.session.commit()
                return

            result = str(self.stdout).split('\n')[0]
            count_success = result.count(".")
            count_failed = result.count("F")

            self.question.test_output = f'{count_success}/{count_success + count_failed}\n' \
                                        f'Test passati: {count_success}\n' \
                                        f'Test falliti: {count_failed}'

            if count_failed == 0:
                self.question.test_output_summary = 'Tutti i test passati'
                self.question.test_output_icon = url_for('static', filename="icon/check-mark-48.png")
            elif count_failed != 0 and count_success != 0:
                self.question.test_output_summary = 'Alcuni test passati e altri no'
                self.question.test_output_icon = url_for('static', filename="icon/cross-mark-48.png")
            else:
                self.question.test_output_summary = 'Nessun test passato'
                self.question.test_output_icon = url_for('static', filename="icon/cross-mark-48.png")

            tmp_out = self.stdout.split('\n')
            del tmp_out[0]
            self.question.compiler_output = '\n'.join(tmp_out)

            db.session.commit()

        elif self.question.type == 3:
            with open(PATH + '/RunningFile.py', 'w') as f:
                f.write(self.question.answer)

            t = CommandRun(['python3', PATH + '/RunningFile.py'], self)
            t.start()
            t.join()

            if self.stderr == '':
                self.question.compiler_output = 'Il compilatore non ha trovato nessun errore.'
            else:
                self.question.test_output = ''
                self.question.compiler_output = self.stderr
                self.question.test_output_summary = 'Errore compilazione'
                self.question.test_output_icon = url_for('static', filename="icon/cross-mark-48.png")
                flash('Errore compilazione', 'warning')
                db.session.commit()
                return

            with open(PATH + '/TestFile.py', 'w') as f:
                f.write(TEST_CONTENT)

            t = CommandRun(['python3', PATH + '/TestFile.py'], self)
            t.start()
            t.join()

            if 'La compilazione ha richiesto più di 5 secondi' in self.stdout:
                self.question.test_output = ''
                self.question.compiler_output = self.stdout
                self.question.test_output_summary = 'Errore test'
                self.question.test_output_icon = url_for('static', filename="icon/cross-mark-48.png")
                flash('Errore test', 'warning')
                db.session.commit()
                return

            result = str(self.stderr).split('\n')[0]
            count_success = result.count(".")
            count_failed = result.count("F")
            count_failed += result.count("E")

            self.question.test_output = f'{count_success}/{count_success + count_failed}\n' \
                                        f'Test passati: {count_success}\n' \
                                        f'Test falliti: {count_failed}'

            if count_failed == 0 and count_success != 0:
                self.question.test_output_summary = 'Tutti i test passati'
                self.question.test_output_icon = url_for('static', filename="icon/check-mark-48.png")
            elif count_failed != 0 and count_success != 0:
                self.question.test_output_summary = 'Alcuni test passati e altri no'
                self.question.test_output_icon = url_for('static', filename="icon/cross-mark-48.png")
            else:
                self.question.test_output_summary = 'Nessun test passato'
                self.question.test_output_icon = url_for('static', filename="icon/cross-mark-48.png")

            result = str(self.stderr).split('----------------------------------------------------------------------')
            out = []
            for i in range(count_failed):
                if len(result) > i + 1:
                    out.append(result[i + 1]
                               .split("======================================================================")[0])

            self.question.compiler_output = ''.join(out)

            db.session.commit()

        db.session.commit()


class CommandRun(threading.Thread):
    def __init__(self, command, run_manager):
        threading.Thread.__init__(self)
        self.command = command
        self.run_manager = run_manager

    def run(self):
        try:
            process = subprocess.run(self.command, capture_output=True, encoding="utf-8",
                                     timeout=5)
            self.run_manager.stdout = process.stdout
            self.run_manager.stderr = process.stderr

        except subprocess.TimeoutExpired as e:
            self.run_manager.stdout = f'La compilazione ha richiesto più di 5 secondi\n{e}'
