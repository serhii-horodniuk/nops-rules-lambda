AUTOSCALING_LAMBDA_EVENT = {
    "version": "0",
    "id": "601dce79-d826-6d29-8ae5-08f9b3144315",
    "detail-type": "nops_scheduler_start_stop",
    "source": "aws.partner/nops.io/12345677901/nops_uat_notification_14875_nopsqa-UAT-demo",
    "account": "12345677901",
    "time": "2022-12-05T20:00:00Z",
    "region": "eu-north-1",
    "resources": [
        "arn:aws:autoscaling:us-east-1:12345677901:autoScalingGroup:71f448aa-8436-4cdb-888e-b9d417bb12c8:autoScalingGroupName/JENKINS-SLAVE-TEST"
    ],
    "detail": {
        "event_type": "scheduler_start_stop",
        "action": "update_ec2_auto_scaling",
        "action_details": {"DesiredCapacity": 2},
        "action_id": 607,
        "event_timestamp": 1.6702704e9,
        "scheduler": {
            "id": "db140d55-bb88-4283-b24f-5fbb8e528598",
            "client": 14875,
            "project": 17637,
            "user": 3127,
            "name": "liza-5 dec-dynamic",
            "account_number": "12345677901",
            "resources": [
                {
                    "id": 535,
                    "created": "2022-12-05T19:17:25.311392Z",
                    "modified": "2022-12-05T19:17:25.311392Z",
                    "item_type": "autoscaling_groups",
                    "item_id": "1234556",
                    "resource_id": "arn:aws:autoscaling:us-east-1:12345677901:autoScalingGroup:71f448aa-8436-4cdb-888e-b9d417bb12c8:autoScalingGroupName/JENKINS-SLAVE-TEST",
                    "resource_name": "JENKINS-SLAVE-TEST",
                    "resource_arn": None,
                    "state": "active",
                    "region": "us-east-1",
                    "scheduler": "db140d55-bb88-4283-b24f-5fbb8e528598",
                }
            ],
            "actions": [
                {
                    "id": 607,
                    "created": "2022-12-05T19:17:25.308255Z",
                    "modified": "2022-12-05T19:17:25.308255Z",
                    "action": "update_auto_scaling_group",
                    "action_details": {"DesiredCapacity": 2},
                    "action_type": "selected_day_of_week",
                    "day_of_week": ["mon"],
                    "hour": 20,
                    "minute": 0,
                    "state": "active",
                    "last_run": None,
                    "last_manual_trigger": None,
                    "run_date": None,
                    "scheduler": "db140d55-bb88-4283-b24f-5fbb8e528598",
                },
                {
                    "id": 608,
                    "created": "2022-12-05T19:17:25.310165Z",
                    "modified": "2022-12-05T19:17:25.310165Z",
                    "action": "update_auto_scaling_group",
                    "action_details": {"DesiredCapacity": 3},
                    "action_type": "selected_day_of_week",
                    "day_of_week": ["mon"],
                    "hour": 8,
                    "minute": 0,
                    "state": "active",
                    "last_run": None,
                    "last_manual_trigger": None,
                    "run_date": None,
                    "scheduler": "db140d55-bb88-4283-b24f-5fbb8e528598",
                },
            ],
            "state": "active",
            "eventbridge_configuration": "1e17e4ad-1590-4401-baf6-d0a472394c0b",
            "scheduler_for": "scheduler_start_stop",
        },
        "triggered_by": "automatically",
    },
}

NODEGROUP_START_LAMBDA_EVENT = {
    "version": "0",
    "id": "601dce79-d826-6d29-8ae5-08f9b3144315",
    "detail-type": "nops_scheduler_start_stop",
    "source": "aws.partner/nops.io/12345677901/nops_uat_notification_14875_nopsqa-UAT-demo",
    "account": "12345677901",
    "time": "2022-12-05T20:00:00Z",
    "region": "eu-north-1",
    "resources": [],
    "detail": {
        "event_type": "scheduler_start_stop",
        "action": "start",
        "action_id": 607,
        "event_timestamp": 1.6702704e9,
        "scheduler": {
            "id": "db140d55-bb88-4283-b24f-5fbb8e528598",
            "client": 14875,
            "project": 17637,
            "user": 3127,
            "name": "liza-5 dec-dynamic",
            "account_number": "12345677901",
            "resources": [],
            "actions": [],
            "state": "active",
            "eventbridge_configuration": "1e17e4ad-1590-4401-baf6-d0a472394c0b",
            "scheduler_for": "scheduler_start_stop",
        },
        "triggered_by": "automatically",
    },
}


