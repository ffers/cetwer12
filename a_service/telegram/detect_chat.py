from settings import Settings
from abc import ABC

class Chat(ABC):
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def execute(self, text):
        pass

class Manager(Chat):
    def execute(self, text):
        return "Comand for chat meneger"
    
class Stock(Chat):
    def execute(self, text):
        return "Comand for chat stock"
    
class Courier(Chat):
    def execute(self, text):
        return "Comand for chat courier"
    
class CheckText:
    def execute(self, text):
        pass
    pass



class FlagStrategy:
    def __init__(self, settings):
        self.settings = settings or Settings()

    def get_flag(self, chat_id, text):
        chat = {
            self.settings.CHAT_ID_MANAGER: Manager,
            self.settings.CH_ID_STOCK: Stock,
            self.settings.CH_ID_COURIER: Courier
        }
        if chat.get(chat_id, None):
            return chat[chat_id](text)

    

# update color
    def work_with_product(self, data):
            if "text" in data["message"]:
                text = data["message"]["text"]
                chat_id = data["message"]["chat"]["id"]
                print(text)
                update_color = self.pc_cl.manager_bot(text)
                return update_color
            else:
                return "Щось не те..."
        
# update color
    def parse(self, text):
            if "#взял" in text or "#склад" in text:
                pass
            if "35:" in text or "45:" in text:
                print("ПРАЦЮЄ")
                data = self.parse_text(text)
                flag = self.count_flag(text)
            if "35:" in text and "45:" in text:
                pass
# update color 
    def count_flag(self, text):
        if "#взял" in text:
            return "#взял"
        if "#склад" in text:
            return "#склад"
        if "#редактируєм" in text:
            return "#склад"
# update color       
    def count_size(self, text):
        if "45:" in text:
            return Colorrep45, "45:"
        if "35:" in text:
            return Colorrep35, "35:"

# update color
    def parse_text(self, text):
        taken_text = re.findall(r'(\d+х-*\d+)', text)
        print(taken_text)
        # pars = taken_text.split(', ')
        data = {int(par.split('х')[0]): int(par.split('х')[1]) for par in taken_text}
        print(data)
        return data
# bad func
    def await_order(self, order, flag=None, id=None):
        print(f"ДИвимось флаг {flag}")
        resp = None
        if flag == "prom_to_crm":
            data_for_tg = crmtotg_cl.manger(order)
            resp = crm_cl.add_order(order, data_for_tg)
        if flag == "update_to_crm":
            resp = up_to_srm.manager(order)
        else:
            tg_serv.see_flag(order, flag)
        return resp
    
# check for message or call_back
    def await_tg_button(self, data):
        if "message" in data: #працює з усіма відповдями
            self.await_telegram(data)
            # button_hand(data)
        if "callback_query" in data:
            self.await_button(data)
        return '', 200

# work with callback bed func
    def await_button(self, data): #працює з Підтвердженнями
        chat_id = data["callback_query"]["message"]["chat"]["id"]
        if int(tg_cntrl.chat_id_confirm) == chat_id:
            key = data["callback_query"]["message"]["reply_markup"]
            call_back_id = data["callback_query"]["id"]
            tg_cntrl.answerCallbackQuery(call_back_id, "Працюю")
            # resp_tg = tg_cntrl.sendMessage(tg_cntrl.chat_id_confirm, "Працюю")
            # send_message_id, send_chat_id = self.serv.id_message(resp_tg)
            if "inline_keyboard" in key:
                text_order, data_keyb, text_data_back = tg_serv.await_button_parse(data)
                print(f"need {key}")
                order_id = tg_serv.search_order_number(text_order)
                order_obj = ord_cntrl.load_for_order_code(order_id)
                resp = self.defintion_status(data_keyb, order_obj.id)
                # tg_cntrl.deleteMessage(tg_cntrl.chat_id_confirm, send_message_id)
                return resp
            
# work with callback bed func
    def defintion_status(self, data_keyb, order_id):
        resp = None
        print(f"data_keyb {data_keyb}")
        if "1" == data_keyb:
            resp = ord_cntrl.confirmed_order(order_id)
            print(resp) 
        if "2" == data_keyb:
            resp = ord_cntrl.question_order(order_id)
        return resp
#rouster
# sorted chat for  work
# sorted comand
# where make text for drop

class FlagStrategy:
    @staticmethod
    def get_flag(text):
        flags = {
            "#взял": "#взял",
            "#склад": "#склад",
            "#редактируєм": "#склад",
            "#приход": None
        }
        return flags.get(text, None)