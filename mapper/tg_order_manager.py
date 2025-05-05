from dataclasses import dataclass
from DTO import OrderDTO
import re

@dataclass
class TextBlocks:
    status_order: str = None
    order_number_description: str = None 
    costumer_comment: str = None
    product_block_header: str = None
    costumer_phone: str = None
    costumer_name: str = None
    payment_method_sum: str = None
    delivery_method: str = None
    recipient_name: str = None
    recipient_phone: str = None
    address_line: str = None
    product_footer: str = None



class TextOrderManager:
    def __init__(self, order: OrderDTO):
        self.order = order
        self.store_color = self.take_store_color(order)
        self.status_color = self.status_color_take(order)
        self.tx_bl = TextBlocks()

    def take_store_color(self, order):
        store_id = order.source_order.id
        marketplace_color = { 
        1: "🔵",
        2: "🟣",
        3: "🟢",
        }
        if store_id in marketplace_color:
            return marketplace_color[store_id]
        else:
            "⬜️"

    def status_color_take(self, order):
        store_id = order.ordered_status_id
        status_color = { 
        1: "🔵",
        2: "🟣",
        3: "🟢",
        1: "🟠",
        10: "⚪️"
        }
        if store_id in status_color:
            return status_color[store_id]
        else:
            return "⬜️"
    
    def builder(self):
        self.tx_bl.status_order = self.status_order(self.order)
        self.tx_bl.order_number_description = self.order_number_description(self.order)
        self.tx_bl.costumer_comment = self.costumer_comment(self.order)
        self.tx_bl.product_block_header = self.product_block_header(self.order)
        self.tx_bl.costumer_name = self.costumer_name(self.order)
        self.tx_bl.costumer_phone = self.costumer_phone(self.order)
        self.tx_bl.address_line = self.address_line(self.order)
        self.tx_bl.payment_method_sum = self.payment_method_sum(self.order)
        self.tx_bl.delivery_method = self.delivery_method(self.order)
        self.tx_bl.recipient_name = self.recipient_name(self.order)
        self.tx_bl.recipient_phone = self.recipient_phone(self.order)
        self.tx_bl.product_footer = self.product_block_footer(self.order)
        return self.general_text()
    
    def general_text(self):
        return (
            f"{self.tx_bl.status_order}"
            f"{self.tx_bl.order_number_description}\n"
            f"{self.tx_bl.product_block_header}\n"
            f"{self.tx_bl.costumer_comment}\n"
            f"{self.tx_bl.costumer_name}"
            f"{self.tx_bl.costumer_phone}\n"
            f"{self.tx_bl.payment_method_sum}"
            f"{self.tx_bl.delivery_method}\n"
            f"{self.tx_bl.address_line}"
            f"{self.tx_bl.recipient_phone}"
            f"{self.tx_bl.recipient_name}\n"
            f"{self.tx_bl.product_footer}"
            f"▪️▪️▪️"
        )
    
    def status_order(self, order: OrderDTO):
        return f"{self.status_color} {order.ordered_status.name}\n"
    
    def product_block_header(self, order):
        text = ""
        for product in order.ordered_product:
            text += f"{self.store_color} {product.products.article} - " 
            text += f"{product.quantity}шт - {product.price}\n"
        text += f"Сумма: {order.sum_price} грн\n"
        return text
    
    def costumer_comment(self, order):
        if order.description:
            return f"{self.store_color} Нотатка:\n" + order.description
        else:
            return "Нотаток від клієнта нема\n"
        
    def costumer_name(self, order):
        text = "Покупець:\n"
        text += f"{order.costumer.last_name} {order.costumer.first_name}\n"
        return text
    
    def costumer_phone(self, order):
        phone = re.sub(r"^\d{2}", "", order.costumer.phone)
        return f"{phone}\n"
    
    def delivery_method(self, order: OrderDTO):
        return f"{order.delivery_method.name}\n"
    
    def payment_method_sum(self, order):
        sum_before_goods = self.sum_before_goods(order)
        text = f"Спосіб оплати - {order.payment_method.name}, " 
        text += f"{self.payment_status(order)} "
        text += f"{sum_before_goods}\n" 
        print("payment_method_sum:", text)
        return text
    
    def sum_before_goods(self, order):
        if order.sum_before_goods:
            return order.sum_before_goods
        else:
            return order.sum_price 
    
    def recipient_name(self, order):
        text = f"{order.recipient.last_name} {order.recipient.first_name}\n"
        return text

    
    def recipient_phone(self, order):
        return f"{order.recipient.phone}\n"
    
    
    def order_number_description(self, order):
        text = f"{self.store_color} "
        if order.store:
            text += f"{order.store.name} "
        text += f"Замовлення № {order.order_code}\n"
        return text

    
    def address_line(self, order):
        city_name = "Адреса Доставки:\n"
        return f"{city_name}{order.warehouse_text}\n"
    
    
    def product_block_footer(self, order):
        text = "На всяк випадок:\n"
        for product in order.ordered_product:
            text += f" {product.products.product_name}\n"
        return text
    
    def payment_status(self, order):
        print("payment_status", order)
        print("payment_status", order.payment_method_id)
        if order.payment_method_id == 5:
            s = order.payment_status_id
            print("payment_status2", s)
            statuses = {
                1: "Сплачено",
                2: "Несплачено",
                3: "Повернуто"
            }
            if s in statuses:
                return statuses[s]
        return ""
    
        
