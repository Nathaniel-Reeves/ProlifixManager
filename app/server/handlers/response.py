"""
{
    "data": [],
    "messages": {
        "flash": [
            {
                "message": "",
                "message_detail": "",
                "message_type": "",
                "debug_code": "",
                "color": "",
                "icon": "",
                "link": "",
                "dismissible": 1,
                "count_down": 0,
            }
        ],
        "form": {
            "[input_id]": {
                "message": "",
                "message_detail": "",
                "message_type": "",
                "debug_code": "",
                "color": "",
                "icon": "",
                "link": ""
            }
        }
    }
}
"""

import json
from enum import Enum


class MessageType(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"


class Message:
    def __init__(
        self,
        alert_heading=None,
        message=None,
        message_detail=None,
        message_type=MessageType.PRIMARY,
        debug_code="0",
        link="",
    ):
        self.alert_heading = alert_heading
        self.message = message
        self.message_detail = message_detail
        self.message_type = message_type
        self.icon = ""
        self.color = ""
        self.debug_code = debug_code
        self.link = link

        self.set_message_type(message_type, debug_code)

    def set_message_type(self, message_type, debug_code):
        if not isinstance(message_type, MessageType):
            raise ValueError("Invalid message type")
        self.message_type = message_type
        self.color = message_type.value
        self.set_icon(message_type)
        self.set_debug_code(debug_code)

    def set_debug_code(self, debug_code):
        self.debug_code = debug_code

    def set_link(self, link):
        self.link = link

    def set_icon(self, message_type):
        if message_type == MessageType.PRIMARY:
            self.icon = "star-fill"
        elif message_type == MessageType.SECONDARY:
            self.icon = "search"
        elif message_type == MessageType.SUCCESS:
            self.icon = "check-circle"
        elif message_type == MessageType.DANGER:
            self.icon = "exclamation-octagon"
        elif message_type == MessageType.WARNING:
            self.icon = "exclamation-triangle"
        elif message_type == MessageType.INFO:
            self.icon = "info-circle"
        elif message_type == MessageType.LIGHT:
            self.icon = "star-fill"
        elif message_type == MessageType.DARK:
            self.icon = "star-fill"
        else:
            raise Exception("Unknown message type: " + str(message_type))

    def to_json(self):
        return {
            "alert_heading": self.alert_heading,
            "message": self.message,
            "message_detail": self.message_detail,
            "message_type": self.message_type.value,
            "icon": self.icon,
            "color": self.color,
            "debug_code": self.debug_code,
            "link": self.link
        }

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def __dict__(self):
        return self.to_json()

    def __hash__(self):
        return hash(self.to_json())


class FlashMessage(Message):
    def __init__(
        self,
        alert_heading=None,
        message=None,
        message_detail=None,
        message_type=MessageType.PRIMARY,
        debug_code="0",
        link="",
        dismissible=True,
        count_down=0
    ):
        super().__init__(
            alert_heading,
            message,
            message_detail,
            message_type,
            debug_code,
            link
        )
        self.dismissible = dismissible
        self.count_down = count_down

    def to_json(self):
        message_obj = super().to_json()
        message_obj["dismissible"] = self.dismissible
        message_obj["count_down"] = self.count_down
        return message_obj


class CustomResponse:
    def __init__(self, flash_messages=None, form_messages=None, data=None):
        self.flash_messages = flash_messages or []
        self.form_messages = form_messages or {}
        self.data = data or []

    def insert_flash_message(self, flash_message):
        self.flash_messages.append(flash_message)

    def insert_form_message(self, form_id, message):
        self.form_messages[form_id] = message

    def insert_data(self, data):
        self.data.append(data)

    def to_json(self):
        flash_messages = [message.to_json() for message in self.flash_messages]
        form_messages = {form_id: message.to_json() for form_id, message in self.form_messages.items()}
        return {
            "data": self.data,
            "messages": {
                "flash": flash_messages,
                "form": form_messages
            }
        }

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def __dict__(self):
        return self.to_json()