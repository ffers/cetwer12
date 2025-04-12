from dataclasses import dataclass

@dataclass
class TextBlocks:
    product_block_header: str = None
    client_comment: str = None
    address_line: str = None
    order_number_description: str = None 
    contact_number_phone_number: str = None
    contact_name: list = None
    payment_method_sum: list = None
    product_block_footer: str = None

class TextOrderCourier:
    def __init__(self, order):
        self.store_color = self.take_store_color(order)
        self.text_blocks = TextBlocks()

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
    
    def builder(self, order):
        self.text_blocks.product_block_header = self.product_block_header(order)
        self.text_blocks.client_comment = self.client_comment(order)
        self.text_blocks.address_line = self.address_line(order)
        self.text_blocks.order_number_description = self.order_number_description(order)
        self.text_blocks.contact_number_phone_number = self.contact_number_phone_number(order)
        self.text_blocks.contact_name = self.contact_name(order)
        self.text_blocks.payment_method_sum = self.payment_method_sum(order)
        self.text_blocks.product_block_footer = self.product_block_footer(order)
        return self.general_text()
    
    def general_text(self):
        return (
            f"{self.text_blocks.product_block_header}"
            f"{self.text_blocks.client_comment}"
            f"{self.text_blocks.address_line}"
            f"{self.text_blocks.order_number_description}"
            f"{self.text_blocks.contact_number_phone_number}"
            f"{self.text_blocks.contact_name}"
            f"{self.text_blocks.payment_method_sum}"
            f"{self.text_blocks.product_block_footer}"
            f"▪️▪️▪️"
        )
    
    def product_block_footer(self, order):
        text = "На всяк випадок:\n"
        for product in order.ordered_product:
            text += f" {product.products.product_name}\n"
        return text
    
    def payment_method_sum(self, order):
        sum_before_goods = self.sum_before_goods(order)
        text = f"Спосіб оплати - {order.payment_method.name}, " 
        text += f"{sum_before_goods} \n\n" 
        return text
    
    def sum_before_goods(self, order):
        if order.sum_before_goods:
            print("sum_before_goods:", order.sum_before_goods)
            return order.sum_before_goods
        else:
            return order.sum_price 
    
    def contact_name(self, order):
        return f"{order.client_lastname} {order.client_firstname}\n"
    
    def contact_number_phone_number(self, order):
        ttn = order.ttn if order.ttn else "ТТН немає"        
        return f"\n{order.phone};{ttn}\n"
    
    def order_number_description(self, order):
        text = f"\n{self.store_color} {order.source_order.name} "
        text += f"Замовлення № {order.order_code}\n"
        return text
    
    def address_line(self, order):
        city_name = "" if order.city_name else "" # times change
        return f"\n{city_name}{order.warehouse_text}\n"
    
    def client_comment(self, order):
        if order.description:
            return f"\n{self.store_color} Нотатка:\n" + order.description
        else:
            return "\nНотаток від клієнта нема\n"
        
    def product_block_header(self, order):
        text = ""
        for product in order.ordered_product:
            text += f"{self.store_color} {product.products.article} - " 
            text += f"{product.quantity}шт - {product.price}\n"
        text += f"Сумма: {order.sum_price} грн\n"
        return text
