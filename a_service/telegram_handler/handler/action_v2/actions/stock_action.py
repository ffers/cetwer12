
from utils import my_time_v2
from ..base import Command

class ThisSubtrection(Exception):
    pass


class StockAction(Command):
    def execute(self, data_chat): 
        return self.parse_stock(data_chat, self.SourAnCntrl)

    def parse_stock(self, data_chat, sour_cntrl):
        data_chat.resp = [] 
        for item in data_chat.content:
            try:
                data_chat = self.fixed_product(
                    data_chat,
                    sour_cntrl, 
                    item                    
                )
            except Exception as e:
                print(f"Помилка під час обробки '{item}': {e}")                
                data_chat.text = f"{e}\n"
                break
                
        return data_chat 
    
    '''
    в мене по суті є кілька обʼєктів
    артікул str
    кількість int або None
    комент str
    відповідь  str
    і мабуть потрібна відповідь чи ок чи ні
    особливо якщо ні
    resp має з цього робити респ 
    чую що рухаємось в сторону продакт модуля
    бо є ще замовленя тобто типи глобальних обʼєктів 
    '''
    
    def fixed_product(self, data_chat, sour_cntrl, item): # очень сложно неправильно построено
        item_prod = sour_cntrl.load_article(item["article"])
        quantity = item.get("quantity")
        if item_prod:
            print("parse_stock:", data_chat)
            if not data_chat.comment:
                item['quantity'] = 'Нерахується'
                raise ValueError("‼️ Некоректний (комент)")
            data_chat.text = data_chat.comment
            print("dev_parse_color: ", data_chat.comment)
            resp = sour_cntrl.fixed_process(
                item_prod.id, 
                quantity, 
                data_chat.comment,
                my_time_v2()
            )   
            self.balance(sour_cntrl, quantity, item_prod)
            item.update({"crm": resp})     
        else:
            item['quantity'] = "‼️ Такого товару нема"
            
        return data_chat
    
    def balance(self, sour_cntrl, quantity, source):
        try:
            if '-' in str(quantity):
                raise ThisSubtrection('це вичет все гуд')
            source_bal = sour_cntrl.load_article("balance")
            pay = quantity * source.price
            sour_cntrl.fixed_process(
                source_bal.id, 
                -pay, 
                'автоматичне списання',
                my_time_v2()
            )   
            self.logger.info(f'Вичетаня балансу SUCCESS')
            return True
        except ThisSubtrection: return True
        except Exception as e:
            self.logger.error(f'Вичетаня балансу не працює {e}', exc_info=True)
    
 
    
