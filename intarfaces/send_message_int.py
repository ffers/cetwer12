from abc import ABC, abstractmethod

class MessagingInterface(ABC):
    @abstractmethod
    def send_message(self, recipient, message):
        pass