import os
from flask_restful import Resource
from flask import request, redirect, send_from_directory
from flask import current_app as app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Files(Resource):
    def post(self):
        # check if the post request has the file part
        if 'files' not in request.files:
            print('Files.post - Error: No file part')
            return {
                'error': 'No file'
            }, 400

        file = request.files['files']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('Files.post - Error: No selected file')
            return {
                'error': 'No selected file'
            }, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            filePath = os.getcwd() + '/code/' + app.config['UPLOAD_FOLDER'] + filename
            file.save(filePath)

            print('Files.post - File Uploaded: {}'.format(filename))
            return {
                'data': [
                    filename
                ]
            }, 200

        print('Files.post - Error: No File Received')
        return {
            'error': 'No file received'
        }, 400


class File(Resource):
    def get(self, filename):
        print('File.get - File Requested: {}'.format(filename))
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
