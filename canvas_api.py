import requests

base_url = 'etctest.sjtu.edu.cn'
token = 'qgDqat8243PKccVNeFjYyqi8jlSapO7PYecAwzzGsCg2u7vCsKWJqDp7A5nGyYC8'

headers = {
    'Authorization': f'Bearer {token}',
    'Cookie': '_csrf_token=CeVJTebALTkOXpk2MFLN8dcjRJlTnlzd3nCMtK8csYVNriEVrpR5Wksw7kRnOIij7mwC0iKxDqSnQuefwFGIwg%3D%3D; _legacy_normandy_session=myAhTqYsYZlONiunHQx_Tg.EdFHgdnMwSRkPqEqeXRsTxZEBRgOIW75Ow_QeASiREXq4I-ufVxOMfSGMjTQOstQJzryMlFKQnHgWa4NyIi7mgRDMYrBIBz-QVbxE1i8I1wduBglw6litOcim2YoEcbj.I6P4bBfzDun0wle91fNcijMZuXc.ZSeGlA; _normandy_session=myAhTqYsYZlONiunHQx_Tg.EdFHgdnMwSRkPqEqeXRsTxZEBRgOIW75Ow_QeASiREXq4I-ufVxOMfSGMjTQOstQJzryMlFKQnHgWa4NyIi7mgRDMYrBIBz-QVbxE1i8I1wduBglw6litOcim2YoEcbj.I6P4bBfzDun0wle91fNcijMZuXc.ZSeGlA; log_session_id=b1332dcb2138f969dc36ee00c7b50456'
}


def get_course_section(course_id):
    url = f"https://{base_url}/api/v1/courses/{course_id}/sections"
    response = requests.request("GET", url, headers=headers)
    ret_json = response.json()
    if isinstance(ret_json, list):
        return ret_json
    elif isinstance(ret_json, dict):
        return []
    else:
        return []


if __name__ == "__main__":
    get_course_section(10621)
