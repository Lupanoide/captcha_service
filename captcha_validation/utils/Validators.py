import logging
from six import string_types
from captcha_validation.config.Config import Config


class Validator:

    def exec_validation(self, toValidate):
        raise NotImplementedError("Subclasses should implement this!")


class StringValidator(Validator):

    def __init__(self):
        Validator.__init__(self)

    def exec_validation(self, toValidate: str):
        """
        validate if var is a string
        @param toValidate: string
        @return:  bool
        """
        return isinstance(toValidate, string_types)