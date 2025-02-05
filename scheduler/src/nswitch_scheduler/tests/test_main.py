import json

import boto3
from main import HANDLER_MAP
from main import lambda_handler
from main import modify_db_instance
from main import start_ec2_instance
from main import start_rds_instance
from main import stop_ec2_instance
from main import stop_rds_instance
from main import update_ec2_auto_scaling
from moto import mock_autoscaling
from moto import mock_ec2
from moto import mock_rds

from .conftest import AUTOSCALING_LAMBDA_EVENT

EXAMPLE_AMI_ID = "ami-12c6146b"
DEFAULT_ACCOUNT_ID = "123456789012"
LAMBDA_EVENT = {
    "version": "0",
    "id": "6739aa2f-3b23-095d-5ae7-9a7bf8f0b058",
    "detail-type": "nops_scheduler_start_stop",
    "source": "aws.partner/nops.io/12345677901/nops_uat_notification_12_TrucCF1",
    "account": "12345677901",
    "time": "2022-10-21T07:11:28Z",
    "region": "us-west-2",
    "resources": [
        "arn:aws:rds:us-west-2:12345677901:db:database-running-for-dev-scheduler"
    ],
    "detail": {
        "event_type": "scheduler_start_stop",
        "action": "stop",
        "action_id": 535,
        "scheduler": {
            "id": "16c431f5-0555-466f-9768-be03b7d2c26b",
            "client": 12,
            "project": 14,
            "user": 569,
            "name": "test RDs",
            "account_number": "12345677901",
            "resources": [
                {
                    "id": 417,
                    "created": "2022-10-21T07:11:22.975738Z",
                    "modified": "2022-10-21T07:11:22.975738Z",
                    "item_type": "rds",
                    "item_id": "3c2da54fb707d702c354eee752c03f7c",
                    "resource_id": "arn:aws:rds:us-west-2:12345677901:db:database-running-for-dev-scheduler",
                    "resource_name": "database-running-for-dev-scheduler",
                    "resource_arn": None,
                    "state": "active",
                    "region": "us-west-2",
                    "scheduler": "16c431f5-0555-466f-9768-be03b7d2c26b",
                }
            ],
            "actions": [
                {
                    "id": 535,
                    "created": "2022-10-20T09:58:18.559741Z",
                    "modified": "2022-10-21T07:11:22.974020Z",
                    "action": "start",
                    "action_type": "selected_day_of_week",
                    "day_of_week": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
                    "hour": 8,
                    "minute": 0,
                    "state": "active",
                    "last_run": None,
                    "last_manual_trigger": None,
                    "scheduler": "16c431f5-0555-466f-9768-be03b7d2c26b",
                },
                {
                    "id": 536,
                    "created": "2022-10-20T09:58:18.561810Z",
                    "modified": "2022-10-21T07:11:22.975023Z",
                    "action": "stop",
                    "action_type": "selected_day_of_week",
                    "day_of_week": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
                    "hour": 20,
                    "minute": 0,
                    "state": "active",
                    "last_run": None,
                    "last_manual_trigger": None,
                    "scheduler": "16c431f5-0555-466f-9768-be03b7d2c26b",
                },
            ],
            "state": "active",
            "eventbridge_configuration": "46a55424-0f38-4d2f-bcb4-7bd2b697c0e9",
        },
    },
}


def test_get_handler_map():
    assert HANDLER_MAP["ec2"]["start"]
    assert HANDLER_MAP["ec2"]["stop"]
    assert HANDLER_MAP["rds"]["start"]
    assert HANDLER_MAP["rds"]["stop"]
    assert HANDLER_MAP["rds_cluster"]["start"]
    assert HANDLER_MAP["rds_cluster"]["stop"]
    assert HANDLER_MAP["autoscaling_groups"]["start"]
    assert HANDLER_MAP["autoscaling_groups"]["stop"]
    assert HANDLER_MAP["autoscaling_groups"]["update_ec2_auto_scaling"]
    assert HANDLER_MAP["eks_nodegroup"]["start"]
    assert HANDLER_MAP["eks_nodegroup"]["stop"]


