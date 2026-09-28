PYTHON ?= python3
HOST := host/one_shot_proof.py

.PHONY: dry-run syntax lab-test help

help:
	@printf '%s\n' \
	  'make dry-run  - pinned local rootfs audit; no config or network' \
	  'make lab-test - Docker RDP+SMB integration on 127.0.0.1 only'

dry-run:
	$(PYTHON) $(HOST)

syntax:
	$(PYTHON) -m py_compile $(HOST)
	$(PYTHON) -m py_compile lab/client.py lab/server.py
	sh -n lab/entrypoint.sh lab/client.sh lab/healthcheck.sh lab/startwm.sh

lab-test: syntax
	$(PYTHON) $(HOST) --local-selftest
