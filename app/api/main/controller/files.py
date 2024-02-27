from flask import (
    current_app as app
)
import os
import pathlib
from werkzeug.utils import secure_filename
import hashlib
from sqlalchemy import select, insert, text
from view.response import (
    VariantType,
    FlashMessage,
    CustomResponse,
    error_message
)
import model as db

def matchup_recursive(data, file_meta_key, file_meta_value, updates, finished):
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
    for file_meta_key, file_meta_value in data["doc"]["files"].items():
        updates = 0
        data, updates, finished = matchup_recursive(data, file_meta_key, file_meta_value, updates, False)
        if updates < 1:
            raise NameError("Could not update file.")
        if updates > 1:
            raise NameError("Too many file updates.  Should only have one, found: " + updates)
    data["doc"].pop("files")
    return data

def save_files(data, session):
    if 'doc' in data.keys():
        if "files" in data["doc"].keys():
            pop_list = []
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

def save_file(file_data, session):
    
    # Get File Hash
    file_hash = md5_from_file(file_data["file_obj"])
    
    # Check if File Exists in DB, Save if not
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

    filename = f"fn[{fn}]║id_code[{id_code}]║pg[{page}]║hash[{file_hash}]║"
    
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
            "pg": file_data["page"],
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
    md5 = hashlib.md5()
    content_copy = file["content"][:]
    while True:
        data = content_copy[:block_size]
        if not data:
            break
        md5.update(data)
        content_copy = content_copy[block_size:]
        
    return md5.hexdigest()