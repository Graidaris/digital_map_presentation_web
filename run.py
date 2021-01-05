from dmpw import app

app.run(debug=True)


# import os

# from flask import Flask, flash, request, redirect, url_for
# from markupsafe import escape
# import re

# from werkzeug.utils import secure_filename

# from dmpw.db_extractor.db_extractor import DB_Extractor

# app = Flask(__name__)

# UPLOAD_FOLDER = './dmpw/client/data_bases/'
# ALLOWED_EXTENSIONS = {'sqlite'}


# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# @app.route('/db/<dbname>')
# def show_user_profile(dbname):
#     us_db = DB_Extractor(dbname)
#     us_db.init_db()
#     us_db.extract_geometry_column_name()

#     names = ''
#     for colName in us_db.geometry_column_name:
#         names = f"{names}, {colName}"
        
#     characters_to_remove = '(),\''
#     pattern = f'[{characters_to_remove}]'
#     names = re.sub(pattern, "", names)
#     return f'COLUMN NAMES: {names}'



# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return f"File {filename} is uploded"
#             # return redirect(url_for('uploaded_file',
#             #                         filename=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''