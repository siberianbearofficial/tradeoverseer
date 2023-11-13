from utils.exceptions import NotFoundError, ExistsError


class InventoryItemNotFoundError(NotFoundError):
    def __str__(self):
        return 'Inventory item not found.'


class InventoryItemExistsError(ExistsError):
    def __str__(self):
        return 'Inventory item with this uuid already exists.'


class ReadInventoryDenied(PermissionError):
    def __str__(self):
        return 'Author does not have read_inventory permission.'


class InsertInventoryDenied(PermissionError):
    def __str__(self):
        return 'Author does not have insert_inventory permission.'


class UpdateInventoryDenied(PermissionError):
    def __str__(self):
        return 'Author does not have update_inventory permission.'


class DeleteInventoryDenied(PermissionError):
    def __str__(self):
        return 'Author does not have delete_inventory permission.'
