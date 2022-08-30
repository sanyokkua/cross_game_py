from flask import request

from crossgameflask.application.errors.exceptions import AttributeIsNotFoundInTheFormException, IncorrectStringValue


def validate_form_str_attribute(attr_name: str) -> None:
    if attr_name is None or not isinstance(attr_name, str) or len(attr_name) < 1:
        raise IncorrectStringValue()
    form = request.form
    attr_value: str = form[attr_name]
    if attr_value is None or not isinstance(attr_value, str) or len(attr_value.strip()) < 1:
        raise AttributeIsNotFoundInTheFormException()


def get_str_attr_from_form(attr_name: str) -> str:
    validate_form_str_attribute(attr_name)
    form = request.form
    return form[attr_name]
