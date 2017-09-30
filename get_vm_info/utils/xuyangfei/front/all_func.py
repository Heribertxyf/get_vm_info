#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
from deal_message_v2 import read_csv, write_to_csv, post_request

app = Flask(__name__, template_folder='/home/xyf/data/program')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/sunny-bottom-view-of-high-tropical-palms-picjumbo-com.jpg')
def show_jpg():
    return send_from_directory(DOWNLOAD_ADDRESS, 'sunny-bottom-view-of-high-tropical-palms-picjumbo-com.jpg')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename_download = filename.rsplit('.', 1)[0] + '_CustomerMsg.csv'
            (customer_id, every) = read_csv(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            os.system('rm -f *.csv')
            final_message = post_request(customer_id)
            write_to_csv(filename_download, everyline, final_message)
            return redirect(url_for('download_file', filename_download=filename_download))
    return render_template('Untitled-1.html')


@app.route('/download/<filename_download>')
def download_file(filename_download):
    return render_template('download_page.html', filename_download=filename_download)


@app.route('/download/addr/<filename_download>')
def download_file_addr(filename_download):
    return send_from_directory(DOWNLOAD_ADDRESS, filename_download)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    UPLOAD_FOLDER = '/home/'
    DOWNLOAD_ADDRESS = './'
    filename_download = 'CustomerMsg.csv'
    ALLOWED_EXTENSIONS = set(['csv', 'jpg'])
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['DOWNLOAD_ADDRESS'] = DOWNLOAD_ADDRESS
    app.run(host='0.0.0.0')
