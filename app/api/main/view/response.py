import json
from enum import Enum
import sys
import os


class VariantType(Enum):
    """
    Variant Type Enum
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
        title=None,
        variant=VariantType.PRIMARY,
        debug_code="0",
        link=""
    ):
        """
        :param alert_heading:
        :param message:
        :param title:
        :param variant:
        :param debug_code:
        :param link:
        """

        self.alert_heading = alert_heading
        self.message = message
        self.title = title
        self.variant = variant
        self.icon = ""
        self.color = ""
        self.debug_code = debug_code
        self.link = link

        self.set_variant(variant, debug_code)

        # Require Title
        if not self.title:
            raise ValueError("Missing Title")

        # Require Message
        if not self.message:
            raise ValueError("Missing Message")

    def set_variant(self, variant, debug_code):
        """
        :param variant:
        :param debug_code:
        """

        if not isinstance(variant, VariantType):
            raise ValueError("Invalid message type")
        self.variant = variant
        self.color = variant.value
        self.set_icon(variant)
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

    def set_icon(self, variant):
        """
        :param variant:
        """

        if variant == VariantType.PRIMARY:
            self.icon = "star-fill"
        elif variant == VariantType.SECONDARY:
            self.icon = "search"
        elif variant == VariantType.SUCCESS:
            self.icon = "check-circle"
        elif variant == VariantType.DANGER:
            self.icon = "exclamation-octagon"
        elif variant == VariantType.WARNING:
            self.icon = "exclamation-triangle"
        elif variant == VariantType.INFO:
            self.icon = "info-circle"
        elif variant == VariantType.LIGHT:
            self.icon = "star-fill"
        elif variant == VariantType.DARK:
            self.icon = "star-fill"
        else:
            raise Exception("Unknown message type: " + str(variant))

    def to_json(self):
        """
        Returns a JSON representation of the message
        """

        # Require Title
        if not self.title:
            raise ValueError("Missing Title")

        # Require Message
        if not self.message:
            raise ValueError("Missing Message")

        return {
            "alert_heading": self.alert_heading,
            "message": self.message,
            "title": self.title,
            "variant": self.variant.value,
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
        title="",
        variant=VariantType.PRIMARY,
        debug_code="0",
        link="",
        auto_hide_delay=5000,
        no_auto_hide=False,
        no_close_button=False,
        visible=True
    ):
        """
        :param alert_heading: String (None)
        :param message: String (None)
        :param title: String ("")
        :param variant: VariantType (PRIMARY)
        :param debug_code: String ("")
        :param link: String ("")
        :param auto_hide_delay: Intager (5000ms)
        :param no_auto_hide: Boolean (False)
        :param no_close_button: Boolean (False)
        :param visible: Boolean (True)
        """

        super().__init__(
            alert_heading,
            message,
            title,
            variant,
            debug_code,
            link
        )
        self.auto_hide_delay = auto_hide_delay
        self.no_auto_hide = no_auto_hide
        self.no_close_button = no_close_button
        self.visible = visible

    def to_json(self):
        """
        Returns a JSON representation of the message
        """

        message_obj = super().to_json()

        # Require Title
        if not message_obj["title"]:
            raise ValueError("Missing Title")

        message_obj["auto_hide_delay"] = self.auto_hide_delay
        message_obj["no_auto_hide"] = self.no_auto_hide
        message_obj["no_close_button"] = self.no_close_button
        message_obj["visible"] = self.visible
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

    def get_data(self):
        """Returns the data."""
        return self.json

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

    def get_flash_messages(self):
        """Return Flash Messages"""
        return self.flash_messages

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
    msg = f"Error:{exc_type} -> Dir: {dirname} -> File: {fname} -> Line: {exc_tb.tb_lineno}"
    flash_message = FlashMessage(
        title=str(exc_type),
        message=msg,
        debug_code=(str(exc_obj) + str(exc_tb)),
        variant=VariantType.DANGER,
        no_auto_hide=True
    )
    return flash_message
