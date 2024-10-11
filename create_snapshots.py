import boto3
from datetime import datetime

ec2_client = boto3.client(
    'ec2', region_name='us-east-1', endpoint_url='http://localhost:4566'
)

instances = ec2_client.describe_instances(
    Filters = [{'Name' : 'instance-state-name', 'Values' : ['running']}]
)

for reservations in instances['Reservations']:
    for instance in reservations['Instances']:
        instance_id = instance['InstanceId']
        volumes = ec2_client.describe_volumes(
            Filters = [{'Name' : 'attachment.instance-id', 'Values' : [instance_id]}]
        )

        for volume in volumes['Volumes']:
            volume_id = volume['VolumeId']
            snapshot = ec2_client.create_snapshot(VolumeId=volume_id)
            print(f"Created snapshot {snapshot['SnapshotId']} for volume {volume_id}")

            ec2_client.create_tags(
                Resources=[snapshot['SnapshotId']],
                Tags=[{
                    'Key' : 'Name',
                    'Value' : f"{instance_id}_backup_{datetime.now().strftime('%Y-%m-%d')}"
                }]
            )
            print(f"Tagged shapshot {snapshot['SnapshotId']} with instance {instance_id}")
