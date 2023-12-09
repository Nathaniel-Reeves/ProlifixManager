import pathlib
import datetime
import os
import shutil
from flask import (
    current_app as app
)
from .response import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message
)
from werkzeug.utils import secure_filename

def only_integers(iterable):
    '''
    Converts python list to python list
    of integer values.
    '''
    for item in iterable:
        try:
            yield int(item)
        except ValueError:
            pass

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


def save_files(doc, file_objects, custom_response, location=""):
    """
    Saves files to the specified directory.

    Parameters:
        doc (list): List of files to save.
        file_objects (dict): Dictionary of file objects.
        custom_response (CustomResponse): CustomResponse object.
        location (str): Location to save files. Default is "".

    Returns:
        doc (list): List of files to save.
        custom_response (CustomResponse): CustomResponse object.
    """

    NOT_FOUND = FlashMessage(
        message="No Files Uploaded",
        message_type=MessageType.WARNING
    )

    # Check if uploads are empty
    if not doc or not file_objects:
        custom_response.insert_flash_message(NOT_FOUND)
        return doc, custom_response

    else:
        try:
            new_doc = []
            for file_detail in doc:
                uploaded_files = [x.filename for x in file_objects.values()]
                if file_detail["filename"] not in uploaded_files:
                    custom_response.insert_flash_message(NOT_FOUND)
                else:
                    # Create Directory if it doesn't already exist
                    if location != "":
                        directory = os.path.join(
                            app.config['UPLOAD_FOLDER'], location
                        )
                        pathlib.Path(
                            directory
                        ).mkdir(exist_ok=True, parents=True)

                    # Save file to directory
                    filename = secure_filename(
                                    file_detail["filename"]
                                )

                    file_objects[file_detail["id"]].save(
                        os.path.join(
                            app.config['UPLOAD_FOLDER'], location, filename
                        )
                    )

                    # Update and return doc
                    file_detail["date_uploaded"] = str(
                        datetime.datetime.utcnow())
                    file_detail["link"] = os.path.join(location, filename)
                    file_detail.pop("id")
                    new_doc.append(file_detail)

            return new_doc, custom_response

        except Exception:
            error = error_message()
            custom_response.insert_flash_message(error)
            return doc, custom_response


def delete_directory(location, custom_response, flash_message=None):
    """
    Deletes specified directory recursively.

    Parameters:
        location (str): Location to delete.
        flash_message (FlashMessage): FlashMessage object.
        custom_response (CustomResponse): CustomResponse object.

    Returns:
        custom_response (CustomResponse): CustomResponse object.
    """

    try:
        # Delete Files
        shutil.rmtree(
            os.path.join(
                app.config['UPLOAD_FOLDER'], location
            )
        )
        if isinstance(flash_message, FlashMessage):
            custom_response.insert_flash_message(flash_message)

        return True, custom_response
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response

def validate_float_in_dict(dict, field, min=0, max=999999, equal_to=True):
    '''
    Validates that the value of a field in a dictionary
    is a float.
    '''
    if field not in dict:
        return False
    try:
        float(dict[field])
    except ValueError:
        return False
    if equal_to:
        if float(dict[field]) <= min:
            return False
        if float(dict[field]) >= max:
            return False
        return True
    if float(dict[field]) < min:
        return False
    if float(dict[field]) > max:
        return False
    return True


def validate_int_in_dict(dict, field, min_v=0, max_v=99999999999, equal_to=True):
    '''
    Validates that the value of a field in a dictionary
    is a int.
    '''
    if field not in dict:
        return False
    if isinstance(dict[field], int):
        if equal_to:
            if int(dict[field]) >= min_v and \
            int(dict[field]) < max_v:
                return True
            return False
        if int(dict[field]) > min_v and \
            int(dict[field]) < max_v:
            return True
        return False
    return False
