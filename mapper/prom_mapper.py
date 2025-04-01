

from DTO.order_dto import \
    OrderDTO, ProductDto, \
    CostumerDto, RecipientDto

from a_service import ProductServ
import re


def promMapper(prom: dict, ProductServ) -> OrderDTO:
    prod_serv = ProductServ()
    return OrderDTO(
        id=None,
        timestamp=prom.get("date_created"),
        phone=add_phone(prom),
        email=prom.get("email"),
        ttn=None,
        ttn_ref=None,
        client_firstname=prom.get("client_first_name"),
        client_lastname=prom.get("client_last_name"),
        client_surname=_safe(prom.get("client_second_name")),
        delivery_option=_get_delivery_name(prom),
        city_name=_get_city_name(prom),
        city_ref=None,
        region=None,
        area=None,
        warehouse_option=None,
        warehouse_text=prom.get("delivery_address"),
        warehouse_ref=_get_ttn_ref(prom),
        sum_price=_parse_price(prom["full_price"]),
        sum_before_goods=None,
        description=prom.get("client_notes", None),
        description_delivery=None,
        cpa_commission=_get_cpa(prom),
        client_id=prom.get("client_id"),
        send_time=None,
        order_id_sources=None,
        order_code=f"P-{prom.get('id')}",
        payment_status_id=add_prompay_status(prom),
        ordered_status_id=10,
        warehouse_method_id=None,
        source_order_id=2,
        payment_method_id=add_payment_method_id(prom),
        delivery_method_id=add_delivery_method(prom),
        author_id=55,
        recipient=_map_recipient(prom),
        recipient_id=None,
        costumer=_map_costumer(prom),
        costumer_id=None,
        ordered_product=_map_products(prom, prod_serv)
    )

def add_phone(order):
        draft_phone = order['phone']
        item_filter = re.findall(r'\d{12}', draft_phone)
        phone = item_filter[0]
        return phone

def _map_products(prom: dict, prod_serv: ProductServ) -> list[ProductDto]:
    products = []
    for p in prom.get("products", []):
        prod = prod_serv.load_item_by_article(p["sku"])
        products.append(ProductDto(
            quantity=int(p["quantity"]),
            price=_parse_price(p["price"]),
            order_id=None,
            product_id=prod.id
        ))
    return products


def _map_costumer(prom: dict) -> CostumerDto:
    client = prom.get("client", {})
    return CostumerDto(
        first_name=prom.get("client_first_name", ""),
        last_name=prom.get("client_last_name", ""),
        second_name=_safe(client.get("second_name")),
        phone=prom["phone"],
        email=prom.get("email")
    )


def _map_recipient(prom: dict) -> RecipientDto:
    r = prom.get("delivery_recipient", {})
    return RecipientDto(
        first_name=prom.get("client_first_name", ""),
        last_name=prom.get("client_last_name", ""),
        second_name=_safe(r.get("second_name")),
        phone=prom["phone"],
        email=prom.get("email")
    )

def add_prompay_status(order):
        status_id = None
        payment_option = order["payment_option"]["id"]
        if payment_option == 7547964:
            payment_data = order["payment_data"]
            if payment_data != None:
                if "paid" == payment_data["status"]:
                    status_id = 1
                elif "refunded" == payment_data["status"]:
                    status_id = 3
                else:
                    status_id = 2
                return status_id
            else:
                status_id = 2
        return status_id

def add_delivery_method(order):
        mapping = {
            13013934: 1,
            15255183: 2,
            13844336: 3,
            14383961: 4,
            13013935: 5,
        }
        return mapping.get(order["delivery_option"]["id"])

def add_payment_method_id(order):
        payment_method_id = None
        payment_option = order["payment_option"]["id"]
        if payment_option in (9289897, 8362873):
            payment_method_id = 1
        if payment_option in (9289898, 7111681):
            payment_method_id = 2
        if payment_option == 7495540:
            payment_method_id = 3
        if payment_option == 8281881:
            payment_method_id = 4
        if payment_option == 7547964:
            payment_method_id = 5
        return payment_method_id

def _parse_price(p: str) -> float:
    return float(p.replace(" грн", "").strip())


def _get_delivery_name(prom: dict) -> str | None:
    return prom.get("delivery_option", {}).get("name")


def _get_delivery_id(prom: dict) -> int | None:
    return prom.get("delivery_option", {}).get("id")


def _get_payment_id(prom: dict) -> int | None:
    return prom.get("payment_option", {}).get("id")


def _get_ttn(prom: dict) -> str | None:
    return prom.get("delivery_provider_data", {}).get("declaration_number")


def _get_ttn_ref(prom: dict) -> str | None:
    return prom.get("delivery_provider_data", {}).get("recipient_warehouse_id")


def _get_city_name(prom: dict) -> str:
    return prom.get("delivery_address", "").split(",")[0]


def _get_cpa(prom: dict) -> str | None:
    return prom.get("cpa_commission", {}).get("amount")


def _safe(value: str | None) -> str | None:
    return value if value else None

    