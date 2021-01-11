error_dict = {  # pylint: disable=C0103
    'field_required': 'This field is required',
    'not_empty': 'This cannot be empty',
    'string_characters': 'Field must start with an alphabet, only contain alphanumeric characters, non-consecutive fullstops, hyphens, spaces and apostrophes',
    'url_syntax': '{0} is not a valid url',
    'email_syntax': 'This is not a valid email address',
    'string_length': 'Field must be {0} characters or less',
    'user_not_found': 'A user with this email and password was not found'
}

jwt_errors = {
    'token_expired': 'Token expired. Please login to get a new token.',
    'invalid_token': 'Authorization failed due to an Invalid token.',
    'invalid_secret': 'Cannot verify the token provided as the expected issuer does not match.',
    'token_user_not_found': "No user found for token provided"
}
