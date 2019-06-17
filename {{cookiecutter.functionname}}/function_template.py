# -*- coding: utf-8 -*-

"""{{ cookiecutter.functionname }} Template"""

from troposphere import (
    Parameter,
    Template,
    GetAtt,
    Sub,
    Ref
)

from ozone.templates.awslambda import template
from ozone.resources.iam.roles import role_trust_policy

{% if cookiecutter.create_role %}
from troposphere.iam import Role
ROLE = Role(
    'LambdaFunctionRole',
    AssumeRolePolicyDocument=role_trust_policy('lambda'),
    ManagedPolicyArns=[
        'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    ],
    ### ADD POLICIES HERE ###
    # Policies=[]
)
TPL = template(Role=ROLE, Runtime="{{ cookiecutter.runtime }}")
TPL.add_resource(ROLE)
{% else %}

TPL = template(Runtime="{{ cookiecutter.runtime }}")
{% endif %}

with open("{{cookiecutter.functionname }}.yml", 'w') as fd:
    fd.write(TPL.to_yaml())
