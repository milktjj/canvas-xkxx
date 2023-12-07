# from share_sql import course_df
import db
import config
from collections import OrderedDict
import share_sql
import canvas_api as api
from flask_cors import CORS
import jwt
import json
from jwcrypto import jwk
import os
import share_sql
from flask import (Flask, jsonify, request, redirect, send_from_directory)
import s3
import audio
from datetime import datetime
import time
import os
import random
import heapq
import string
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import ws

port = 8080
# base_url = '10.119.10.48:13000'
base_url = 'lms.sjtu.edu.cn/xk-web'
# web_url = f'10.119.10.48:{port}'
web_url = 'lms.sjtu.edu.cn/xk'
canvas_domain = 'etctest'
client_id = 10000000000026
refresh_time = int(time.time())
file_heap = []


key_pair = {
    "p": "54xA0vFaPsrzAwPzk8QIY8xHEgC_WBHfK02PR1F7msjBpf0db_gboBXgs3m_PtF4ykAZR-BMCfnQQbz6hMr1VyG-kxB1GqpZADD0WeumRb2P7-6Rm_Q6o6XgulfZehS4CTJ_u8eZahwlWwHbMQRmHGpHL96qb0dq2SX2wj9OrV0",
    "kty": "RSA",
    "q": "kCA8g2LsEAvb1anzDaLr3LqOOty2fycPPhrCVUg2WoxZfJ1Mz0nM2H2U5yiYM6Fv9ggR8_hIpinFyQNrwWyHSMRB-UqSQW8viL5_VX10oP4mFVwSO0B2A0xHwufI_7oM50YrL5CJFXK7YcMbWjRNpxP6DXUVNH-q63GnYpIgnzU",
    "d": "GniOrR6yafzpvmh7n4tH8ZJScT4RJ3GZwKT3ivMfTXtnL4hNyFkyakjpvbbvf30LywThIkHPcTVVX75slP8dgjz08Gwrgalhb-fAv1OTijOlr8zjzUek4tnZT0KzsKU94oZZy__exCKM5Izeyotgb8JQAQNGT0YpdWtGXISLNw-sUaMmdfYRxZoooVErfgUjduKyxLy-1ss8j-WoHDcvjjxOG5OBGD65WLiOMsm-XKFtcEAZZPpGqP7S-q-TI8uem4rx2uE6TKKTw2pYmC9h8m_ROxzi8O8phbsNRa3MP7qVWhaQC8to5Hc7RD9jBsa_NmyRBjcXRzxWNWWTNI1VQQ",
    "e": "AQAB",
    "use": "enc",
    "kid": "IPaVTf0jSkmaGhwCee5OTnufsWq1V2jZO2nJuQv3yys",
    "qi": "Szz5mcUNT24Ax7yh3nfDRcpPPi_SLudifQRe3GvjSyj6bCQCQzFSSWB5AZ3OzXmsTbvsVssWZKhnHyL6ycHypIJ5PzIkmunv2SpexaEqxupx47uPEsKnSEZirgP8GL7BsyMfprcBp8J5t6mSfig5ma-vzCApKLy7cQC5OIVKpII",
    "dp": "eVq8rtHn5nkfnDj59DwN2aA6r2jM4C-ds2hW6539FkaZl5FtWD3E3MYamnX4kcffcsDdfxpDQAc56vpMokRtCVmaNCGv_mXBd6QwrOAgqPSM98clcYMzKInLml5okN9DBS7-W0BlW4Oc4HG8m5genE3nOWOOF_xqN5z6Exxy89E",
    "alg": "RSA1_5",
    "dq": "doMrf1ZeiqtVr5I6HGJ11GFLBzfqkRALRqQ2XG4u07JI-2FVgbZLzVEmmhYVYY9EQ2lLafQluQzsaGh5uOmHLNzE6zrYnRnSWn1as2-f8apKopG9JB_Tas7Uy35RF4djiOF4LXqKXqqjTrZizX_owpR4r4wxTaQVZdllLHbAgGk",
    "n": "glwMuneQv7yquwWn-TKyceyIas-lngYGWk9pfdu5h2aBU3oP3Qv61aqqy04L-SmJgQ082Qt_Z248k89MoJS1T6_OZW-5eb72j3Na2xJx_dRyQSVjYRhvASE-bLmmpyUjAYsf-laKbSKRkJ2mbGHHbYwdTbOoBcewgasfxlijCppY_1m2iIgDz2t5kE-td5Ys5-dqGAHMNdEBg3JQYfj5qzTDzZ2BlIt5QgKMdqKRlK88MpOavcwVFBJPQ0HWP3chdbDILYkw0JruxgS6ndAS28Er5eGXTG4QYSAo7foT4iMkbEcVjl8Rcho2Bs2YMKgu2ww2iE4YjMCdxIzXrpanQQ"
}

