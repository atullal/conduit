from rest_framework.exceptions import APIException

class ProfileDoesNotExists(APIException):
    status_code = 400
    default_detail = "The requested profile does not exists."