AUTOSCALING_EVENT = {
    "version": "0",
    "id": "42ed2209-7690-948f-3fa6-2b77211d0268",
    "detail-type": "nops_scheduler_start_stop",
    "source": "aws.partner/nops.io/202279780353/nops_prod_notification_4725_ASG_EV",
    "account": "202279780353",
    "time": "2023-03-07T15:59:53Z",
    "region": "us-east-1",
    "resources": [
        "arn:aws:autoscaling:us-east-1:202279780353:autoScalingGroup:6a903e38-d58a-43f6-85dc-ac3172bebfab:autoScalingGroupName/autoscaling-test-3-default-20221206162356365000000008"
    ],
    "detail": {
        "event_type": "scheduler_start_stop",
        "action": "start",
        "action_details": {},
        "action_id": 3246,
        "event_timestamp": 1678204793.0,
        "scheduler": {
            "id": "84967221-f99f-4be7-8f70-342f8ed08c0b",
            "client": 4725,
            "project": 24770,
            "user": 6958,
            "name": ">0 DESIRED CAPACITY ASG",
            "account_number": "202279780353",
            "resources": [
                {
                    "id": 6243,
                    "created": "2023-03-06T20:05:41.569396Z",
                    "modified": "2023-03-06T20:05:41.569396Z",
                    "item_type": "autoscaling_groups",
                    "item_id": "ff82fdf5f51a554ebeb385167e1e66a3",
                    "resource_id": "arn:aws:autoscaling:us-east-1:202279780353:autoScalingGroup:6a903e38-d58a-43f6-85dc-ac3172bebfab:autoScalingGroupName/autoscaling-test-3-default-20221206162356365000000008",
                    "resource_name": "autoscaling-test-3-default-20221206162356365000000008",
                    "resource_arn": None,
                    "state": "active",
                    "region": "us-east-1",
                    "resource_details": {
                        "MaxSize": 15,
                        "MinSize": 0,
                        "DesiredCapacity": 12,
                    },
                    "scheduler": "84967221-f99f-4be7-8f70-342f8ed08c0b",
                }
            ],
            "actions": [
                {
                    "id": 3245,
                    "position": 131,
                    "created": "2023-03-06T20:05:41.566851Z",
                    "modified": "2023-03-07T15:57:58.365986Z",
                    "action": "stop",
                    "action_details": {},
                    "action_type": "selected_day_of_week",
                    "day_of_week": ["sat"],
                    "hour": 11,
                    "minute": 0,
                    "state": "active",
                    "last_run": None,
                    "last_manual_trigger": "2023-03-07T15:57:58.013513Z",
                    "run_date": None,
                    "scheduler": "84967221-f99f-4be7-8f70-342f8ed08c0b",
                },
                {
                    "id": 3246,
                    "position": 132,
                    "created": "2023-03-06T20:05:41.568312Z",
                    "modified": "2023-03-07T15:54:19.369050Z",
                    "action": "start",
                    "action_details": {},
                    "action_type": "selected_day_of_week",
                    "day_of_week": ["sat"],
                    "hour": 12,
                    "minute": 0,
                    "state": "active",
                    "last_run": None,
                    "last_manual_trigger": "2023-03-07T15:54:19.026043Z",
                    "run_date": None,
                    "scheduler": "84967221-f99f-4be7-8f70-342f8ed08c0b",
                },
            ],
            "state": "active",
            "eventbridge_configuration": "7ee87fc6-5c8f-4ae6-8a2d-6b49d8c1a337",
            "scheduler_for": "scheduler_start_stop",
            "description": "",
            "recommendation_hash": "",
        },
        "triggered_by": "manually",
    },
}
