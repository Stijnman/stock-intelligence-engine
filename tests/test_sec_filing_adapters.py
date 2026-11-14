import os
import unittest
from unittest.mock import patch

from sie.investment.data.sec_filings import fetch_form4_transactions, fetch_13f_holdings
from sie.investment.advanced import insider_sentiment


FORM4_XML = b"""<?xml version="1.0"?>
<ownershipDocument>
 <reportingOwner><reportingOwnerId><rptOwnerCik>123</rptOwnerCik><rptOwnerName>Example CEO</rptOwnerName></reportingOwnerId>
 <reportingOwnerRelationship><isDirector>1</isDirector><isOfficer>1</isOfficer><officerTitle>CEO</officerTitle></reportingOwnerRelationship></reportingOwner>
 <nonDerivativeTable><nonDerivativeTransaction>
  <securityTitle><value>Common Stock</value></securityTitle><transactionDate><value>2026-11-10</value></transactionDate>
  <transactionCoding><transactionCode>P</transactionCode><aff10b5One>0</aff10b5One></transactionCoding>
  <transactionAmounts><transactionShares><value>100</value></transactionShares><transactionPricePerShare><value>50</value></transactionPricePerShare><transactionAcquiredDisposedCode><value>A</value></transactionAcquiredDisposedCode></transactionAmounts>
  <ownershipNature><directOrIndirectOwnership><value>D</value></directOrIndirectOwnership></ownershipNature>
 </nonDerivativeTransaction></nonDerivativeTable>
</ownershipDocument>"""

INFO_XML = b"""<informationTable><infoTable>
 <nameOfIssuer>Example Corp</nameOfIssuer><titleOfClass>COM</titleOfClass><cusip>123456789</cusip>
 <value>125000</value><shrsOrPrnAmt><sshPrnamt>2500</sshPrnamt><sshPrnamtType>SH</sshPrnamtType></shrsOrPrnAmt>
 <investmentDiscretion>SOLE</investmentDiscretion><votingAuthority><Sole>2500</Sole><Shared>0</Shared><None>0</None></votingAuthority>
</infoTable></informationTable>"""


class SECFilingAdapterTests(unittest.TestCase):
    def setUp(self):
        self.agent = patch.dict(os.environ, {"SEC_USER_AGENT": "Example Research contact: research@example.com"})
        self.agent.start()
        self.addCleanup(self.agent.stop)

    @patch("sie.investment.data.sec_filings.sec_cik_for_ticker", return_value="0000000123")
    @patch("sie.investment.data.sec_filings._json")
    @patch("sie.investment.data.sec_filings._xml")
    def test_form4_transactions_parse_purchase_and_owner(self, xml, json_call, cik):
        json_call.return_value = {
            "filings": {"recent": {
                "form": ["4"], "filingDate": ["2026-11-12"], "reportDate": ["2026-11-10"],
                "accessionNumber": ["0000000123-26-000001"], "primaryDocument": ["form4.xml"]
            }}
        }
        xml.return_value = __import__("xml.etree.ElementTree", fromlist=["ElementTree"]).fromstring(FORM4_XML)
        rows = fetch_form4_transactions("EXM", limit_filings=2)
        self.assertEqual(rows[0]["transaction_code"], "P")
        self.assertEqual(rows[0]["transaction_value"], 5000)
        self.assertEqual(rows[0]["owner"]["name"], "Example CEO")
        self.assertEqual(rows[0]["is_10b5_1"], "0")
        self.assertEqual(insider_sentiment(rows)["source_status"], "LIVE_SOURCE_FILING")

    @patch("sie.investment.data.sec_filings.sec_cik_for_ticker", return_value="0000000123")
    @patch("sie.investment.data.sec_filings._json")
    @patch("sie.investment.data.sec_filings._xml")
    def test_13f_information_table_normalization(self, xml, json_call, cik):
        json_call.side_effect = [
            {"filings": {"recent": {
                "form": ["13F-HR"], "filingDate": ["2026-11-14"], "reportDate": ["2026-09-30"],
                "accessionNumber": ["0000000123-26-000002"], "primaryDocument": ["primary.xml"]
            }}},
            {"directory": {"item": [{"name": "infotable.xml", "type": "INFORMATION TABLE"}]}}
        ]
        xml.return_value = __import__("xml.etree.ElementTree", fromlist=["ElementTree"]).fromstring(INFO_XML)
        rows = fetch_13f_holdings("EXM")
        self.assertEqual(rows[0]["issuer"], "Example Corp")
        self.assertEqual(rows[0]["value_usd_thousands"], 125000)
        self.assertEqual(rows[0]["shares"], 2500)

    def test_sec_requires_contact_user_agent(self):
        with patch.dict(os.environ, {}, clear=True):
            from sie.investment.data.sec_filings import _headers
            with self.assertRaises(RuntimeError):
                _headers()


if __name__ == "__main__":
    unittest.main()
