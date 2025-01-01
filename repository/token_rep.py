from server_flask.db import db
from DTO import UserTokenDTO


class TokenRep:
    def add_token(self, d: UserTokenDTO):
        try:
            item = UserToken(
        timestamp=d.timestamp,
        project_id=d.project_id,
        user_id=d.user_id,
        np_token=d.np_token,
        prom_token=d.prom_token,
        telegram_bot_token=d.telegram_bot_token,
        telegram_bot_token_test=d.telegram_bot_token_test,
        payment_token=d.payment_token,
        shop_id=d.shop_id,
        np_phone=d.np_phone,
        sms_token=d.sms_token,
        np_sender_refs=d.np_sender_refs,
        np_count_refs=d.np_count_refs,
        np_city_cender=d.np_city_cender,
        np_adress_contr=d.np_adress_contr,
        np_conter_recipient=d.np_conter_recipient,
        np_conter_recipient_owner_form=d.np_conter_recipient_owner_form,
        np_conter_recipent_counterparty=d.np_conter_recipent_counterparty,
        db_username=d.db_username,
        db_password=d.db_password,
        chat_id_info=d.chat_id_info,
        chat_id_confirmation=d.chat_id_confirmation,
        chat_id_helper=d.chat_id_helper,
        ch_id_np=d.ch_id_np,
        ch_id_sk=d.ch_id_sk,
        ch_id_ukr=d.ch_id_ukr,
        ch_id_roz=d.ch_id_roz,
        ch_id_stok=d.ch_id_stok,
        ch_id_shop=d.ch_id_shop,
        token_to_srm_send_with_prom=d.token_to_srm_send_with_prom,
        token_to_srm_update_with_prom=d.token_to_srm_update_with_prom,
        x_telegram_api_bot_token=d.x_telegram_api_bot_token,
        fromatter_log=d.fromatter_log,
        checkbox_license_key=d.checkbox_license_key,
        checkbox_host=d.checkbox_host,
        checkbox_client_name=d.checkbox_client_name,
        checkbox_pin_cashier=d.checkbox_pin_cashier,
        checkbox_client_version=d.checkbox_client_version,
        device_id=d.device_id,
        checkbox_access_token=d.checkbox_access_token
            )
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            return False, e
        
    def update_token(self):
        pass

        


