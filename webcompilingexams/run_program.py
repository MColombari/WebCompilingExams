import os
import subprocess
import threading
from flask import flash, redirect, url_for
from webcompilingexams import db, app


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
        self.user.is_running = True
        db.session.commit()

        if self.question.type == 2:
            t = JavaCompileRun(self.question.answer, self.question.user_id, self)
            t.start()
            t.join()
        elif self.question.type == 3:
            pass

        if self.terminal_output:
            self.question.compiler_output = self.terminal_output

        if self.test_output:
            self.question.compiler_output = self.test_output

        if self.flash and self.flash_type:
            flash(self.flash, self.flash_type)

        self.user.is_running = False
        db.session.commit()

    def test(self):
        pass


class JavaCompileRun(threading.Thread):
    def __init__(self, program, user_id, run_manager):
        threading.Thread.__init__(self)
        self.program = program
        self.user_id = user_id
        self.run_manager = run_manager

    def run(self):
        PATH = f'/app/student_exam/u{self.user_id}'
        flash_type = 'success'

        with open(PATH + '/RunningFile.java', 'w') as f:
            f.write("public class RunningFile{\n"
                    "   public static void main(String[] args){}\n"
                    f"   {self.program}\n"
                    "}\n")

        try:
            process = subprocess.run(['java', PATH + '/RunningFile.java'], capture_output=True, encoding="utf-8",
                                     timeout=5)
            if process.stderr == '':
                self.run_manager.terminal_output = "Il compilatore non ha trovato nessun errore."
            else:
                self.run_manager.terminal_output = process.stderr

            with open(PATH + '/compuler_out.txt', 'w') as f:
                f.write(f'stdout:\n{process.stdout}\nstderr:\n{process.stderr}')
        except subprocess.TimeoutExpired as e:
            self.run_manager.terminal_output = f'La compilazione ha richiesto più di 5 secondi\n{e}'
            flash_type = 'warning'
        finally:
            self.run_manager.flash = 'Compilazione completata'
            self.run_manager.flash_type = flash_type
