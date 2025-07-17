export CWD 	:= $(shell pwd)

VDIR = $(CWD)/venv
PYTHON = $(VDIR)/bin/python3

$(VERBOSE).SILENT:
.KEEP_STATE:

define log
[ "$<" ] && \
	( printf "Makelog %-30s %-30s %s\n" "$@" "$<" "$(1)" )\
	|| ( printf "Makelog %-10s %s\n" "$@" "$(1)" )
endef

.PHONY: all clean install _virtualenv

# On Debian/Ubuntu systems, you need to install the python3-venv
# package using the following command.
#     apt install python3.11-venv
# You may need to use sudo with that command.  After installing the python3-venv
# package, recreate your virtual environment.
_virtualenv:
	$(call log,Creating virtual environment)
	@which python3 >/dev/null 2>&1 || ( echo "Python3 is not installed. Please install Python3." && exit 1 )
	@which pip3 >/dev/null 2>&1 || ( echo "Pip3 is not installed. Please install Pip3." && exit 1 )
	@which virtualenv >/dev/null 2>&1 || ( echo "Virtualenv is not installed. Please install Virtualenv." && exit 1 )

	python3 -m venv $(VDIR)
	$(PYTHON) -m pip install --upgrade pip
	
	. $(VDIR)/bin/activate

clean:
	$(call log,Cleaning up)
	rm -rf $(VDIR)
	rm -rf $(CWD)/__pycache__
	rm -rf $(CWD)/.pytest_cache
	rm -rf $(CWD)/.mypy_cache
	rm -rf $(CWD)/.coverage
	rm -rf $(CWD)/.coverage.*
	rm -f $(CW)/coverage.xml
	rm -f $(CWD)/htmlcov
	rm -rf $(CWD)/*.egg-info

install: clean _virtualenv
	$(call log, "Installing dependencies")
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .

.PHONY: zk
zk:
	$(call log,Entering Zookeeper container)
	sudo docker exec -it zookeeper /bin/bash
