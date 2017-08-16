from flask import flash, redirect, url_for
from flask_security import current_user

from ..datamodel.model import Test, TestInstance, User


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
                                                                  user: User=current_user):
    if test_instance.student != user:
        flash("Tento případ testu nepatří přihlášenému uživateli.", "error")
        return redirect(url_for("test_overview", test_id=test.id))


