import os
import csv

from flask import request
from models.models import DataBaseConnector

# 保存できるファイルの拡張子
ALLOWED_EXTENSION_NAMES = {'mp4'}
COLUMN_NAME = ["ID", "動画名", "歩行者数", "自転車", "動力付き二輪車", "乗用車",
               "小型貨物車", "バス", "普通貨物"]


def allowed_extensions(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSION_NAMES


class Flask_Event:
    def __init__(self):
        self.file_name = None
        pass

    def save_file_name(self, file_name):
        self.file_name = file_name
        return 0

    @staticmethod
    def upload_files(upload_folder):
        files = request.files.getlist('files')
        for file in files:
            if file and allowed_extensions(file.filename):
                file_name = file.filename
                file.save(os.path.join(upload_folder, file_name))
        return files

    def insert_date(self):
        title = self.file_name
        pedestrian = int(request.form["pedestrian_num"])
        bicycle = int(request.form["bicycle_num"])
        motorbike = int(request.form["motorbike_num"])
        passenger_car = int(request.form["passenger_car_num"])
        small_freight_car = int(request.form["small_freight_car_num"])
        bus = int(request.form["bus_num"])
        ordinary_freight_car = int(request.form["ordinary_freight_car_num"])
        data_base = DataBaseConnector()
        data_base.add_row(title, pedestrian, bicycle, motorbike, passenger_car,
                          small_freight_car, bus, ordinary_freight_car)

    @staticmethod
    def output_meta_date():
        data_base = DataBaseConnector()
        return data_base.output_meta_date()

    @staticmethod
    def save_csv(file_path):
        data_base = DataBaseConnector()
        data_rows = data_base.output_meta_date()
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(COLUMN_NAME)
            writer.writerows(data_rows)
        return 0
