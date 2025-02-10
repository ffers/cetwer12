from datetime import datetime

class Formatter:
    @staticmethod
    def format(order):
        return (
            f"🟢 {order.product_code} - {order.quantity} - {order.total_price}\n"
            f" Cумма {order.total_price}\n\n"
            f"Дата створення замовлення {order.created_at}\n\n"
            f"Нотаток від клієнта: {order.note or 'нема'}\n\n"
            f"{order.delivery_service}\n"
            f"Оплата: {order.payment_method}, order_id={order.order_id} "
            f"status_payment_id={order.payment_status_id} "
            f"name='{order.payment_status_name}' title='{order.payment_status_title}' "
            f"value={order.payment_value} payment_invoice_id={order.payment_invoice_id} "
            f"created_at='{order.created_at}'\n"
            f"\nПокупець:\n{order.customer_name}\n{order.customer_phone}\n\n"
            f"🟢 Замовлення Розетка Маркет № {order.order_id}\n\n"
            f"Отримувач:\n{order.recipient_address}\n"
            f"{order.recipient_name}\n{order.recipient_phone}\n\n"
            f"Назва: {order.product_name}\n\n"
            f"delivery_service_id: {order.delivery_service_id}\n"
            f"payment_method_id: {order.payment_method_id}\n"
            f"delivery_method_id: {order.delivery_method_id}\n"
        )
