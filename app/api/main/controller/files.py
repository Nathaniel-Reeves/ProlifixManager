from flask import (
    current_app as app
)
import os
import pathlib
from werkzeug.utils import secure_filename
import hashlib
from sqlalchemy import select, insert, update, delete
import model as db

def matchup_recursive(data, file_meta_key, file_meta_value, updates, finished):
    """Recursivly search through request data for each saved file_data to matchup the file_data to the request data"""
    if finished:
        return data, updates, finished
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "files":
                continue
            if key == "file_pointer" and value == file_meta_key:
                data["file_pointer"] = file_meta_value["file_pointer"]
                data["file_hash"] = file_meta_value["file_hash"]
                data["id_code"] = file_meta_value["id_code"]
                if "url_preview" in data.keys():
                    data.pop("url_preview")
                updates += 1
                return data, updates, True
            else:
                data[key], updates, finished = matchup_recursive(data[key], file_meta_key, file_meta_value, updates, finished)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i], updates, finished = matchup_recursive(item, file_meta_key, file_meta_value, updates, finished)
    return data, updates, finished

def matchup_saved_file_to_data(data):
    """Recursivly search through request data for each saved file_data to matchup the file_data to the request data"""
    for file_meta_key, file_meta_value in data["doc"]["files"].items():
        updates = 0
        data, updates, finished = matchup_recursive(data, file_meta_key, file_meta_value, updates, False)
        if updates < 1 or not finished:
            raise NameError("Could not update file.")
        if updates > 1:
            raise NameError("Too many file updates.  Should only have one, found: " + updates)
    data["doc"].pop("files")
    return data

def save_files(data, session):
    """Save files from form request while pairing file with database records.

    Args:
        data: dictionary
        session: database session

    Note: this function expects the following format for data:
    TODO: Finish Docstring
    {
        <key>: {}
        files: {

        }
    }
    """
    if 'doc' in data.keys():
        if "remove_files" in data["doc"].keys() and data['doc']['remove_files']:
            print(data['doc']['remove_files'])
            for remove_hash in data['doc']['remove_files']:
                remove_file(remove_hash, session)
        if "remove_files" in data["doc"].keys():
            data['doc'].pop("remove_files")
        if "files" in data["doc"].keys():
            if len(data["doc"]["files"]) > 0:
                save = {}
                for file in data["doc"]["files"].keys():
                    compare = ["file_obj", "filename", "type", "page", "id_code"]
                    keys = data["doc"]["files"][file].keys()
                    values = list(data["doc"]["files"][file].values())
                    if len(compare & keys) == 5 and all(values):
                        file_data = data["doc"]["files"][file]
                        file_hash, filename, pointer = save_file(file_data, session)
                        data["doc"]["files"][file].pop("file_obj")
                        save[file] = data["doc"]["files"][file].copy()
                        save[file]["filename"] = filename
                        save[file]["file_pointer"] = pointer
                        save[file]["file_hash"] = file_hash
                    else:
                        raise Exception("Missing File Information.")
                data["doc"]["files"] = save.copy()
                return matchup_saved_file_to_data(data)
    return data

def remove_file(file_hash, session):
    """Remove file from server if no more references exist, decrement ref counter
    Args:
        file_hash (string): Hash of file to remove
        session (Session): Database Session
    """
    # Check if File Exists in DB and increment ref count, Save if not
    stream = session.execute(
        select(db.Files).where(db.Files.file_hash == file_hash)
    )
    raw_data = stream.all()

    if len(raw_data) <= 0:
        raise ValueError("Invalid File Hash to Remove: " + file_hash)

    if (raw_data[0][0].to_dict()["ref_count"] > 1):
        stm = (
            update(db.Files)
            .where(db.Files.file_hash == file_hash)
            .values(ref_count=raw_data[0][0].to_dict()["ref_count"] - 1)
        )
        session.execute(stm)
        session.commit()
        return
    else:
        pointer = os.path.join(
            app.config['UPLOAD_FOLDER'], raw_data[0][0].to_dict()["file_pointer"]
        )
        os.remove(pointer)

        stm = (
            delete(db.Files)
            .where(db.Files.file_hash == file_hash)
        )
        session.execute(stm)
        session.commit()
        return

def save_file(file_data, session):
    """Save file to server filesystem and to Files database

    Args:
        file_data (Dict): _description_
        session (Session): _description_

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        Tuple: (file_hash, file_name, file_pointer)
    """

    # Get File Hash
    file_hash = md5_from_file(file_data["file_obj"])

    # Check if File Exists in DB and increment ref count, Save if not
    stream = session.execute(
        select(db.Files).where(db.Files.file_hash == file_hash)
    )
    raw_data = stream.all()

    # Save File to Filesystem

    # Create File Name
    fn = secure_filename(
        str(file_data["filename"]).replace(" ", "_").replace("/","-")
    )
    id_code = secure_filename(
        str(file_data["id_code"]).replace(" ", "_").replace("/","-")
    )
    page = secure_filename(
        str(file_data["page"]).replace(" ", "_").replace("/","-")
    )

    filename = f"║fn[{fn}]║id_code[{id_code}]║pg[{page}]║hash[{file_hash}]║"

    if file_data["file_obj"]["content_type"] == "application/pdf":
        filename += ".pdf"
    elif file_data["file_obj"]["content_type"] == "image/jpeg":
        filename += ".jpeg"
    elif file_data["file_obj"]["content_type"] == "image/png":
        filename += ".png"
    else:
        raise Exception("Invalid File Type")

    if len(raw_data) > 0:
        # Do not save the file to the filesystem if it already exists.
        # Increment Ref Counter
        stm = (
            update(db.Files)
            .where(db.Files.file_hash == file_hash)
            .values(ref_count=raw_data[0][0].to_dict()["ref_count"] + 1)
        )
        session.execute(stm)
        session.commit()
        return raw_data[0][0].get_id(), raw_data[0][0].file_name, raw_data[0][0].file_pointer

    # Create Directory if it doesn't already exist
    directory = os.path.join(
        app.config['UPLOAD_FOLDER'], file_data["type"]
    )

    pointer = os.path.join(file_data["type"], filename)

    pathlib.Path(
        directory
    ).mkdir(exist_ok=True, parents=True)

    path = os.path.join(
        directory, filename
    )

    # Save File
    with open(path, 'wb') as file:
        file.write(file_data["file_obj"]["content"])

    # Save File Info in DB
    stream = session.execute(
        insert(db.Files).returning(db.Files),
        {
            "file_hash": file_hash,
            "file_name": fn,
            "file_type": file_data["type"],
            "file_pointer": pointer,
            "id_code": file_data["id_code"],
            "pg": file_data["page"]
        }
    )
    raw_data = stream.all()
    new_file_id = raw_data[0][0].get_id()
    if new_file_id != file_hash:
        session.rollback()
        raise Exception("File Hash Mismatch")
    else:
        session.commit()

    return file_hash, filename, pointer

def md5_from_file(file, block_size=2**14):
    """Creates md5 Hash from file contents."""
    md5 = hashlib.md5()
    content_copy = file["content"][:]
    while True:
        data = content_copy[:block_size]
        if not data:
            break
        md5.update(data)
        content_copy = content_copy[block_size:]

    return md5.hexdigest()