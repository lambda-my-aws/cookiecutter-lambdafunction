################################################################################
#
# {{ cookiecutter.function_name }}
#
################################################################################

RM			= rm -f
ECHO			= echo -e
TAG			= etags
PIP			= pip
PYTHON			= python3
SHELL			= /bin/bash

SRC			= function.py
AWS			= aws

VENV 			?= .venv
VENV_ACTIVATE		=. $(VENV)/bin/activate

ifndef VERBOSE
.SILENT:
endif

STACK			:=lambda-function-{{ cookiecutter.function_name }}
FUNCTION_NAME		:={{ cookiecutter.function_name }}
BUCKET_NAME		:={{ cookiecutter.bucket_name }}

export VIRTUAL_ENV 	:= $(abspath ${VENV})
export PATH 		:= ${VIRTUAL_ENV}/bin:${PATH}

all			: venv template package


${VENV}			:
			python3 -m venv $@


venv-install		: requirements_dev.txt | ${VENV}
			pip install -U pip
			pip install --upgrade -r requirements_dev.txt

venv			:
			test -d ${VENV} || $(MAKE) venv-install
			$(VENV_ACTIVATE)
			which python


clean-template		:
			$(RM) $(FUNCTION_NAME).yml

clean			: clean-template
			$(RM) $(FUNCTION_NAME).zip


template		: clean-template package $(VENV_ACTIVATE)
			$(AWS) cloudformation package --s3-bucket $(BUCKET_NAME) \
			--template-file function_template.yml \
			--output-template-file $(FUNCTION_NAME).yml

package			: clean
			zip -r9 $(FUNCTION_NAME).zip function.py


create			: template $(VENV_ACTIVATE)
			$(AWS) cloudformation create-stack --stack-name $(STACK) \
			--template-body file://$(FUNCTION_NAME).yml \
			--capabilities CAPABILITY_IAM \
{% if cookiecutter.use_vpc == 'y' %}			--parameters file://function_params.json{% endif %}

update			: template publish $(VENV_ACTIVATE)
			$(AWS) cloudformation update-stack --stack-name $(STACK) \
			--template-body file://$(FUNCTION_NAME).yml \
			--capabilities CAPABILITY_IAM \
{% if cookiecutter.use_vpc == 'y' %}			--parameters file://function_params.json{% endif %}

delete			: clean-template
			$(AWS) cloudformation delete-stack --stack-name $(STACK)

validate		: $(VENV_ACTIVATE)
			$(AWS) cloudformation validate-template \
			--template-body file://$(FUNCTION_NAME).yml

events			: $(VENV_ACTIVATE)
			$(AWS) cloudformation describe-stack-events \
			--stack-name $(STACK) \
			--region $(AWS_REGION)

watch			:
			watch --interval 1 "bash -c 'make events | head -40'"


.PHONY			: all venv venv-install clean clean-template package publish
