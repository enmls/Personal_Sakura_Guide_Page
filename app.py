# -*- encoding: utf-8 -*-
import flask
import json
import requests
import userconfig
import datetime
import os
from flask import Flask, render_template, request, jsonify, send_from_directory, session,redirect
from werkzeug.utils import secure_filename
import io
import contextlib

def gettime():
    # 获取当前日期时间
    now = datetime.datetime.now()

    # 格式化输出日期时间
    formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')

    # 输出日期时间
    return formatted_now

app = Flask('myflask')
app.secret_key = "xsaxxxxxxxxx"
# app.config['SESSION_REFRESH_EACH_REQUEST'] = True   #每个请求到刷新会话



def ip_address(ip):

    from czdb.db_searcher import DbSearcher

    database_path = "cz88_public_v4.czdb"
    query_type = "BTREE"
    key = "xxxxxxxxxxxxx"

    #db_searcher = DbSearcher(database_path, query_type, key)

    try:
        #region = db_searcher.search(ip)

        return '中国'

    except Exception as e:
        print(f"An error occurred during the search: {e}")
        return e

    # finally:
    #     db_searcher.close()

#拦截国外ip
def decide_c(region):
    if "中国" in region:
        return True
    else:
        return render_template("404h.html")




@app.before_request
def make_session_permanent():
    session.permanent = True    #关闭浏览器时会自动过期
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)


@app.route('/')
def index():
    ip_ad = request.remote_addr
    city = ip_address(ip_ad)
    if decide_c(city)==True or ip_ad=="127.0.0.1":
        return render_template('index.html', ip_ad=ip_ad,city=city)
    else:
        return render_template("404h.html")



@app.route('/tree')
def tree():
    ip_ad = request.remote_addr
    if ip_address(ip_ad)==True:
        return render_template('404h.html')
    else:
        return render_template("404h.html")


#======================文件上传部分======================
# 配置上传文件夹
#UPLOAD_FOLDER = '/project/dataA'
UPLOAD_FOLDER = 'D:\\test111\\'
# 确保该目录存在，如果不存在则创建
#os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 限制上传大小，比如最大 100MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024

# 捕获文件过大的异常 (HTTP 413)
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "文件过大！最大支持 1GB"}), 413


# 1. 页面主路由 (保留你的逻辑)
@app.route("/dataA")
def dataA():
    if "username" not in session:
        return redirect("/login")
    return render_template("dataA.html")



# 2. 文件上传接口 (新增)
@app.route('/upload', methods=['POST'])
def upload_file():
    # 简单的权限检查，防止未授权直接调用接口
    if "username" not in session:
        return jsonify({"error": "未登录"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "没有文件部分"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400

    if file:
        # secure_filename 会处理文件名中的特殊字符，防止路径穿越攻击
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 保存文件
        file.save(save_path)

        # 获取文件信息返回给前端
        file_size = os.path.getsize(save_path)
        return jsonify({
            "message": "上传成功",
            "filename": filename,
            "size": file_size
        })


# 3. 获取文件列表接口 (新增，用于页面加载时显示服务器上已有的文件)
@app.route('/get_files', methods=['GET'])
def get_files():
    if "username" not in session:
        return jsonify({"error": "未登录"}), 403

    files = []
    try:
        # 遍历目录
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(path):
                files.append({
                    "name": filename,
                    "size": os.path.getsize(path),
                    "time": os.path.getmtime(path)
                })
        # 按时间倒序排列
        files.sort(key=lambda x: x['time'], reverse=True)
    except Exception as e:
        print(f"读取目录错误: {e}")

    return jsonify(files)


# 4. 文件下载接口 (新增)
@app.route('/download/<filename>')
def download_file(filename):
    if "username" not in session:
        return redirect("/login")

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)




# 5.【新增】删除文件接口
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    # 1. 权限检查
    if "username" not in session:
        return jsonify({"error": "未登录"}), 403

    # 2. 安全处理文件名 (防止路径穿越攻击)
    safe_filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)

    # 3. 检查文件是否存在
    if not os.path.exists(file_path):
        return jsonify({"error": "文件不存在"}), 404

    try:
        # 4. 执行删除
        os.remove(file_path)
        return jsonify({"message": "删除成功"})
    except Exception as e:
        print(f"删除文件失败: {e}")
        return jsonify({"error": "删除失败，服务器错误"}), 500


#======================文件上传部分结束======================

@app.route("/login", methods=["POST", "GET"])
def login():
    if "username" not in session:
        message = ''
        ip_ad = request.remote_addr
        city = ip_address(ip_ad)
        if decide_c(city)==True or ip_ad=="127.0.0.1":
            if request.method == "POST":
                # 判断请求内容类型
                if request.is_json:
                    # 从 JSON 中获取数据
                    data = request.get_json()
                    username = data.get("email")
                    password = data.get("password")
                else:
                    # 兼容普通表单提交
                    username = request.form.get("email")
                    password = request.form.get("password")
                # --- 修改结束 ---

                if userconfig.check_user(username, password):
                    session["username"] = username
                    # 登录成功，为了让前端 fetch 能够正确识别，建议返回 JSON 而不是重定向 HTML
                    return {"status": "success", "redirect": "/dataA"}
                else:
                    # 登录失败，返回 JSON 错误信息
                    return {"status": "error", "message": "用户名或密码错误"}, 400  # 返回 400 状态码方便前端 catch

            # GET 请求或直接访问页面
            return render_template("login.html", message=message)
        else:
            return render_template("404h.html")
    else:
        return render_template("dataA.html")




@app.route("/onlinepy")
def onlinepy():
    if "username" not in session:
        return redirect("/login")
    return render_template("Onlinepy.html")

@app.route('/api/run', methods=['POST'])  # 确认这里只写了 POST
def run_code():
    # --- 新增调试信息：打印请求方法 ---
    print(f"--- 收到请求: Method = {request.method} ---")
    # ----------------------------------

    # 如果收到的是 GET，直接返回错误提示（方便调试）
    if request.method == 'GET':
        return jsonify({"error": "请使用 POST 请求"}), 405

    data = request.json
    code = data.get('code', '')
    print(f"收到的代码长度: {len(code)} 字符")

    buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(buffer):
            exec(code, {})

        output = buffer.getvalue()
        return jsonify({
            'output': output,
            'error': None
        })
    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}"
        print(f"执行出错: {error_msg}")
        return jsonify({
            'output': buffer.getvalue(),
            'error': error_msg
        }), 200


@app.route("/page1")
def Page_switching1():
    return render_template("404h.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host="0.0.0.0",port=80)
