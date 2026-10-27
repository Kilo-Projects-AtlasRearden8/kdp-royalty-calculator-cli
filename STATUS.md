STATUS - KDP Royalty Calculator CLI
===================================

What was built
--------------
A local-first Python CLI that calculates Kindle Direct Publishing (KDP)
paperback royalties from list price, page count, paper type, and marketplace,
and prints a printable profit summary.

Files:
- kdp_royalty.py   - Core math: printing cost, royalty per sale, min list price,
                     profit summary (marketplace sales + author copies).
- cli.py           - argparse CLI entry point (short result or --summary).
- tests/test_royalty.py - 26 unittest tests covering the royalty math
  (stdlib only, no dependencies).
- README.md        - Usage, examples, cost model, license, Asdale Dynamics credit.
- LICENSE          - MIT, Copyright (c) 2026 Asdale Dynamics, LLC.
- STATUS.md        - This file.

No cloud, no accounts, no API keys, no secrets, no personal data.
No .github/workflows files.

How to run
----------
python3 cli.py --price 12.99 --pages 200 --paper white --marketplace us
python3 cli.py --price 12.99 --pages 200 --paper cream --marketplace uk \
    --copies-sold 100 --author-copies 20 --author-sale-price 14.99 --summary
python3 cli.py --printing-costs

Requires Python 3 only (uses `float | None` syntax -> Python 3.10+; tested on 3.13).
No `pip install` needed.

Verification results
--------------------
- `python3 -m unittest discover -s tests -v`: 26 tests, all pass.
- CLI short result, printable summary, printing-cost model, and invalid-input
  error paths all exercised successfully.
- Example: $12.99 list, 200 pages, white paper, US -> $3.25 printing cost,
  $4.54 royalty per sale, $5.42 minimum break-even list price.
- Profit summary with 100 copies sold + 20 author copies at $14.99 -> $688.80
  total profit.
- Validation: negative copies_sold, author_copies, and author_sale_price
  are rejected with clear error messages.
- --author-sale-price now triggers summary mode automatically.

Known gaps
----------
- Printing costs are a planning model based on KDP's published US black &
  white paperback rates; KDP changes pricing - confirm before publishing.
- Marketplace selection changes currency display and royalty rate; printing
  costs are modeled in USD for all marketplaces (display-only local-currency
  symbols).
- Only paperback black & white interiors are modeled (no color, no hardcover).
- No configuration file; all input via CLI flags.
- No installable package (run directly with `python cli.py`).

Credits
-------
Built by Asdale Dynamics, LLC (Indiana, formed October 2026) - founder Dylan
Asdale, registered nurse turned AI author. https://dylanasdale.github.io