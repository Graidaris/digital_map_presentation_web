import os
import re

from dmpw import app
from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename

from .db_extractor.db_extractor import DB_Extractor

ALLOWED_EXTENSIONS = {'sqlite'}



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(f'/map/{filename}')
        
    return render_template("index.html")    


@app.route("/map/<filename>")
def map(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    dbext = DB_Extractor(db_path=filepath)
    dbext.init_db()
    dbext.extract_geometry_column_name()

    characters_to_remove = '(),\''
    pattern = f'[{characters_to_remove}]'

    names = []
    for name in dbext.geometry_column_name:
        add_name = re.sub(pattern, "", str(name))
        names.append(add_name)

    return render_template("dig_map.html", layers_names=names)

@app.route("/map")
def defoult_map():
    return render_template("dig_map.html")