"""Command-line interface for the KDP paperback royalty calculator."""

from __future__ import annotations

import argparse
import sys

from kdp_royalty import (
    KdpError,
    MARKETPLACES,
    MAX_PAGES,
    MIN_PAGES,
    profit_summary,
    royalty_per_sale,
)

PRINTING_COSTS_DOC = (
    "Printing cost model (USD, black & white paperback, standard trim):\n"
    "  White paper: 24-108 pp: $2.15 + $0.012/page; 109-828 pp: $0.85 + $0.012/page\n"
    "  Cream paper: 24-108 pp: $2.15 + $0.012/page; 109-828 pp: $0.90 + $0.012/page\n"
    "Royalty: 60% of list price minus printing cost (40% expanded distribution).\n"
)


def _money(value: float, symbol: str) -> str:
    return f"{symbol}{value:,.2f}"


def _format_result(sale: dict) -> str:
    lines = [
        "KDP Royalty Calculation",
        "-----------------------",
        f"Marketplace:   {sale['marketplace_name']} ({sale['currency']})",
        f"List price:    {_money(sale['list_price'], sale['symbol'])}",
        f"Royalty rate:  {sale['royalty_rate'] * 100:.0f}% "
        + ("(expanded distribution)" if sale["expanded_distribution"] else ""),
        f"Pages:         {sale['pages']}",
        f"Paper:         {sale['paper']}",
        f"Printing cost: {_money(sale['printing_cost'], sale['symbol'])}",
        f"Royalty/sale:  {_money(sale['royalty_per_sale'], sale['symbol'])}",
        f"Min list price: {_money(sale['min_list_price'], sale['symbol'])} "
        "(to earn $0.00 royalty)",
    ]
    if sale["royalty_per_sale"] < 0:
        lines.append(
            "WARNING: list price is below the break-even point; each sale loses money."
        )
    return "\n".join(lines)


def _format_summary(summary: dict) -> str:
    sym = summary["symbol"]
    lines = [
        "KDP Profit Summary (printable)",
        "================================",
        f"Title model:   {summary['marketplace_name']} paperback",
        f"List price:    {_money(summary['list_price'], sym)}",
        f"Royalty rate:  {summary['royalty_rate'] * 100:.0f}%",
        f"Pages:         {summary['pages']} ({summary['paper']} paper)",
        f"Printing cost: {_money(summary['printing_cost'], sym)} per copy",
        f"Royalty/sale:  {_money(summary['royalty_per_copy'], sym)} per marketplace sale",
        "",
        "Projected sales:",
        f"  Marketplace copies sold: {summary['copies_sold']}",
        f"  Royalty income:          {_money(summary['royalty_income'], sym)}",
        "",
        "Author copies:",
        f"  Copies purchased: {summary['author_copies']}",
        f"  Cost to author:   {_money(summary['author_cost'], sym)} "
        f"({_money(summary['printing_cost'], sym)} each)",
        f"  Resale price:     {_money(summary['author_sale_price'], sym)} each",
        f"  Author revenue:   {_money(summary['author_revenue'], sym)}",
        f"  Author profit:    {_money(summary['author_profit'], sym)}",
        "",
        "Totals:",
        f"  Total copies:      {summary['total_copies']}",
        f"  TOTAL PROFIT:      {_money(summary['total_profit'], sym)}",
        "",
        "Break-even:",
        f"  Minimum list price: {_money(summary['min_list_price'], sym)}",
        "",
        "Notes:",
        "  Author copies earn no KDP royalty; profit is resale price minus printing cost.",
        "  Figures are estimates. Confirm current KDP pricing before publishing.",
        "",
        "Built by Asdale Dynamics, LLC - https://dylanasdale.github.io",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate KDP paperback royalties and print a profit summary.",
    )
    parser.add_argument(
        "--price",
        type=float,
        help="List price of the paperback.",
    )
    parser.add_argument(
        "--pages",
        type=int,
        help=f"Page count ({MIN_PAGES}-{MAX_PAGES}).",
    )
    parser.add_argument(
        "--paper",
        choices=["white", "cream"],
        default="white",
        help="Interior paper type (default: white).",
    )
    parser.add_argument(
        "--marketplace",
        choices=sorted(MARKETPLACES),
        default="us",
        help="KDP marketplace (default: us).",
    )
    parser.add_argument(
        "--expanded-distribution",
        action="store_true",
        help="Use the 40% expanded-distribution royalty rate (default: 60%).",
    )
    parser.add_argument(
        "--copies-sold",
        type=int,
        default=0,
        help="Projected marketplace sales (default: 0).",
    )
    parser.add_argument(
        "--author-copies",
        type=int,
        default=0,
        help="Author-purchased copies resold directly (default: 0).",
    )
    parser.add_argument(
        "--author-sale-price",
        type=float,
        help="Resale price for author copies (default: list price).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a printable profit summary instead of the short result.",
    )
    parser.add_argument(
        "--printing-costs",
        action="store_true",
        help="Show the printing-cost model and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.printing_costs:
        print(PRINTING_COSTS_DOC)
        print("Built by Asdale Dynamics, LLC - https://dylanasdale.github.io")
        return 0

    if args.price is None or args.pages is None:
        parser.error("--price and --pages are required unless --printing-costs is given")

    try:
        if args.summary or args.copies_sold or args.author_copies or args.author_sale_price is not None:
            summary = profit_summary(
                list_price=args.price,
                pages=args.pages,
                paper=args.paper,
                marketplace=args.marketplace,
                expanded_distribution=args.expanded_distribution,
                copies_sold=args.copies_sold,
                author_copies=args.author_copies,
                author_sale_price=args.author_sale_price,
            )
            print(_format_summary(summary))
        else:
            sale = royalty_per_sale(
                list_price=args.price,
                pages=args.pages,
                paper=args.paper,
                marketplace=args.marketplace,
                expanded_distribution=args.expanded_distribution,
            )
            print(_format_result(sale))
    except KdpError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
