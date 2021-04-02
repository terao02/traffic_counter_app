import os
import glob

from flask import Flask, render_template, request, redirect, url_for
from flask import make_response

from models.flask_backend import Flask_Event


app = Flask(__name__)
flask_event = Flask_Event()

# log設定追加
import logging
app.logger.setLevel(logging.DEBUG)


# 画像を保存するパス
UPLOAD_FOLDER = './static/uploads/'
ERROR_MESSAGES = {"upload_error": ["ファイルをアップロードできませんでした。",
                                   "[保存可能ファイル拡張子: '.mp4']"],
                  "file_name_error": ["ファイル名がありません"]}

app.config['SECRET_KEY'] = os.urandom(24)


def catch_files_list(upload_dir):
    uploaded_files_list = glob.glob(upload_dir + "*")
    return uploaded_files_list


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('menu.html')


@app.route('/return_upload', methods=['GET', 'POST'])
def return_upload():
    return render_template('upload.html')


@app.route('/output_table', methods=['GET', 'POST'])
def output_table():
    data_table = flask_event.output_meta_date()
    return render_template('show_table.html', meta_date=data_table)


@app.route('/download', methods=['GET', 'POST'])
def download():
    flask_event.save_csv("static/temp/traffic_data.csv")
    response = make_response()
    response.data = open("static/temp/traffic_data.csv", "rb").read()
    print("保存完了")
    return index()


@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        files = flask_event.upload_files(UPLOAD_FOLDER)
        flask_event.save_file_name(files[0].filename)
        if len(files) != 0:
            return redirect("/video_view")
        else:
            error_message = ERROR_MESSAGES["upload_error"]
            return render_template('upload.html',
                                   error_message=error_message)
    else:
        return redirect(url_for('index'))


@app.route('/video_view', methods=['GET', 'POST'])
def video_view():
    video_name = "static/uploads/" + flask_event.file_name
    return render_template("video_player.html", file_name=video_name)


@app.route("/add_data", methods=['POST'])
def add_data():
    flask_event.insert_date()
    return index()


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000,
                        type=int, help="port to listen on")
    args = parser.parse_args()
    port = args.port
    app.config["port"] = port
    app.run(host="0.0.0.0", port=port, threaded=True, debug=True)
