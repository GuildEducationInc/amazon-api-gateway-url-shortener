.DEFAULT_GOAL := default

FUNCTION=comms-url-shortener
REGION=us-west-2
ENVIRONMENT_NAME = $(firstword $(subst -, ,$(STAGE)))
S3_BUCKET="guild-$(ENVIRONMENT_NAME)-lambda-artifacts-$(REGION)"
STACK_NAME="$(FUNCTION)-$(REGION)-$(STAGE)"

default:
	@echo Please specify a target.

install:
	@pip install --upgrade pip
	@pip install -r src/requirements.txt

install.test: install
	@pip install -r requirements-test.txt

test:
	@PYTHONPATH=./src:../common/src pytest tests

lint:
	mypy ./src --config-file mypy.ini
	pylint ./src
	black --check ./src ./tests
	isort --check-only ./src ./tests

format:
	isort ./src ./tests
	black ./src ./tests

build:
	@rm -fr .dist
	@mkdir .dist
	# @cd ../common && make build
	# @cp -R ../common/.dist/* .dist/
	@cp -R src/* .dist/
	@sam build

package: build
	@if test -z "$(STAGE)"; then echo "*** STAGE not set. Set STAGE with: export STAGE=env ***"; exit 1; fi
	sam package \
	--s3-bucket $(S3_BUCKET) \
	--output-template-file "package.$(STAGE).yaml"

deploy:
	sam deploy \
	--no-fail-on-empty-changeset \
	--template-file "package.$(STAGE).yaml" \
	--stack-name $(STACK_NAME) \
	--capabilities CAPABILITY_NAMED_IAM \
	--region $(REGION) \
	--parameter-overrides 'EnvironmentName=$(ENVIRONMENT_NAME) StageName=$(STAGE)'
