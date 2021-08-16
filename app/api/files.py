import os

from flask import request, current_app, send_from_directory, jsonify
from flask_login import login_required, current_user
from typing import Optional, Tuple
from werkzeug.datastructures import FileStorage

from . import api
from .utils import FileManager


@api.route('/files', methods=['POST'])
@login_required
def upload_file():
    file: Optional[FileStorage] = request.files.get('file')

    error: Optional[Tuple[str, int]] = FileManager.validate_file(file)
    if error:
        return error

    file_uuid: str = FileManager.save_file(file)
    return jsonify(file_uuid)


@api.route('/files', methods=['DELETE'])
@login_required
def delete_file():
    file_uuid: Optional[str] = request.args.get('file_uuid')
    error: Optional[Tuple[str, int]] = FileManager.delete_file(
        file_uuid, current_user.id, check_file_uuid=True
    )
    if error:
        return error

    return 'File was deleted', 200


@api.route('/files', methods=['GET'])
def download_file():
    file_uuid: Optional[str] = request.args.get('file_uuid')
    error: Optional[Tuple[str, int]] = FileManager.validate_file_uuid(file_uuid)
    if error:
        return error

    return send_from_directory(
        directory=os.path.join(current_app.config['UPLOAD_FOLDER'], file_uuid[:2]),
        path=file_uuid
    )
