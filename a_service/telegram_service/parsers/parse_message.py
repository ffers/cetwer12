from .parse_text import ParseText
from flatten_dict import flatten

class ParseMsg:
    def __init__(self, data, pointer):
        self.data = data
        self.pointer = pointer

    def execute(self):
        pass

class SearchType(ParseMsg):
    def execute(self):
        for handler in self.pointer:
            if handler in self.data:
                return handler
        return "unknown"

class TakeChat(ParseMsg):
    def execute(self):
        chat_way = {
            "callback_query": "callback_query.message.chat.id",
            "edited_message": "edited_message.chat.id",
            "message": "message.chat.id",
        }
        if self.pointer in chat_way:
            return self.data[chat_way[self.pointer]]
        
class TakeText(ParseMsg):
    def execute(self):
        data = flatten(self.data, "dot")
        way = {
            "callback_query": "callback_query.message.text",
            "edited_message": "edited_message.text",
            "reply_to_message": "message.reply_to_message.text",
            "message": "message.text",
        }
        if self.pointer in way:
            return data[way[self.pointer]]
            
class ReplyText(ParseMsg):
    def execute(self):
        data = flatten(self.data, "dot")
        if "message.reply_to_message.text" in data:
            return data["message.reply_to_message.text"]
        if "callback_query.message.reply_markup.inline_keyboard" in data:
            return data["callback_query.message.reply_markup.inline_keyboard"]

    
class CommandText(ParseMsg):
    def execute(self):
        for key, item in self.data.items():
            print(key, item, "CommandText")
            if key in self.pointer:
                return item
        if "#" in self.pointer:
            return "somethin"

class ChatKeyParse(ParseMsg):
    def execute(self):
        for key, item in self.data.items():
            if key == self.pointer:
                return item
        return "Чат не зареєстровано"

class ParseMsgFactory:
    @staticmethod
    def factory(cmd, data, pointer):
        commands = {
            "type": SearchType,
            "takechat" : TakeChat,
            "chatname": ChatKeyParse,
            "commandtext": CommandText,
            "taketext": TakeText,
            "replytext": ReplyText,
        }
        if cmd in commands:
            return commands[cmd](data, pointer).execute()
        

    # def entities(msg):
    #     """ Перевіряє, чи є в повідомленні команда бота. """
        
    #     for entity in  msg.get("entities", []):
    #         match entity.get("type"):
    #             case "bot_command":
    #                 return "bot_command"
    #             case "hashtag":
    #                 return "hashtag"
    #             case "mention":
    #                 return "mention"
    #     return "message"
    

    
   

      








