from datetime import timedelta, datetime
from typing import Union, NamedTuple

from flask import flash, redirect, url_for
from flask_security import current_user

from .classes import BayesNetDataModelWrapper
from ..datamodel.model import Test, TestInstance, User
from ..datamodel.procedures import get_latest_answers_update_timestamp_by_test_instance, close_test_instance


def entropy_remaining(test_instance: TestInstance,
                      bayes_net_data_model_wrapper: BayesNetDataModelWrapper = None) -> Union[float, None]:
    if test_instance.test.stop_max_entropy is not None:
        if bayes_net_data_model_wrapper is None:
            bayes_net_data_model_wrapper = BayesNetDataModelWrapper(test_instance)
        return bayes_net_data_model_wrapper.get_total_skills_entropy() - test_instance.test.stop_max_entropy
    else:
        return None  # just to be explicit


def time_remaining(test_instance: TestInstance) -> Union[timedelta, None]:
    if test_instance.test.stop_max_time is not None:
        determining_time = get_latest_answers_update_timestamp_by_test_instance(test_instance) \
            if test_instance.closed_at else datetime.now()
        return test_instance.test.stop_max_time - (determining_time - test_instance.created_at)
    else:
        return None  # just to be explicit


def questions_remaining(test_instance: TestInstance, locked_in_only: bool = True) -> Union[int, None]:
    if test_instance.test.stop_min_answers is not None:
        return test_instance.test.stop_min_answers - len([a for a in test_instance.answers
                                                          if not locked_in_only or a.closed_at is not None])
    else:
        return None  # just to be explicit


def pretty_time_delta(td: timedelta):
    seconds = td.total_seconds()
    sign_string = '- ' if seconds < 0 else ''
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%s%dd %dh %dm %ds' % (sign_string, days, hours, minutes, seconds)
    elif hours > 0:
        return '%s%dh %dm %ds' % (sign_string, hours, minutes, seconds)
    elif minutes > 0:
        return '%s%dm %ds' % (sign_string, minutes, seconds)
    else:
        return '%s%ds' % (sign_string, seconds)


class StoppingCriteriaStates(NamedTuple):
    entropy_remaining: float
    time_remaining: timedelta
    questions_remaining: int

    def get_pretty_time_remaining(self):
        return pretty_time_delta(self.time_remaining)


def get_stopping_criteria_states(test_instance: TestInstance,
                                 bayes_net_data_model_wrapper: BayesNetDataModelWrapper = None):
    return StoppingCriteriaStates(entropy_remaining=entropy_remaining(test_instance,
                                                                      bayes_net_data_model_wrapper),
                                  time_remaining=time_remaining(test_instance),
                                  questions_remaining=questions_remaining(test_instance))


def stopping_criteria_met(test_instance: TestInstance,
                          stopping_criteria_states: StoppingCriteriaStates = None,
                          bayes_net_data_model_wrapper: BayesNetDataModelWrapper = None):
    low_enough_entropy = False
    max_time_reached = False
    min_questions_answered = False

    if stopping_criteria_states is None:
        stopping_criteria_states = get_stopping_criteria_states(test_instance, bayes_net_data_model_wrapper)

    if (test_instance.test.stop_max_entropy is not None and
                stopping_criteria_states.entropy_remaining < 0):
        low_enough_entropy = True
        flash("Cílová entropie výsledků dosažena.", "warning")

    if (test_instance.test.stop_max_time is not None and
                stopping_criteria_states.time_remaining.total_seconds() < 0):
        max_time_reached = True
        flash("Čas na test vyčerpán.", "warning")

    if (test_instance.test.stop_min_answers is not None and
                stopping_criteria_states.questions_remaining <= 0):
        min_questions_answered = True
        flash("Požadovaný počet zodpovězených otázek dosažen.", "warning")

    return low_enough_entropy or max_time_reached or min_questions_answered


def close_test_instance_if_criteria_met(test_instance: TestInstance,
                                        stopping_criteria_states: StoppingCriteriaStates = None,
                                        bayes_net_data_model_wrapper: BayesNetDataModelWrapper = None):
    if test_instance.closed_at is not None \
            or stopping_criteria_met(test_instance, stopping_criteria_states, bayes_net_data_model_wrapper):
        close_test_instance(test_instance)


def check_test_existence_and_redirect_if_not_exists(test: Test):
    if test is None:
        flash("Test s daným identifikačním číslem neexistuje.", "error")
        return redirect(url_for("tests_list"))


def check_test_instance_existence_and_test_correspondence_and_redirect_on_error(
        test: Test, test_instance: TestInstance):
    if test_instance is None:
        flash("Případ testu s daným identifikačním číslem neexistuje.", "error")
        return redirect(url_for("test_overview", test_id=test.id))
    if test_instance.test != test:
        flash("Identifikační čísla testu a případu testu si neodpovídají.", "error")
        return redirect(url_for("test_overview", test_id=test.id))


def check_user_test_instance_correspondence_and_redirect_on_error(test: Test, test_instance: TestInstance,
                                                                  user: User = current_user):
    if test_instance.student != user:
        flash("Tento případ testu nepatří přihlášenému uživateli.", "error")
        return redirect(url_for("test_overview", test_id=test.id))
