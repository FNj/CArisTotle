from flask import render_template, redirect, url_for, flash
from flask_security import current_user
from flask_security.decorators import login_required

from .common.classes import BayesNetDataModelWrapper
from .common.procedures import check_test_existence_and_redirect_if_not_exists, \
    check_test_instance_existence_and_test_correspondence_and_redirect_on_error, \
    check_user_test_instance_correspondence_and_redirect_on_error, \
    time_remaining, get_stopping_criteria_states, close_test_instance_if_criteria_met
from .config import app, db
from .datamodel.model import Test, SelectionCriterion, TestInstance, Question, PossibleAnswer
from .datamodel.procedures import list_tests, get_entity_by_type_and_id, create_and_get_test_instance, \
    list_test_instances_by_test_and_student, submit_or_update_answer, list_selection_criteria, \
    list_answers_by_test_instance, list_unanswered_questions, get_answer_by_question_and_test_instance
from .forms import TestInstanceOptionsForm, QuestionMultipleChoiceAnswerForm


@app.route('/')
def index():
    return render_template('common.html')


@app.route('/test')
def tests_list():
    tests = list_tests()
    return render_template("tests_list.html", tests=tests)


@app.route('/test/<int:test_id>')
@login_required
def test_overview(test_id):
    test: Test = get_entity_by_type_and_id(Test, test_id)
    check_test_existence_and_redirect_if_not_exists(test)
    if current_user.is_authenticated:
        test_instances = list_test_instances_by_test_and_student(test, current_user)
    else:
        test_instances = []
    possible_criteria = list_selection_criteria()
    test_instance_options_form = TestInstanceOptionsForm(possible_criteria=[(sc.id, sc.name) for sc
                                                                            in possible_criteria],
                                                         default_criterion=test.default_selection_criterion.id)
    return render_template("test_overview.html", test=test, test_instances=test_instances,
                           test_instance_options_form=test_instance_options_form,
                           possible_criteria=possible_criteria)


@app.route('/test/<int:test_id>/instantiate', methods=['POST'])
@login_required
def create_test_instance(test_id):
    test: Test = get_entity_by_type_and_id(Test, test_id)
    check_test_existence_and_redirect_if_not_exists(test)
    possible_criteria = list_selection_criteria()
    test_instance_options_form = TestInstanceOptionsForm(possible_criteria=[(sc.id, sc.name) for sc
                                                                            in possible_criteria],
                                                         default_criterion=None)
    if test_instance_options_form.validate_on_submit():
        selection_criterion = get_entity_by_type_and_id(SelectionCriterion,
                                                        test_instance_options_form.criterion.data)
        test_instance = create_and_get_test_instance(test, current_user,
                                                     test_instance_options_form.name.data,
                                                     selection_criterion=selection_criterion)
        db.session.commit()
        return redirect(url_for("test_instance_overview", test_id=test.id, test_instance_id=test_instance.id))
    else:
        flash("Formulář byl špatně vyplněn.", "error")
        return redirect(url_for("test_overview", test_id=test.id))


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>')
@login_required
def test_instance_overview(test_id, test_instance_id):
    test: Test = get_entity_by_type_and_id(Test, test_id)
    check_test_existence_and_redirect_if_not_exists(test)
    test_instance: TestInstance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    check_test_instance_existence_and_test_correspondence_and_redirect_on_error(test, test_instance)
    check_user_test_instance_correspondence_and_redirect_on_error(test, test_instance)

    bayes_net = BayesNetDataModelWrapper(test_instance)
    stopping_criteria_states = get_stopping_criteria_states(test_instance, bayes_net)
    close_test_instance_if_criteria_met(test_instance, stopping_criteria_states, bayes_net)
    test_results = bayes_net.get_results()
    return render_template("test_instance_overview.html", test=test,
                           test_instance=test_instance, test_results=test_results,
                           locked_in_answers=[a for a in test_instance.answers if a.closed_at is not None],
                           stopping_criteria_states=stopping_criteria_states)


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>/question')
@login_required
def questions_list(test_id, test_instance_id):
    test: Test = get_entity_by_type_and_id(Test, test_id)
    check_test_existence_and_redirect_if_not_exists(test)
    test_instance: TestInstance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    check_test_instance_existence_and_test_correspondence_and_redirect_on_error(test, test_instance)
    check_user_test_instance_correspondence_and_redirect_on_error(test, test_instance)

    answers = list_answers_by_test_instance(test_instance)
    unanswered_questions = list_unanswered_questions(test_instance)
    stopping_criteria_states = get_stopping_criteria_states(test_instance)
    close_test_instance_if_criteria_met(test_instance, stopping_criteria_states)
    return render_template("questions_list.html", test=test_instance.test, test_instance=test_instance,
                           answers=answers, unanswered_questions=unanswered_questions,
                           stopping_criteria_states=stopping_criteria_states)


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>/question/<int:question_id>')
@login_required
def question_overview(test_id, test_instance_id, question_id):
    test: Test = get_entity_by_type_and_id(Test, test_id)
    check_test_existence_and_redirect_if_not_exists(test)
    test_instance: TestInstance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    check_test_instance_existence_and_test_correspondence_and_redirect_on_error(test, test_instance)
    check_user_test_instance_correspondence_and_redirect_on_error(test, test_instance)

    question: Question = get_entity_by_type_and_id(Question, question_id)
    possible_answers = question.possible_answers
    existing_answer = get_answer_by_question_and_test_instance(question, test_instance)
    answer_form = QuestionMultipleChoiceAnswerForm([(pa.id, pa.text) for pa in possible_answers])
    if existing_answer:
        answer_form.answer.default = existing_answer.possible_answer.id
    stopping_criteria_states = get_stopping_criteria_states(test_instance)
    close_test_instance_if_criteria_met(test_instance, stopping_criteria_states)
    return render_template("question_overview.html", test=test_instance.test,
                           test_instance=test_instance, question=question, answer_form=answer_form,
                           existing_answer=existing_answer,
                           stopping_criteria_states=stopping_criteria_states)


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>/question/<int:question_id>/post_answer',
           methods=['POST'])
