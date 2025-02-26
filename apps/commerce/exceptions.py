class VendingMachineError(Exception):
    """Базовый класс для исключений торгового автомата"""
    pass

class ProductNotFoundError(VendingMachineError):
    """Продукт не найден"""
    pass


class InsufficientProductQuantityError(VendingMachineError):
    """Недостаточно товара"""
    pass


class InsufficientFundsError(VendingMachineError):
    """Недостаточно денег"""
    pass
