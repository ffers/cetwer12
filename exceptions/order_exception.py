

class OrderAlreadyExistsError(Exception):
    pass

class OrderNotFoundException(Exception):
    pass

class OrderNotPaidException(Exception):
    pass

class OrderNotUpdateStatusException(Exception):
    pass

class AllOrderPayException(Exception):
    pass
