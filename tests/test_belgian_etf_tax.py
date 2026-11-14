import unittest
from unittest.mock import patch

from sie.investment.belgian_tax import (
    calculate_net_dividend_yield, calculate_reynders_tax, calculate_tob,
)
from sie.investment.etfs import analyze_etf
from sie.investment.data.fsma_uci import parse_fsma_xlsx, fetch_fsma_uci_registry


class BelgianTaxTests(unittest.TestCase):
    def test_registered_sicav_distribution_tob(self):
        result = calculate_tob(10000, legal_form="sicav", distribution="distribution", registration="fsma")
        self.assertEqual(result["rate_pct"], 0.12)
        self.assertEqual(result["tob_eur"], 12)

    def test_registered_sicav_capitalisation_fsma(self):
        result = calculate_tob(10000, legal_form="sicav", distribution="capitalisation", registration="fsma")
        self.assertEqual(result["rate_pct"], 1.32)
        self.assertEqual(result["tob_eur"], 132)

    def test_registered_sicav_capitalisation_eea(self):
        result = calculate_tob(10000, legal_form="sicav", distribution="capitalisation", registration="eea")
        self.assertEqual(result["rate_pct"], 0.12)

    def test_unregistered_sicav(self):
        result = calculate_tob(10000, legal_form="sicav", distribution="capitalisation", registration="unregistered")
        self.assertEqual(result["rate_pct"], 0.35)

    def test_fcp_registered_and_unregistered(self):
        registered = calculate_tob(10000, legal_form="fcp", distribution="capitalisation", registration="eea")
        unregistered = calculate_tob(10000, legal_form="fcp", distribution="distribution", registration="unregistered")
        self.assertEqual(registered["tob_eur"], 12)
        self.assertEqual(unregistered["tob_eur"], 35)

    def test_tob_cap(self):
        result = calculate_tob(2_000_000, legal_form="sicav", distribution="distribution", registration="fsma")
        self.assertEqual(result["tob_eur"], 1300)

    def test_unknown_registration_does_not_guess(self):
        result = calculate_tob(10000, legal_form="sicav", distribution="distribution", registration="unknown")
        self.assertIsNone(result["tax_eur"])
        self.assertEqual(result["status"], "needs_registration_evidence")

    def test_net_dividend_yield(self):
        result = calculate_net_dividend_yield(annual_distribution_per_share=4, market_price=100, legal_form="sicav")
        self.assertEqual(result["gross_yield_pct"], 4)
        self.assertEqual(result["net_cash_yield_pct"], 2.8)
        self.assertEqual(result["belgian_withholding_eur"], 1.2)

    def test_foreign_withholding_is_separate_input(self):
        result = calculate_net_dividend_yield(
            annual_distribution_per_share=4, market_price=100, legal_form="sicav",
            investor_level_foreign_withholding_pct=15,
        )
        self.assertAlmostEqual(result["net_distribution_eur"], 2.38)

    def test_fcp_with_breakdown_has_no_second_distribution_withholding(self):
        result = calculate_net_dividend_yield(
            annual_distribution_per_share=4, market_price=100, legal_form="fcp",
            fcp_breakdown_available=True,
        )
        self.assertEqual(result["belgian_withholding_rate_pct"], 0)
        self.assertEqual(result["net_cash_yield_pct"], 4)
        self.assertTrue(any("underlying income remains taxable" in note for note in result["limitations"]))

    def test_reynders_screen_does_not_tax_entire_gain(self):
        before = calculate_reynders_tax(debt_claims_pct=20, acquired_on="2017-12-31")
        after_missing = calculate_reynders_tax(debt_claims_pct=20, acquired_on="2018-01-01")
        after_known = calculate_reynders_tax(debt_claims_pct=20, acquired_on="2018-01-01", taxable_debt_income_eur=40)
        self.assertEqual(before["threshold_pct"], 25)
        self.assertEqual(before["estimated_reynders_withholding_eur"], 0)
        self.assertIsNone(after_missing["estimated_reynders_withholding_eur"])
        self.assertEqual(after_known["estimated_reynders_withholding_eur"], 12)

    def test_fsma_registry_evidence_overrides_unverified_user_flag(self):
        result = analyze_etf({
            "ticker": "TEST", "ter_pct": 0.2, "aum": 1000000, "domicile": "IE",
            "ucits": True, "distribution": "accumulation",
            "fsma_registry": {"status": "not_found", "matches": [], "as_of": "2026-11-13"},
        })
        self.assertIsNone(result["checks"]["ucits"])
        self.assertEqual(result["checks"]["ucits_evidence"]["status"], "not_found")

    def test_positive_fsma_ucits_match_is_verified(self):
        result = analyze_etf({
            "ticker": "TEST", "ter_pct": 0.2, "aum": 1000000, "domicile": "IE",
            "ucits": False, "distribution": "distribution",
            "fsma_registry": {"status": "matched", "as_of": "2026-11-13", "source_url": "https://fsma.be",
                             "matches": [{"is_ucits": True, "fsma_code": "123", "isin": None}]},
        })
        self.assertIs(result["checks"]["ucits"], True)
        self.assertEqual(result["checks"]["ucits_evidence"]["status"], "verified_in_fsma_register")

    def test_user_ucits_claim_is_not_marked_as_verified(self):
        result = analyze_etf({"ticker": "X", "ucits": True})
        self.assertEqual(result["checks"]["ucits_evidence"]["status"], "user_supplied_unverified")

    def test_etf_costs_and_net_yield(self):
        result = analyze_etf({
            "ticker": "TEST", "ter_pct": 0.2, "aum": 1000000, "domicile": "IE",
            "ucits": True, "distribution": "distribution", "legal_form": "fcp",
            "annual_distribution_per_share": 4, "market_price": 100,
        })
        self.assertEqual(result["checks"]["annual_cost_per_10000_eur"], 20)
        self.assertEqual(result["net_dividend"]["net_cash_yield_pct"], 2.8)

    def test_parse_fsma_xlsx(self):
        import zipfile
        from io import BytesIO
        import xml.etree.ElementTree as ET
        xml = b'''<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>
        <row r="1"><c r="A1" t="inlineStr"><is><t>Status as at 01/01/2026</t></is></c></row>
        <row r="2"></row><row r="3"><c r="A3" t="inlineStr"><is><t>CIS FSMA CODE</t></is></c></row>
        <row r="4"><c r="A4" t="inlineStr"><is><t>123</t></is></c><c r="C4" t="inlineStr"><is><t>Fund</t></is></c><c r="E4" t="inlineStr"><is><t>Fonds</t></is></c><c r="F4" t="inlineStr"><is><t>CIS F PUCITS</t></is></c><c r="G4" t="inlineStr"><is><t>IE</t></is></c><c r="V4" t="inlineStr"><is><t>123-1</t></is></c><c r="X4" t="inlineStr"><is><t>Compartment</t></is></c></row>
        </sheetData></worksheet>'''
        b=BytesIO()
        with zipfile.ZipFile(b,"w") as z: z.writestr("xl/worksheets/sheet1.xml",xml)
        result=parse_fsma_xlsx(b.getvalue())
        self.assertEqual(result["as_of"], "Status as at 01/01/2026")
        self.assertTrue(result["records"][0]["is_ucits"])
        self.assertEqual(result["records"][0]["compartment_name_nl"], "Compartment")
        with patch("sie.investment.data.fsma_uci.get_bytes", return_value=b.getvalue()):
            by_name = fetch_fsma_uci_registry(name="Compartment")
            by_isin = fetch_fsma_uci_registry(isin="IE0000000000")
        self.assertEqual(by_name["status"], "matched")
        self.assertEqual(by_name["matches"][0]["ucits_status"], "UCITS")
        self.assertEqual(by_isin["status"], "isin_not_available_in_fsma_export")


