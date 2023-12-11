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
import sys
import os


class MessageType(Enum):
    """
    Message Type Enum
    """
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"


class Message:
    """
    Message class
    """

    def __init__(
        self,
        alert_heading=None,
        message=None,
        message_detail=None,
        message_type=MessageType.PRIMARY,
        debug_code="0",
        link="",
    ):
        """
        :param alert_heading:
        :param message:
        :param message_detail:
        :param message_type:
        :param debug_code:
        :param link:
        """

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
        """
        :param message_type:
        :param debug_code:
        """

        if not isinstance(message_type, MessageType):
            raise ValueError("Invalid message type")
        self.message_type = message_type
        self.color = message_type.value
        self.set_icon(message_type)
        self.set_debug_code(debug_code)

    def set_debug_code(self, debug_code):
        """
        :param debug_code:
        """

        self.debug_code = debug_code

    def set_link(self, link):
        """
        :param link:
        """

        self.link = link

    def set_icon(self, message_type):
        """
        :param message_type:
        """

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
        """
        Returns a JSON representation of the message
        """

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
        """
        Returns a string representation of the message
        """

        return json.dumps(self.to_json())

    def __repr__(self):
        """
        Returns a string representation of the message
        """

        return self.__str__()

    def __dict__(self):
        """
        Returns a dictionary representation of the message
        """

        return self.to_json()

    def __hash__(self):
        """
        Returns a hash representation of the message
        """

        return hash(self.to_json())


class FlashMessage(Message):
    """
    FlashMessage class
    """

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
        """
        :param alert_heading:
        :param message:
        :param message_detail:
        :param message_type:
        :param debug_code:
        :param link:
        :param dismissible:
        :param count_down:
        """

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
        """
        Returns a JSON representation of the message
        """

        message_obj = super().to_json()
        message_obj["dismissible"] = self.dismissible
        message_obj["count_down"] = self.count_down
        return message_obj


class CustomResponse:
    """
    CustomResponse is a wrapper class for a JSON response.
    """

    def __init__(self, flash_messages=None, form_messages=None, data=None):
        """
        Args:
            flash_messages (list[FlashMessage]): List of flash messages.
            form_messages (dict[str, FormMessage]): Dictionary of form messages.
            data (list): List of data.
        """

        self.flash_messages = flash_messages or []
        self.form_messages = form_messages or {}
        self.json = data or []
        self.status_code = 200

    def insert_flash_message(self, flash_message):
        """
        Args:
            flash_message (FlashMessage): Flash message.
        """
        self.flash_messages.append(flash_message)

    def insert_flash_messages(self, flash_messages):
        """
        Args:
            flash_messages (list): List of FlashMessage Objects
        """
        self.flash_messages += flash_messages

    def insert_form_message(self, form_id, message):
        """
        Args:
            form_id (str): Form ID.
            message (FormMessage): Form message.
        """

        self.form_messages[form_id] = message

    def insert_form_messages(self, form_messages):
        """
        Args:
            form_messages (dict[str, FormMessage]): Dictionary of form messages.
        """

        self.form_messages.update(form_messages)

    def insert_data(self, data):
        """
        Args:
            data (list): Data.
        """
        self.json.append(data)

    def to_json(self):
        """
        Returns:
            dict: JSON response.
        """
        flash_messages = [message.to_json() for message in self.flash_messages]
        form_messages = {
            form_id: message.to_json() for form_id, message in self.form_messages.items()
            }
        return {
            "data": self.json,
            "messages": {
                "flash": flash_messages,
                "form": form_messages
            }
        }

    def set_status_code(self, status_code):
        """
        Sets the status code of the response.

        Args:
            status_code (int): status code.
        """
        self.status_code = status_code

    def get_status_code(self):
        """
        Gets Status Code

        Returns:
            int: status_code
        """
        return self.status_code

    def __str__(self):
        """
        Returns:
            str: JSON response.
        """
        return json.dumps(self.to_json())

    def __repr__(self):
        """
        Returns:
            str: JSON response.
        """
        return self.__str__()

    def __dict__(self):
        """
        Returns:
            dict: JSON response.
        """
        return self.to_json()


def error_message():
    """
    Creates an error flash message object.

    Args:
        None
    Returns:
        flash_message (FlashMessage)
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    dirname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[0]
    flash_message = FlashMessage(
        message=str(exc_obj),
        debug_code=(
            f"Error:{exc_type} -> Dir: {dirname} -> File: {fname} -> Line: {exc_tb.tb_lineno}"),
        message_type=MessageType.DANGER
    )
    return flash_message
