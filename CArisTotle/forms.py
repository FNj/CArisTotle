from flask_security.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [DataRequired()])
    fullname = StringField('Full name', [DataRequired()])


class TestInstanceOptionsForm(FlaskForm):
    name = StringField('Název případu', [DataRequired()])
    criterion = RadioField('Výběrové kritérium', [DataRequired()], coerce=int)
    submit = SubmitField('Spustit nový případ testu')

    def __init__(self, possible_criteria, default_criterion, **kwargs):
        super().__init__(**kwargs)
        self.criterion.choices = possible_criteria
        if default_criterion is not None:
            self.criterion.default = str(default_criterion)
            self.process()


# class QuestionMultipleChoiceAnswerForm(FlaskForm):
#     answer = SelectField('Odpověď', [DataRequired()], coerce=int)
#     submit = SubmitField('Odeslat odpověď')
#
#     def __init__(self, possible_answers, **kwargs):
#         super().__init__(**kwargs)
#         self.answer.choices = possible_answers

class QuestionMultipleChoiceAnswerForm(FlaskForm):
    answer = RadioField('Odpověď', [DataRequired()], coerce=int)
    # lock_in = BooleanField('Uzamknout a vyhodnotit otázku')
    submit = SubmitField('Odeslat odpověď')

    def __init__(self, possible_answers, **kwargs):
        super().__init__(**kwargs)
        self.answer.choices = possible_answers

# class QuestionMultipleChoiceAnswerForm(FlaskForm):  # Deprecated
#     answer = IntegerField(widget=HiddenInput())
#     submit = SubmitField('Odeslat odpověď')
#
#     @classmethod
#     def from_answer_id(cls, possible_answer_id):
#         form = cls()
#         form.answer.data = possible_answer_id
