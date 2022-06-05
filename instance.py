import boto3


class Instance:
    region = "eu-central-1"
    ec2 = boto3.client('ec2', region_name=region)

    def __init__(self, image_id="", instance_type="", min_count=1, max_count=1, tags=None, tenant=""):
        self.tenant = tenant
        if tags is None:
            tags = []
        self.tags = tags
        self.instance_type = instance_type
        self.max = max_count
        self.min = min_count
        self.image_id = image_id

    def create_key_pair(self):
        response = self.ec2.create_key_pair(KeyName=self.tenant)
        return response['KeyMaterial']

    def get_vpc(self):
        response = self.ec2.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    def create_security_group(self, ports=[80]):
        self.ec2.create_security_group(
            Description=f"Security group for {self.tenant} tenant EC2 instance",
            GroupName=f"{self.tenant}-sg",
            VpcId='string',
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'tenant',
                            'Value': self.tenant
                        },
                    ]
                },
            ]
        )

    def create_instances(self):
        private_key = self.create_key_pair()
        ec2 = boto3.resource('ec2', region_name=self.region)
        instances = ec2.create_instances(
            ImageId=self.image_id,
            MinCount=self.min,
            MaxCount=self.max,
            InstanceType=self.instance_type,
            KeyName=self.tenant,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{
                    'Key': "tenant",
                    "Value": self.tenant
                }]
            }]
        )
        for instance in instances:
            instance.wait_until_running()
        instance_ids = [i.id for i in instances]
        return {'instances': instance_ids, 'private_key': private_key}
