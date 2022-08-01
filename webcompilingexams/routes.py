from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.exceptions import HTTPException
from webcompilingexams import app, db, QUESTION_TYPE
from webcompilingexams.form import LoginForm, QuestionForm
from flask import render_template, redirect, url_for, flash, request

from webcompilingexams.load_exam_information import DebugExamInformation
from webcompilingexams.load_question import DebugLoadQuestion
from webcompilingexams.models import User

from datetime import datetime

DATE = str(datetime.today().strftime('%Y / %m / %d'))
CHARACTER_SEPARATOR = '\n'


# @app.route('/')
# def hello_world():
#    return render_template("hello_page.html", title='Home',
#                           bottom_bar_left=DATE,
#                           bottom_bar_center='Pagina di benvenuto',
#                           bottom_bar_right='Non ancora registrato')


@app.route('/', methods=['GET', 'POST'])
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        if current_user.exam_started:
            flash('L\'esame è in corso, non è possibile registrarsi nuovamente', 'danger')
            return redirect(url_for('exam'))
        flash('Utente già registrato', 'warning')
        return redirect(url_for('start_exam'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User(id=int(form.matricola.data), name=form.nome.data, surname=form.cognome.data,
                    email=form.email.data, exam_started=False, exam_finished=False, index_question=0)
        db.session.add(user)
        db.session.commit()
        login_user(user, True)

        # next_page = request.args.get('next')

        flash('User inserito con successo', 'success')

        # if next_page:
        #     return redirect(next_page)  # Vai alla pagina a cui ha cercato di andare precedentemente senza il login.

        return redirect(url_for('start_exam'))

    return render_template('user_registration.html', title='Registration', form=form,
                           bottom_bar_left=DATE,
                           bottom_bar_center='Registrazione',
                           bottom_bar_right='Attesa registrazione'
                           )


@app.route('/start')
@login_required
def start_exam():
    if current_user.exam_started:
        flash('L\'esame è giè iniziato', 'danger')
        return redirect(url_for('exam'))

    information = DebugExamInformation().load()
    return render_template("start_exam.html", title='Start',
                           bottom_bar_left=DATE,
                           bottom_bar_center='Inizio esame',
                           bottom_bar_right='In attesa dell\' inizio dell\'esame',
                           exam_information=information
                           )


@app.route('/starting')
@login_required
def starting_exam():
    if current_user.exam_started:
        flash('L\'esame è giè iniziato', 'danger')
        return redirect(url_for('exam'))

    questions = DebugLoadQuestion(current_user).load()
    for q in questions:
        db.session.add(q)

    current_user.exam_started = True
    db.session.commit()

    return redirect(url_for('exam'))


@app.route('/exam', methods=['GET', 'POST'])
@login_required
def exam():
    index_current_question = current_user.index_question
    if index_current_question < 0:
        index_current_question = 0
    elif index_current_question >= len(current_user.questions):
        index_current_question = len(current_user.questions) - 1

    if index_current_question != current_user.index_question:
        current_user.index_question = index_current_question
        db.session.commit()

    current_question = None
    for q in current_user.questions:
        if q.number == index_current_question:
            current_question = q

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
                    current_question.answer = current_question.answer.replace(f'{CHARACTER_SEPARATOR}{answer_selected}',
                                                                              '')
                else:
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

        if request.form.get('compile') == 'True':
            flash('Inizio compilazione', 'warning')
            return redirect(url_for('exam'))

        if request.form.get('test') == 'True':
            flash('Inizio test', 'warning')
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
            flash('Logout eseguito con successo', 'success')
            return redirect(url_for('logout'))

    if current_question.type == 1:
        options = current_question.options.split(CHARACTER_SEPARATOR)
        form.multiple_field_data = [(str(i), options[i]) for i in range(len(options))]
    else:
        form.text.data = current_question.answer

    return render_template("exam.html", title='Esame',
                           bottom_bar_left=DATE,
                           bottom_bar_center='Esame',
                           bottom_bar_right='Esame in svolgimento',
                           question=current_question,
                           questions_number=len(current_user.questions),
                           preselected=current_question.answer.split(CHARACTER_SEPARATOR),
                           index=index_current_question,
                           form=form,
                           QUESTION_TYPE=QUESTION_TYPE
                           )


@app.route('/recap')
@login_required
def recap():
    if not current_user.exam_started:
        flash('L\'esame non è stato iniziato', 'danger')
        return redirect(url_for('start_exam'))
    return render_template('recap.html', title='Recap Esame',
                           bottom_bar_left=DATE,
                           bottom_bar_center='Esame',
                           bottom_bar_right='Revisione domande',
                           sorted_questions=sorted(current_user.questions, key=lambda q: q.number))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    current_user.exam_started = True
    db.session.commit()

    flash('User scollegato con successo', 'success')
    return redirect(url_for('registration'))


@app.errorhandler(HTTPException)
def errorhandler(e):
    print(f"{e.code}, {e.name}, {e.description}")
    return e  # Da completare