key_pair_set = {
    "keys": [
        {
            "p": "54xA0vFaPsrzAwPzk8QIY8xHEgC_WBHfK02PR1F7msjBpf0db_gboBXgs3m_PtF4ykAZR-BMCfnQQbz6hMr1VyG-kxB1GqpZADD0WeumRb2P7-6Rm_Q6o6XgulfZehS4CTJ_u8eZahwlWwHbMQRmHGpHL96qb0dq2SX2wj9OrV0",
            "kty": "RSA",
            "q": "kCA8g2LsEAvb1anzDaLr3LqOOty2fycPPhrCVUg2WoxZfJ1Mz0nM2H2U5yiYM6Fv9ggR8_hIpinFyQNrwWyHSMRB-UqSQW8viL5_VX10oP4mFVwSO0B2A0xHwufI_7oM50YrL5CJFXK7YcMbWjRNpxP6DXUVNH-q63GnYpIgnzU",
            "d": "GniOrR6yafzpvmh7n4LH8ZJScT4RJ3GZwKT3ivMfTXtnL4hNyFkyakjpvbbvf30LywThIkHPcTVVX75slP8dgjz08Gwrgalhb-fAv1OTijOlr8zjzUek4tnZT0KzsKU94oZZy__exCKM5Izeyotgb8JQAQNGT0YpdWtGXISLNw-sUaMmdfYRxZoooVErfgUjduKyxLy-1ss8j-WoHDcvjjxOG5OBGD65WLiOMsm-XKFtcEAZZPpGqP7S-q-TI8uem4rx2uE6TKKTw2pYmC9h8m_ROxzi8O8phbsNRa3MP7qVWhaQC8to5Hc7RD9jBsa_NmyRBjcXRzxWNWWTNI1VQQ",
            "e": "AQAB",
            "use": "enc",
            "kid": "IPaVTf0jSkmaGhwCee5OTnufsWq1V2jZO2nJuQv3yys",
            "qi": "Szz5mcUNT24Ax7yh3nfDRcpPPi_SLudifQRe3GvjSyj6bCQCQzFSSWB5AZ3OzXmsTbvsVssWZKhnHyL6ycHypIJ5PzIkmunv2SpexaEqxupx47uPEsKnSEZirgP8GL7BsyMfprcBp8J5t6mSfig5ma-vzCApKLy7cQC5OIVKpII",
            "dp": "eVq8rtHn5nkfnDj59DwN2aA6r2jM4C-ds2hW6539FkaZl5FtWD3E3MYamnX4kcffcsDdfxpDQAc56vpMokRtCVmaNCGv_mXBd6QwrOAgqPSM98clcYMzKInLml5okN9DBS7-W0BlW4Oc4HG8m5genE3nOWOOF_xqN5z6Exxy89E",
            "alg": "RSA1_5",
            "dq": "doMrf1ZeiqtVr5I6HGJ11GFLBzfqkRALRqQ2XG4u07JI-2FVgbZLzVEmmhYVYY9EQ2lLafQluQzsaGh5uOmHLNzE6zrYnRnSWn1as2-f8apKopG9JB_Tas7Uy35RF4djiOF4LXqKXqqjTrZizX_owpR4r4wxTaQVZdllLHbAgGk",
            "n": "glwMuneQv7yquwWn-TKyceyIas-lngYGWk9pfdu5h2aBU3oP3Qv61aqqy04L-SmJgQ082Qt_Z248k89MoJS1T6_OZW-5eb72j3Na2xJx_dRyQSVjYRhvASE-bLmmpyUjAYsf-laKbSKRkJ2mbGHHbYwdTbOoBcewgasfxlijCppY_1m2iIgDz2t5kE-td5Ys5-dqGAHMNdEBg3JQYfj5qzTDzZ2BlIt5QgKMdqKRlK88MpOavcwVFBJPQ0HWP3chdbDILYkw0JruxgS6ndAS28Er5eGXTG4QYSAo7foT4iMkbEcVjl8Rcho2Bs2YMKgu2ww2iE4YjMCdxIzXrpanQQ"
        }
    ]
}

