from flask_security.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [DataRequired()])
    fullname = StringField('Full name', [DataRequired()])


class TestInstanceOptionsForm(FlaskForm):
    criterion = SelectField('Výběrové kritérium', [DataRequired()], coerce=int,
                            choices=[(1, 'Kritérium 1'), (2, 'Kritérium 2'), (3, 'Kritérium 3')])
    submit = SubmitField('Spustit test')

    def __init__(self, default_criterion):
        self.criterion.data = str(default_criterion)
        super().__init__()


# class QuestionMultipleChoiceAnswerForm(FlaskForm):
#     answer = SelectField('Odpověď', [DataRequired()], coerce=int)
#     submit = SubmitField('Odeslat odpověď')
#
#     def __init__(self, possible_answers, **kwargs):
#         super().__init__(**kwargs)
#         self.answer.choices = possible_answers

class QuestionMultipleChoiceAnswerForm(FlaskForm):
    answer = RadioField('Odpověď', [DataRequired()], coerce=int)
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
