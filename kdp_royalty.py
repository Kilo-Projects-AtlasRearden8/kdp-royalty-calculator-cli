"""KDP paperback royalty calculator.

Pure Python standard library. No cloud, no accounts, no API keys, no secrets.

Printing-cost model: KDP paperback, black & white interior, standard trim
(5" x 8" to 8.25" x 10.625"), US marketplace list prices in USD.

KDP pays a 60% royalty on the list price minus the printing cost for paperback
sales across most marketplaces (40% for expanded distribution). These cost
figures are a planning model based on KDP's published printing costs and may
change; always confirm against KDP's current pricing before publishing.

Attribution: built by Asdale Dynamics, LLC (https://dylanasdale.github.io).
"""

from __future__ import annotations

MIN_PAGES = 24
MAX_PAGES = 828

# (low, high, fixed_cost_usd, per_page_cost_usd) per paper type and page bracket
PRINTING_COSTS: dict[str, list[tuple[int, int, float, float]]] = {
    "white": [
        (24, 108, 2.15, 0.012),
        (109, 828, 0.85, 0.012),
    ],
    "cream": [
        (24, 108, 2.15, 0.012),
        (109, 828, 0.90, 0.012),
    ],
}

ROYALTY_RATE_STANDARD = 0.60
ROYALTY_RATE_EXPANDED = 0.40

MARKETPLACES: dict[str, dict[str, str]] = {
    "us": {"name": "United States", "currency": "USD", "symbol": "$"},
    "uk": {"name": "United Kingdom", "currency": "GBP", "symbol": "\u00a3"},
    "de": {"name": "Germany", "currency": "EUR", "symbol": "\u20ac"},
    "fr": {"name": "France", "currency": "EUR", "symbol": "\u20ac"},
    "es": {"name": "Spain", "currency": "EUR", "symbol": "\u20ac"},
    "it": {"name": "Italy", "currency": "EUR", "symbol": "\u20ac"},
    "jp": {"name": "Japan", "currency": "JPY", "symbol": "\u00a5"},
    "ca": {"name": "Canada", "currency": "CAD", "symbol": "CA$"},
    "au": {"name": "Australia", "currency": "AUD", "symbol": "AU$"},
    "br": {"name": "Brazil", "currency": "BRL", "symbol": "R$"},
    "mx": {"name": "Mexico", "currency": "MXN", "symbol": "MX$"},
    "in": {"name": "India", "currency": "INR", "symbol": "\u20b9"},
}


class KdpError(ValueError):
    """Raised for invalid calculator inputs."""


def printing_cost(pages: int, paper: str = "white") -> float:
    """Return the KDP printing cost in USD for a paperback.

    Parameters
    ----------
    pages:
        Page count. Must be between 24 and 828 inclusive.
    paper:
        Interior paper type: ``"white"`` or ``"cream"``.
    """
    paper = paper.lower()
    if paper not in PRINTING_COSTS:
        raise KdpError(
            f"Unknown paper type '{paper}'. Use one of: {', '.join(PRINTING_COSTS)}"
        )
    if not isinstance(pages, int) or pages < MIN_PAGES or pages > MAX_PAGES:
        raise KdpError(
            f"Page count must be an integer between {MIN_PAGES} and {MAX_PAGES}, got {pages!r}"
        )
    for low, high, fixed, per_page in PRINTING_COSTS[paper]:
        if low <= pages <= high:
            return round(fixed + per_page * pages, 2)
    raise KdpError(f"No printing-cost bracket for {pages} pages ({paper} paper).")


def royalty_rate(expanded_distribution: bool = False) -> float:
    """Return the KDP paperback royalty rate as a fraction of list price."""
    return ROYALTY_RATE_EXPANDED if expanded_distribution else ROYALTY_RATE_STANDARD


def royalty_per_sale(
    list_price: float,
    pages: int,
    paper: str = "white",
    marketplace: str = "us",
    expanded_distribution: bool = False,
) -> dict:
    """Calculate the royalty earned on one paperback sale.

    Returns a dict with list price, royalty rate, printing cost, royalty per
    sale, minimum viable list price, and marketplace info.
    """
    marketplace = marketplace.lower()
    if marketplace not in MARKETPLACES:
        raise KdpError(
            f"Unknown marketplace '{marketplace}'. Use one of: {', '.join(sorted(MARKETPLACES))}"
        )
    if list_price < 0:
        raise KdpError("List price cannot be negative.")

    rate = royalty_rate(expanded_distribution)
    cost = printing_cost(pages, paper)
    royalty = round(list_price * rate - cost, 2)
    min_price = round(cost / rate, 2)

    return {
        "marketplace": marketplace,
        "marketplace_name": MARKETPLACES[marketplace]["name"],
        "currency": MARKETPLACES[marketplace]["currency"],
        "symbol": MARKETPLACES[marketplace]["symbol"],
        "list_price": round(float(list_price), 2),
        "royalty_rate": rate,
        "pages": pages,
        "paper": paper,
        "printing_cost": cost,
        "royalty_per_sale": royalty,
        "min_list_price": min_price,
        "expanded_distribution": expanded_distribution,
    }


def profit_summary(
    list_price: float,
    pages: int,
    copies_sold: int = 0,
    author_copies: int = 0,
    author_sale_price: float | None = None,
    paper: str = "white",
    marketplace: str = "us",
    expanded_distribution: bool = False,
) -> dict:
    """Build a printable profit summary for a paperback title.

    Parameters
    ----------
    list_price:
        Customer-facing list price.
    pages:
        Page count.
    copies_sold:
        Marketplace sales to project royalty for.
    author_copies:
        Author-purchased copies (bought at printing cost, no royalty paid).
    author_sale_price:
        Price at which author copies are resold directly. Defaults to list
        price.
    paper:
        Interior paper type.
    marketplace:
        KDP marketplace code.
    expanded_distribution:
        Use the 40% expanded-distribution royalty rate instead of 60%.
    """
    if not isinstance(copies_sold, int) or copies_sold < 0:
        raise KdpError("copies_sold must be a non-negative integer.")
    if not isinstance(author_copies, int) or author_copies < 0:
        raise KdpError("author_copies must be a non-negative integer.")
    if author_sale_price is not None and author_sale_price < 0:
        raise KdpError("author_sale_price cannot be negative.")

    sale = royalty_per_sale(
        list_price, pages, paper, marketplace, expanded_distribution
    )
    if author_sale_price is None:
        author_sale_price = list_price

    royalty_income = round(sale["royalty_per_sale"] * copies_sold, 2)
    author_cost = round(sale["printing_cost"] * author_copies, 2)
    author_revenue = round(author_sale_price * author_copies, 2)
    author_profit = round(author_revenue - author_cost, 2)
    total_profit = round(royalty_income + author_profit, 2)
    total_copies = copies_sold + author_copies

    return {
        **sale,
        "copies_sold": copies_sold,
        "author_copies": author_copies,
        "author_sale_price": round(float(author_sale_price), 2),
        "royalty_income": royalty_income,
        "author_cost": author_cost,
        "author_revenue": author_revenue,
        "author_profit": author_profit,
        "total_profit": total_profit,
        "total_copies": total_copies,
        "royalty_per_copy": sale["royalty_per_sale"],
        "profit_per_copy_marketplace": sale["royalty_per_sale"],
        "profit_per_copy_author": round(author_sale_price - sale["printing_cost"], 2),
    }
