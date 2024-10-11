import boto3

ec2_client = boto3.client(
    'ec2', region_name='us-east-1', endpoint_url='http://localhost:4566'
)

response = ec2_client.run_instances(
    ImageId = 'ami-12345678',
    InstanceType = 't2.micro',
    MinCount = 1,
    MaxCount = 1,
    KeyName = 'flask-ins-key'
)

print(f"Instance created = {response['Instances'][0]['InstanceId']}")