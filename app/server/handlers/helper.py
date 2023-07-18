import pathlib
import datetime
import os
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
    Convets python list to python list
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
                        pathlib.Path(
                            app.config['UPLOAD_FOLDER'], location
                        ).mkdir(exist_ok=True, parents=True)

                    # Save file to directory
                    filename = secure_filename(file_detail["filename"])
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
