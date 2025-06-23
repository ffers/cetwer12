
# infrastructure.py
from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker
from api import EvoClient, RozetMain, TgClient
from repository import StoreRepositorySQLAlchemy as StoreRepoSQL, OrderRep as OrderRepo
from a_service import EvoService, RozetkaServ, TgServNew
from a_service.order_service import OrderServ

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # long-living
    evo_client  = providers.Singleton(EvoClient, token=config.evo.api_token)
    rozet_main  = providers.Singleton(RozetMain)
    tg_client   = providers.Singleton(TgClient, token=config.tg.bot_token)

    # per-request
    db_session = providers.Resource(sessionmaker, bind=config.db.engine)

    store_repo = providers.Factory(StoreRepoSQL, session=db_session)
    order_repo = providers.Factory(OrderRepo, session=db_session)

    evo_service = providers.Factory(EvoService, evo_client, store_repo)
    roz_service = providers.Factory(RozetkaServ, rozet_main, store_repo)
    tg_service  = providers.Factory(TgServNew, tg_client)

    order_service = providers.Factory(
        OrderServ,
        evo_serv=evo_service,
        roz_serv=roz_service,
        tg_serv=tg_service,
        order_repo=order_repo,
        store_repo=store_repo,
    )
