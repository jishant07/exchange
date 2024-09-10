import constants
from cerberus import Validator

def success(result, status = 200):  
    
    return {
        "status" : constants.STATUS["SUCCESS"],
        "result" : result
    }, status

def failure(error, status = 500):
    return {
        "status" : constants.STATUS["FAILURE"],
        "error" : error
    }, status


def schema_validator(schema, request_body):
    validator = Validator(schema)
    validator.allow_unknown = False
    if validator.validate(request_body):
        return True, None
    else:
        print("SCHEMA ERROR => ", validator.errors)
        return False, validator.errors