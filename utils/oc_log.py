import logging

def oc_log(file_path, name_log):
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    order_cntrl_handler = logging.FileHandler(file_path)
    order_cntrl_handler.setFormatter(log_formatter)
    OC_log = logging.getLogger(name_log)
    OC_log.setLevel(logging.INFO)
    OC_log.addHandler(order_cntrl_handler)
    return OC_log