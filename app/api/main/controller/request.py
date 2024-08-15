from flask import (
    current_app as app
)
import os
import pathlib
from werkzeug.utils import secure_filename
import hashlib
from sqlalchemy import select, insert, update, delete, CursorResult
from sqlalchemy.sql import text
from base64 import b64decode
from view.response import (
    VariantType,
    FlashMessage,
    error_message,
    CustomResponse
)
import model as db
from model.connector import get_session

import json

class CustomRequest:

    def __init__(self, request):
        self.request = request
        self.custom_response = CustomResponse()
        self.error = False
        self.saved_files = {}
        self.session = None
        self.temp_key_lookup = {}
        self.custom_upsert = False
        self.custom_delete = False
        self.valid_tables = (
            'Organizations',
            'Processes',
            'Components',
            'Facilities',
            'Organization_Names',
            'People',
            'Product_Master',
            'Product_Variant',
            'Purchase_Orders',
            'Sales_Orders',
            'Equipment',
            'Component_Names',
            'Users',
            'Formula_Master',
            'Item_id',
            'Manufacturing_Process',
            'Purchase_Order_Detail',
            'Sale_Order_Detail',
            'Sales_Orders_Payments',
            'Inventory',
            'Formula_Detail',
            'Manufacturing_Process_Edges',
            'Process_Components',
            'Lot_Numbers',
            'Inventory_Log',
            'Ingredient_Brands_Join',
            'Ingredients_Join',
            'Component_Brands_Join',
            'Components_Join',
            'Inventory_Log_Edges'
        )

        # print("Payload", json.dumps(self.request.json['payload'], indent=4))

    def get_response(self):
        return self.custom_response

    def handle_request(self):
        self.error = not self._get_session()
        if self.error:
            return

        if not self.error:
            self.error = not self.validate_request_data()
        print("validate request data:", self.error)

        # if self.custom_upsert:
        #     print(self.request.json['upsert_order'])
        # if self.custom_delete:
        #     print(self.request.json['delete_order'])

        if not self.error:
            self.error = not self.delete_files()
        print('delete files:', self.error)

        if not self.error:
            self.error = not self.save_files()
        print('save files:', self.error)

        if not self.error:
            self.error = not self.process_upserts()
        print('process upserts:', self.error)

        if not self.error:
            self.error = not self.process_deletes()
        print('process deletes:', self.error)

        self.finish_transaction()
        self.close_session()
        return

    def finish_transaction(self):
        if self.error:
            self.session.rollback()
            for file in self.saved_files.values():
                self._remove_file_from_filesystem(file["file_pointer"])
            self.custom_response.insert_data({
                "saved_files": self.saved_files,
                "temp_key_lookup": self.temp_key_lookup
            })
            self.custom_response.insert_flash_message(
                FlashMessage(
                    variant=VariantType.DANGER,
                    title="Failure!",
                    message="Failed to Save."
                )
            )
        else:
            self.session.commit()
            self.custom_response.insert_data({
                "saved_files": self.saved_files,
                "temp_key_lookup": self.temp_key_lookup
            })
            self.custom_response.insert_flash_message(
                FlashMessage(
                    variant=VariantType.SUCCESS,
                    title="Success!",
                    message="Saved successfully."
                )
            )
            self.custom_response.set_status_code(201)

    def close_session(self):
        self.session.close()

    def process_upserts(self):
        upserts = self.request.json['payload']['upsert']
        if self.custom_upsert:
            tables = self.request.json['upsert_order']
        else:
            tables = self.valid_tables
        flag = True
        for table in tables:
            if table in upserts.keys():
                for record in upserts[table]:
                    flag = self._upsert_record(table, record)
                    if not flag:

                        return flag
        return flag

    def _upsert_record(self, table_name, record):
        temp_key = None
        # Validate the correct columns are used
        table = getattr(db, table_name)
        table_columns = table.__table__.columns.keys()
        pk_col = table().get_id_name()
        if isinstance(pk_col, tuple):
            # TODO: Right now, this only removes single pk columns.
            # TODO: Need to add support for composite pks.
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Not Implemented",
                message=f'Composite keys not implememted yet (upsert).'
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            return False

        for key in record.keys():
            if key not in table_columns:
                flash_message = FlashMessage(
                    variant=VariantType.DANGER,
                    title="Invalid Request!",
                    message=f'{key} is not a valid column for {table_name}.'
                )
                self.custom_response.insert_flash_message(flash_message)
                self.custom_response.set_status_code(400)
                return False
            if isinstance(record[key], str) and "temp-" in record[key]:
                temp_key = record[key]
                if temp_key in self.temp_key_lookup.keys() and not (self.temp_key_lookup[temp_key] == {}):
                    record[key] = self.temp_key_lookup[temp_key]['new_id']
                else:
                    self.temp_key_lookup[temp_key] = {}

        if pk_col in record.keys():
            if isinstance(record[pk_col], int):
                if 'date_entered' in record.keys():
                    record.pop('date_entered')
                if 'date_modified' in record.keys():
                    record.pop('date_modified')
                stm = update(table).values(record).where(getattr(table, pk_col) == record[pk_col])
            elif isinstance(record[pk_col], str) and "temp-" in record[pk_col]:
                temp_key = record.pop(pk_col)
                stm = insert(table).values(record)
            else:
                flash_message = FlashMessage(
                    variant=VariantType.DANGER,
                    title="Invalid Request!",
                    message=f'{pk_col} is a invalid value for {table}.  PK col = {record[pk_col]}.'
                )
                self.custom_response.insert_flash_message(flash_message)
                self.custom_response.set_status_code(400)
                return False
        else:
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message=f'{pk_col} is missing from the upsert request for {table}.'
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            return False

        new_id, outcome = self._execute_query(stm)
        if new_id and temp_key:
            data = { 'table_name': table_name, 'new_id' : new_id, 'pk' : pk_col, 'temp_key': temp_key }
            self.temp_key_lookup[temp_key] = data
        return outcome

    def process_deletes(self):
        deletes = self.request.json['payload']['delete']
        if self.custom_delete:
            tables = self.request.json['delete_order']
        else:
            tables = list(self.valid_tables)
            tables.reverse()
        flag = True
        for table in tables:
            if table in deletes.keys():
                for record in deletes[table]:
                    flag = self._delete_record(table, record)
                    if not flag:
                        return flag
        return flag

    def _delete_record(self, table, record):
        # Validate the correct columns are used
        table_columns = getattr(db, table).__table__.columns.keys()
        if not isinstance(record, dict):
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message=f'Invalid record for {table}.'
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            return False
        for key in record.keys():
            if key not in table_columns:
                flash_message = FlashMessage(
                    variant=VariantType.DANGER,
                    title="Invalid Request!",
                    message=f'{key} is not a valid column for {table}.'
                )
                self.custom_response.insert_flash_message(flash_message)
                self.custom_response.set_status_code(400)
                return False

        table = getattr(db, table)
        pk_col = table().get_id_name()
        if isinstance(pk_col, tuple):
            # TODO: Right now, this only removes single pk columns.
            # TODO: Need to add support for composite pks.
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Not Implemented",
                message=f'Composite keys not implememted yet (upsert).'
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            return False

        # Validate the pk column exists in record
        if pk_col in record.keys() and isinstance(record[pk_col], int):
            stm = delete(table).where(getattr(table, pk_col) == record[pk_col])
        else:
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message=f'{pk_col} is missing from the delete request for {table}.'
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            return False

        id, outcome = self._execute_query(stm)
        return outcome

    def validate_request_data(self):
        """
        Validate request data
        """
        flag = True
        if not 'payload' in self.request.json:
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message="Payload is missing."
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            flag = False

        if not 'upsert' in self.request.json['payload']:
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message="Upsert is missing."
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            flag = False

        for table in self.request.json['payload']['upsert']:
            if table not in self.valid_tables:
                flash_message = FlashMessage(
                    variant=VariantType.DANGER,
                    title="Invalid Request!",
                    message=f'{table} is not a valid table.'
                )
                self.custom_response.insert_flash_message(flash_message)
                self.custom_response.set_status_code(400)
                flag = False

        if not 'delete' in self.request.json['payload']:
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message="Delete is missing."
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            flag = False

        for table in self.request.json['payload']['delete']:
            if table not in self.valid_tables:
                flash_message = FlashMessage(
                    variant=VariantType.DANGER,
                    title="Invalid Request!",
                    message=f'{table} is not a valid table.'
                )
                self.custom_response.insert_flash_message(flash_message)
                self.custom_response.set_status_code(400)
                flag = False

        if not 'upsert_file_data' in self.request.json:
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message="Upsert file data is missing."
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            flag = False

        if not 'delete_file_data' in self.request.json:
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message="Delete file data is missing."
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            flag = False

        if len(self.request.json['payload']['upsert']) == 0 and len(self.request.json['payload']['delete']) == 0:
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message="No data to upsert or delete."
            )
            self.custom_response.insert_flash_message(flash_message)
            self.custom_response.set_status_code(400)
            flag = False

        # Custom Upsert Order
        if (self.request.json['upsert_order']):
            self.custom_upsert = True
            for table in self.request.json['upsert_order']:
                if table not in self.valid_tables:
                    flash_message = FlashMessage(
                        variant=VariantType.DANGER,
                        title="Invalid Request!",
                        message=f'{table} is not a valid table.'
                    )
                    self.custom_response.insert_flash_message(flash_message)
                    self.custom_response.set_status_code(400)
                    flag = False

        # Custom Delete Order
        if (self.request.json['delete_order']):
            self.custom_delete = True
            for table in self.request.json['delete_order']:
                if table not in self.valid_tables:
                    flash_message = FlashMessage(
                        variant=VariantType.DANGER,
                        title="Invalid Request!",
                        message=f'{table} is not a valid table.'
                    )
                    self.custom_response.insert_flash_message(flash_message)
                    self.custom_response.set_status_code(400)
                    flag = False

        return flag

    def save_files(self):
        """
        Save Files
        """
        # Convert files from base 64 into file objects
        for file_key, file_data in self.request.json['upsert_file_data'].items():
            header, encoded = file_data["data_uri"].split("base64,", 1)
            file_data["file_obj"] = b64decode(encoded)

        if len(self.request.json['upsert_file_data']) > 0:
            for file_key, file_data in self.request.json['upsert_file_data'].items():

                valid_file_data_keys = ["filename", "filetype", "dir", "page", "size", "id_code", "data_uri", "ref_count"]
                file_data_keys = file_data.keys()
                file_data_values = list(file_data.values())

                # check ref_count is number
                if not isinstance(file_data['ref_count'], int):
                    flash_message = FlashMessage(
                        variant=VariantType.DANGER,
                        title="Saving Files Failure!",
                        message="ref_count is not a number."
                    )
                    self.custom_response.insert_flash_message(flash_message)
                    self.custom_response.set_status_code(400)
                    return False

                # check ref_count is greater than zero
                if file_data['ref_count'] < 1:
                    flash_message = FlashMessage(
                        variant=VariantType.DANGER,
                        title="Saving Files Failure!",
                        message="ref_count must be greater than zero."
                    )
                    self.custom_response.insert_flash_message(flash_message)
                    self.custom_response.set_status_code(400)
                    return False

                # Catch invalid file data
                if len(valid_file_data_keys & file_data_keys) != 8 or not all(file_data_values):
                    flash_message = FlashMessage(
                        variant=VariantType.DANGER,
                        title="Saving Files Failure!",
                        message="Invalid File Meta Data."
                    )
                    self.custom_response.insert_flash_message(flash_message)
                    self.custom_response.set_status_code(400)
                    return False

                file_hash, filename, pointer = self._save_file(file_data)
                file_data.pop("file_obj")
                file_data.pop("data_uri")
                self.saved_files[file_key] = file_data.copy()
                self.saved_files[file_key]["filename"] = filename
                self.saved_files[file_key]["file_pointer"] = pointer
                self.saved_files[file_key]["file_hash"] = file_hash
                self.saved_files[file_key]["ref_count"] = file_data['ref_count']
                self.saved_files[file_key]["temp_id"] = file_key

        return self._matchup_saved_files()

    def delete_files(self):
        try:
            for remove_hash in self.request.json['delete_file_data']:
                self._remove_file(remove_hash)
            return True
        except Exception:
            error = error_message()
            self.custom_response.insert_flash_message(error)
            self.custom_response.set_status_code(400)
            return False

    def _matchup_saved_files(self):
        """Recursively search through request
        data for each saved file_data to
        matchup the file_data to the request data."""

        data = self.request.json["payload"]["upsert"].copy()
        for file_meta_key, file_meta_value in self.saved_files.items():
            updates = 0
            data, updates, finished = self._matchup_recursive(data, file_meta_key, file_meta_value, updates, False)

            if updates != file_meta_value['ref_count'] or not finished:
                flash_message = FlashMessage(
                    variant=VariantType.DANGER,
                    title="File Matchup Failure!",
                    message=f"Could not update file. finished={finished}, updates={updates}, ref_count={file_meta_value['ref_count']}"
                )
                self.custom_response.insert_flash_message(flash_message)
                self.custom_response.set_status_code(400)
                return False

        self.request.json["payload"]["upsert"] = data
        return True

    def _matchup_recursive(self, data, file_meta_key, file_meta_value, updates, finished):
        """Recursively search through request
        data for each saved file_data to
        matchup the file_data to the request data."""

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
                    data["temp_key"] = file_meta_key
                    if "url_preview" in data.keys():
                        data.pop("url_preview")
                    updates += 1

                    finished = False
                    if updates == file_meta_value['ref_count']:
                        finished = True
                    return data, updates, finished
                else:
                    data[key], updates, finished = self._matchup_recursive(data[key], file_meta_key, file_meta_value, updates, finished)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                data[i], updates, finished = self._matchup_recursive(item, file_meta_key, file_meta_value, updates, finished)
        return data, updates, finished

    def _remove_file(self, file_hash):
        """Remove file from server if no more references exist, decrement ref counter
        Args:
            file_hash (string): Hash of file to remove
            session (Session): Database Session
        """
        # Check if File Exists in DB and decrement ref count, Delete if 0 references
        stream = self.session.execute(
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
            self.session.execute(stm)
            return
        else:
            self._remove_file_from_filesystem(raw_data[0][0].to_dict()["file_pointer"])

            stm = (
                delete(db.Files)
                .where(db.Files.file_hash == file_hash)
            )
            self.session.execute(stm)
            return

    def _remove_file_from_filesystem(self, path):
        pointer = os.path.join(
            app.config['UPLOAD_FOLDER'], path
        )
        os.remove(pointer)

    def _save_file(self, file_data):
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
        file_hash = self.md5_from_file(file_data["file_obj"])

        # Check if File Exists in DB and increment ref count, Save if not
        stream = self.session.execute(
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

        if file_data["filetype"] == "application/pdf":
            filename += ".pdf"
        elif file_data["filetype"] == "image/jpeg":
            filename += ".jpeg"
        elif file_data["filetype"] == "image/png":
            filename += ".png"
        else:
            raise Exception("Invalid File Type")

        if len(raw_data) > 0:
            # Do not save the file to the filesystem if it already exists.
            # Increment Ref Counter
            stm = (
                update(db.Files)
                .where(db.Files.file_hash == file_hash)
                .values(ref_count=raw_data[0][0].to_dict()["ref_count"] + file_data["ref_count"])
            )
            self.session.execute(stm)
            return raw_data[0][0].get_id(), raw_data[0][0].file_name, raw_data[0][0].file_pointer

        # Create Directory if it doesn't already exist
        directory = os.path.join(
            app.config['UPLOAD_FOLDER'], file_data["dir"]
        )

        pointer = os.path.join(file_data["dir"], filename)

        pathlib.Path(
            directory
        ).mkdir(exist_ok=True, parents=True)

        path = os.path.join(
            directory, filename
        )

        # Save File
        with open(path, 'wb') as file:
            file.write(file_data["file_obj"])

        # Save File Info in DB
        stream = self.session.execute(
            insert(db.Files).returning(db.Files),
            {
                "file_hash": file_hash,
                "file_name": fn,
                "file_type": file_data["filetype"],
                "file_pointer": pointer,
                "id_code": file_data["id_code"],
                "pg": file_data["page"],
                "ref_count": file_data["ref_count"]
            }
        )
        raw_data = stream.all()
        new_file_id = raw_data[0][0].get_id()
        if new_file_id != file_hash:
            self.session.rollback()
            raise Exception("File Hash Mismatch")

        return file_hash, filename, pointer

    def md5_from_file(self, file, block_size=2**14):
        """Creates md5 Hash from file contents."""
        md5 = hashlib.md5()
        content_copy = file[:]
        while True:
            data = content_copy[:block_size]
            if not data:
                break
            md5.update(data)
            content_copy = content_copy[block_size:]

        return md5.hexdigest()

    def _get_session(self):
        # Connect to the database
        try:
            self.session = get_session()
            return True
        except Exception:
            error = error_message()
            self.custom_response.insert_flash_message(error)
            self.custom_response.set_status_code(500)
            return False

    def _execute_query(self, stm):
        record_id = None
        # Execute the query
        try:
            stream = self.session.execute(stm)
            if stream.is_insert:
                record_id = stream.inserted_primary_key[0]
        except Exception:
            error = error_message()
            # print("Error: ", error)
            # print(stm)
            self.custom_response.insert_flash_message(error)
            self.custom_response.set_status_code(400)
            return None, False

        return record_id, True

def check_organization_levenshtein(request):
    custom_response = CustomResponse()

    data = request.json

    # Connect to the database
    try:
        session = get_session()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
        return custom_response

    for name_obj in data:
        # Validate Request Data
        if 'organization_name' not in name_obj.keys() or 'organization_initial' not in name_obj.keys():
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message="organization_name or organization_initial is missing."
            )
            custom_response.insert_flash_message(flash_message)
            custom_response.set_status_code(400)
            session.close()
            return custom_response

        # Build Query
        org_name = str(name_obj['organization_name']).strip()
        org_initial = str(name_obj['organization_initial']).strip()
        name_obj['similar_names'] = []

        stm = text(f"""
            SELECT
                `organization_id`,
                `organization_name`,
                `organization_initial`,
                sys.LEVENSHTEIN_RATIO(`organization_name`, '{org_name}') AS duplicate_probability_score_name,
                sys.LEVENSHTEIN_RATIO(`organization_initial`, '{org_initial}') AS duplicate_probability_score_initial
            FROM `Organizations`.`Organization_Names`
            WHERE
                sys.LEVENSHTEIN_RATIO(`organization_name`, '{org_name}') > 50 OR
                sys.LEVENSHTEIN_RATIO(`organization_initial`, '{org_initial}') > 50
            ORDER BY
                duplicate_probability_score_name DESC,
                duplicate_probability_score_initial DESC;""")

        # Execute the query
        raw_data = {}
        try:
            raw_data = session.execute(stm).all()
        except Exception:
            error = error_message()
            custom_response.insert_flash_message(error)
            custom_response.set_status_code(400)
            session.close()
            return custom_response
        for row in raw_data:
            d = {
                'organization_id': int(row[0]),
                'organization_name': row[1],
                'organization_initial': row[2],
                'duplicate_probability_score_name': int(row[3]),
                'duplicate_probability_score_initial': int(row[4])
            }
            name_obj['similar_names'].append(d)
        custom_response.insert_data(name_obj)

    session.close()
    custom_response.set_status_code(200)
    return custom_response


def check_component_levenshtein(request):
    custom_response = CustomResponse()

    data = request.json

    # Connect to the database
    try:
        session = get_session()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
        return custom_response

    for name_obj in data:
        # Validate Request Data
        if 'component_name' not in name_obj.keys():
            flash_message = FlashMessage(
                variant=VariantType.DANGER,
                title="Invalid Request!",
                message="component_name is missing."
            )
            custom_response.insert_flash_message(flash_message)
            custom_response.set_status_code(400)
            session.close()
            return custom_response

        # Build Query
        component_name = str(name_obj['component_name']).strip()
        name_obj['similar_names'] = []

        stm = text(f"""
            SELECT
                JSON_ARRAYAGG(JSON_OBJECT(
                    'component_id', a.`component_id`,
                    'component_name', a.`component_name`,
                    'duplicate_probability_score_name', sys.LEVENSHTEIN_RATIO(a.`component_name`, '{component_name}'),
                    'component_names', (
                        SELECT JSON_ARRAYAGG(JSON_OBJECT(
                            'name_id', `name_id`,
                            'component_id', `component_id`,
                            'component_name', `component_name`,
                            'primary_name', `primary_name`,
                            'botanical_name', `botanical_name`
                        ))
                        FROM `Inventory`.`Component_Names`
                        WHERE `component_id` = a.`component_id`
                    ),
                    'certified_usda_organic', b.`certified_usda_organic`,
                    'certified_halal', b.`certified_halal`,
                    'certified_kosher', b.`certified_kosher`,
                    'certified_gluten_free', b.`certified_gluten_free`,
                    'certified_national_sanitation_foundation', b.`certified_national_sanitation_foundation`,
                    'certified_us_pharmacopeia', b.`certified_us_pharmacopeia`,
                    'certified_non_gmo', b.`certified_non_gmo`,
                    'certified_vegan', b.`certified_vegan`,
                    'certified_fda', b.`certified_fda`,
                    'certified_wildcrafted', b.`certified_wildcrafted`,
                    'certified_made_with_organic', b.`certified_made_with_organic`,
                    'certified_gmp', b.`certified_gmp`
                )) AS similar_names,
                sys.LEVENSHTEIN_RATIO(a.`component_name`, '{component_name}') AS duplicate_probability_score_name
            FROM `Inventory`.`Component_Names` a
            JOIN `Inventory`.`Components` b ON
                a.`component_id` = b.`component_id`
            WHERE
                sys.LEVENSHTEIN_RATIO(`component_name`, '{component_name}') > 50
            ORDER BY
                duplicate_probability_score_name DESC;""")

        # Execute the query
        raw_data = {}
        try:
            raw_data = session.execute(stm).all()
        except Exception:
            error = error_message()
            custom_response.insert_flash_message(error)
            custom_response.set_status_code(400)
            session.close()
            return custom_response
        data = raw_data[0][0] if raw_data[0][0] else "[]"
        name_obj['similar_names'] = json.loads(data)
        custom_response.insert_data(name_obj)

    session.close()
    custom_response.set_status_code(200)
    return custom_response