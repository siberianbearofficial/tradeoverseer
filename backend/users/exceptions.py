from utils.exceptions import NotFoundError, ExistsError


class UserNotFoundError(NotFoundError):
    def __str__(self):
        return 'User not found.'


class UsernameTakenError(ExistsError):
    def __str__(self):
        return 'User with the same username already exists.'


class UserExistsError(ExistsError):
    def __str__(self):
        return 'User with this uuid already exists.'


class InsertUserDenied(PermissionError):
    def __str__(self):
        return 'Author does not have insert_users permission.'


class UpdateUserDenied(PermissionError):
    def __str__(self):
        return 'Author does not have update_users permission.'


class DeleteUserDenied(PermissionError):
    def __str__(self):
        return 'Author does not have delete_users permission.'


class ChangePasswordDenied(PermissionError):
    def __str__(self):
        return 'It is allowed to change the password only of your account.'
