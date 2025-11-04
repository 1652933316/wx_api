from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# 定义 JSON 存储文件路径（确保文件所在目录存在）
JSON_FILE_PATH = "data_storage.json"

app.config['JSON_AS_ASCII'] = False  # 禁用 JSON 中文转 ASCII（避免返回 \uXXXX 转义符）
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=gbk'  # JSON 响应头指定 utf-8

# 初始化 JSON 文件（如果文件不存在则创建空列表）
if not os.path.exists(JSON_FILE_PATH):
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)  # 用列表存储多条数据，方便扩展


@app.route("/save-data", methods=["POST"])
def save_data_to_json():
    """
    接收 POST 请求数据，存储到本地 JSON 文件
    支持 Content-Type: application/json 或 form-data 格式的请求
    """
    try:
        # 1. 获取请求数据（优先解析 JSON 格式，其次是表单格式）
        if request.is_json:
            data = request.get_json()  # 解析 JSON 数据
        else:
            data = request.form.to_dict()  # 解析表单数据（form-data/x-www-form-urlencoded）

        # 2. 数据验证（确保请求包含有效数据，可根据实际需求修改）
        if not data:
            return jsonify({"code": 400, "message": "请求数据不能为空"}), 400

        # 3. 读取现有 JSON 数据
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
            existing_data = json.load(f)  # 读取为列表格式

        # 4. 添加新数据（如果需要单条数据覆盖，可改为 existing_data = data）
        existing_data= data

        # 5. 写入 JSON 文件（indent=2 美化格式，ensure_ascii=False 支持中文）
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

        return jsonify({
            "code": 200,
            "message": "数据保存成功",
            "data": data  # 返回保存的具体数据
        }), 200

    except json.JSONDecodeError:
        return jsonify({"code": 400, "message": "JSON 格式错误"}), 400
    except Exception as e:
        return jsonify({"code": 500, "message": f"服务器错误：{str(e)}"}), 500


@app.route("/get-data", methods=["GET"])
def get_data_from_json():
    """
    响应 GET 请求，读取本地 JSON 文件并返回数据
    """
    try:
        # 1. 读取 JSON 文件
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(data['msgs'][0].split("；"))
        return jsonify({
            "code": 200,
            "message": "数据读取成功",
            "data": data['msgs'][0].split("；")  # 返回全部存储数据
        }), 200

    except FileNotFoundError:
        return jsonify({"code": 404, "message": "数据文件不存在"}), 404
    except json.JSONDecodeError:
        return jsonify({"code": 500, "message": "数据文件格式损坏"}), 500
    except Exception as e:
        return jsonify({"code": 500, "message": f"服务器错误：{str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)