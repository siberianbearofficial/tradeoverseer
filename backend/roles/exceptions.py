from utils.exceptions import NotFoundError, ExistsError


class RoleNotFoundError(NotFoundError):
    def __str__(self):
        return 'Role not found.'


class RoleExistsError(ExistsError):
    def __str__(self):
        return 'Role with this uuid already exists.'


class ReadRoleDenied(PermissionError):
    def __str__(self):
        return 'Author does not have read_roles permission.'


class InsertRoleDenied(PermissionError):
    def __str__(self):
        return 'Author does not have insert_roles permission.'


class UpdateRoleDenied(PermissionError):
    def __str__(self):
        return 'Author does not have update_roles permission.'


class DeleteRoleDenied(PermissionError):
    def __str__(self):
        return 'Author does not have delete_roles permission.'
