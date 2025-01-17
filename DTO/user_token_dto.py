from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from datetime import datetime

class UserTokenDTO(BaseModel):
    id: Optional[int] = None
    timestamp: Optional[datetime] = None
    project_id: Optional[int] = None
    user_id: int
    np_token: Optional[str] = None
    prom_token: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_bot_token_test: Optional[str] = None
    payment_token: Optional[str] = None
    shop_id: Optional[str] = None
    np_phone: Optional[str] = None
    sms_token: Optional[str] = None
    np_sender_refs: Optional[str] = None
    np_count_refs: Optional[str] = None
    np_city_cender: Optional[str] = None
    np_adress_contr: Optional[str] = None
    np_conter_recipient: Optional[str] = None
    np_conter_recipient_owner_form: Optional[str] = None
    np_conter_recipent_counterparty: Optional[str] = None
    db_username: Optional[str] = None
    db_password: Optional[str] = None
    chat_id_info: Optional[str] = None
    chat_id_confirmation: Optional[str] = None
    chat_id_helper: Optional[str] = None
    ch_id_np: Optional[str] = None
    ch_id_sk: Optional[str] = None
    ch_id_ukr: Optional[str] = None
    ch_id_roz: Optional[str] = None
    ch_id_stok: Optional[str] = None
    ch_id_shop: Optional[str] = None
    token_to_srm_send_with_prom: Optional[str] = None
    token_to_srm_update_with_prom: Optional[str] = None
    x_telegram_api_bot_token: Optional[str] = None
    fromatter_log: Optional[str] = None
    checkbox_license_key: Optional[str] = None
    checkbox_host: Optional[str] = None
    checkbox_client_name: Optional[str] = None
    checkbox_pin_cashier: Optional[str] = None
    checkbox_client_version: Optional[str] = None
    device_id: Optional[str] = None
    checkbox_access_token: Optional[str] = None
