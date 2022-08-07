import os
import subprocess
import threading

from flask import flash

from webcompilingexams import db


class RunManager:
    def __init__(self, user, question):
        self.user = user
        self.question = question
        self.terminal_output = None
        self.test_output = None
        self.flash = None
        self.flash_type = None

    @staticmethod
    def create_directory(user_id):
        os.mkdir(f'/app/student_exam/u{user_id}')

    def compile(self):
        PATH = f'/app/student_exam/u{self.user.id}'

        if self.question.type == 2:
            with open(PATH + '/RunningFile.java', 'w') as f:
                f.write("public class RunningFile{\n"
                        f"   {self.question.answer}\n"
                        "}")
            # '-proc:only' suppress .class file generation.
            # '-Xlint:none' suppress warning due to a warning generated using '-proc:only'.
            t = CompileRun(['javac', '-proc:only', '-Xlint:none', PATH + '/RunningFile.java'], self)
            t.start()
            t.join()

        elif self.question.type == 3:
            with open(PATH + '/RunningFile.py', 'w') as f:
                f.write(self.question.answer)

            t = CompileRun(['python3', PATH + '/RunningFile.py'], self)
            t.start()
            t.join()

        if self.terminal_output:
            self.question.compiler_output = self.terminal_output

        if self.test_output:
            self.question.compiler_output = self.test_output

        if self.flash and self.flash_type:
            flash(self.flash, self.flash_type)

        db.session.commit()

    def test(self):
        pass


class CompileRun(threading.Thread):
    def __init__(self, command, run_manager):
        threading.Thread.__init__(self)
        self.command = command
        self.run_manager = run_manager

    def run(self):
        flash_type = 'success'
        try:

            process = subprocess.run(self.command, capture_output=True, encoding="utf-8",
                                     timeout=5)
            if process.stderr == '':
                self.run_manager.terminal_output = "Il compilatore non ha trovato nessun errore."
            else:
                self.run_manager.terminal_output = process.stderr
        except subprocess.TimeoutExpired as e:
            self.run_manager.terminal_output = f'La compilazione ha richiesto più di 5 secondi\n{e}'
            flash_type = 'warning'
        finally:
            self.run_manager.flash = 'Compilazione completata'
            self.run_manager.flash_type = flash_type
