# Makefile
# 	# docker run -p 8888:8888 -t afcda/ds-sandbox:latest 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


COLOR_RED		=	\033[1;31m
COLOR_GREEN		=	\033[1;32m
COLOR_RESET		=	\033[0m

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@printf "$(COLOR_GREEN)	build $(COLOR_RESET)			to build container for ENV={env} \n"
	@printf "$(COLOR_GREEN)	run $(COLOR_RESET)			run competition-seasons dev environment task in ECS \n"


build:
	@printf "$(COLOR_RED)	Building Docker image $(COLOR_RESET) \n"
	docker build -f Dockerfile -t afcda/ds-sandbox:latest .
	
	@echo

run: build
	@printf "$(COLOR_RED)	Running Docker image $(COLOR_RESET) \n"

	docker run -it --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work afcda/ds-sandbox:latest
