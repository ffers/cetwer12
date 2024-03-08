import json, re, logging, pytz
from scrypt_order.sms_client import WriteBalanceSms, WriteSendSms
from datetime import datetime, timezone


logging.basicConfig(filename='../common_asx/log_sms.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
current_datetime = datetime.now(timezone.utc)
georgia_timezone = pytz.timezone('Asia/Tbilisi')
current_time_georgia = datetime.now(georgia_timezone)
payment_option_sum = 7111681
payment_option_100 = 7495540
filename = "../common_asx/data.json"
file_proc_order = "../common_asx/processed_orders.json"

data_sms = {
    "phone" : ["380989323122"],
    "message" : "test text",
    "src_addr" : "Jemis"
        }
data_status = {
    "id_sms": ["1092704994"]
}
# Завантаження оброблених ордерів із файлу
logging.info("Перевіряємо чи треба смс...")
def load_processed_orders():
    try:
        with open(file_proc_order, "r") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

# Збереження оброблених ордерів у файл
def save_processed_orders(processed_orders):
    with open(file_proc_order, "w") as file:
        json.dump(list(processed_orders), file)

def CreateText(phone_num_plus, order_id, sum_order_uah):

    sum_order = re.findall(r'\b\d+[.,]?\d*\b', sum_order_uah)
    sum_order = ''.join(sum_order)
    phone_num = re.findall(r'\d+', phone_num_plus)
    text = f"Zamovlenya #{order_id}. Karta: 5169330535212366 FOP Tyshenko D. Summa: {sum_order} grn. zvyazok 0989323122"
    print(text)
    data_sms["message"] = text
    data_sms["phone"] =  phone_num
    return data_sms



# Приклад обробки ордерів
def process_order():
    processed_orders = load_processed_orders()
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    for order in data["orders"]:
        order_id = order["id"]
        if order["payment_option"] != None:
            pay_option_order = order["payment_option"]["id"]
            if order_id not in processed_orders:
                if pay_option_order == payment_option_sum or pay_option_order == payment_option_100:
                    logging.info(f"Обробка ордера: {order_id}")
                    phone_num = order["phone"]
                    sum_order = order["full_price"]
                    if pay_option_order == payment_option_100:
                        sum_order = "100 грн"
                        print(f"Нашли ордер {order_id} на оплату {sum_order}")
                    text_sms = CreateText(phone_num, order_id, sum_order)
                    # WriteSendSms(text_sms)
                    WriteBalanceSms()
                    processed_orders.add(order_id)
                    save_processed_orders(processed_orders)



            # if send_sms or balance is None:
            #     return print(current_time_georgia.strftime("%Y-%m-%d %H:%M:%S"),
            #                  "Сталася помилка під час виконання запиту в SMSCLUB.")
            # else:
            #     logging.info(f"Sms по замовленню {order_id} надіслано по номеру - {phone_num}, сумма {sum_order}")
            #     logging.info(balance)

                # Додавання ордера до множини оброблених ордерів




