import unittest

from prospector.extract import extract_pay, extract_tools, extract_years
from prospector.score import rank_companies, score_company, enrich_posting


class ExtractTests(unittest.TestCase):
    def test_tools(self):
        t = extract_tools("You will build workflows in Clay and HubSpot, write SQL, use Claude.")
        self.assertEqual(set(t), {"Clay", "HubSpot", "SQL", "LLM/AI"})

    def test_outreach_word_is_not_the_product(self):
        self.assertEqual(extract_tools("Own outbound outreach to enterprise accounts"), [])
        self.assertEqual(extract_tools("Experience with Outreach.io"), ["Outreach.io"])

    def test_clay_word_boundary(self):
        self.assertEqual(extract_tools("a claypot restaurant"), [])

    def test_years(self):
        self.assertEqual(extract_years("Requires 5+ years of experience"), 5)
        self.assertEqual(extract_years("3-5 years in sales ops"), 3)
        self.assertIsNone(extract_years("no experience stated"))

    def test_pay(self):
        self.assertEqual(extract_pay("Base pay $135,000 - $180,000 per year"), (135000, 180000))
        self.assertEqual(extract_pay("$120k to $160k"), (120000, 160000))
        self.assertIsNone(extract_pay("$5 - $10 an hour perk"))


class ScoreTests(unittest.TestCase):
    def posting(self, company, title, text):
        return {"company": company, "title": title, "description": text, "url": "u"}

    def test_gtm_engineer_with_stack_beats_single_generic_role(self):
        ps = [
            self.posting("A", "GTM Engineer", "Clay HubSpot Python"),
            self.posting("A", "Revenue Operations Manager", "Salesforce"),
            self.posting("B", "Growth Marketing Manager", "email campaigns"),
        ]
        rows = rank_companies(ps, ["Clay", "HubSpot"])
        self.assertEqual(rows[0]["company"], "A")
        self.assertGreater(rows[0]["score"], rows[1]["score"])

    def test_score_is_capped_at_100(self):
        ps = [enrich_posting(self.posting("A", "GTM Engineer", "Clay HubSpot llm")) for _ in range(9)]
        score, _ = score_company(ps, ["Clay", "HubSpot"])
        self.assertLessEqual(score, 100)

    def test_no_target_tools_does_not_crash(self):
        ps = [enrich_posting(self.posting("A", "GTM Engineer", "x"))]
        score, reasons = score_company(ps, [])
        self.assertTrue(reasons)


if __name__ == "__main__":
    unittest.main()
