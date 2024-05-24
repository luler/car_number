# coding=utf-8
import hashlib
import re
import shutil
import uuid

from flask import Flask, render_template, request, jsonify
import cv2
from hyperlpr import *

app = Flask(__name__)
# 允许上传最大，16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def json_return(code, message, info=[]):
    data = {}
    data['code'] = int(code)
    data['message'] = str(message)
    data['info'] = info
    return jsonify(data)


def recognize(filename):
    # 通过文件名读入一张图片 放到 image中
    image = cv2.imread(filename)
    # 识别一张图片并返回json结果
    return HyperLPR_plate_recognition(image)


# 获取文件md5
def md5_file(file_path):
    md5_obj = hashlib.md5()
    with open(file_path, 'rb') as file_obj:
        md5_obj.update(file_obj.read())
    file_md5_id = md5_obj.hexdigest()
    return file_md5_id


@app.route('/work', methods=['GET', 'POST'])  # 设置请求路由
def work():
    if request.method == 'POST':
        try:
            # 如果请求方法是POST
            f = request.files['file']
            ext = re.search(".([a-z|A-Z]*?)$", f.filename).group(1).lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                raise Exception('不支持当前文件后缀名')
            filename = str(uuid.uuid1()) + '.' + ext
            prefix = "./upload_images/"
            temp_file = prefix + filename
            f.save(temp_file)
            # 很坑，f.read在f.save前，保存的文件会是空的
            last_file = prefix + md5_file(temp_file) + '.' + ext
            shutil.move(temp_file, last_file)
            # 保存请求上来的文件
            res = recognize(last_file)
            return json_return(200, '识别成功', res)
        except Exception as err:
            return json_return(400, str(err))
    # 简易测试页面
    return render_template('upload.html')


if __name__ == '__main__':
    # 入口函数，# 运行app 指定IP 指定端口
    # threaded 开启多线程运行模式，否则为单进程模式，并发请求会等待
    app.run("0.0.0.0", port=8000, threaded=True, debug=False)