public_key = {
    "kty": "RSA",
    "e": "AQAB",
    "use": "enc",
    "kid": "IPaVTf0jSkmaGhwCee5OTnufsWq1V2jZO2nJuQv3yys",
    "alg": "RSA1_5",
    "n": "glwMuneQv7yquwWn-TKyceyIas-lngYGWk9pfdu5h2aBU3oP3Qv61aqqy04L-SmJgQ082Qt_Z248k89MoJS1T6_OZW-5eb72j3Na2xJx_dRyQSVjYRhvASE-bLmmpyUjAYsf-laKbSKRkJ2mbGHHbYwdTbOoBcewgasfxlijCppY_1m2iIgDz2t5kE-td5Ys5-dqGAHMNdEBg3JQYfj5qzTDzZ2BlIt5QgKMdqKRlK88MpOavcwVFBJPQ0HWP3chdbDILYkw0JruxgS6ndAS28Er5eGXTG4QYSAo7foT4iMkbEcVjl8Rcho2Bs2YMKgu2ww2iE4YjMCdxIzXrpanQQ"
}

app = Flask(__name__)
CORS(app,  supports_credentials=True)
executor = ThreadPoolExecutor(max_workers=30)


# @app.route('/', methods=['GET', 'POST'])
# def hello():
#     return "Hello World!"


# @app.route('/')
# def index():
#     file_list = os.listdir('.')
#     html = '<ul>'
#     for filename in file_list:
#         html += f'<li><a href="{filename}">{filename}</a></li>'
#     html += '</ul>'
#     return html
#
#
# @app.route('/<path:path>')
# def serve_file(path):
#     return send_from_directory('.', path)

# async def refresh(ws):
#     while True:
#         msg = await ws.recv()
#         print(f"< {msg}")
#         s = await reload()
#         await ws.send(s)
#
#
# async def reload():
#     pass
#
#
# async def socket():
#     uri = "ws://localhost:18080"
#     async with websockets.connect(uri) as ws:
#         await refresh(ws)

@app.route('/jwk')
def jwk():
    return public_key


@app.route('/canvas-login', methods=['POST'])
def canvas_login():
    params = {'login_hint': request.form['login_hint'],
              'lti_message_hint': request.form['lti_message_hint']}
    params.update({'redirect_uri': f'https://{web_url}/hello', 'client_id': client_id, 'scope': 'openid',
                  'response_type': 'id_token', 'nonce': 1234, 'prompt': None, 'response_mode': 'form_post'})
    print(params)
    query_string = '&'.join(
        [f'{key}={value}' for key, value in params.items()])
    return redirect(f'https://{canvas_domain}.sjtu.edu.cn/api/lti/authorize_redirect?{query_string}')


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    id_token = request.form.get('id_token')
    return redirect(f"https://{base_url}/courses?token={id_token}", code=302)


@app.route('/lti1_1', methods=['POST'])
def lti1_1():
    sis_id = request.form.get('custom_course_sis_id')
    return redirect(f"https://{base_url}/courses?course_sis_id={sis_id}", code=302)


@app.route('/upload', methods=['POST'])
def upload():
    # 检查是否有文件被上传
    if 'music' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['music']
    # 检查文件名是否为空
    if file.filename == '':
        return 'Empty filename.', 400
    status = 200
    try:
        current_timestamp = int(datetime.timestamp(datetime.now()))
        file_name = f'{current_timestamp}.amr'
        mp3_file_name = f'{current_timestamp}.mp3'
        file.save(file_name)
        audio.amr_to_mp3(file_name, mp3_file_name)
        s3.upload_obj_to_s3(mp3_file_name, s3.prefix+mp3_file_name)
        db.insert_data(current_timestamp, False)
    except:
        status = 400
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
        if os.path.exists(mp3_file_name):
            os.remove(mp3_file_name)
        print("delete")
    return {}


