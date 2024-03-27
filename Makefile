# Automate some testing commands

.PHONY: all unit integration end2end

all: unit integration end2end

unit:
		pytest tests/unit/* -v

integration:
		pytest tests/integration/* -v

end2end:
		pytest tests/end-to-end/* -v
