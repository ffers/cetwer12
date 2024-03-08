import logging, pytz


logging.basicConfig(filename='../common_asx/log_order.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

georgia_timezone = pytz.timezone('Asia/Tbilisi')



# Завантаження оброблених ордерів із файлу
logging.info("Шукаєм нові замовленя...")




