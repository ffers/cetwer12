class ParseResponce:
    def __init__(self):
        pass

    def text_report_add(self, pointer):  
        pointer.text = pointer.comment 
        for item in pointer.resp:
            pointer.text += "{}: {}\n".format(
                item["article"], 
                item["quantity"]
                )
        return pointer 
    
    def text_unknown_command(self, pointer):
        pointer.text = "Невідома команда або не використовуйте: #"
        return pointer
    
    def search_6_numbers(self, data_chat):
        pass