@mock_ec2
def test_start_stop_instance():
    ec2 = boto3.resource("ec2", region_name="us-east-1")
    reservation = ec2.create_instances(ImageId=EXAMPLE_AMI_ID, MinCount=2, MaxCount=2)
    instance1, instance2 = reservation
    assert instance1.state["Name"] == "pending"

    resource = {"resource_id": instance1.id, "region": "us-east-1"}
    result = start_ec2_instance(resource)
    assert result.startswith("Given EC2 instance is started")

    resource = {"resource_id": instance2.id, "region": "us-east-1"}
    result = stop_ec2_instance(resource)
    assert result.startswith("Given EC2 instance is stopped")
    instances = ec2.instances.all()
    for instance in instances:

        if instance.id == instance1.id:
            assert instance.state["Name"] == "running"
        elif instance.id == instance2.id:
            assert instance.state["Name"] == "stopped"
        else:
            assert False, "Invalid instance id"


@mock_rds
def test_stop_start_rds():
    conn = boto3.client("rds", region_name="us-west-2")
    database = conn.create_db_instance(
        DBInstanceIdentifier="db-master-1",
        AllocatedStorage=10,
        Engine="postgres",
        DBName="staging-postgres",
        DBInstanceClass="db.m1.small",
        LicenseModel="license-included",
        MasterUsername="root",
        MasterUserPassword="hunter2",
        Port=1234,
        DBSecurityGroups=["my_sg"],
        VpcSecurityGroupIds=["sg-123456"],
        EnableCloudwatchLogsExports=["audit", "error"],
    )
    db_instance = database["DBInstance"]
    assert db_instance["DBInstanceStatus"] == "available"
    resource = {"resource_id": db_instance["DBInstanceArn"], "region": "us-west-2"}
    result = stop_rds_instance(resource)
    assert result.startswith("Given RDS instance is stopped")
    mydb = conn.describe_db_instances(
        DBInstanceIdentifier=database["DBInstance"]["DBInstanceIdentifier"]
    )["DBInstances"][0]
    assert mydb["DBInstanceStatus"] == "stopped"
    result = start_rds_instance(resource)
    assert result.startswith("Given RDS instance is started")
    mydb = conn.describe_db_instances(
        DBInstanceIdentifier=database["DBInstance"]["DBInstanceIdentifier"]
    )["DBInstances"][0]
    assert mydb["DBInstanceStatus"] == "available"


@mock_rds
def test_lambda_handler():
    conn = boto3.client("rds", region_name="us-west-2")
    conn.create_db_instance(
        DBInstanceIdentifier="database-running-for-dev-scheduler",
        AllocatedStorage=10,
        Engine="postgres",
        DBName="staging-postgres",
        DBInstanceClass="db.m1.small",
        LicenseModel="license-included",
        MasterUsername="root",
        MasterUserPassword="hunter2",
        Port=1234,
        DBSecurityGroups=["my_sg"],
        VpcSecurityGroupIds=["sg-123456"],
        EnableCloudwatchLogsExports=["audit", "error"],
    )

    result = lambda_handler(LAMBDA_EVENT, {})
    message = json.loads(result["Message"])
    assert (
        message["results"][0]
        == "Given RDS instance is stopped - database-running-for-dev-scheduler"
    )


