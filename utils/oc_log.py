import logging

class UtilsAsx:
    def oc_log(self, name_log):
        file_path = f"../common_asx/log/{name_log}.log"
        log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        log_formatter = logging.Formatter(log_format)
        order_cntrl_handler = logging.FileHandler(file_path)
        order_cntrl_handler.setFormatter(log_formatter)
        OC_log = logging.getLogger(name_log)
        OC_log.setLevel(logging.INFO)
        OC_log.addHandler(order_cntrl_handler)
        return OC_log



util_asx = UtilsAsx()