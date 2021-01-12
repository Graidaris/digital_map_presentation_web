import os

from dmpw import app
from flask import render_template, request, flash, redirect, jsonify
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
        
    files_names = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return render_template("index.html",files_names=files_names)    


@app.route("/map/<filename>")
def map(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    dbext = DB_Extractor(db_path=filepath)
    dbext.init_db()
    dbext.extract_geometry_column_name()

    names = []
    for name in dbext.geometry_column_name:
        add_name = DB_Extractor.del_char(name)
        names.append(add_name)
            
    geo_linestrings, geo_poligons, geo_points = dbext.extract_geometry()

    return render_template("map.html",
                            filename=filename,
                            layers_names=names,
                            geo_statistic = dbext.geo_statistic
                            )

@app.route("/map")
def defoult_map():
    return render_template("map.html")

@app.route('/getGeometry', methods=['GET'])
def getGeometry():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'lab1.sqlite')
    dbext = DB_Extractor(db_path=filepath)
    dbext.init_db()
    dbext.extract_geometry_column_name()

    geo_linestrings, geo_poligons, geo_points = dbext.extract_geometry()
    return jsonify(
        geo_linestrings=geo_linestrings,
        geo_poligons=geo_poligons,
        geo_points=geo_points,
        geo_statistic=dbext.geo_statistic
    )
