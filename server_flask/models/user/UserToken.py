from datetime import datetime
from server_flask.db import db
from DTO import UserTokenDTO


class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id', name='fk_usertoken_project_id'))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', name='fk_usertoken_user_id'), nullable=False, unique=True)
    np_token = db.Column(db.String(255))
    prom_token = db.Column(db.String(255))
    telegram_bot_token = db.Column(db.String(255))
    telegram_bot_token_test = db.Column(db.String(255))
    payment_token = db.Column(db.String(255))
    shop_id = db.Column(db.String(255))
    np_phone = db.Column(db.String(255))
    sms_token = db.Column(db.String(255))
    np_sender_refs = db.Column(db.String(255))
    np_count_refs = db.Column(db.String(255)) 
    np_city_cender = db.Column(db.String(255))
    np_adress_contr = db.Column(db.String(255))
    np_conter_recipient = db.Column(db.String(255))
    np_conter_recipient_owner_form = db.Column(db.String(255))
    np_conter_recipent_counterparty = db.Column(db.String(255))
    db_username = db.Column(db.String(255))
    db_password = db.Column(db.String(255))
    chat_id_info = db.Column(db.String(255))
    chat_id_confirmation = db.Column(db.String(255))
    chat_id_helper = db.Column(db.String(255))
    ch_id_np = db.Column(db.String(255))
    ch_id_sk = db.Column(db.String(255))
    ch_id_ukr = db.Column(db.String(255))
    ch_id_roz = db.Column(db.String(255))
    ch_id_stok = db.Column(db.String(255))
    ch_id_shop = db.Column(db.String(255))
    token_to_srm_send_with_prom = db.Column(db.String(255))
    token_to_srm_update_with_prom = db.Column(db.String(255))
    x_telegram_api_bot_token = db.Column(db.String(255))
    fromatter_log = db.Column(db.String(255))
    checkbox_license_key = db.Column(db.String(255))
    checkbox_host = db.Column(db.String(255))
    checkbox_client_name = db.Column(db.String(255))
    checkbox_pin_cashier = db.Column(db.String(255))
    checkbox_client_version = db.Column(db.String(255))
    device_id = db.Column(db.String(255))
    checkbox_access_token = db.Column(db.String(512))

    def __init__(self, d: UserTokenDTO):
        """
        Кастомний конструктор для створення екземпляра UserToken з UserTokenDTO.
        """
        self.project_id = d.project_id
        self.user_id = d.user_id
        self.np_token = d.np_token
        self.prom_token = d.prom_token
        self.telegram_bot_token = d.telegram_bot_token
        self.telegram_bot_token_test = d.telegram_bot_token_test
        self.payment_token = d.payment_token
        self.shop_id = d.shop_id
        self.np_phone = d.np_phone
        self.sms_token = d.sms_token
        self.np_sender_refs = d.np_sender_refs
        self.np_count_refs = d.np_count_refs
        self.np_city_cender = d.np_city_cender
        self.np_adress_contr = d.np_adress_contr
        self.np_conter_recipient = d.np_conter_recipient
        self.np_conter_recipient_owner_form = d.np_conter_recipient_owner_form
        self.np_conter_recipent_counterparty = d.np_conter_recipent_counterparty
        self.db_username = d.db_username
        self.db_password = d.db_password
        self.chat_id_info = d.chat_id_info
        self.chat_id_confirmation = d.chat_id_confirmation
        self.chat_id_helper = d.chat_id_helper
        self.ch_id_np = d.ch_id_np
        self.ch_id_sk = d.ch_id_sk
        self.ch_id_ukr = d.ch_id_ukr
        self.ch_id_roz = d.ch_id_roz
        self.ch_id_stok = d.ch_id_stok
        self.ch_id_shop = d.ch_id_shop
        self.token_to_srm_send_with_prom = d.token_to_srm_send_with_prom
        self.token_to_srm_update_with_prom = d.token_to_srm_update_with_prom
        self.x_telegram_api_bot_token = d.x_telegram_api_bot_token
        self.fromatter_log = d.fromatter_log
        self.checkbox_license_key = d.checkbox_license_key
        self.checkbox_host = d.checkbox_host
        self.checkbox_client_name = d.checkbox_client_name
        self.checkbox_pin_cashier = d.checkbox_pin_cashier
        self.checkbox_client_version = d.checkbox_client_version
        self.device_id = d.device_id
        self.checkbox_access_token = d.checkbox_access_token

    def update_from_dto(self, d: UserTokenDTO):
        self.project_id = d.project_id or self.project_id
        self.user_id = d.user_id or self.user_id
        self.np_token = d.np_token or self.np_token
        self.prom_token = d.prom_token or self.prom_token
        self.telegram_bot_token = d.telegram_bot_token or self.telegram_bot_token
        self.telegram_bot_token_test = d.telegram_bot_token_test or self.telegram_bot_token_test
        self.payment_token = d.payment_token or self.payment_token
        self.shop_id = d.shop_id or self.shop_id
        self.np_phone = d.np_phone or self.np_phone
        self.sms_token = d.sms_token or self.sms_token
        self.np_sender_refs = d.np_sender_refs or self.np_sender_refs
        self.np_count_refs = d.np_count_refs or self.np_count_refs
        self.np_city_cender = d.np_city_cender or self.np_city_cender
        self.np_adress_contr = d.np_adress_contr or self.np_adress_contr
        self.np_conter_recipient = d.np_conter_recipient or self.np_conter_recipient
        self.np_conter_recipient_owner_form = d.np_conter_recipient_owner_form or self.np_conter_recipient_owner_form
        self.np_conter_recipent_counterparty = d.np_conter_recipent_counterparty or self.np_conter_recipent_counterparty
        self.db_username = d.db_username or self.db_username
        self.db_password = d.db_password or self.db_password
        self.chat_id_info = d.chat_id_info or self.chat_id_info
        self.chat_id_confirmation = d.chat_id_confirmation or self.chat_id_confirmation
        self.chat_id_helper = d.chat_id_helper or self.chat_id_helper
        self.ch_id_np = d.ch_id_np or self.ch_id_np
        self.ch_id_sk = d.ch_id_sk or self.ch_id_sk
        self.ch_id_ukr = d.ch_id_ukr or self.ch_id_ukr
        self.ch_id_roz = d.ch_id_roz or self.ch_id_roz
        self.ch_id_stok = d.ch_id_stok or self.ch_id_stok
        self.ch_id_shop = d.ch_id_shop or self.ch_id_shop
        self.token_to_srm_send_with_prom = d.token_to_srm_send_with_prom or self.token_to_srm_send_with_prom
        self.token_to_srm_update_with_prom = d.token_to_srm_update_with_prom or self.token_to_srm_update_with_prom
        self.x_telegram_api_bot_token = d.x_telegram_api_bot_token or self.x_telegram_api_bot_token
        self.fromatter_log = d.fromatter_log or self.fromatter_log
        self.checkbox_license_key = d.checkbox_license_key or self.checkbox_license_key
        self.checkbox_host = d.checkbox_host or self.checkbox_host
        self.checkbox_client_name = d.checkbox_client_name or self.checkbox_client_name
        self.checkbox_pin_cashier = d.checkbox_pin_cashier or self.checkbox_pin_cashier
        self.checkbox_client_version = d.checkbox_client_version or self.checkbox_client_version
        self.device_id = d.device_id or self.device_id
        self.checkbox_access_token = d.checkbox_access_token or self.checkbox_access_token



                    