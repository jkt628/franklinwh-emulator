export SHELL:=/bin/bash

.PHONY: install check

install: cert.crt pyproject.toml
	pip install -e .

%.key: Makefile
	openssl genrsa -out $@ 2048
%.csr: %.key %.conf
	openssl req -new -key $(word 1,$^) -out $@ -config $(word 2,$^)
%.crt: %.csr %.key %.conf
	openssl x509 -req -days 365 -out $@ -in $(word 1,$^) -key $(word 2,$^) -extfile <(sed -n /extfile/p $(word 3,$^))
check:: cert.crt
	openssl x509 -in $< -text -noout

# cSpell:words extfile noout
