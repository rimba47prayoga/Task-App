from rest_framework.exceptions import APIException


class TaskAppError(APIException):
    status_code = 503
    detail = 'Error occurs'
    error_code = 'unknown-error'

    def __init__(self, *args, **kwargs):
        if kwargs.get('status_code'):
            self.status_code = kwargs.get('status_code')
        if kwargs.get('message'):
            self.detail = kwargs.get('message')
        if kwargs.get('error_code'):
            self.error_code = kwargs.get('error_code')


class TaskAppErrorCode(object):
    USER_NOT_REGISTERED = 'user-not-registered'
    INCORRECT_PASSWORD = 'incorrect-password'
    NOT_SELECT_PROJECT = 'not-select-project'
