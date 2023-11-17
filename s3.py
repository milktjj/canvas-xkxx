import boto3
import os
from datetime import datetime, timedelta

# 使用示例
# 替换为您要列出文件的前缀（可选，如果要列出整个存储桶中的文件，则不需要指定前缀）
prefix = 'account_22/tjj/'

# 使用示例
endpoint_url = 'https://s3.jcloud.sjtu.edu.cn:443'
access_key = 'b8a5fb0a69c741b5b5a0aa2436cc8302'  # 替换为您的访问密钥
secret_key = '81d302be327143288815b425cd907952'  # 替换为您的秘密密钥
bucket_name = '331a60d07b0a4ac5b121dba66bf2b863-tjj-canvas-test'  # 替换为您的存储桶名称
key = 'account_1/attachments/7617390/2.mp4'  # 替换为您要下载的文件的键
destination_path = './'  # 替换为您要保存文件的路径


def download_s3_file(endpoint_url, access_key, secret_key, bucket_name, key, destination_path):
    s3 = boto3.client('s3', endpoint_url=endpoint_url,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)

    try:
        s3.download_file(bucket_name, key, destination_path)
        print(f"文件下载成功！保存在 {destination_path}")
    except Exception as e:
        print(f"文件下载失败：{str(e)}")


def list_s3_objects(endpoint_url, bucket_name, access_key, secret_key, prefix=None):
    s3 = boto3.client('s3', endpoint_url=endpoint_url,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' in response:
        objects = response['Contents']
        for obj in objects:
            print(obj['Key'])
    else:
        print("存储桶中没有文件。")


def get_s3_file_url(object_name):
    try:
        s3 = boto3.client('s3', endpoint_url=endpoint_url,
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)
        response = s3.generate_presigned_url('get_object', Params={
                                             'Bucket': bucket_name, 'Key': object_name})
        return response
    except:
        print("AWS凭证未配置")


# download_s3_file(endpoint_url, access_key, secret_key, bucket_name, key, destination_path)
# list_s3_objects(endpoint_url, bucket_name, access_key, secret_key, prefix)


def upload_obj_to_s3(file_path, object_name):
    try:
        s3 = boto3.client('s3', endpoint_url=endpoint_url,
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)
        s3.upload_file(file_path, bucket_name, object_name)
        # s3.upload_fileobj(file, bucket_name, object_name)
        print("文件上传成功")
    except FileNotFoundError:
        print("找不到指定的文件")


if __name__ == "__main__":
    upload_obj_to_s3("plant.png", bucket_name, "account_22/tjj/plant_2.png")

    file_url = get_s3_file_url('account_22/tjj/plant.png')
    print("上传文件的URL:", file_url)