if __name__ == "__main__":
    unittest.main()

class EtfCostExtractionTests(unittest.TestCase):
    def test_extracts_kid_cost_components_separately(self):
        from sie.investment.data.etf_costs import parse_issuer_cost_document
        text = '''ESSENTIËLE-INFORMATIEDOCUMENT\nProduct: Test UCITS ETF\nISIN IE00B4L5Y983\nDit document is gedateerd op 01/11/2026.\nWat zijn de kosten?\nManagement fees and other administrative or operating costs 0.20%\nTransaction costs 0.03%\nReduction in Yield 0.23%\nEntry costs 0.00%\nExit costs 0.00%\n'''
        result = parse_issuer_cost_document(text, isin="IE00B4L5Y983", issuer="vanguard", source_url="https://fund-docs.vanguard.com/test.pdf")
        self.assertEqual(result["status"], "extracted_from_issuer_kid")
        self.assertEqual(result["costs"]["ongoing_charges_pct"]["value_pct"], 0.2)
        self.assertEqual(result["costs"]["transaction_costs_pct"]["value_pct"], 0.03)
        self.assertEqual(result["costs"]["reduction_in_yield_pct"]["value_pct"], 0.23)
        self.assertFalse(result["quality"]["ongoing_charges_is_ter"])
        self.assertEqual(result["document_date"], "01/11/2026")

    def test_wrong_isin_is_not_marked_verified(self):
        from sie.investment.data.etf_costs import parse_issuer_cost_document
        result = parse_issuer_cost_document("KID costs ongoing charges 0.20%", isin="IE00B4L5Y983", issuer="xtrackers", source_url="https://etf.dws.com/x.pdf")
        self.assertEqual(result["status"], "isin_not_confirmed_in_document")
        self.assertFalse(result["isin_confirmed"])

    def test_rejects_non_issuer_document_host(self):
        from sie.investment.data.etf_costs import extract_etf_costs
        with self.assertRaises(ValueError):
            extract_etf_costs("IE00B4L5Y983", issuer="vanguard", document_url="https://example.com/fake.pdf")

    def test_issuer_aliases(self):
        from sie.investment.data.etf_costs import _issuer_for
        self.assertEqual(_issuer_for(None, "blackrock"), "ishares")
        self.assertEqual(_issuer_for(None, "dws"), "xtrackers")

    def test_kid_euro_amounts_are_not_misread_as_percentages(self):
        from sie.investment.data.etf_costs import parse_issuer_cost_document
        text = '''Key Information Document\nProduct: Example ETF\nISIN IE00B4L5Y983\nThis document is dated 09 April 2026.\nComposition of Costs\nEntry costs The Fund does not charge an entry fee. EUR 0\nExit costs The Fund does not charge an exit fee. EUR 0\nManagement fees and other 0.20% of your investment p.a. EUR 20\nadministrative or operating costs\nTransaction costs 0.03% per year EUR 3\n'''
        result = parse_issuer_cost_document(text, isin="IE00B4L5Y983", issuer="ishares", source_url="https://www.ishares.com/example.pdf")
        self.assertEqual(result["document_date"], "09 April 2026")
        self.assertEqual(result["costs"]["entry_costs_pct"]["value_eur"], 0)
        self.assertIsNone(result["costs"]["entry_costs_pct"].get("value_pct"))
        self.assertEqual(result["costs"]["ongoing_charges_pct"]["value_pct"], 0.2)
        self.assertEqual(result["costs"]["transaction_costs_pct"]["value_pct"], 0.03)

    def test_rejects_lookalike_issuer_domains(self):
        from sie.investment.data.etf_costs import extract_etf_costs
        with self.assertRaises(ValueError):
            extract_etf_costs("IE00B4L5Y983", issuer="ishares", document_url="https://ishares.com.attacker.example/fake.pdf")

    def test_extracts_non_eur_kid_cost_amounts_with_currency(self):
        from sie.investment.data.etf_costs import parse_issuer_cost_document
        text = '''Key Information Document\nProduct: Xtrackers Example ETF\nISIN IE00BJ0KDQ92\nWhat are the costs?\nEntry costs We do not charge an entry fee. 0 USD\nExit costs We do not charge an exit fee. 0 USD\nManagement fees and 0.12% per year 12 USD\nTransaction costs 0.01% per year 1 USD\n'''
        result = parse_issuer_cost_document(text, isin="IE00BJ0KDQ92", issuer="xtrackers", source_url="https://etf.dws.com/test.pdf")
        self.assertEqual(result["costs"]["entry_costs_pct"]["value_amount"], 0)
        self.assertEqual(result["costs"]["entry_costs_pct"]["amount_currency"], "USD")
        self.assertEqual(result["costs"]["ongoing_charges_pct"]["amount"], 12)
        self.assertEqual(result["costs"]["ongoing_charges_pct"]["amount_currency"], "USD")

    def test_amundi_discovers_latest_public_kid_and_factsheet_by_isin(self):
        from sie.investment.data.etf_costs import _amundi_documents
        product = {"products": [{"productId": "LU1681038169", "characteristics": {"ISIN": "LU1681038169"}}]}
        docs = {"LU1681038169": [
            {"status": "PUBLIC", "language": "English", "recordDate": 10,
             "url": "/pdfDocuments/old.pdf", "documentType": {"name": "kidpriips"}},
            {"status": "PUBLIC", "language": "English", "recordDate": 20,
             "url": "/pdfDocuments/latest-kid.pdf", "documentType": {"name": "kidpriips"}},
            {"status": "PUBLIC", "language": "English", "recordDate": 30,
             "url": "/pdfDocuments/latest-factsheet.pdf", "documentType": {"name": "monthlyfactsheet"}},
            {"status": "PRIVATE", "language": "English", "recordDate": 40,
             "url": "/pdfDocuments/private.pdf", "documentType": {"name": "kidpriips"}},
        ]}
        with patch("sie.investment.data.etf_costs._post_json", side_effect=[product, docs]):
            urls = _amundi_documents("LU1681038169")
        self.assertEqual(urls, [
            "https://www.amundietf.com/pdfDocuments/latest-kid.pdf",
            "https://www.amundietf.com/pdfDocuments/latest-factsheet.pdf",
        ])

    def test_ishares_discovers_priips_kid_and_factsheet_by_isin(self):
        from sie.investment.data.etf_costs import _ishares_documents
        rss = b'''<rss><channel><item><title>ETF</title><link>https://www.ishares.com/uk/individual/en/products/251882/ishares-msci-world-ucits-etf</link></item></channel></rss>'''
        page = b'''<html><head><title>iShares Core S&amp;P 500 UCITS ETF | CSPX | iShares</title></head>
        <body>ISIN IE00B5BMR087 <a href="https://www.ishares.com/gls-download/literature/kiid/ucits_kiid-ishares-core-sp-500-ucits-etf-usd-acc-gb-ie00b5bmr087-en.pdf">KIID</a>
        <a href="https://www.ishares.com/gls-download/literature/fact-sheet/cspx-fact-sheet-en-gb.pdf">Factsheet</a></body></html>'''
        with patch("sie.investment.data.etf_costs._request", side_effect=[rss, page]):
            urls = _ishares_documents("IE00B5BMR087")
        self.assertIn("eu-priips-ishares-core-sp-500-ucits-etf-usd-acc-ie00b5bmr087-en.pdf", urls[0])
        self.assertTrue(urls[-1].endswith("cspx-fact-sheet-en-gb.pdf"))

    def test_factsheet_document_type_and_asof_date_are_not_confused_with_inception(self):
        from sie.investment.data.etf_costs import parse_issuer_cost_document
        text = """iShares Core MSCI World UCITS ETF\nFACTSHEET\nShare class inception date: 25-Sept-2009\nPerformance, Portfolio Breakdowns and Net Asset information as at: 31-Oct-2026. All other data as at 04-Nov-2026.\nISIN IE00B4L5Y983\nTotal Expense Ratio : 0.20%\n"""
        result = parse_issuer_cost_document(text, isin="IE00B4L5Y983", issuer="ishares",
                                            source_url="https://www.ishares.com/factsheet.pdf", document_type="factsheet")
        self.assertEqual(result["document_type"], "factsheet")
        self.assertEqual(result["document_date"], "31-Oct-2026")
        self.assertEqual(result["status"], "extracted_from_issuer_factsheet")

    def test_extracts_xtrackers_accurate_as_at_date(self):
        from sie.investment.data.etf_costs import parse_issuer_cost_document
        text = """Key Information Document\nXtrackers MSCI World UCITS ETF\nISIN IE00BJ0KDQ92\nThis key information is accurate as at 06.03.2026.\nWhat are the costs?\nManagement fees and other administrative or operating costs 0.12%\nTransaction costs 0.01%\n"""
        result = parse_issuer_cost_document(text, isin="IE00BJ0KDQ92", issuer="xtrackers",
                                            source_url="https://etf.dws.com/kid.pdf")
        self.assertEqual(result["document_date"], "06.03.2026")

    def test_extraction_rejects_costs_when_document_does_not_confirm_requested_isin(self):
        from sie.investment.data.etf_costs import extract_etf_costs
        with patch("sie.investment.data.etf_costs._discover_document", return_value=["https://fund-docs.vanguard.com/test.pdf"]), \
             patch("sie.investment.data.etf_costs.get_bytes", return_value=b"%PDF-fake"), \
             patch("sie.investment.data.etf_costs._extract_pdf_text", return_value="ISIN IE0000000000\nOngoing charges 0.20%"):
            result = extract_etf_costs("IE00B4L5Y983", issuer="vanguard")
        self.assertEqual(result["status"], "isin_not_confirmed_in_document")
        self.assertFalse(result["isin_confirmed"])
        self.assertEqual(result["costs"], {})
        self.assertEqual(result["documents"][0]["costs"], {})
