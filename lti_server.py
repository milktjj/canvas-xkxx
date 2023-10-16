# from share_sql import course_df
import share_sql
import canvas_api as api
from flask_cors import CORS
import jwt
import json
from jwcrypto import jwk
import os
import share_sql
from flask import (Flask, request, redirect, send_from_directory)

base_url = '127.0.0.1:3000'
web_url = '127.0.0.1:8080'
canvas_domain = 'etctest'
client_id = 10000000000026

key_pair = {
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

# @app.route('/', methods=['GET', 'POST'])
# def hello():
#     return "Hello World!"


@app.route('/')
def index():
    file_list = os.listdir('.')
    html = '<ul>'
    for filename in file_list:
        html += f'<li><a href="{filename}">{filename}</a></li>'
    html += '</ul>'
    return html


@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)


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


@app.route('/courses/<course_id>/info', methods=['GET'])
def get_course_info(course_id):
    course_section_list = api.get_course_section(course_id)
    if len(course_section_list) == 0:
        return handle_error()
    ret_course_id = course_section_list[0].get('course_id')
    if str(ret_course_id) != course_id:
        return handle_error()
    data = share_sql.get_course_info_by_sis(
        course_section_list[0].get('sis_course_id'))
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
    share_sql.refresh_course_df()
    context = ('cert.pem', 'key.pem')  # 证书和密钥文件路径
    app.run(port=8080, debug=True, ssl_context=context)
