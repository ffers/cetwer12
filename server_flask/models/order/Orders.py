from datetime import datetime
from server_flask.db import db

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50))
    ttn = db.Column(db.String(50))
    ttn_ref = db.Column(db.String(50)) # edit
    client_firstname = db.Column(db.String(50))
    client_lastname = db.Column(db.String(50))
    client_surname = db.Column(db.String(50))
    # recipient_id = db.Column(db.Integer, db.ForeignKey(
    #     'recipient_delivery.id', name='fk_orders_recipient_delivery_id'))
    delivery_option = db.Column(db.String(50))
    city_name = db.Column(db.String(50))
    city_ref = db.Column(db.String(50))
    region = db.Column(db.String(50))
    area = db.Column(db.String(50))
    warehouse_option = db.Column(db.String(50))
    warehouse_text = db.Column(db.String(255))
    warehouse_ref = db.Column(db.String(50))
    # payment_option = db.Column(db.String(50))
    sum_price = db.Column(db.Float)
    sum_before_goods = db.Column(db.Float)
    description = db.Column(db.String(300))
    history = db.Column(db.String(500))
    description_delivery = db.Column(db.String(50))
    cpa_commission = db.Column(db.String(50)) 
    client_id = db.Column(db.Integer)
    send_time = db.Column(db.DateTime)
    order_id_sources = db.Column(db.String(50))
    order_code = db.Column(db.String(50), unique=True)
    ordered_product = db.relationship('OrderedProduct', backref='orders', cascade='all, delete-orphan')
    delivery_order = db.relationship("DeliveryOrder", back_populates="orders", uselist=False, cascade="all, delete-orphan")
    prompay_status = db.relationship("PrompayStatus", back_populates="orders")
    prompay_status_id = db.Column(db.Integer, db.ForeignKey(
        'prompay_status.id', name='fk_orders_prompay_status_id'))
    ordered_status = db.relationship("OrderedStatus", back_populates="orders")
    ordered_status_id = db.Column(db.Integer, db.ForeignKey(
        'ordered_status.id', name='fk_orders_ordered_status_id'))
    warehouse_method = db.relationship("WarehouseMethod", back_populates="orders")
    warehouse_method_id = db.Column(db.Integer, db.ForeignKey(
        'warehouse_method.id', name='fk_orders_warehouse_method_id'))
    source_order = db.relationship("SourceOrder", back_populates="orders")
    source_order_id = db.Column(db.Integer, db.ForeignKey(
        'source_order.id', name='fk_orders_source_order_id'))
    payment_method = db.relationship("PaymentMethod", back_populates="orders")
    payment_method_id = db.Column(db.Integer, db.ForeignKey(
        'payment_method.id', name='fk_orders_payment_method_id'))
    delivery_method = db.relationship("DeliveryMethod", back_populates="orders")
    delivery_method_id = db.Column(db.Integer, db.ForeignKey(
        'delivery_method.id', name='fk_orders_delivery_method_id'))
    author_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', name='fk_orders_users_id', ondelete="CASCADE"), nullable=True)
    comments = db.relationship('Comment', backref='orders', passive_deletes=True)
    likes = db.relationship('Likes', backref='orders', passive_deletes=True)
    telegram_ordered = db.relationship('TelegramOrdered', backref='orders', cascade='all, delete-orphan')
    products = db.relationship('Products', secondary='ordered_product', overlaps="ordered_product,orders")

