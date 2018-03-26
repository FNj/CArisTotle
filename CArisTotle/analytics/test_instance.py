from ..datamodel.model import User, Test, Question, PossibleAnswer, TestInstance, Answer, SelectionCriterion, \
    Skill, SkillState, Role, QuestionState
import pandas as pd
from typing import Tuple, List
from .common import get_df_from_sql

# def get_question_and_answers_df(q_a_tuples_list: List[Tuple[Question, PossibleAnswer, QuestionState]]) -> pd.DataFrame:
#     tup_list = [(tup[0].id, tup[0].text,  # Question id and text
#                  (tup[1].id if tup[1] is not None else None), tup[1].text,
#                  tup[2].id, tup[2].number, tup[2].score, tup[2].description)  # Possible answer id, number,
#                                                                               #  score and description
#                 for tup in q_a_tuples_list]
#     return pd.DataFrame.from_records(tup_list)


def get_question_and_answers_df(test_instance: TestInstance) -> pd.DataFrame:
    test_id = test_instance.test_id
    test_instance_id = test_instance.id
    sql = """
SELECT 
    q.id AS question_id, q.text AS question_text,
    pa.id AS possible_answer_id, pa.text AS possible_answer_text,
    qs.id AS state_id, qs.number AS state_number, qs.score AS state_score, qs.description AS state_description
FROM
    questions q
    LEFT JOIN answers a ON q.id = a.question_id AND a.test_instance_id = {test_instance_id}
    LEFT JOIN possible_answers pa ON a.possible_answer_id = pa.id
    LEFT JOIN question_states qs ON pa.state_id = qs.id
WHERE
    q.test_id = {test_id}""".format(test_id=test_id, test_instance_id=test_instance_id)
    return get_df_from_sql(sql)