@mock_autoscaling
@mock_ec2
def test_update_autoscaling():
    conn = boto3.client("autoscaling", region_name="us-east-1")

    conn.create_launch_configuration(
        LaunchConfigurationName="TestLC",
        ImageId=EXAMPLE_AMI_ID,
        InstanceType="t2.medium",
    )

    conn.create_auto_scaling_group(
        AutoScalingGroupName="TestGroup1",
        MinSize=1,
        DesiredCapacity=6,
        MaxSize=10,
        LaunchConfigurationName="TestLC",
        AvailabilityZones=["us-east-1e"],
        Tags=[
            {
                "ResourceId": "arn:TestGroup1",
                "ResourceType": "auto-scaling-group",
                "PropagateAtLaunch": True,
                "Key": "TestTagKey1",
                "Value": "TestTagValue1",
            }
        ],
    )
    resource = {
        "resource_id": "TestGroup1",
        "region": "us-east-1",
        "resource_name": "TestGroup1",
    }
    action_details = {"DesiredCapacity": 3}
    update_ec2_auto_scaling(resource, action_details)
    details = conn.describe_auto_scaling_groups(AutoScalingGroupNames=["TestGroup1"])
    assert details["AutoScalingGroups"][0]["DesiredCapacity"] == 3


@mock_autoscaling
@mock_ec2
def test_handle_autoscaling():
    conn = boto3.client("autoscaling", region_name="us-east-1")

    conn.create_launch_configuration(
        LaunchConfigurationName="TestLC",
        ImageId=EXAMPLE_AMI_ID,
        InstanceType="t2.medium",
    )

    conn.create_auto_scaling_group(
        AutoScalingGroupName="JENKINS-SLAVE-TEST",
        MinSize=1,
        DesiredCapacity=6,
        MaxSize=10,
        LaunchConfigurationName="TestLC",
        AvailabilityZones=["us-east-1e"],
        Tags=[
            {
                "ResourceId": "JENKINS-SLAVE-TEST",
                "ResourceType": "auto-scaling-group",
                "PropagateAtLaunch": True,
                "Key": "TestTagKey1",
                "Value": "TestTagValue1",
            }
        ],
    )
    result = lambda_handler(AUTOSCALING_LAMBDA_EVENT, {})
    message = json.loads(result["Message"])
    assert (
        message["results"][0] == "Given auto scaling group updated - JENKINS-SLAVE-TEST"
    )


@mock_rds
def test_modify_rds():
    conn = boto3.client("rds", region_name="us-west-2")
    database = conn.create_db_instance(
        DBInstanceIdentifier="db-master-1",
        AllocatedStorage=10,
        Engine="aurora",
        DBName="staging-postgres",
        DBInstanceClass="db.r3",
        LicenseModel="license-included",
        MasterUsername="root",
        MasterUserPassword="hunter2",
        Port=1234,
        DBSecurityGroups=["my_sg"],
        VpcSecurityGroupIds=["sg-123456"],
        EnableCloudwatchLogsExports=["audit", "error"],
    )
    db_instance = database["DBInstance"]
    assert db_instance["DBInstanceStatus"] == "available"
    resource = {"resource_id": db_instance["DBInstanceArn"], "region": "us-west-2"}
    mydb = conn.describe_db_instances(
        DBInstanceIdentifier=database["DBInstance"]["DBInstanceIdentifier"]
    )["DBInstances"][0]
    assert mydb["DBInstanceStatus"] == "available"

    modify_db_instance(
        resource, action_details={"DBInstanceClass": "db.r5", "ApplyImmediately": True}
    )
    mydb = conn.describe_db_instances(
        DBInstanceIdentifier=database["DBInstance"]["DBInstanceIdentifier"]
    )["DBInstances"][0]


@mock_ec2
def test_hibernate_instance():
    ec2 = boto3.resource("ec2", region_name="us-east-1")
    reservation = ec2.create_instances(ImageId=EXAMPLE_AMI_ID, MinCount=2, MaxCount=2)
    instance1, instance2 = reservation
    assert instance1.state["Name"] == "pending"

    resource = {"resource_id": instance2.id, "region": "us-east-1"}
    result = stop_ec2_instance(resource, action_details={"Hibernate": True})
    assert result.startswith("Given EC2 instance is stopped")
    instances = ec2.instances.all()
    for instance in instances:

        if instance.id == instance1.id:
            assert instance.state["Name"] == "running"
        elif instance.id == instance2.id:
            assert instance.state["Name"] == "stopped"
        else:
            assert False, "Invalid instance id"
