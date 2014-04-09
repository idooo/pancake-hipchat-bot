# -*- coding: UTF-8 -*-

class AWSBasic():

    REGION = 'ap-southeast-2'

    ZONE = 'ap-southeast-2a'
    RESERVED_ZONE = 'ap-southeast-2b'

    conn = False

    def __init__(self, aws_access_key_id, aws_secret_access_key, region=False):
        if region:
            self.REGION = region

        self.connect(aws_access_key_id, aws_secret_access_key, region)

    def connect(self, aws_access_key_id, aws_secret_access_key, region=False):
        pass