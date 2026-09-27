# Stock Market Simulator

[![CI](https://github.com/DylanThomas22/stock-market-simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/DylanThomas22/stock-market-simulator/actions/workflows/ci.yml)

A command-line paper-trading application built with Python. It retrieves current stock data from Finnhub, executes simulated buy and sell transactions, calculates portfolio performance, and persists each local portfolio as JSON.

> This project uses simulated money and does not place real trades.

## Features

- Start each local portfolio with $100,000 in simulated cash
- Look up stock prices and company names through the Finnhub REST API
- Buy whole or fractional shares
- Track weighted-average cost basis when adding to a position
- Sell partial or complete positions
- Calculate realized and unrealized profit/loss
- View current holdings and total account value
- Persist portfolios and transaction history between sessions
- Keep API credentials and user-generated data out of version control
- Validate core behavior automatically with GitHub Actions

## Example

~~~text
========== PORTFOLIO ==========
Cash Balance: $99,800.00

Ticker   | Company              |     Shares |     Avg Cost |      Current
EXMP     | Example Corp         |       2.00 | $     100.00 | $     125.00

Total Positions:      1
Total Invested:       $200.00
Current Stock Value:  $250.00
Unrealized P/L:       $50.00
Cash Balance:         $99,800.00
Total Account Value:  $100,050.00
~~~

## How it works

| Module | Responsibility |
| --- | --- |
| <code>main.py</code> | Runs the terminal menu and coordinates user actions |
| <code>portfolio.py</code> | Applies trading rules and calculates cost basis and P/L |
| <code>market.py</code> | Retrieves and validates quote and company data |
| <code>storage.py</code> | Validates local profile names and persists portfolios atomically |
| <code>api.py</code> | Loads the Finnhub API key from the environment |

Market requests use an explicit timeout and fail safely when quote data is unavailable. Portfolio summaries fetch each position once per calculation so the displayed values are internally consistent.

## Getting started

### Prerequisites

- Python 3.10 or newer
- A free [Finnhub API key](https://finnhub.io/)

### Installation

Clone the repository:

~~~powershell
git clone https://github.com/DylanThomas22/stock-market-simulator.git
cd stock-market-simulator
~~~

Create and activate a virtual environment on Windows:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
~~~

On macOS or Linux:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

Install the dependencies:

~~~powershell
python -m pip install -r requirements.txt
~~~

Copy the environment template:

~~~powershell
Copy-Item .env.example .env
~~~

On macOS or Linux, use <code>cp .env.example .env</code>.

Add your Finnhub key to <code>.env</code>:

~~~dotenv
FINNHUB_API_KEY=your_key_here
~~~

Run the application:

~~~powershell
python main.py
~~~

The login name creates a local portfolio namespace; it is not an authentication system. Valid names contain 1-32 letters, numbers, hyphens, or underscores.

## Running tests

The tests use mocked market responses and temporary storage, so they do not call Finnhub or modify saved portfolios.

~~~powershell
python -m unittest discover -s tests -v
~~~

## Project structure

~~~text
stock-market-simulator/
|-- .github/workflows/ci.yml
|-- tests/
|   |-- test_api.py
|   |-- test_market.py
|   |-- test_portfolio.py
|   +-- test_storage.py
|-- .env.example
|-- .gitignore
|-- api.py
|-- main.py
|-- market.py
|-- portfolio.py
|-- requirements.txt
+-- storage.py
~~~

## Engineering decisions

- **Weighted-average cost basis:** Additional purchases recalculate the position's average entry price.
- **Defensive API handling:** Network failures, unsuccessful responses, malformed data, and invalid quotes do not corrupt portfolio state.
- **Atomic persistence:** Portfolio data is written to a temporary file before replacing the saved JSON file.
- **Secret management:** The API key is loaded from <code>.env</code>, which is excluded from Git.
- **Deterministic tests:** Unit tests mock external quotes and isolate filesystem writes.

## Current scope

- Transactions are simulations; no brokerage is connected.
- Portfolios are local JSON files designed for a single-user CLI workflow.
- Quotes depend on Finnhub availability and the capabilities of the configured API plan.
- Monetary calculations currently use Python floating-point values, which is acceptable for this educational simulator but would be replaced with fixed-point or decimal arithmetic in a financial production system.

## Author

Built by [Dylan Thomas](https://github.com/DylanThomas22).
