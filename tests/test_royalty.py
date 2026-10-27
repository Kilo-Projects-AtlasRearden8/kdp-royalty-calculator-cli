"""Tests for the KDP royalty math (standard library unittest only)."""

from __future__ import annotations

import unittest

from kdp_royalty import (
    KdpError,
    MAX_PAGES,
    MIN_PAGES,
    printing_cost,
    royalty_per_sale,
    profit_summary,
    royalty_rate,
)

TWOPLACES = lambda value: round(value, 2)


class TestPrintingCost(unittest.TestCase):
    def test_white_24_pages(self):
        self.assertEqual(printing_cost(24, "white"), TWOPLACES(2.15 + 0.012 * 24))

    def test_white_108_pages(self):
        self.assertEqual(printing_cost(108, "white"), TWOPLACES(2.15 + 0.012 * 108))

    def test_white_109_pages(self):
        self.assertEqual(printing_cost(109, "white"), TWOPLACES(0.85 + 0.012 * 109))

    def test_white_828_pages(self):
        self.assertEqual(printing_cost(828, "white"), TWOPLACES(0.85 + 0.012 * 828))

    def test_cream_matches_white_bracket_one(self):
        self.assertEqual(printing_cost(50, "cream"), printing_cost(50, "white"))

    def test_cream_bracket_two(self):
        self.assertEqual(printing_cost(200, "cream"), 0.90 + 0.012 * 200)

    def test_below_min_pages(self):
        with self.assertRaises(KdpError):
            printing_cost(23)

    def test_above_max_pages(self):
        with self.assertRaises(KdpError):
            printing_cost(829)

    def test_unknown_paper(self):
        with self.assertRaises(KdpError):
            printing_cost(100, "recycled")

    def test_non_integer_pages(self):
        with self.assertRaises(KdpError):
            printing_cost(100.5)


class TestRoyaltyRate(unittest.TestCase):
    def test_standard_rate(self):
        self.assertEqual(royalty_rate(False), 0.60)

    def test_expanded_rate(self):
        self.assertEqual(royalty_rate(True), 0.40)


class TestRoyaltyPerSale(unittest.TestCase):
    def test_known_calculation(self):
        # 200 pages, white: 0.85 + 2.40 = 3.25; price 12.99 -> 7.794 - 3.25 = 4.544 -> 4.54
        result = royalty_per_sale(12.99, 200, "white", "us")
        self.assertEqual(result["printing_cost"], 3.25)
        self.assertEqual(result["royalty_per_sale"], 4.54)
        self.assertEqual(result["royalty_rate"], 0.60)
        self.assertEqual(result["min_list_price"], round(3.25 / 0.60, 2))

    def test_expanded_distribution_rate(self):
        result = royalty_per_sale(12.99, 200, "white", "us", expanded_distribution=True)
        self.assertEqual(result["royalty_rate"], 0.40)
        self.assertEqual(result["royalty_per_sale"], round(12.99 * 0.40 - 3.25, 2))

    def test_negative_royalty_when_price_too_low(self):
        result = royalty_per_sale(1.00, 200, "white", "us")
        self.assertLess(result["royalty_per_sale"], 0)

    def test_negative_price_rejected(self):
        with self.assertRaises(KdpError):
            royalty_per_sale(-5.00, 100, "white", "us")

    def test_unknown_marketplace_rejected(self):
        with self.assertRaises(KdpError):
            royalty_per_sale(10.00, 100, "white", "xx")

    def test_marketplace_symbols(self):
        us = royalty_per_sale(10.00, 100, "white", "us")
        uk = royalty_per_sale(10.00, 100, "white", "uk")
        jp = royalty_per_sale(10.00, 100, "white", "jp")
        self.assertEqual(us["symbol"], "$")
        self.assertEqual(uk["symbol"], "\u00a3")
        self.assertEqual(jp["symbol"], "\u00a5")


class TestProfitSummary(unittest.TestCase):
    def test_basic_summary(self):
        summary = profit_summary(12.99, 200, copies_sold=100, author_copies=20)
        self.assertEqual(summary["printing_cost"], 3.25)
        self.assertEqual(summary["royalty_per_copy"], 4.54)
        self.assertEqual(summary["royalty_income"], 454.00)
        self.assertEqual(summary["author_cost"], 65.00)
        self.assertEqual(summary["author_revenue"], 259.80)
        self.assertEqual(summary["author_profit"], 194.80)
        self.assertEqual(summary["total_profit"], 648.80)
        self.assertEqual(summary["total_copies"], 120)

    def test_author_sale_price_defaults_to_list(self):
        summary = profit_summary(12.99, 200, author_copies=5)
        self.assertEqual(summary["author_sale_price"], 12.99)

    def test_zero_copies(self):
        summary = profit_summary(12.99, 200)
        self.assertEqual(summary["total_profit"], 0.00)

    def test_negative_copies_sold_rejected(self):
        with self.assertRaises(KdpError):
            profit_summary(12.99, 200, copies_sold=-1)

    def test_negative_author_copies_rejected(self):
        with self.assertRaises(KdpError):
            profit_summary(12.99, 200, author_copies=-1)

    def test_negative_author_sale_price_rejected(self):
        with self.assertRaises(KdpError):
            profit_summary(12.99, 200, author_copies=10, author_sale_price=-5.00)

    def test_expanded_distribution_summary(self):
        summary = profit_summary(
            12.99, 200, copies_sold=100, author_copies=20, expanded_distribution=True
        )
        self.assertEqual(summary["royalty_rate"], 0.40)
        # 12.99 * 0.40 - 3.25 = 5.196 - 3.25 = 1.946 -> 1.95
        self.assertEqual(summary["royalty_per_copy"], 1.95)
        self.assertEqual(summary["royalty_income"], 195.00)
        self.assertEqual(summary["total_profit"], 195.00 + 194.80)

    def test_custom_author_sale_price(self):
        summary = profit_summary(12.99, 200, author_copies=10, author_sale_price=15.00)
        self.assertEqual(summary["author_sale_price"], 15.00)
        self.assertEqual(summary["author_profit"], round(15.00 * 10 - 3.25 * 10, 2))


if __name__ == "__main__":
    unittest.main()
