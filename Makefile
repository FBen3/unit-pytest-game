# Automate some testing commands

.PHONY: all unit integration end2end

all: install

install:
		pip install -r requirements.txt

test: unit integration end2end

unit:
		pytest tests/unit/* -v

integration:
		pytest tests/integration/* -v

end2end:
		pytest tests/end-to-end/* -v
