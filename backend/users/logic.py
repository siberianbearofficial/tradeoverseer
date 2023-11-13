from re import fullmatch

CORRECT_PASSWORD_PATTERN = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$'


def validate_username(username: str):
    if not username:
        raise ValueError('Username required.')
    if len(username) < 8:
        raise ValueError('Invalid username. Should contain at least 8 symbols.')


def validate_password(password: str):
    if not password:
        raise ValueError('Password required.')
    if len(password) < 8:
        raise ValueError('Invalid password. Should contain at least 8 symbols.')
    if not fullmatch(CORRECT_PASSWORD_PATTERN, password):
        raise ValueError('Invalid password. Should contain numbers, uppercase and lowercase Latin letters')


if __name__ == '__main__':
    validate_password(input().strip())
