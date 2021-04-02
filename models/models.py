import sqlite3

# データベースファイルのパス
DB_PATH = 'models/traffic_data.db'


class DataBaseConnector:
    def __init__(self):
        # データベース接続とカーソル生成
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
                            "CREATE TABLE IF NOT EXISTS traffic ("
                            "id INTEGER PRIMARY KEY, "
                            "name TEXT, "
                            "pedestrian INTEGER, "
                            "bicycle INTEGER, "
                            "motorbike INTEGER, "
                            "passenger_car INTEGER, "
                            "small_freight_car INTEGER, "
                            "bus INTEGER, "
                            "ordinary_freight_car INTEGER"
                            ")")
        self.cursor.execute("SELECT COUNT(id) from traffic")
        rows = self.cursor.fetchall()
        self.id = rows[0][0]

    def add_row(self, name, pedestrian, bicycle, motorbike, passenger_car,
                small_freight_car, bus, ordinary_freight_car):
        self.cursor.execute("INSERT INTO traffic VALUES("
                       ":id, :name, :pedestrian, :bicycle, :motorbike,"
                       ":passenger_car, :small_freight_car, :bus,"
                       ":ordinary_freight_car"
                       ")",
                       {"id": self.id,
                        "name": name,
                        "pedestrian": pedestrian,
                        "bicycle": bicycle,
                        "motorbike": motorbike,
                        "passenger_car": passenger_car,
                        "small_freight_car": small_freight_car,
                        "bus": bus,
                        "ordinary_freight_car": ordinary_freight_car})
        # 保存を実行（忘れると保存されないので注意）
        self.connection.commit()

    def output_meta_date(self):
        # 1. カーソルをイテレータ (iterator) として扱う
        self.cursor.execute('select * from traffic')
        out_put = []
        for row in self.cursor:
            # rowオブジェクトでデータが取得できる。タプル型の結果が取得
            out_put.append(list(row))
        return out_put

    def __del__(self):
        # 接続を閉じる
        self.connection.close()
