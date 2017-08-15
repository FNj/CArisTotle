from flask import render_template, redirect, url_for
from flask_security import current_user
from flask_security.decorators import login_required

from .common.classes import BayesNetDataModelWrapper
from .config import app, db
from .datamodel.model import Test, SelectionCriterion, TestInstance, Question, PossibleAnswer
from .datamodel.procedures import list_tests, get_entity_by_type_and_id, create_and_get_test_instance, \
    list_test_instances_by_test_and_student, submit_or_update_answer, list_selection_criteria
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
    possible_criteria = list_selection_criteria()
    test_instance_options_form = TestInstanceOptionsForm(possible_criteria=[(sc.id, sc.name) for sc
                                                                            in possible_criteria],
                                                         default_criterion=None)
    if test_instance_options_form.validate_on_submit():
        selection_criterion = get_entity_by_type_and_id(SelectionCriterion,
                                                        test_instance_options_form.criterion.data)
        test_instance = create_and_get_test_instance(test, current_user,
                                                     selection_criterion=selection_criterion)
        db.session.commit()
        return redirect(url_for("questions_list", test_id=test.id, test_instance_id=test_instance.id))
    else:
        return "Formulář byl špatně vyplněn."


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>')
@login_required
def test_instance_overview(test_id, test_instance_id):
    test_instance: TestInstance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    if test_instance.student == current_user:
        return render_template("test_instance_overview.html", test_instance=test_instance)
    else:
        return "Tento případ testu nepatří přihlášenému uživateli."


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>/question')
@login_required
def questions_list(test_id, test_instance_id):
    test_instance: TestInstance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    if test_instance.student == current_user:
        return render_template("questions_list.html", test_instance=test_instance)
    else:
        return "Tento případ testu nepatří přihlášenému uživateli."


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>/question/<int:question_id>')
@login_required
def question_overview(test_id, test_instance_id, question_id):
    test_instance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    if test_instance.student == current_user:
        question: Question = get_entity_by_type_and_id(Question, question_id)
        possible_answers = question.possible_answers
        answer_form = QuestionMultipleChoiceAnswerForm([(pa.id, pa.text) for pa in possible_answers])
        return render_template("question_overview.html", test_instance=test_instance, question=question,
                               answer_form=answer_form)
    else:
        return "Tento případ testu nepatří přihlášenému uživateli."


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>/question/<int:question_id>/post_answer',
           methods=['POST'])
@login_required
def post_answer(test_id, test_instance_id, question_id):
    test_instance: TestInstance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    if test_instance.student == current_user:
        question: Question = get_entity_by_type_and_id(Question, question_id)
        possible_answers = question.possible_answers
        answer_form = QuestionMultipleChoiceAnswerForm([(pa.id, pa.text) for pa in possible_answers])
        if answer_form.validate_on_submit():
            possible_answer: PossibleAnswer = get_entity_by_type_and_id(PossibleAnswer,
                                                                        answer_form.answer.data)
            submit_or_update_answer(test_instance, possible_answer)
            db.session.commit()
            return redirect(url_for("questions_list", test_id=test_id, test_instance_id=test_instance_id))
    else:
        return "Tento případ testu nepatří přihlášenému uživateli."


@app.route('/test/<int:test_id>/instance/<int:test_instance_id>/pick_question')
@login_required
def pick_question(test_id, test_instance_id):
    test_instance: TestInstance = get_entity_by_type_and_id(TestInstance, test_instance_id)
    bayes_net = BayesNetDataModelWrapper(test_instance)
    picked_questions = bayes_net.pick_questions()
    if picked_questions:
        picked_question = picked_questions[0]
        return redirect(url_for('question_overview', test_id=test_id, test_instance_id=test_instance_id,
                                question_id=picked_question.id))
    else:
        return "Nejsou již nezodpovězené otázky."
