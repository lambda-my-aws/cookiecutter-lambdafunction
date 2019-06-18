# -*- coding: utf-8 -*-

"""{{ cookiecutter.function_name }} Template"""

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from troposphere import (
    Parameter,
    Condition,
    Template,
    Equals,
    GetAtt,
    Sub,
    Ref
)

from troposphere.awslambda import (
    Function,
    LayerVersion,
    Permission,
    Alias,
    Version,
    Code,
    Environment
)

from ozone.resources.iam.roles import role_trust_policy
from ozone.templates.awslambda import lambda_function
import yaml

with open('function_config.yml', 'r') as fd:
    CONFIG = yaml.load(fd.read(), Loader=Loader)

TPL = Template('Template for function {{ cookiecutter.function_name}}')

RELEASE = TPL.add_parameter(Parameter(
    'ReleaseNewAlias',
    Type="String",
    AllowedValues = ['True', 'False'],
    Default = 'False'
))

ALIAS_NAME = TPL.add_parameter(Parameter(
    'NewAliasName',
    Type="String",
    AllowedValues = ['True', 'False'],
    Default = 'False'
))

RELEASE_CON = TPL.add_condition(
    'ReleaseAlias',
    {
        'ReleaseAlias': Equals(
            Ref(RELEASE),
            'True'
        )
    }
)

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
TPL.add_resource(ROLE)
{% endif %}

FUNCTION = lambda_function(**CONFIG)
TPL.add_resource(FUNCTION)

VERSION = TPL.add_resource(Version(
    'LambdaVersion',
    FunctionName=GetAtt(FUNCTION, 'Arn')
))

ALIAS = TPL.add_resource(Alias(
    'LambdaAlias',
    Name = Ref(ALIAS_NAME),
    DependsOn = [RELEASE_CON],
    Description = Sub({%raw%}f'Alias to version ${{{VERSION.title}}}'){%endraw%},
    FunctionName = Ref(FUNCTION),
    FunctionVersion = Ref(VERSION)
))

with open("{{cookiecutter.function_name }}.yml", 'w') as fd:
    fd.write(TPL.to_yaml())
