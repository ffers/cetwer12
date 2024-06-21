import os, json, requests, time, logging, re
from os.path import join, dirname
from dotenv import load_dotenv
from .create_data import get_search_contact, time_now, WarehouseRefCl
from .create_data import NpClient


env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)

SUN = {}
Order = {}
ware = WarehouseRefCl(SUN)
np_cl = NpClient()
chat_id = "-421982888"
delivery_np = 13013934
json_data_prom = "../common_asx/data.json"
json_data_np_dict = "api/nova_poshta/create_data/json_dict/json_data_np_dict.json"
contact_np = "api/nova_poshta/create_data/json_dict/contact_np.json"

OptionsSeat = { "OptionsSeat" : [
                    {
                    "volumetricVolume":"1",
                    "volumetricWidth":"30",
                    "volumetricLength":"30",
                    "volumetricHeight":"30",
                    "weight":"1"
                    }]}

dict_ttn_prom = {
              "order_id": "",
              "declaration_id": "",
              "delivery_type": "nova_poshta"
            }

dict_status_prom = {
          "ids": [ 0 ],
          "custom_status_id":  137639
        }

logging.basicConfig(filename='../common_asx/log_order.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Шукаєм прийняті замовлення...")


def json_read_dict(file):
    with open(file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)

def load_processed_orders():
    try:
        with open("../common_asx/created_ttn.json", "r") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

# Збереження оброблених ордерів у файл
def save_processed_orders(processed_orders):
    with open("../common_asx/created_ttn.json", "w") as file:
        json.dump(list(processed_orders), file)

def create_data_np(order):
    SUN["apiKey"] = get_from_env("NP_TOKEN")
    SUN["Page"] = 1
    if order["client_first_name"] == None or order["client_first_name"] == "":
        SUN["FirstName"] = "Відсутнє"
        print("Відсутнє FirstName")
    else:
        SUN["FirstName"] = order["client_first_name"]
    if order["client_last_name"] == None or order["client_last_name"] == "":
        SUN["LastName"] = " "
        print("Відсутнє LastName")
    else:
        SUN["LastName"] = order["client_last_name"]
    if order["client_second_name"] == None or order["client_second_name"] == "":
        SUN["MiddleName"] = " "
    else:
        SUN["MiddleName"] = order["client_second_name"]
    if order["phone"] == None :
        SUN["Phone"] = "Відсутнє"
        print("Відсутнє Phone")
    else:
        parse_phone(order["phone"])

def parse_phone(order_phone):
    item_filter = re.findall(r'\d{12}', order_phone)
    RecipientsPhone = item_filter[0]
    SUN.update({"RecipientsPhone": RecipientsPhone})

def contact_filter(contact):
    for item_contact in contact["data"]:
        phone = item_contact["Phones"]
        print(SUN["RecipientsPhone"], phone)
        try:
            if phone == SUN["RecipientsPhone"]:
                print("Контакт нашли")
                ContactRef = item_contact["Ref"] #нашли контакт то нам нужен реф
            else:
                ContactRef = None
                print("Не знайдено контакт")
            return ContactRef

        except:
            print("Номер не верний!")

def search_contact_Ref( order):
    time.sleep(1)
    contactRef = get_search_contact(json_read_dict(json_data_np_dict), SUN)
    ContactSender = contact_filter(contactRef)
    if ContactSender == None:
        print("Создаем новий контакт!")
        create_contact = np_cl.create_contact(SUN)
        print(json.dumps(create_contact, ensure_ascii=False))
        return create_contact
    else:
        print("Контак знайдено Ref отримано!")
        return ContactSender

def search_money(order):
    print("Шукаєм наложку")
    Cost = ''.join(re.findall(r'\b\d+[.,]?\d*\b', order["full_price"]))
    SUN.update({"AfterpaymentOnGoodsCost" : None, "appraised":order["full_price"], "Cost":Cost})
    if order["payment_option"]["id"] in (7111682, 8362873, 7495540, 9289897):
        print("Є наложка")
        SUN.update({"AfterpaymentOnGoodsCost": Cost})
    else:
        print("Наложки нема!")
    return SUN

def time_now_resp():
    date_time = time_now()
    next_time = next(date_time)
    test_time = next_time.strftime("%d.%m.%Y")
    SUN.update({"DateTime" : test_time})

def recipient_cr():
    ref = np_cl.create_contragent(SUN)
    SUN.update({"Recipient": ref})

def updait_dic(obj_order):
    SUN.clear()
    Order.clear()
    Order.update(obj_order)


def create_ttn_order(sun):
    created_ttn = np_cl.runup_doc(sun)
    print(created_ttn)
    return created_ttn

# def create_crm_order(sun):
#     data =

def create_ttn_button(order):
    updait_dic(order)
    order_id = order["id"]
    time_now_resp()
    print(f"Добавляєм ордер в буфер для створення замовлення {order_id}")
    create_data_np(order)
    ware.RefWarehouse(order)
    RecipientAddress = order["delivery_provider_data"]["recipient_warehouse_id"]
    recipient_cr()
    RecipientContact = search_contact_Ref(order)
    print(RecipientAddress)
    description = f"Одяг Jemis {order_id}"
    SUN.update({"RecipientAddress": RecipientAddress, "ContactRecipient": RecipientContact, "Description": description})
    search_money(order)
    created_ttn = create_ttn_order(SUN)
    return created_ttn

class CreateNpData():
    def sun_send(self):
        return SUN

    def order_send(self):
        return Order







