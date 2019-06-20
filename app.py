from flask import Flask, request
from flask_apscheduler import APScheduler
import config as cfg
from data import Data
from lfw import LFW
import json


# 定时任务。每天23点更新推荐
class Config(object):
    JOBS = [
        {
            'id': 'update',
            'func': 'app:update',
            'args': None,
            'trigger': 'cron',
            "hour": 23,
            "minute": 0
        }
    ]
    SCHEDULER_API_ENABLED = True
    pass


# 更新数据
def update():
    lfw.update()

# 创建app
def create_app():
    app = Flask(__name__)
    scheduler = APScheduler()
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    return app
    pass


# 创建
app = create_app()
data = Data()
lfw = LFW(data)


@app.route('/', methods=["GET"])
def recommend():
    # 通过post获取userID
    inputs = request.form['userID'].strip()
    if not inputs.isdigit():
        res = {"status": 0, "data": "请输入合法的用户ID"}
        res = json.dumps(res, ensure_ascii=False)
        return res
    try:
        # 执行预测
        userID = int(inputs)
        result = lfw.predict(userID, cfg.topN)
        # 推荐列表为空
        if result is None:
            res = {"status": 6001, "message": "获取推荐列表为空"}
        # 正常结果返回
        else:
            rooms = []
            for room in result:
                rooms.append(int(room))
            res = {"status": 0, "data": rooms}
            res = json.dumps(res, ensure_ascii=False)
        return res
    # 捕获异常
    except Exception as e:
        res = {"status": 6000, "message": str(e)}
        res = json.dumps(res, ensure_ascii=False)
        return res
    pass


if __name__ == '__main__':
    app.run()
