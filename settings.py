import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()

        # Telegram Bot Tokens
        self.TELEGRAM_BOT_TOKEN1 = os.getenv("TELEGRAM_BOT_TOKEN1")
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

        # Payment
        self.PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
        self.SHOP_ID = os.getenv("SHOP_ID")

        # Nova Poshta
        self.NP_PHONE = os.getenv("NP_PHONE")
        self.NP_TOKEN = os.getenv("NP_TOKEN")
        self.NP_SENDER_REFLS = os.getenv("NP_SENDER_REFLS")
        self.NP_COUNT_REFLS = os.getenv("NP_COUNT_REFLS")
        self.NP_CITY_SENDER = os.getenv("NP_CITY_SENDER")
        self.NP_SENDER_ADRESS = os.getenv("NP_SENDER_ADRESS")
        self.NP_CITY_DELIVERY = os.getenv("NP_CITY_DELIVERY")
        self.NP_ADRESS_CONTR = os.getenv("NP_ADRESS_CONTR")
        self.NP_CONTER_RECIPIENT = os.getenv("NP_CONTER_RECIPIENT")
        self.NP_CONTER_RECIPIENT_OWNER_FORM = os.getenv("NP_CONTER_RECIPIENT_OWNER_FORM")
        self.NP_CONTER_RECIPIENT_COUNTERPARTY = os.getenv("NP_CONTER_RECIPIENT_COUNTERPARTY")

        # SMS & PROM API
        self.PROM_TOKEN = os.getenv("PROM_TOKEN")
        self.SMS_TOKEN = os.getenv("SMS_TOKEN")

        # Database
        self.DB_USERNAME = os.getenv("DB_USERNAME")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD") 
        self.SECRET_KEY_FLASK = os.getenv("SECRET_KEY_FLASK")

        # Telegram Chat IDs
        self.CH_ID_INFO = int(os.getenv("CHAT_ID_INFO"))
        self.CH_ID_MANAGER = int(os.getenv("CHAT_ID_CONFIRMATION"))
        self.CH_ID_HELPER = int(os.getenv("CHAT_ID_HELPER"))
        self.CH_ID_NP = int(os.getenv("CH_ID_NP"))
        self.CH_ID_STOCK = int(os.getenv("CH_ID_SK"))
        self.CH_ID_UKR = int(os.getenv("CH_ID_UKR"))
        self.CH_ID_ROZ = int(os.getenv("CH_ID_ROZ"))
        self.CH_ID_CASH = int(os.getenv("CH_ID_CASH"))
        self.CH_ID_SHOP = int(os.getenv("CH_ID_SHOP"))
        self.CH_ID_COURIER = int(os.getenv("CH_ID_CORECTOR"))

        # CRM & API URLs
        self.URL_TO_CRM = os.getenv("URL_TO_CRM")
        self.URL_TO_UPDATE = os.getenv("URL_TO_UPDATE")
        self.SEND_TO_CRM_TOKEN = os.getenv("SEND_TO_CRM_TOKEN")
        self.X_TELEGRAM_API_BOT_TOKEN = os.getenv("X_TELEGRAM_API_BOT_TOKEN")

        # Logs & Security
        self.FROMATTER_LOG = os.getenv("FROMATTER_LOG")
        self.CHECKBOX_LICENSE_KEY = os.getenv("CHECKBOX_LICENSE_KEY")

        # Checkbox API
        self.CHECKBOX_HOST = os.getenv("CHECKBOX_HOST")
        self.CHECKBOX_CLIENT_NAME = os.getenv("CHECKBOX_CLIENT_NAME")
        self.CHECKBOX_PIN_CASHIER = os.getenv("CHECKBOX_PIN_CASHIER")
        self.CHECKBOX_CLIENT_VERSION = os.getenv("CHECKBOX_CLIENT_VERSION")
        self.DEVICE_ID = os.getenv("DEVICE_ID")

        # Rozetka API
        self.ROZET_USERNAME = os.getenv("rozet_username")
        self.ROZET_PASSWORD = os.getenv("rozet_password")

        # CRM Host
        self.HOSTCRM = os.getenv("HOSTCRM")

        self.handlers =  {
            "callback_query",
            "edited_message",
            "message"
            }  
        
        self.commands = {
            "#взял": "take",
            "#склад": "stock",
            "#редактируєм": "edit",
            "#прихід": "arrival",
            "#коментар":"comment",
            "#нові":"new_orders",
            "/new_orders":"new_orders",
            "somthin":"somthin",
            }
        
        self.chats = {
            self.CH_ID_COURIER: "courier",
            self.CH_ID_MANAGER: "manager",
            self.CH_ID_STOCK: "stock",
            self.CH_ID_NP: "np_delivery",
            self.CH_ID_ROZ: "roz_delivery",
            self.CH_ID_UKR: "urk_delivery",

        }
        
        


