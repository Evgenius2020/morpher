import os
import pathlib
import shutil

from flask import Flask, request, flash, redirect, render_template, send_file
import uuid

from constants import Constants
from morphify import morphify

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[-1].lower() in Constants.IMAGE_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        input_files = request.files.getlist('input_files')
        stranger_files = request.files.getlist('stranger_files')
        if not input_files or not stranger_files:
            flash('Select files!', 'error')
            return redirect(request.url)
        user_uuid = uuid.uuid4()
        data_folder = os.path.join(UPLOAD_FOLDER, str(user_uuid))

        try:
            input_dir = os.path.join(data_folder, 'input')
            for input_file in input_files:
                pathlib.Path(input_dir).mkdir(parents=True, exist_ok=True)
                input_file.save(
                    os.path.join(input_dir, input_file.filename))

            stranger_dir = os.path.join(data_folder, 'stranger')
            for stranger_file in stranger_files:
                pathlib.Path(stranger_dir).mkdir(parents=True,
                                                 exist_ok=True)
                stranger_file.save(
                    os.path.join(stranger_dir, stranger_file.filename))

            output_dir = os.path.join(data_folder, 'output')
            morphify(input_dir, stranger_dir, output_dir)

            code = list(os.listdir(output_dir))[0]
            zip_path = os.path.join(output_dir, f'{code}')
            shutil.make_archive(zip_path, 'zip', zip_path)

            return send_file(f'{zip_path}.zip', as_attachment=True)
        finally:
            shutil.rmtree(data_folder)
    return \
        render_template('index.html',
                        mix_backgrounds=Constants.MIX_BACKGROUNDS,
                        accept_extensions=','.join(Constants.IMAGE_EXTENSIONS))
