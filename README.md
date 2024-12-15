## Programming Exercise - Auction House


Notes:

- All source code, including tests are located inside project directory
- `Python 3.10` was used during development & testing
- Test framework: `Pytest`
- Program expects a user supplied path to an input file
- Optional `-s`,`--save` flag to persist database state between runs
- Program expects a **Postgres database to be hosted**, (e.g. via Docker)
- Program expects user supplied `config.ini` in project root, specifying DB credentials

Quickstart:

- **Install**: `make`
- **Run**: `python3 application/main.py path/to/auction_file.txt`
- **Keep data from previous run**: `python3 application/main.py -s path/to/continue_auction.txt`
- **Run test suite**: `pytest`
- **Run unit tests**: `pytest tests/unit/*`
- **Run integration tests**: `pytest tests/integration/*`
- **Run end-to-end tests**: `pytest tests/end-to-end/*`
- <details>
  <summary>Coverage Report</summary>
  <pre>
  Name                           Stmts   Miss  Cover
  --------------------------------------------------
  application/auction.py            58      7    88%
  application/config.py             12      1    92%
  application/db_procedures.py      92     13    86%
  --------------------------------------------------
  TOTAL                            162     21    87%
  </pre>
  </details>

Follow-up:

- <details> 
  <summary>Untested code:</summary>
  <ul>
    <li><code>config.py</code></li>
    <li><code>check_no_bids()</code></li>
  </ul>
  </details>
- <details>
  <summary>Non-exhaustive un-addressed edge cases:</summary>
  <ol>
    <li>Bids with the same amount from the same user</li>
    <li>Bids placed before auction starts</li>
    <li>Decreasing bid amounts from the same user</li>
    <li>Multiple auctions for the same item</li>
    <li>Edge Case in bid increments</li>
  </ol>
  </details>
- <details>
  <summary>Potential augmentation:</summary>
  <ul>
    <li>Error logging</li>
    <li>Refactor to allow for better dependency injection during testing</li>
    <li>Decoupling application logic and implementing a Database Abstraction Layer</li>
  </ul>
  </details>

  


