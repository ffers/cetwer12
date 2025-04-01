from .parse_text import ParseText
from flatten_dict import flatten
import re

class ParseMsg:
    def __init__(self, data, pointer):
        self.data = data
        self.pointer = pointer

    def execute(self):
        pass

class SearchType(ParseMsg):
    def execute(self):
        data = flatten(self.data, "dot")
        for handler in self.pointer:
            if handler in data:
                return handler
        return "unknown"

class TakeChat(ParseMsg):
    def execute(self):
        data = flatten(self.data, "dot")
        chat_way = {
            "callback_query.id": "callback_query.message.chat.id",
            "edited_message.text": "edited_message.chat.id",
            "message.text": "message.chat.id",
        }
        if self.pointer in chat_way:
            return data[chat_way[self.pointer]]
        
class TakeText(ParseMsg):
    def execute(self):
        data = flatten(self.data, "dot")
        way = {
            "callback_query.id": "callback_query.message.text",
            "edited_message.text": "edited_message.text",
            "reply_to_message": "message.reply_to_message.text",
            "message.text": "message.text",
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

class TakeAuthor(ParseMsg):
    def execute(self):
        data = flatten(self.data, "dot")
        print("TakeAuthor:", data)
        if "message.from.first_name" in data:
            return data["message.from.first_name"]
        if "message.from.username" in data:
            return data["message.from.username"]
        return "Невідомий"

    
class CommandText(ParseMsg):
    def execute(self):
        for key, item in self.data.items():
            if key in self.pointer:
                return item
        if re.search(r"\d{6,}", self.pointer):
            return "search_order"
        if "#" in self.pointer:
            return "unknown_command"
        return "just_message"

class ChatName(ParseMsg):
    def execute(self):
        for key, item in self.data.items():
            if key == self.pointer:
                return item
        return "unknown_chat"
    
class CheckType(ParseMsg):
    def execute(self):
        data = flatten(self.data, "dot")
        if "message.reply_to_message.text" in data:
            return "reply_to_message"
        if "callback_query.message.reply_markup.inline_keyboard" in data:
            return "callback_query"
        if "message.text" in data:
            return "message.text"

class ParseMsgFactory:
    @staticmethod
    def factory(cmd, data, pointer):
        commands = {
            "type": SearchType,
            "takechat" : TakeChat,
            "chatname": ChatName,
            "commandtext": CommandText,
            "taketext": TakeText,
            "replytext": ReplyText,
            "request": CheckType,
            "takeauthor": TakeAuthor
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
    

    
   

      








