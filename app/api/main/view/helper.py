import pathlib
import datetime
import time
import os
import shutil
import json
from flask import (
    current_app as app
)
from .response import (
    VariantType,
    FlashMessage,
    error_message
)
from werkzeug.utils import secure_filename

def collect_form_data(request):
    """
    Converts form data and file data into one dictionary.

    if files and 'doc' key in form data are present, it will store data as such:
      {
          ... (other form data with keys)
          "files": {
              "file_key": {
                  "file_obj": file_object
                  ... (other file data stored from doc key in form)
              }
          }
      }

    Args:
        request flask.Request: flask request object

    Returns:
        dict: all form elements with file data.
    """
    start = time.time()
    limit = start + 1
    while True:
        form_data = dict(request.form) # TODO: This occationally stalls the program
        now = time.time()
        if now > limit or form_data:
            break

    for key, value in form_data.items():
        if value == 'false':
            form_data[key] = False
            continue
        if value == 'true':
            form_data[key] = True
            continue
        if value == 'undefined' or value == 'null':
            form_data[key] = None
            continue
        if "." in value:
            try:
                form_data[key] = float(value)
                continue
            except ValueError:
                form_data[key] = str(value)
                continue
        else:
            try:
                form_data[key] = int(value)
                continue
            except ValueError:
                form_data[key] = str(value)
                continue

    file_data = request.files
    if "doc" in form_data.keys():
        doc = json.loads(form_data["doc"])

        if file_data and "files" in doc.keys():
            for file_key in file_data.keys():
                if file_key in doc["files"].keys():
                    file_obj ={
                        "filename": file_data[file_key].filename,
                        "content_type": file_data[file_key].content_type,
                        "content_length": file_data[file_key].content_length,
                        "content": file_data[file_key].read()
                    }
                    doc["files"][file_key]["file_obj"] = file_obj

        form_data["doc"] = doc
    return form_data

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
    """Check if the filename/extestion is allowed."""
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

    not_found = FlashMessage(
        message="No Files Uploaded",
        variant=VariantType.WARNING
    )

    # Check if uploads are empty
    if not doc or not file_objects:
        custom_response.insert_flash_message(not_found)
        return doc, custom_response

    try:
        new_doc = []
        for file_detail in doc:
            uploaded_files = [x.filename for x in file_objects.values()]
            if file_detail["filename"] not in uploaded_files:
                custom_response.insert_flash_message(not_found)
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

def validate_float_in_dict(dictionary, field, minimum=0, maximum=999999, equal_to=True):
    '''
    Validates that the value of a field in a dictionary
    is a float.
    '''
    if field not in dictionary:
        return False
    try:
        float(dictionary[field])
    except ValueError:
        return False
    if equal_to:
        if float(dictionary[field]) <= minimum:
            return False
        if float(dictionary[field]) >= maximum:
            return False
        return True
    if float(dictionary[field]) < minimum:
        return False
    if float(dictionary[field]) > maximum:
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

def check_type(valid_types, types_request, empty_means_all=True):
    """
    Checks if the types_request is a list of valid types.

    Args:
        valid_types (list): List if valid strings.
        types_request (list):Requested query in list of strings.
        empty_means_all (bool, optional): if all items in the valid list are selected, return an empty list if True, and the full list if False. Defaults to True.

    Returns:
        List
    """
    types = []
    for type in valid_types:
        if type in types_request:
            types.append(type)
    if empty_means_all and types == valid_types:  # Empty list means get all types
        types = []
    return types