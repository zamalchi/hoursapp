
HOST?=localhost
PORT?=8080

LBLUE=`echo -e "\033[1;34m"`
LGREEN=`echo -e "\033[1;32m"`
PURPLE=`echo -e "\033[35m"`
WHITE=`echo -e "\033[1;37m"`
NORMAL=`echo -e "\033[m"`

# SERVING
# ----------------------------------------------------------------------
run:
	/usr/bin/env python app.py -p $(PORT)

debug:
	/usr/bin/env python app.py -p $(PORT) -d

debug-watch:
	/usr/bin/env python app.py -p $(PORT) -d -r

# mock:
# 	/usr/bin/env python app.py -a $(LHOST) -p $(LPORT) -d -m

# TESTING
# ----------------------------------------------------------------------
# test: test-slurm test-slurm-shell

# test-slurm: clean
# 	/usr/bin/env python -m modu.tests.slurmTest

# test-slurm-shell: clean
# 	/usr/bin/env python -m modu.tests.slurmTestShell

# mock-test: mock-test-slurm mock-test-slurm-shell

# mock-test-slurm: clean
# 	/usr/bin/env python -m modu.tests.mockSlurmTest

# mock-test-slurm-shell: clean
# 	/usr/bin/env python -m modu.tests.mockSlurmTestShell

# COMPILING / TRANSPILING
# ----------------------------------------------------------------------
scss:
	./src/scss/transpiler.sh

scss-watch:
	./src/scss/transpiler.sh --watch

# INSTALL
# ----------------------------------------------------------------------
install:
	sudo ./installers/centos7-installer.sh

# MISC
# ----------------------------------------------------------------------
clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

# HELP
# ----------------------------------------------------------------------
help:
	@echo "${PURPLE}----------------------------------------------------------------------${NORMAL}"
	@echo "    HOST ADDRESS : ${WHITE}http://$(HOST):$(PORT)${NORMAL}"
	@echo "${PURPLE}----------------------------------------------------------------------${NORMAL}"
	@echo "    ${LGREEN}run${NORMAL}"
	@echo "        ${LBLUE}Run the hours server.${NORMAL}"
	@echo "        ${LBLUE}  vars: PORT${NORMAL}"
	@echo "    ${LGREEN}debug${NORMAL}"
	@echo "        ${LBLUE}Run the hours server in debug mode.${NORMAL}"
	@echo "        ${LBLUE}  vars: PORT${NORMAL}"
	@echo "    ${LGREEN}debug-watch${NORMAL}"
	@echo "        ${LBLUE}Run the hours server in debug mode with live reload.${NORMAL}"
	@echo "${PURPLE}----------------------------------------------------------------------${NORMAL}"
	@echo "    ${LGREEN}install${NORMAL}"
	@echo "        ${LBLUE}Installs modules. Only Centos7.${NORMAL}"
	@echo "${PURPLE}----------------------------------------------------------------------${NORMAL}"
	@echo "    ${LGREEN}scss${NORMAL}"
	@echo "        ${LBLUE}Compile scss source files to css static files.${NORMAL}"
	@echo "    ${LGREEN}scss-watch${NORMAL}"
	@echo "        ${LBLUE}Watch for changes and recompile scss.${NORMAL}"
	@echo "${PURPLE}----------------------------------------------------------------------${NORMAL}"
	@echo "    ${LGREEN}clean${NORMAL}"
	@echo "        ${LBLUE}Remove python artifacts.${NORMAL}"
	@echo "${PURPLE}----------------------------------------------------------------------${NORMAL}"

# ----------------------------------------------------------------------

.PHONY: clean test-slurm test-slurm-shell mock-test-slurm mock-test-slurm-shell

# @echo "    ${LGREEN}debug${NORMAL}"
# @echo "        ${LBLUE}Run the slurm server in debug mode.${NORMAL}"
# @echo "        ${LBLUE}  vars: HOST, PORT${NORMAL}"
# @echo "    ${LGREEN}debug-watch${NORMAL}"
# @echo "        ${LBLUE}Run the slurm server in debug mode with live reload.${NORMAL}"
# @echo "    ${LGREEN}mock${NORMAL}"
# @echo "        ${LBLUE}Run the slurm server locally in debug mode and with mock data.${NORMAL}"
# @echo "        ${LBLUE}  vars : LHOST, LPORT${NORMAL}"
# @echo "${PURPLE}----------------------------------------------------------------------${NORMAL}"
# @echo "    ${LGREEN}test${NORMAL}"
# @echo "        ${LBLUE}Run testing suite.${NORMAL}"
# @echo "    ${LGREEN}test-slurm${NORMAL}"
# @echo "        ${LBLUE}Run modu.tests.slurmTest.${NORMAL}"
# @echo "        ${LBLUE}Tests integrity of slurm data parsing.${NORMAL}"
# @echo "    ${LGREEN}test-slurm-shell${NORMAL}"
# @echo "        ${LBLUE}Run modu.tests.slurmTestShell.${NORMAL}"
# @echo "        ${LBLUE}Returns an interactive shell.${NORMAL}"
# @echo "${PURPLE}----------------------------------------------------------------------${NORMAL}"
# @echo "    ${LGREEN}mock-test${NORMAL}"
# @echo "        ${LBLUE}Run testing suite with mock data.${NORMAL}"
# @echo "    ${LGREEN}mock-test-slurm${NORMAL}"
# @echo "        ${LBLUE}Run modu.tests.mockSlurmTest.${NORMAL}"
# @echo "        ${LBLUE}Tests integrity of slurm mock data parsing.${NORMAL}"
# @echo "    ${LGREEN}mock-test-slurm-shell${NORMAL}"
# @echo "        ${LBLUE}Run modu.tests.mockSlurmTestShell.${NORMAL}"
# @echo "        ${LBLUE}Returns an interactive shell.${NORMAL}"