@app.route('/ping', methods=['POST'])
def set_ping():
    config.ping_time = int(time.time())
    return {}


@app.route('/ping', methods=['GET'])
def get_ping():
    if int(time.time()) - config.ping_time < 10:
        return {"status": True}
    return {"status": False}

@app.route('/config', methods=['GET'])
def get_config():
    return config.get_config_info()


@app.route('/config', methods=['POST'])
def update_config():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    print(key, value)
    if key is None or value is None:
        return {}
    return config.update_config_info(key, value)


@app.route('/uploadB', methods=['POST'])
def uploadBin():
    if 'pcm' not in request.files:
        return {"status": 200}

    file = request.files['pcm']
    if file.filename == '':
        return {"status": 200}
    ifilename = './'+generate_random_string(32) + '.pcm'
    heapq.heappush(file_heap, (int(time.time() * 1000), ifilename))
    file.save(ifilename)
    heap_size_triger = config.get_config_info()['fileLen']
    if len(file_heap) >= heap_size_triger:
        file_list = []
        for _ in range(heap_size_triger):
            if file_heap:
                timestamp, filename = heapq.heappop(file_heap)
                print(filename)
                file_list.append(filename)
            else:
                break
        sorted_files = sorted(file_list)

        merged_file_path = "./temp.pcm"
        merged_file = open(merged_file_path, "wb")

        for file_path in sorted_files:
            with open(file_path, "rb") as file:
                data = file.read()
                merged_file.write(data)
                if os.path.exists(file_path):
                    os.remove(file_path)
        merged_file.close()
        try:
            executor.submit(audio.pcm_to_s3, merged_file_path)
        except Exception as e:
            print(str(e))
    return {}


def generate_random_string(length):
    # 从大小写字母和数字中生成随机字符
    characters = string.ascii_letters + string.digits
    # 使用random.choice()函数从字符集中随机选择字符，并将它们组合在一起
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


@app.route('/getsharelink', methods=['GET'])
def get_share_link():
    timestamp = request.args.get('t')
    if not timestamp:
        return {}
    file_name = f'{timestamp}.mp3'
    url = s3.get_s3_file_url(s3.prefix+file_name)
    return {"url": url}


@app.route('/list', methods=['GET'])
def get_tear_list():
    date = request.args.get('date')
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    keys = ['t', 'l']
    values = db.query_data_by_date(date)
    if not values:
        values = []
    results = [dict(zip(keys, value)) for value in values]
    return jsonify(results)


@app.route('/refreshTime', methods=['GET'])
def get_refresh_time():
    return {"t": refresh_time}


@app.route('/courses/<course_id>/info', methods=['GET'])
def get_course_info(course_id):
    # course_section_list = api.get_course_section(course_id)
    # if len(course_section_list) == 0:
    #     return handle_error()
    # ret_course_id = course_section_list[0].get('course_id')
    # if str(ret_course_id) != course_id:
    #     return handle_error()
    # data = share_sql.get_course_info_by_sis(
    #     course_section_list[0].get('sis_course_id'))
    current_timestamp = int(time.time())
    if refresh_time + 6*60*60 < current_timestamp:
        share_sql.refresh_course_df()
    data = share_sql.get_course_info_by_sis(course_id)

    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response


def handle_error():
    return redirect(f"https://{web_url}", code=302)


def decode_jwt(token, public_key):
    try:
        # 解码JWT
        decoded_token = jwt.decode(
            token,
            key=public_key,
            algorithms=['RS1_5'],
            options={'verify_signature': False}
        )
        # 返回解码后的内容
        print(decoded_token)
        return decoded_token
    except jwt.ExpiredSignatureError:
        # 处理过期的JWT
        print("Token已过期")
    except jwt.InvalidTokenError:
        # 处理无效的JWT
        print("无效的Token")


if __name__ == '__main__':
    # share_sql.refresh_course_df()
    # context = ('cert.pem', 'key.pem')  # 证书和密钥文件路径
    ws.run_websocket_server()
