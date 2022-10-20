import requests
from pulumi_policy import (
    EnforcementLevel,
    PolicyPack,
    ReportViolation,
    ResourceValidationArgs,
    ResourceValidationPolicy,
    PolicyConfigSchema
)


def map_swag_to_form(swag_var):
    data_json = {
        'usp': 'pp_url'
    }
    swag = swag_var
    data_json['entry.1720843992'] = swag['name']
    data_json['entry.511943887'] = swag['email']
    data_json['entry.1289952319'] = swag['address']
    data_json['entry.1240089905'] = swag['size']
    return data_json


def pulumi_swag_not_submitted(args: ResourceValidationArgs, report_violation: ReportViolation):
    if not args.resource_type == "pulumi:pulumi:Stack":
        return
    swag = args.get_config()
    data_dict = map_swag_to_form(swag)
    print(data_dict)
    headers = {
        "Referer": "https://docs.google.com/forms/d/e/1FAIpQLSfBr2f6rhXYbMXi8Caftu-zWtNPRDoWUEukrTJKuwO3OyYRvg/viewform",
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
    }
    response = requests.post(
        url="https://docs.google.com/forms/d/e/1FAIpQLSfBr2f6rhXYbMXi8Caftu-zWtNPRDoWUEukrTJKuwO3OyYRvg/formResponse",
        headers=headers,
        data=data_dict
    )
    print(response.status_code)


submit_swag = ResourceValidationPolicy(
    name="pulumi-challenge-swag",
    description="stuff",
    validate=pulumi_swag_not_submitted,
    config_schema=PolicyConfigSchema(
        properties={
            "name": {
                "type": "string",
                "minLength": 2
            },
            "email": {
                "type": "string",
                "minLength": 6,
                "format": "email"
            },
            "address": {
                "type": "string",
                "minLength": 2
            },
            "size": {
                "type": "string",
                "minLength": 1,
                "enum": [
                    "XS",
                    "S",
                    "M",
                    "L",
                    "XL"
                ]
            }
        },
        required=[
            "name",
            "email",
            "address",
            "size"
        ]
    )
)

PolicyPack(
    name="aws-python",
    enforcement_level=EnforcementLevel.MANDATORY,
    policies=[
        submit_swag
    ],
)