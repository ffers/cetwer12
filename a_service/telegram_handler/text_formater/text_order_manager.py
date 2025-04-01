from dataclasses import dataclass
from DTO import OrderDTO

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
        store_id = order.ordered_status.id
        status_color = { 
        1: "🔵",
        2: "🟣",
        3: "🟢",
        10: "⚪️"
        }
        if store_id in status_color:
            return status_color[store_id]
        else:
            "⬜️"
    
    def builder(self):
        self.tx_bl.status_order = self.status_order(self.order)
        self.tx_bl.order_number_description = self.order_number_description(self.order)
        self.tx_bl.costumer_comment = self.costumer_comment(self.order)
        self.tx_bl.product_block_header = self.product_block_header(self.order)
        self.tx_bl.costumer_name = self.recipient_name(self.order)
        self.tx_bl.costumer_phone = self.contact_number_phone_number(self.order)
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
            f"{self.tx_bl.order_number_description}"
            f"{self.tx_bl.costumer_comment}"
            f"{self.tx_bl.product_block_header}"
            f"{self.tx_bl.costumer_name}"
            f"{self.tx_bl.costumer_phone}"
            f"{self.tx_bl.address_line}"
            f"{self.tx_bl.payment_method_sum}"
            f"{self.tx_bl.delivery_method}"
            f"{self.tx_bl.recipient_name}"
            f"{self.tx_bl.recipient_phone}"
            f"{self.tx_bl.product_footer}"
        )
    
    def status_order(self, order: OrderDTO):
        return f"{self.status_color} {order.ordered_status.name}"
    
    def product_block_header(self, order):
        text = ""
        for product in order.ordered_product:
            text += f"{self.store_color} {product.products.article} - " 
            text += f"{product.quantity}шт - {product.price}\n"
        text += f"Сумма: {order.sum_price} грн\n"
        return text
    
    def costumer_comment(self, order):
        if order.description:
            return f"\n{self.store_color} Нотатка:\n" + order.description
        else:
            return "\nНотаток від клієнта нема\n"
        
    def costumer_name(self, order):
        text = "\nПокупець:\n"
        text += f"{order.costumer.last_name} {order.costumer.first_name}\n"
        return text
    
    def costumer_phone(self, order):
        return f"{order.costumer.phone}\n"
    
        
    def payment_method_sum(self, order):
        sum_before_goods = self.sum_before_goods(order)
        text = f"Спосіб оплати - {order.payment_method.name}, " 
        text += f"{sum_before_goods} \n\n" 
        return text
    
    def sum_before_goods(self, order):
        if order.sum_before_goods:
            return order.sum_before_goods
        else:
            return order.sum_price 
    
    def recipient_name(self, order):
        text = "\nОтримувач:\n"
        text += f"{order.recipient.last_name} {order.recipient.first_name}\n"
        return text

    
    def recipient_phone(self, order):
        return f"{order.recipient.phone}\n"
    
    
    def order_number_description(self, order):
        text = f"\n{self.store_color} {order.source_order.name} "
        text += f"Замовлення № {order.order_code}\n"
        return text
    
    def contact_number_phone_number(self, order):
        ttn = order.ttn if order.ttn else "ТТН немає"        
        return f"\n{order.costumer.phone};{ttn}\n"
    
    def address_line(self, order):
        city_name = f"{order.city_name}, " if order.city_name else ""
        return f"\n{city_name}{order.warehouse_text}\n"
    
    def delivery_method(self, order: OrderDTO):
        return f"{order.delivery_method.name}"
    
    def product_block_footer(self, order):
        text = "На всяк випадок:\n"
        for product in order.ordered_product:
            text += f" {product.products.product_name}\n"
        return text
    
        
