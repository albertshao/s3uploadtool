"""
this file functions operations aiming to S3 bucket, including permission validation,
files' uploading, S3 api calling and so on
"""
import os
import time
import logging
import boto3
import threading



from botocore.exceptions import ClientError


class AwsCaller(object):
    """
    The util class calls aws api to implement all the operations.
    """
    def __init__(self, values):
        """
        init the aws client.
        :param values:  the python dict expected to contains all the parameters.
        """
        self.s3name = values.get('name', None)
        self.region = values.get('region', None)
        self.accessId = values.get('accessId', None)
        self.access_key = values.get('access_key', None)
        self.s3 = None
        self.uploaded_files_lists = []
        self.UPLOAD_TIME_OUT = 30 * 60 * 60 # 30 minutes

    def _get_endpoint(self, file_name):
        end_url = 'http://{s3}.s3-website-{region}.amazonaws.com/{file}'.format(
            s3=self.s3name, region=self.region, file=file_name
        )
        return end_url

    def _init_default_s3(self):
        """
        init the default s3 with accessId and access_key.
        :param accessId:
        :param access_key:
        :return:
        """
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=self.accessId,
            aws_secret_access_key=self.access_key,
            region_name=self.region,

        )

    def check_object_exists(self, key):
        try:
            self.s3.meta.client.head_object(Bucket=self.s3name, Key=key)
        except ClientError as e:
            print(e)
            return int(e.response['Error']['Code']) != 404
        return True

    def validate_permission(self):
        """
        Validate whether user with accessId and access_key has access to the S3.
        :param accessId: string, given by ops colleague
        :param access_key: string, correspond with accessId
        :return: tuple, (True, msg) or (False, reason)
        """
        result = (False, '')
        try:
            # create the resource client with credients.
            if self.s3 is None:
                self._init_default_s3()

            #  check whether the bucket exists, raise exception if not exist.
            self.s3.meta.client.head_bucket(Bucket=self.s3name)

            result = (True, 'validate successfully')

        except ClientError as err:
            print(err)
            if 'SignatureDoesNotMatch' in str(err) or 'Forbidden' in str(err):
                result = (False,'SignatureDoesNotMatch')
            elif 'AccessDenied' in str(err):
                result = (False, 'AccessDenied')
            elif 'HeadBucket operation' in str(err):
                result = (False, 'BucketDoesnotExist')
            else:
                result = (False, 'ValidateFailure')

        return result

    def batch_upload_files(self, file_list):
        """
        Uploads the locals file to the specific S3 Bucket
        :param file_list:  the python list which contains local file paths.
        :return:
        """
        self.uploaded_files_lists.clear()

        def upload_file(self, file_path):
            start_time = time.time()
            file_name = os.path.basename(file_path)

            logging.warning('Uploading %s to Amazon S3 bucket %s' % (file_name, self.s3name))
            self.s3.Object(self.s3name, file_name).put(
                Body=open(file_path, 'rb'))
            timedelta = time.time() - start_time
            ret = self.check_object_exists(file_name)
            while timedelta < self.UPLOAD_TIME_OUT and not ret:
                time.sleep(2)
                ret = self.check_object_exists(file_name)
                timedelta = time.time() - start_time
            if ret:
                self.uploaded_files_lists.append(self._get_endpoint(file_name))
            else:
                self.uploaded_files_lists.append('%s uploads failure, timeout' % file_name)

        thread_list = []
        for file_path in file_list:
            thread_list.append(threading.Thread(target=upload_file, args=(self,file_path)))
        for th in thread_list:
            th.start()


    def get_uploaded_files(self):
        return self.uploaded_files_lists

    def list_objects(self):
        all_objects = self.s3.meta.client.list_objects(Bucket=self.s3name)
        if 'Contents' in all_objects:
            for item in all_objects['Contents']:
                print(item.get('Key'))
        # print('--------')
        # for obj in bucket.objects.all():
        #     logging.info('Key: %s' % obj.key)
        # print('*' * 6)
        # for obj in bucket.objects.filter(Prefix="settings/"):
        #     print(obj.key)

    def clear_bucket(self):
        bucket=self.s3.Bucket(self.s3name)
        objects = []
        for obj in bucket.objects.all():
            objects.append({'Key': obj.key})

        response = bucket.delete_objects(
            Delete={
                'Objects': objects
            }
        )
        print(response)

    def upload_directory(self, directory):
        bucket = self.s3.Bucket(self.s3name)
        file_paths = []
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(subdir, file)
                file_paths.append({
                    'Key': full_path[len(directory) + 1:],
                    'full_path':full_path}
                )

        def upload_s3(self, file_info):
            start_time = time.time()
            timedelta = time.time() - start_time
            with open(file_info['full_path'], 'rb') as data:
                bucket.put_object(Key=file_info['Key'], Body=data)
            ret = self.check_object_exists(file_info['Key'])
            while timedelta < self.UPLOAD_TIME_OUT and not ret:
                time.sleep(2)
                ret = self.check_object_exists(file_info['Key'])
                timedelta = time.time() - start_time
            if ret:
                self.uploaded_files_lists.append(self._get_endpoint(file_info['Key']))
            else:
                self.uploaded_files_lists.append('%s uploads failure, timeout' % file_info['Key'])

        thread_list = []
        for file_info in file_paths:
            thread_list.append(threading.Thread(target=upload_s3, args=(self,file_info)))
        for th in thread_list:
            th.start()


    def batch_upload_directory(self, directory_list):
        """
        Uploads the directory to the specific S3 Bucket
        :param file_list:  the python list which contains local file paths.
        :return:
        """
        self.uploaded_files_lists.clear()
        for directory in directory_list:
            self.upload_directory(directory)
