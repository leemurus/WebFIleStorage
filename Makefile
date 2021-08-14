ROOT_DIR:=$(shell pwd)

TARGET_PYTHON_VERSION := python3.9

VENV_DIR := $(ROOT_DIR)/.venv
VENV_PIP := $(VENV_DIR)/bin/pip
VENV_PYTHON := $(VENV_DIR)/bin/python

REQUIREMENTS_FILE := $(ROOT_DIR)/requirements.txt
START_FILE := $(ROOT_DIR)/main.py

.PHONY:run
run: venv
	$(VENV_PYTHON) $(START_FILE)

.PHONY: venv
venv: $(VENV_DIR)
	echo $(ROOT_DIR)
	$(VENV_PIP) install -r $(REQUIREMENTS_FILE)

$(VENV_DIR):
	virtualenv --python=$(TARGET_PYTHON_VERSION) $(VENV_DIR)