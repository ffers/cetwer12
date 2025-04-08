
from dependency_injector import containers, providers

class Services:
    def __init__(self, tg, order_serv, repo):
        self.tg = tg
        self.order_serv = order_serv 
        self.order_repo = order_repo



class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    tg_service = providers.Singleton(TgService)
    tg_controller = providers.Singleton(TgController)
    order_repo = providers.Singleton(OrderRepository)

    services = providers.Factory(
        Services,
        tg=tg_service,
        ctrl=tg_controller,
        repo=order_repo,
    )
