

from DTO.order_dto import \
    OrderDTO, ProductDto, \
    CostumerDto, RecipientDto

from a_service import ProductServ
import re

from utils import OC_logger

logger = OC_logger.oc_log('prom_mapper')

class PromMapperException(Exception):
     pass

def promMapper(prom: dict, ProductServ, store_id) -> OrderDTO:
    try:
        prod_serv = ProductServ()
        payment_id = add_payment_method_id(prom)
        ref = _get_ttn_ref(prom)
        warehouse_text = _get_warehouse_text(prom, ref)
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
            warehouse_text=warehouse_text,
            warehouse_ref=ref,
            sum_price=_parse_price(prom["full_price"]),
            sum_before_goods=None,
            description=prom.get("client_notes", None),
            description_delivery=None,
            cpa_commission=_get_cpa(prom),
            client_id=prom.get("client_id"),
            send_time=None,
            order_id_sources=None,
            order_code=f"P-{prom.get('id')}",
            ordered_status_id=10,
            warehouse_method_id=None,
            source_order_id=2,
            payment_method_id=payment_id,
            payment_status_id=add_prompay_status(payment_id, prom),
            delivery_method_id=add_delivery_method(prom),
            author_id=55,
            recipient=_map_recipient(prom),
            recipient_id=None,
            costumer=_map_costumer(prom),
            costumer_id=None,
            store_id=store_id,
            ordered_product=_map_products(prom, prod_serv)
        )
    except Exception as e:
         print(f"data = {prom}, type = {type(prom)}")
         logger.error(f'{e}')
         raise PromMapperException(f'Помилка обробкі ордера')

def add_phone(order):
        draft_phone = order['phone']
        item_filter = re.findall(r'\d{12}', draft_phone)
        phone = item_filter[0]
        return phone

def _map_products(prom: dict, prod_serv: ProductServ) -> list[ProductDto]:
    products = []
    for p in prom.get("products", []):
        prod = prod_serv.load_item_by_article(p["sku"], p["name"])
        products.append(ProductDto(
            quantity=int(p["quantity"]),
            price=_parse_price(p["price"]),
            order_id=None,
            product_id=prod.id
        ))
    return products


def _map_costumer(prom: dict) -> CostumerDto:
    c = prom.get("client", {})
    return CostumerDto(
        first_name=c.get("first_name", ""),
        last_name=c.get("last_name", ""),
        second_name=_safe(c.get("second_name")),
        phone=c.get('phone', ''),
        email=prom.get("email")
    )


def _map_recipient(prom: dict) -> RecipientDto:
    r = prom.get("delivery_recipient", {})
    return RecipientDto(
        first_name=r.get("first_name", ""),
        last_name=r.get("last_name", ""),
        second_name=_safe(r.get("second_name")),
        phone=r.get('phone', ''),
        email=None
    )

def _get_warehouse_text(prom: dict, ref: str):
    text = prom.get("delivery_address")
    if ref == 'street':
         text = '📦 Курьєрська доставка: ' + text
    return text

def add_prompay_status(payment_id, order):
        if payment_id == 5:
            payment_data = order["payment_data"]
            if payment_data != None:
                if "paid" == payment_data["status"]:
                    status_id = 1
                elif "refunded" == payment_data["status"]:
                    status_id = 3
                else:
                    status_id = 2
                print("add_prompay_status:", status_id)
                return status_id
        return 2

def add_delivery_method(order):
        mapping = {
            "nova_poshta": 1,
            "rozetka_delivery": 2,
            "ukrposhta": 3,
            "meest_express": 4,
            "pickup": 5,
        }
        return mapping.get(order["delivery_provider_data"]["provider"])

def add_payment_method_id(order):
        payment_method_id = None
        payment_option = order["payment_option"]["name"]
        if payment_option == "Наложенный платеж":
            payment_method_id = 1
        if payment_option == "Оплата на счет":
            payment_method_id = 2
        if payment_option == "Оплата картой Visa, Mastercard - WayForPay":
            payment_method_id = 4
        if payment_option == "Пром-оплата":
            payment_method_id = 5
        return payment_method_id

def _parse_price(num_str_text):
        try:
            num_str = ''.join(re.findall(r'\b\d+[.,]?\d*\b', num_str_text))
            # if '\xa0' in num_str:
            #      num_str = num_str.replace('\xa0', '')
            #      print("format_float:", num_str)
            if "," in num_str:
                num_str = num_str.replace(',', '.')     
            num = float(num_str)
            # Якщо число - ціле, додаємо ".00"
            if num.is_integer(): 
                num_dr = f"{int(num)}.00"
                return float(num_dr)
            else:
                return float(num)
        except ValueError:
            return "Неправильний формат числа"



def _get_delivery_name(prom: dict) -> str | None:
    return prom.get("delivery_option", {}).get("name")


def _get_delivery_id(prom: dict) -> int | None:
    return prom.get("delivery_option", {}).get("id")


def _get_payment_id(prom: dict) -> int | None:
    return prom.get("payment_option", {}).get("id")


def _get_ttn(prom: dict) -> str | None:
    return prom.get("delivery_provider_data", {}).get("declaration_number")


def _get_ttn_ref(prom: dict) -> str | None:
    del_data = prom.get("delivery_provider_data", {})
    ref = del_data.get("recipient_warehouse_id")
    if ref:
        return ref
    street = del_data.get('recipient_address').get('city_id')
    if street:
         return 'street'
    raise ValueError("Адресси нема чекаем")
    


def _get_city_name(prom: dict) -> str:
    return prom.get("delivery_address", "").split(",")[0]


def _get_cpa(prom: dict) -> str | None:
    sum = 0
    for p in prom.get("products", []):
        cpa = prom.get("cpa_commission", {}).get("amount")  
        cpa = format_float(cpa)
        sum += cpa
    return str(sum)

def format_float(num_str):  
    try:  
        num = float(num_str)   
        # Якщо число - ціле, додаємо ".00"
        if num.is_integer():
            num_dr = f"{int(num)}.00"
            return float(num_dr)
        else:
            return float(num)
    except ValueError:
        return "Неправильний формат числа"



def _safe(value: str | None) -> str | None:
    return value if value else None

    