@login_required
def post_answer(test_id, test_instance_id, question_id):
    test: Test = get_entity_by_type_and_id(Test, test_id)
    check_test_existence_and_redirect_if_not_exists(test)
    test_instance: TestInstance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    check_test_instance_existence_and_test_correspondence_and_redirect_on_error(test, test_instance)
    check_user_test_instance_correspondence_and_redirect_on_error(test, test_instance)

    question: Question = get_entity_by_type_and_id(Question, question_id)
    possible_answers = question.possible_answers
    answer_form = QuestionMultipleChoiceAnswerForm([(pa.id, pa.text) for pa in possible_answers])
    if answer_form.validate_on_submit():  # TODO: tidy this
        possible_answer: PossibleAnswer = get_entity_by_type_and_id(PossibleAnswer,
                                                                    answer_form.answer.data)
        if time_remaining(test_instance).total_seconds() >= -app.config['CARISTOTLE_TIME_LIMIT_GRACE_SECONDS']:
            submit_or_update_answer(test_instance, possible_answer, answer_form.lock_in.data)
            if answer_form.lock_in.data:
                flash("Odpověď na otázku {} vyhodnocena na stav: {}".format(question.name,
                                                                        possible_answer.state.description),
                      "message")
        else:
            flash("Otázka zodpovězena po vypršení času. Nebyla zaznamenána.", "warning")
        db.session.commit()
        return redirect(url_for("test_instance_overview", test_id=test_id,
                                test_instance_id=test_instance_id))
    else:
        flash("Formulář byl špatně vyplněn.", "error")
        return redirect(url_for("question_overview", test_id=test.id, test_instance_id=test_instance.id,
                                question_id=question.id))


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>/pick_question')
@login_required
def pick_question(test_id, test_instance_id):
    test: Test = get_entity_by_type_and_id(Test, test_id)
    check_test_existence_and_redirect_if_not_exists(test)
    test_instance: TestInstance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    check_test_instance_existence_and_test_correspondence_and_redirect_on_error(test, test_instance)

    bayes_net = BayesNetDataModelWrapper(test_instance)
    picked_questions = bayes_net.pick_questions()
    if picked_questions:
        picked_question = picked_questions[0]
        return redirect(url_for('question_overview', test_id=test_id, test_instance_id=test_instance_id,
                                question_id=picked_question.id))
    else:
        flash("Nejsou již nezodpovězené otázky.", "warning")
        return redirect(url_for("test_instance_overview", test_id=test.id,
                                test_instance_id=test_instance.id))
