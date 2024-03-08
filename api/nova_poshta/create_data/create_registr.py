from . import ListClient, NpClient
from dotenv import load_dotenv
import os

np_cl = NpClient()
ls_cl = ListClient()
load_dotenv()

file_doc = "../common_asx/ttn_ref_list.json"
file_reg = "../common_asx/reg_ref_list.json"

class RegistrDoc():
    def create_ref(self, created_ttn):
        ttn_ref = created_ttn["data"][0]["Ref"]
        return ttn_ref
    def save_reg(self, resp):
        ref = resp["data"][0]["Ref"]
        ls_cl.add_in_list(file_reg, ref)

    def delete_doc(self):
        ls_cl.remove_in_list(file_doc)

    def create_reg(self):
        data_for_registr = ls_cl.load_processed(file_doc)
        resp = np_cl.insertDocumentsReg(data_for_registr)
        print(resp)
        return resp

    def add_reg(self):
        data_for_registr = ls_cl.load_processed(file_doc)
        ref_reg = ls_cl.load_processed(file_reg[-1])
        resp = np_cl.AddDocumentsReg(data_for_registr, ref_reg)
        print(resp)
        return resp

    def deleteReg(self):
        Ref = ls_cl.load_processed(file_reg[-1])
        resp = np_cl.deleteScanSheet(list(Ref))
        print(resp)
        return resp





