from flask import jsonify

def error_response(status_code, error_code, message):
    """
    Create a standard error response format.
    :param status_code: HTTP status code.
    :param error_code: Custom error code.
    :param message: Error message.
    :return: JSON response.
    """
    return jsonify({
        'status_code': status_code,
        'error_code': error_code,
        'message': message
    }), status_code


def bad_request(message, error_code=400):
    return error_response(400, error_code, message)