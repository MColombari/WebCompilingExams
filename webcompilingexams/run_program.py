import os
import shutil
import subprocess
import threading

from flask import flash, url_for

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
        LOCAL_PATH = f'student_exam/u{self.user.id:06}'

        if self.question.type == 2:
            words = self.question.answer.split()
            class_index = [out[0] for out in enumerate(words) if out[1].lower() == 'class']
            if len(class_index) > 0 and (class_index[0] + 1) <= (len(words) - 1):
                class_name = words[class_index[0] + 1].replace("{", "")
            else:
                flash('Nessuna classe trovata', 'warning')
                return

            with open(PATH + f'/{class_name}.java', 'w') as f:
                f.write(f'package student_exam.u{self.user.id:06};\n')
                f.write(self.question.answer)

            if not os.path.isfile(TEST_PATH):
                self.question.compiler_output = ''
                self.question.test_output = 'Errore, test non trovato!'
                flash('Errore esecuzione', 'danger')
                db.session.commit()
                return

            test_name = TEST_PATH.split('/')[-1]
            with open(PATH + '/' + test_name, 'w') as f_out:
                f_out.write(f'package student_exam.u{self.user.id:06};\n')
                with open(TEST_PATH, 'r') as f_in:
                    f_out.write(f_in.read())

            t = CommandRun(['javac', LOCAL_PATH + '/' + test_name, LOCAL_PATH + f'/{class_name}.java'], self)
            t.start()
            t.join()

            if (self.stderr != '') or (self.stdout != ''):
                self.question.test_output = 'Compilazione fallita'
                self.question.compiler_output = self.stdout + '\n' + self.stderr
                db.session.commit()
                return

            t = CommandRun(['java', LOCAL_PATH + '/' + test_name.split('.java')[0]], self)
            t.start()
            t.join()

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
