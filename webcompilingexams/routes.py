import os

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta

from webcompilingexams import app, db, QUESTION_TYPE, CHARACTER_SEPARATOR, ADMIN_ID
from webcompilingexams.form import RegistrationForm, QuestionForm, AdminLoginForm, AdminForm
from webcompilingexams.load_exam_information import ExamInformation
from webcompilingexams.load_question import LoadQuestion
from webcompilingexams.log import Log
from webcompilingexams.models import User, Question
from webcompilingexams.run_program import RunManager
from webcompilingexams.save_user_data import SaveUserData
from webcompilingexams import DATE
from webcompilingexams import DIR_DATE

log = Log('/app/log.txt')

if not os.path.isdir('/app/past_student_exam'):
    os.mkdir('/app/past_student_exam')


@app.route('/', methods=['GET', 'POST'])
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        if current_user.exam_started:
            if current_user.exam_finished:
                flash('Logout forzato poiché l\'esame è terminato.', 'danger')
                return redirect(url_for('logout'))
            flash('L\'esame è in corso di svolgimento', 'warning')
            return redirect(url_for('exam'))
        flash('L\'utente è già registrato', 'warning')
        return redirect(url_for('start_exam'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(id=int(form.matricola.data), name=form.nome.data, surname=form.cognome.data,
                    email=form.email.data)

        if User.query.filter_by(id=int(form.matricola.data), email=form.email.data, restart_token=True).count() == 1:
            login_user(user, True)
            user = User.query.filter_by(id=int(form.matricola.data), email=form.email.data, restart_token=True).first()
            user.exam_started = True
            user.exam_finished = False
            user.exam_checked = False
            user.restart_token = False
            db.session.commit()

            log.write(f'[User: {user.id}] used the access token to log again to the exam.')
            return redirect(url_for('start_exam'))

        db.session.add(user)
        db.session.commit()
        login_user(user, True)

        flash('Registrazione utente completata', 'success')

        log.write(f'[User: {user.id}] registered to the exam.')
        return redirect(url_for('start_exam'))

    return render_template('user_registration.html',
                           title='Registration',
                           page_title=ExamInformation('/app/config.yaml').load_title(),
                           form=form,
                           bottom_bar_left=DATE,
                           bottom_bar_center='Registrazione',
                           bottom_bar_right='Attesa registrazione'
                           )


@app.route('/login-admin', methods=['GET', 'POST'])
def login_administrator():
    if current_user.is_authenticated:
        if current_user.id == ADMIN_ID:
            flash("Login amministratore già eseguito", 'warning')
            return redirect(url_for('admin_page'))
        else:
            flash("Accesso alla pagina negato", 'danger')
            return redirect(url_for('start_exam'))

    credential = ExamInformation('/app/config.yaml').load_admin_information()

    form = AdminLoginForm()
    if form.validate_on_submit():
        if (form.name.data == credential["Username"] and
                form.password.data == credential["Password"]):
            user = User(id=ADMIN_ID, name="admin", surname="admin",
                        email="admin")
            count = User.query.filter_by(id=ADMIN_ID).count()
            if count == 0:
                db.session.add(user)
                db.session.commit()

            login_user(user, True)

            flash("Login amministratore eseguito con successo", 'success')

            log.write(f'[Admin] successfully login to the admin page.')
            return redirect(url_for('admin_page'))
        else:
            flash("Nome e/o password errati", 'warning')
            log.write(f'[Unknown] tried unsuccessfully to login to the admin page.')

    return render_template("login_administrator.html",
                           title='Admin Login',
                           page_title=ExamInformation('/app/config.yaml').load_title(),
                           bottom_bar_left=DATE,
                           bottom_bar_center='Login admin',
                           bottom_bar_right='Atteso login',
                           form=form)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_page():
    if current_user.id != ADMIN_ID:
        flash("Accesso alla pagina negato", 'danger')

        log.write(f'[User: {current_user.id}] tried to enter to the admin page.')
        return redirect(url_for('start_exam'))

    users = [u for u in User.query.all() if u.id != ADMIN_ID]
    out_users = users

    # Update answers points.
    if current_user.exam_checked:
        for user in [u for u in users if not u.exam_checked]:
            for question in user.questions:
                if question.type == 1:
                    points = 0
                    correct_answers = question.correct_answer.split(CHARACTER_SEPARATOR)
                    selected_answer = question.answer.split(CHARACTER_SEPARATOR)
                    for s_op in selected_answer:
                        if s_op != '':
                            if s_op in correct_answers:
                                points += 1
                            else:
                                points -= ExamInformation('/app/config.yaml').load_penalty()
                    points = points / len(correct_answers)

                    question.points = points
                    db.session.commit()

                elif question.type >= 2:
                    points = 0
                    if not question.test_output == '':
                        data = question.test_output.split('\n')[0].split('/')
                        if int(data[1]) == 0:
                            points = 0
                        else:
                            points = float(data[0]) / float(data[1])

                    question.points = points
                    db.session.commit()

    form = AdminForm()
    if request.method == 'POST':
        if request.form.get('delete'):
            user_id = request.form.get('delete')
            Question.query.filter_by(user_id=user_id).delete()
            User.query.filter_by(id=user_id).delete()
            db.session.commit()
            flash(f'Utente {user_id:>06} eliminato', 'success')

            log.write(f'[Admin] deleted "User: {user_id}" from the db.')
            return redirect(url_for('admin_page'))

        elif request.form.get('token'):
            user_id = request.form.get('token')
            user = User.query.filter_by(id=user_id).first()
            user.restart_token = True
            db.session.commit()

            log.write(f'[Admin] granted access token to "User: {user_id}".')
            return redirect(url_for('admin_page'))

        elif request.form.get('close_exam') == "True":
            log.write(f'[Admin] close the exam and deleted the db.')

            user_results = []

            for user in User.query.all():
                if user.id != ADMIN_ID:
                    save_user_data(user)

                    points = 0.0
                    weight_sum = 0
                    for question in user.questions:
                        points += (question.points * 100) * question.question_weight
                        weight_sum += question.question_weight

                    if weight_sum != 0:
                        points /= weight_sum

                    user_results.append(f'Matricola: {user.id:06} Punteggio: {points:.2f}/100')

            if not os.path.isdir(f'/app/past_student_exam/exam_{str(DIR_DATE)}'):
                os.mkdir(f'/app/past_student_exam/exam_{str(DIR_DATE)}')

            with open(f'/app/past_student_exam/exam_{str(DIR_DATE)}' + '/results.txt', 'a') as f:
                f.write('\n' + '\n'.join(user_results))

            Question.query.delete()
            User.query.delete()
            db.session.commit()

            admin = User(id=ADMIN_ID, name="admin", surname="admin", email="admin")
            db.session.add(admin)
            db.session.commit()

            login_user(admin, True)

            return redirect(url_for('admin_page'))

        elif request.form.get('stop_exam') == "True":
            log.write(f'[Admin] stop the exam.')

            for user in User.query.all():
                if user.id != ADMIN_ID:
                    user.exam_finished = True
            db.session.commit()

            flash('Tutti gli utenti sono stati scollegati', 'success')

            return redirect(url_for('admin_page'))

        elif request.form.get('check_exam') == "True":
            current_user.exam_checked = not current_user.exam_checked
            db.session.commit()
            return redirect(url_for('admin_page'))

        elif request.form.get('checked'):
            user_id = request.form.get('checked')
            tmp = []
            for question in Question.query.filter_by(user_id=user_id):
                question.points = float(request.form.get(f'question_value-{user_id}-{question.number}')) / 100
                question.question_weight = float(request.form.get(f'question_weight-{user_id}-{question.number}'))
                tmp.append(question.points)

            User.query.filter_by(id=user_id).first().exam_checked = True
            db.session.commit()
            flash(f"Voto salvato per l'utente: {user_id}", 'success')
            return redirect(url_for('admin_page'))

        elif form and form.text.data != '':
            tmp_u = []
            input_data = form.text.data.split(' ')
            for user in users:
                match = [((d in f"{user.id:06}") or
                          (d in user.email) or
                          (d.lower() in user.name.lower()) or
                          (d.lower() in user.surname.lower()))
                         for d in input_data]
                if len(match) > 0 and all(match):
                    tmp_u.append(user)
            out_users = tmp_u

    user_waiting = [user for user in users if (not user.exam_started) and (not user.exam_finished)]
    user_working = [user for user in users if user.exam_started and (not user.exam_finished)]
    user_finish = [user for user in users if user.exam_started and user.exam_finished]
    user_other = [user for user in users if (not user.exam_started) and user.exam_finished]
    user_checked = [user for user in users if user.exam_checked]
    user_not_checked = [user for user in users if not user.exam_checked]

    if current_user.exam_checked:
        out_users.sort(key=lambda x: x.exam_checked)

    return render_template('administrator_page.html',
                           title='Admin',
                           page_title=ExamInformation('/app/config.yaml').load_title(),
                           bottom_bar_left=DATE,
                           bottom_bar_center='Admin page',
                           bottom_bar_right='Controllo esame',
                           form=form,
                           users=out_users,
                           user_waiting=len(user_waiting),
                           user_working=len(user_working),
                           user_finish=len(user_finish),
                           user_other=len(user_other),
                           user_checked=len(user_checked),
                           user_not_checked=len(user_not_checked),
                           CHARACTER_SEPARATOR=CHARACTER_SEPARATOR
                           )


@app.route('/start')
@login_required
def start_exam():
    if current_user.exam_finished:
        flash('Logout forzato poiché l\'esame è terminato.', 'danger')
        return redirect(url_for('logout'))

    if current_user.exam_started:
        flash('L\'esame è in corso di svolgimento', 'warning')
        return redirect(url_for('exam'))

    information = ExamInformation('/app/config.yaml').load_generic_information()
    return render_template("start_exam.html",
                           title='Start',
                           page_title=ExamInformation('/app/config.yaml').load_title(),
                           bottom_bar_left=DATE,
                           bottom_bar_center='Waiting room',
                           bottom_bar_right='In attesa dell\' inizio dell\'esame',
                           exam_information=information
                           )


@app.route('/starting')
@login_required
def starting_exam():
    if current_user.exam_finished:
        flash('Logout forzato poiché l\'esame è terminato.', 'danger')
        return redirect(url_for('logout'))

    if current_user.exam_started:
        flash('L\'esame è in corso di svolgimento', 'warning')
        return redirect(url_for('exam'))

    questions = LoadQuestion(current_user, ExamInformation('/app/config.yaml')).load()
    for q in questions:
        db.session.add(q)

    RunManager.create_directory(current_user.id)

    current_user.time_of_start = str((datetime.today() + timedelta(hours=2)).strftime('%Y / %m / %d - %H:%M:%S'))

    current_user.exam_started = True
    db.session.commit()

    log.write(f'[User: {current_user.id}] started the exam.')
    return redirect(url_for('exam'))


@app.route('/exam', methods=['GET', 'POST'])
@login_required
def exam():
    duration = ExamInformation('/app/config.yaml').load_duration()
    if duration > 0 and current_user.time_of_start != '':
        start_date = datetime.strptime(current_user.time_of_start, '%Y / %m / %d - %H:%M:%S')
        time_now = (datetime.today() + timedelta(hours=2))

        date_difference = time_now - start_date

        if date_difference.total_seconds() > (duration * 60):
            current_user.exam_finished = True
            db.session.commit()
            flash('Logout forzato poiché l\'esame è terminato.', 'danger')
            return redirect(url_for('logout'))

    if current_user.exam_finished:
        flash('Logout forzato poiché l\'esame è terminato.', 'danger')
        return redirect(url_for('logout'))

    if not current_user.exam_started:
        flash('Per accedere alla pagina è necessario avviare l\'esame', 'warning')
        return redirect(url_for('start_exam'))

    index = request.args.get('index')
    if index:
        current_user.index_question = index
        db.session.commit()

    index_current_question = int(current_user.index_question)
    if index_current_question < 0:
        index_current_question = 0
    elif index_current_question >= len(current_user.questions):
        index_current_question = len(current_user.questions) - 1

    if index_current_question != current_user.index_question:
        current_user.index_question = index_current_question
        db.session.commit()

    current_question = next((q for q in current_user.questions if q.number == index_current_question))

    form = QuestionForm()
    if request.method == 'POST':
        # Save answer.
        if current_question.type != 1:
            current_question.answer = str(form.text.data)
            db.session.commit()
        else:
            # This could happen after a selection of a multiple choice question.
            answer_selected = None
            options = current_question.options.split(CHARACTER_SEPARATOR)
            for i in range(len(options)):
                if request.form.get(str(i)) == str(options[i]):
                    answer_selected = i
            if answer_selected is not None:
                if str(answer_selected) in current_question.answer:
                    # Remove selected question.
                    current_question.answer = current_question.answer.replace(f'{CHARACTER_SEPARATOR}{answer_selected}',
                                                                              '')
                else:
                    # Add selected question.
                    current_question.answer += f'{CHARACTER_SEPARATOR}{answer_selected}'
                db.session.commit()

        # Update answer summary.
        if current_question.type <= 1:
            if current_question.answer != '':
                current_question.test_output_summary = 'Risposta fornita'
                current_question.test_output_icon = url_for('static', filename="icon/check-mark-48.png")
            else:
                current_question.test_output_summary = 'Nessuna risposta fornita'
                current_question.test_output_icon = url_for('static', filename="icon/cross-mark-48.png")
            db.session.commit()

        # Other button pressed.
        if request.form.get('compile') == 'True':
            RunManager(current_user, current_question).compile()
            return redirect(url_for('exam'))

        if request.form.get('test') == 'True':
            RunManager(current_user, current_question).test()
            return redirect(url_for('exam'))

        if request.form.get('recap') == 'Revisione domande':
            return redirect(url_for('recap'))

        if request.form.get('sub') == 'Indietro':
            current_user.index_question = index_current_question - 1
            db.session.commit()
            return redirect(url_for('exam'))

        if request.form.get('add') == 'Avanti':
            current_user.index_question = index_current_question + 1
            db.session.commit()
            return redirect(url_for('exam'))

        if request.form.get('end') == 'Termina esame':
            return redirect(url_for('logout'))

    # Render "exam.html" page.
    if current_question.type == 1:
        options = current_question.options.split(CHARACTER_SEPARATOR)
        form.multiple_field_data = [(str(i), options[i]) for i in range(len(options))]
    else:
        form.text.data = current_question.answer

    second_to_end = None
    if duration > 0 and current_user.time_of_start != '':
        start_date = datetime.strptime(current_user.time_of_start, '%Y / %m / %d - %H:%M:%S')
        time_now = (datetime.today() + timedelta(hours=2))

        second_to_end = (duration * 60) - (time_now - start_date).total_seconds()

    return render_template("exam.html",
                           title='Esame',
                           page_title=ExamInformation('/app/config.yaml').load_title(),
                           bottom_bar_left=DATE,
                           bottom_bar_center='Esame',
                           bottom_bar_right='Esame in corso',
                           question=current_question,
                           questions_number=len(current_user.questions),
                           preselected=current_question.answer.split(CHARACTER_SEPARATOR),
                           index=index_current_question,
                           form=form,
                           QUESTION_TYPE=QUESTION_TYPE,
                           second_to_end=second_to_end
                           )


@app.route('/recap')
@login_required
def recap():
    duration = ExamInformation('/app/config.yaml').load_duration()
    if duration > 0 and current_user.time_of_start != '':
        start_date = datetime.strptime(current_user.time_of_start, '%Y / %m / %d - %H:%M:%S')
        time_now = (datetime.today() + timedelta(hours=2))

        date_difference = time_now - start_date

        if date_difference.total_seconds() > (duration * 60):
            current_user.exam_finished = True
            db.session.commit()
            flash('Logout forzato poiché l\'esame è terminato.', 'danger')
            return redirect(url_for('logout'))

    if current_user.exam_finished:
        flash('Logout forzato poiché l\'esame è terminato.', 'danger')
        return redirect(url_for('logout'))

    if not current_user.exam_started:
        flash('Per accedere alla pagina è necessario avviare l\'esame', 'warning')
        return redirect(url_for('start_exam'))
    return render_template('recap.html',
                           title='Recap Esame',
                           page_title=ExamInformation('/app/config.yaml').load_title(),
                           bottom_bar_left=DATE,
                           bottom_bar_center='Recap',
                           bottom_bar_right='Revisione domande',
                           sorted_questions=sorted(current_user.questions, key=lambda q: q.number))


def save_user_data(user):
    if user.id == ADMIN_ID:
        return

    SaveUserData(user).save()
    if not user.exam_finished:
        user.exam_finished = True
        db.session.commit()


@app.route('/logout')
@login_required
def logout():
    if current_user.id == ADMIN_ID:
        logout_user()

        log.write(f'[Admin] logged out.')
        return redirect(url_for('login_administrator'))

    save_user_data(current_user)

    user_id = current_user.id
    logout_user()

    flash('Logout eseguito con successo', 'success')

    log.write(f'[User: {user_id}] terminate the exam and logged out.')
    return render_template('logout_page.html',
                           title='Esame Terminato',
                           page_title=ExamInformation('/app/config.yaml').load_title(),
                           bottom_bar_left=DATE,
                           bottom_bar_center='Uscita',
                           bottom_bar_right='Attesa uscita')


@app.errorhandler(HTTPException)
def errorhandler(e):
    print(f"{e.code}, {e.name}, {e.description}")
    log.write(f'[ERROR] "{e.code}" - "{e.name}" - "{e.description}".')
    return e
