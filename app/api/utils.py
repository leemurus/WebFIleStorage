import os
import uuid

from flask import current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from typing import Optional, Tuple

from app.models import File


class FileManager:
    @classmethod
    def allowed_filename(cls, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS')

    @classmethod
    def validate_file(cls, file: Optional[FileStorage]) -> Optional[Tuple[str, int]]:
        if not file:
            return 'File is missing', 400

        if file.filename == '':
            return 'File has incorrect name', 400

        if not cls.allowed_filename(file.filename):
            return 'File has not allowed type', 400

        return None

    @classmethod
    def validate_file_uuid(cls, file_uuid: Optional[str]) -> Optional[Tuple[str, int]]:
        if not file_uuid:
            return 'Field `file_uuid` is missing', 400

        file = File.query.filter_by(uuid=file_uuid).first()
        if not file:
            return f'File with `{file_uuid}` does not exist', 400

        if file and file.is_deleted:
            return f'File with `{file_uuid}` does not exist, because was removed', 400

        return None

    @classmethod
    def save_file(cls, file: Optional[FileStorage], check_file=False) -> Optional[str]:
        if check_file and cls.validate_file(file):
            return None

        filename = secure_filename(file.filename)
        file_uuid = uuid.uuid4().hex

        file_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], file_uuid[:2])
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)

        file.save(os.path.join(file_dir, file_uuid))
        File(
            uuid=file_uuid,
            owner=current_user,
            filename=filename
        ).commit_to_db()

        return file_uuid

    @classmethod
    def delete_file(cls, file_uuid, user_id: int, check_file_uuid=False) -> Optional[Tuple[str, int]]:
        if check_file_uuid:
            error = cls.validate_file_uuid(file_uuid)
            if error:
                return error

        file = File.query.filter_by(uuid=file_uuid).first()
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_uuid[:2], file_uuid)

        if file.owner_id != user_id:
            return 'You cannot delete the file because it does not belong to you', 400

        if os.path.exists(file_path):
            os.remove(file_path)
            file.is_deleted = True
            file.commit_to_db()
        else:
            return 'File does not exist in filesystem', 500

        return None
