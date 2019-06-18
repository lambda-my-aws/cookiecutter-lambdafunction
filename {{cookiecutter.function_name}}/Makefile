################################################################################
#
# {{ cookiecutter.function_name }}
#
################################################################################

RM		=		rm -f
ECHO		=		echo -e
TAG		=		etags
PIP		=		pip
PYTHON		=		python3
SHELL		=		/bin/bash

SRC		=		function.py
AWS		=		aws

ifndef VERBOSE
.SILENT:
endif

STACK:=lambda-function-{{ cookiecutter.function_name }}
FUNCTION_NAME:={{ cookiecutter.function_name }}
BUCKET_NAME:={{ cookiecutter.bucket_name }}

all		: venv-install template package publish

venv		:
		test -d venv && $(MAKE) venv-upgrade || $(MAKE) venv-install

venv-create	:
		$(RM) -rf venv/
		test -f venv/bin/activate || python3 -m venv venv

venv-install	: venv-create
		. venv/bin/activate
		$(PIP) install pip --upgrade;
		$(PIP) install -r requirements_dev.txt

venv-upgrade	:
		test -f venv/bin/activate || python3 -m venv venv
		. venv/bin/activate;
		$(PIP) install -r requirements_dev.txt --upgrade


clean-template	:
		$(RM) $(FUNCTION_NAME).yml

clean		: clean-template
		$(RM) $(FUNCTION_NAME).zip


template	: clean-template venv
		python function_template.py

package		:
		clean
		zip -r9 $(FUNCTION_NAME).zip function.py

create		: template publish
		aws cloudformation create-stack --stack-name $(STACK) \
		--template-body file://$(FUNCTION_NAME).yml \
		--capabilities CAPABILITY_IAM

update		:
		aws cloudformation update-stack --stack-name $(STACK) \
		--template-body file://$(FUNCTION_NAME)_packaged.yml \
		--capabilities CAPABILITY_IAM

delete		:
		aws cloudformation delete-stack --stack-name $(STACK)

publish		: template package
		aws s3 cp $(FUNCTION_NAME).zip "s3://$(BUCKET_NAME)/$(FUNCTION_NAME).zip"

events:
		aws cloudformation describe-stack-events \
		--stack-name $(STACK) \
		--region $(AWS_REGION)

watch:
		watch --interval 1 "bash -c 'make events | head -40'"


.PHONY		: all venv upgrade-venv clean clean-template package publish venv venv-install venv-upgrade
