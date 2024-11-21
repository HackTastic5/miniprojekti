class UserInputError(Exception):
    pass

def validate_field(field, value, min_len=None, max_len=None, exact_len=None):
    if not value:
        raise UserInputError(f"{field} can not be empty")

    if min_len and len(value) < min_len:
        raise UserInputError(f"{field} length must be greater than {min_len}")
    
    if max_len and len(value) > max_len:
        raise UserInputError(f"{field} length must be smaller than {max_len}")
    
    if exact_len and len(value) != exact_len:
        raise UserInputError(f"{field} length must be {exact_len}")
