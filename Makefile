# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: run

$(VENV)/bin/activate: requirements.txt
	if !([ -d "venv" ]); then \
	    python3 -m venv $(VENV); \
	    ./$(VENV)/bin/pip3 install -r requirements.txt; \
	fi

# venv is a shortcut target
venv: $(VENV)/bin/activate
	. $(VENV)/bin/activate

run: venv
	$(VENV)/bin/python3 main.py

view_log:
	journalctl -e -u subscription_bot.service

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean