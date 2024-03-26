---

### THOUGHT MACHINE

#### Programming Test - Auction House

---

Assumptions:

- All source code, including tests are located inside project directory
- `Python 3.10` was used during development & testing
- Testing framework: `Pytest`
- Program expects a user supplied path to an input file
- Optional `-s`,`--save` flag to persist database between runs
- Program expects a Postgres database to be hosted
- Program expects the user to place their own `config.ini` in project root, specifying DB credentials
- Program can be run from anywhere [!!! make sure this is true !!!]

Quickstart:

- **Run**: `python3 application/main.py path/to/auction_file.txt`
- **Run & keep database state**: `python3 application/main.py -s path/to/auction_continued.txt`
- **Run test suite**: `pytest`
- **Run unit tests**: `pytest tests/unit/*`
- **Run integration tests**: `pytest tests/integration/*`
- **Run end-to-end tests**: `pytest tests/end-to-end/*`
- A

Follow-up:

- Potential augmentation:
  1. A
- Non-exhaustive un-addressed edge cases:
  1. A


