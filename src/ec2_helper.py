# -*- coding: UTF-8 -*-

import re
import boto.ec2
from aws_basic import AWSBasic

class EC2Helper(AWSBasic):

    instances = []
    launch_groups = {}

    RE_STAGING = re.compile('(stage|staging)', re.IGNORECASE)

    def connect(self, access_key, secret_key, region = False):
        """
        Create connection to region
        If region didn't specified - connect to default region

        :type region: str
        :param region: Region to connect
        """
        if not region:
            region = self.REGION

        self.conn = boto.ec2.connect_to_region(region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

        if not self.conn:
            print 'Invalid region name'
            return False

    def __getInstances(self):
        """
        Get instances list from AWS, cache it
        with custom format + create dicts for fast search
        """
        reservations = self.conn.get_all_instances()

        our_instances = []

        for reservation in reservations:
            for instance in reservation.instances:
                our_instances.append(instance)

        self.instances = our_instances

    def getInstanceStatuses(self):
        
        self.__getInstances()

        instances = []

        for instance in self.instances:

            if 'Name' in instance.tags:

                instance_name = instance.tags['Name']

                if re.search(self.RE_STAGING, instance_name):
                    instances.append({
                        'name': instance_name,
                        'state': instance.state,
                        'state_code': instance.state_code
                    })

        return instances
