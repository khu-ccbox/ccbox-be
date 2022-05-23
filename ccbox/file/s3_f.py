import boto3
from django.shortcuts import render
from file import conf

s3_client = boto3.client(
    's3',
    aws_access_key_id=conf.aws_access_key_id,
    aws_secret_access_key=conf.aws_secret_access_key,
    region_name='ap-northeast-2')
s3_resource = boto3.resource(
    's3',
    aws_access_key_id=conf.aws_access_key_id,
    aws_secret_access_key=conf.aws_secret_access_key,
    region_name='ap-northeast-2')
BUCKET = 'ccbox-db'


# def get_file_list():
#     # s3_location = {
#     #     'LocationConstraint': 'ap-northeast-2'
#     # }
#     # s3_client.create_bucket(Bucket='ccbox-test-bucket-00001', CreateBucketConfiguration=s3_location)
#     bucket_list = []
#     for bucket in s3_resource.buckets.all():
#         bucket_list.append(bucket.name)

#     for bucket in bucket_list:
#         for files in s3_resource.Bucket(bucket).objects.all():
#             print(bucket + '의 ' + files)
#     return 0 

# s3_client.upload_file_local(업로드할 파일(코드기준 상대경로), 업로드 할 버킷, 버킷내에서 파일이 가지는 key)
def upload_file_local(path, file_name, key):
    return s3_client.upload_file(path+'/'+file_name, BUCKET, str(key))


def upload_file_server(file, file_name, key):
    return s3_client.upload_fileobj(file, BUCKET, str(key) + '/' + file_name)


# s3_client.download_file_local('버켓이름','버킷내에서 파일이 가지는 key',"로컬에 저장할때 파일이름")
def download_file_local(key, file_name):
    return s3_client.download_file(BUCKET, str(key), str(file_name))


def download_file_url(key, file_name):
    return s3_client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': str(key) + '/' + file_name}, ExpiresIn=60)


def delete_file(key):
    return s3_client.delete_object(Bucket=BUCKET, Key=str(key))


# def make_directory(bucket, user, path):
#     return S3.put_object(Bucket=BUCKET, Key=user+"/"+path)


# def move_file(bucket, user, old_path, new_path):
#     S3.copy_object(Bucket=bucket, CopySource=bucket+"/"+user+"/"+old_path, Key=user+"/"+new_path)
#     S3.delete_object(Bucket=bucket, Key=user+"/"+old_path)
#     return


# def copy_file(bucket, user, old_path, new_path):
#     S3.copy_object(Bucket=bucket, CopySource=bucket+"/"+user+"/"+old_path, Key=user+"/"+new_path)
#     return

