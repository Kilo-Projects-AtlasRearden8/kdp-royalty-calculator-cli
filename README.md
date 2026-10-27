# KDP Royalty Calculator CLI

A friendly, local-first Python tool that calculates Kindle Direct Publishing (KDP)
paperback royalties from your book's list price, page count, paper type, and
marketplace — then prints a clean, copy-pasteable profit summary you can drop
into a spreadsheet or notebook.

Built by **Asdale Dynamics, LLC** — beginner-friendly AI education, books, and
practical tools for authors and small businesses. https://dylanasdale.github.io

No cloud, no accounts, no API keys, no personal data. Pure Python standard
library — nothing to install beyond Python itself.

---

## What it does

Give it your book's details and it tells you:

* **Printing cost per copy** — based on KDP's published cost model
* **Royalty per sale** — 60% of list price minus printing cost (40% with
  expanded distribution)
* **Minimum break-even list price** — the price where you earn $0.00 per sale
* **Optional printable profit summary** — projected income from marketplace
  sales plus author copies you resell yourself

---

## Quick start

```bash
# Short result: royalty on one sale
python cli.py --price 12.99 --pages 200 --paper white --marketplace us

# Printable profit summary: 100 marketplace sales plus 20 author copies
python cli.py --price 12.99 --pages 200 --paper cream --marketplace uk \
    --copies-sold 100 --author-copies 20 --author-sale-price 14.99 --summary

# Show the printing-cost model used
python cli.py --printing-costs
```

---

## Options

| Option | Meaning |
|--------|---------|
| `--price` | List price (required) |
| `--pages` | Page count, 24–828 (required) |
| `--paper` | `white` or `cream` (default: white) |
| `--marketplace` | `us`, `uk`, `de`, `fr`, `es`, `it`, `jp`, `ca`, `au`, `br`, `mx`, `in` (default: us) |
| `--expanded-distribution` | Use the 40% royalty rate instead of 60% |
| `--copies-sold` | Projected marketplace sales for the summary |
| `--author-copies` | Author copies you buy and resell directly |
| `--author-sale-price` | Your resale price for author copies (default: list price) |
| `--summary` | Print the full profit summary |
| `--printing-costs` | Show the cost model and exit |

---

## Example output

```
KDP Profit Summary (printable)
================================
Title model:   United States paperback
List price:    $12.99
Royalty rate:  60%
Pages:         200 (white paper)
Printing cost: $3.25 per copy
Royalty/sale:  $4.54 per marketplace sale

Projected sales:
  Marketplace copies sold: 100
  Royalty income:          $454.00

Author copies:
  Copies purchased: 20
  Cost to author:   $65.00 ($3.25 each)
  Resale price:     $14.99 each
  Author revenue:   $299.80
  Author profit:    $234.80

Totals:
  Total copies:      120
  TOTAL PROFIT:      $688.80

Break-even:
  Minimum list price: $5.42
```

---

## Royalty and cost model

KDP pays a 60% royalty on the list price minus the printing cost for paperback
sales (40% for expanded distribution). Printing costs in this tool follow the
KDP black & white paperback model for standard trim sizes (5" × 8" to
8.25" × 10.625"), US marketplace:

* **White paper:** 24–108 pp: $2.15 + $0.012/page; 109–828 pp: $0.85 + $0.012/page
* **Cream paper:** 24–108 pp: $2.15 + $0.012/page; 109–828 pp: $0.90 + $0.012/page

> **Note:** KDP's prices change. Treat these figures as planning estimates and
> confirm current pricing on KDP before you publish. Currency symbols shown for
> non-US marketplaces are display only; costs are modeled in USD.

---

## Tests

Run the test suite with the standard library only:

```bash
python -m unittest discover -s tests -v
```

---

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

---

## About

Asdale Dynamics, LLC (Indiana, formed October 2026) is founded by Dylan Asdale,
a registered nurse turned AI author. The LLC makes beginner-friendly AI
education, books and guides, and practical open-source tools — including this
calculator for authors publishing through KDP. More at
https://dylanasdale.github.io and in _The Massive AI Manual_.