# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import pytest
from filter import eval_percentage, eval_all_percentages, eval_condition


@pytest.mark.parametrize("project_language_percentage, evaluation, result", [
    (50, "<//100", True), (50, "<//51", True), (50, "<//50", False), (50, "<//10", False)
])
def test_eval_percentage_lt(project_language_percentage, evaluation, result):
    assert eval_percentage(project_language_percentage, evaluation) == result


@pytest.mark.parametrize("project_language_percentage, evaluation, result", [
    (60, "<=//100", True), (60, "<=//60", True), (60, "<=//59", False), (60, "<=//10", False)
])
def test_eval_percentage_lteq(project_language_percentage, evaluation, result):
    assert eval_percentage(project_language_percentage, evaluation) == result


@pytest.mark.parametrize("project_language_percentage, evaluation, result", [
    (60, ">//10", True), (60, ">//59", True), (60, ">//60", False), (60, ">//100", False)
])
def test_eval_percentage_gt(project_language_percentage, evaluation, result):
    assert eval_percentage(project_language_percentage, evaluation) == result


@pytest.mark.parametrize("project_language_percentage, evaluation, result", [
    (60, ">=//10", True), (60, ">=//60", True), (60, ">=//61", False), (60, ">=//100", False)
])
def test_eval_percentage_gteq(project_language_percentage, evaluation, result):
    assert eval_percentage(project_language_percentage, evaluation) == result


@pytest.mark.parametrize("project_language_percentage, evaluation, result", [
    (60, "==//10", False), (60, "==//59", False), (60, "==//60", True), (60, "==//61", False)
])
def test_eval_percentage_eq(project_language_percentage, evaluation, result):
    assert eval_percentage(project_language_percentage, evaluation) == result


@pytest.mark.parametrize("project_language_percentage, evaluation, result", [
    (60, "!=//10", True), (60, "!=//59", True), (60, "!=//60", False), (60, "!=//61", True)
])
def test_eval_percentage_neq(project_language_percentage, evaluation, result):
    assert eval_percentage(project_language_percentage, evaluation) == result


def test_eval_percentage_nooperator():
    project_language_percentage = 10
    evaluation = ".//100"
    assert eval_percentage(project_language_percentage, evaluation) is False


def test_eval_all_percentages_true():
    project_languages = ['Python', 'C', 'C++']
    languages = {
        'Python': '<=//80.0',
        'C': '>//15.0',
        'C++': '==//10.0',
    }
    project = {
        'id': 123,
        'name': 'test-project',
        'languages': {
            'Python': 70.0,
            'C': 20.0,
            'C++': 10.0,
        }
    }
    assert eval_all_percentages(project_languages, project, languages) is True


def test_eval_all_percentages_false():
    project_languages = ['Python', 'C', 'C++']
    languages = {
        'Python': '<=//80.0',
        'C': '==//15.0',
        'C++': '==//10.0',
    }
    project = {
        'id': 123,
        'name': 'test-project',
        'languages': {
            'Python': 70.0,
            'C': 20.0,
            'C++': 10.0,
        }
    }
    assert eval_all_percentages(project_languages, project, languages) is False


def test_eval_all_percentages_true_with_keyerror():
    project_languages = ["Python", "C", "C++", "C#"]
    languages = {
        "Python": "<=//80.0",
        "C": ">//15.0",
        "C++": "<=//10.0",
    }
    project = {
        "id": 123,
        "name": "test-project",
        "languages": {
            "Python": 70.0,
            "C": 20.0,
            "C++": 5.0,
            "C#": 5.0,
        }
    }
    assert eval_all_percentages(project_languages, project, languages) is True


@pytest.mark.parametrize("attribute, operator, condition, result", [
    (123, '==', 123, True), (123, '!=', 123, False), (123, '<=', 500, True), (123, '<', 500, True),
    (123, '>=', 500, False), (123, '>', 500, False)
])
def test_eval_condition_int(attribute, operator, condition, result):
    assert eval_condition(attribute, operator, condition) == result


@pytest.mark.parametrize("attribute, operator, condition, result", [
    (100.0, '==', 100.0, True), (45.5, '!=', 45.5, False), (12.3, '<=', 50.0, True), (12.3, '<', 50.0, True),
    (12.3, '>=', 50.0, False), (12.3, '>', 50.0, False)
])
def test_eval_condition_float(attribute, operator, condition, result):
    assert eval_condition(attribute, operator, condition) == result


@pytest.mark.parametrize("attribute, operator, condition, result", [
    ('String', 'contains', 'ing', True), ('Pytest', 'contains', 'example', False)
])
def test_eval_condition_str_contains(attribute, operator, condition, result):
    assert eval_condition(attribute, operator, condition) == result


@pytest.mark.parametrize("attribute, operator, condition, result", [
    ('String123', '', '#(.*\d)#', True), ('example project 123', '', '#(.*example\s.*)#', True)
])
def test_eval_condition_regex(attribute, operator, condition, result):
    assert eval_condition(attribute, operator, condition) == result
