#Makefile

Dockerfile_fastapi = Dockerfile
SETTING_FILE = dep.yml
IMAGE = fastimage
# CONTAINER = fastcontainer
REPO_NAME = kangaroo-0000/rsa-auth

all: docker_build docker_run

docker_build:
	@docker build -f $(Dockerfile_fastapi) -t $(IMAGE) .

docker_run: docker_build
	@docker-compose -f $(SETTING_FILE) up -d

docker_clean:
	@docker-compose stop  -f $(SETTING_FILE)
	@docker-compose rm -f $(SETTING_FILE)

ori_down_run:
	@docker-compose -f $(SETTING_FILE) down


