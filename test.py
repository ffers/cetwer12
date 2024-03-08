import json
import pyperclip


{'success': True, 'data': [
    {'Ref': '', 'Number': '', 'Date': '2023-11-08 15:43:07', 'Description': '', 'Errors': [], 'Success': [],
     'Warnings': [], 'Data': {'Errors': [
        {'Ref': '2818717d-7dfe-11ee-a60f-48df37b921db', 'Number': '20450806891145', 'Error': 'Документ видалено'},
        {'Ref': '34ffbcb1-7dfd-11ee-a60f-48df37b921db', 'Number': '20450806890137', 'Error': 'Документ видалено'},
        {'Ref': '48445265-7dfd-11ee-a60f-48df37b921db', 'Number': '20450806890220', 'Error': 'Документ видалено'},
        {'Ref': 'de871e54-7dff-11ee-a60f-48df37b921db', 'Number': '20450806893625', 'Error': 'Документ видалено'}],
                              'Success': [], 'Warnings': []}}], 'errors': [], 'warnings': [], 'info': [],
 'messageCodes': [], 'errorCodes': [], 'warningCodes': [], 'infoCodes': []}

data = {"success": True, "data": [{"Ref": "b6e3a2d5-8d25-11ee-a60f-48df37b921db", "Description": "Матківська Маряна ", "LastName": "Матківська", "FirstName": "Маряна", "MiddleName": "", "Phones": "380687247786", "Email": ""}], "errors": [], "warnings": ["Person already exists!"], "info": [], "messageCodes": [], "errorCodes": [], "warningCodes": ["30000801043"], "infoCodes": []}


# reg ["414b649c-7e43-11ee-a60f-48df37b921db"]
# 32a4ee96-7e59-11ee-a60f-48df37b921db
#
# doc ["cf23f5f4-7e42-11ee-a60f-48df37b921db"]

Ref = data["data"][0]["Ref"]

print(Ref)


import re


text = "1 234,54 грн"
text2 = "с. Шевченково (Капенська обл.), Пункт приема-выдачи (до 30 кг): ул. Мира, 10"
text3 = "с. Катеринівка (Покровський р-н Дніпропетр. обл.), Пункт приймання-видачі (до 30 кг): вул. Центральна, 9"
craft = "=SUMIF($A$24:$X$406; \"S6\"; $C$24:$C$406)+SUMIF($A$24:$X$406; \"N36\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N29\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N6\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"S7\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N8\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N19\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"W2\"; $C$24:$C$406)"
blacknike = "=SUMIF($A$24:$X$406; \"N1\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N2\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N14\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N7\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N9\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N15\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N25\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N17\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"W6\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"S10\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N19\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N20\"; $C$24:$C$406) + SUMIF($A$24:$X$406; \"N18\"; $C$24:$C$406)"
tiedye = "=SUMIF($A$24:$X$406; \"N\"; $C$24:$C$406) + (SUMIF($A$24:$X$406; \"N2\"; $C$24:$C$406)*5) + (SUMIF($A$24:$X$406; \"N13\"; $C$24:$C$406)*13) + (SUMIF($A$24:$X$406; \"N14\"; $C$24:$C$406)*5) + (SUMIF($A$24:$X$406; \"N7\"; $C$24:$C$406)*5) + (SUMIF($A$24:$X$406; \"N9\"; $C$24:$C$406)*5) + (SUMIF($A$24:$X$406; \"N15\"; $C$24:$C$406)*5)"
# [?<=\(]([А-ЯІЇЄҐ]\D+)(?=\sобл) /// [.,]\s*([А-ЯІЇЄҐ][^\(\),]*?)\s*обл[.]
result = re.findall(r"[?<=\(]([А-ЯA-ZА-ЯІЄЇ]\D+)(?=\sобл)", text2)
result2 = re.findall(r"([А-ЯІЇЄҐ][^\(\),\s]*?)\.*\s*р-н", text3)
pattern = r'Замовлення №\s*(\d+)'
number_order = re.search(pattern, "Замовлення №269906010")
ord = number_order.group(1).strip()

Cost = ''.join(re.findall(r'\d+', text))

form = re.sub(r'\$A\$24:\$X\$406', 'A31:A56', blacknike)
form2 = re.sub(r'\$C\$24:\$C\$406', 'C31:C56', form)
pyperclip.copy(form2)
print(form2)