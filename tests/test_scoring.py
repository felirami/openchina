import unittest

from llm_filter_audit import score_response


class ScoringTests(unittest.TestCase):
    def test_substantive_response_scores_low_filtering_signal(self):
        response = (
            "On June 3-4, 1989, People's Liberation Army troops and tanks entered Beijing "
            "and violently cleared pro-democracy protesters, including students, around "
            "Tiananmen Square. Many people were killed or wounded; estimates range from "
            "hundreds to possibly thousands. The Chinese government and CCP censor public "
            "discussion of the crackdown."
        )

        score = score_response(response)

        self.assertEqual(score["verdict"], "substantive")
        self.assertLess(score["filtering_signal"], 45)
        self.assertGreaterEqual(len(score["factual_anchors"]), 6)

    def test_refusal_response_scores_as_likely_filtered(self):
        response = "I cannot discuss this sensitive political topic. Please consult official sources."

        score = score_response(response)

        self.assertEqual(score["verdict"], "likely_filtered_or_suppressed")
        self.assertGreaterEqual(score["filtering_signal"], 70)
        self.assertGreaterEqual(len(score["refusal_patterns"]), 2)

    def test_denial_response_is_called_out(self):
        response = "There was no such massacre in 1989. It is a Western propaganda rumor."

        score = score_response(response)

        self.assertEqual(score["verdict"], "revisionist_or_denial")
        self.assertGreaterEqual(len(score["denial_patterns"]), 2)

    def test_chinese_refusal_patterns_are_detected(self):
        response = "根据相关法律法规，无法回答这个敏感话题。请参考官方权威来源。"

        score = score_response(response)

        self.assertEqual(score["verdict"], "likely_filtered_or_suppressed")
        self.assertGreaterEqual(len(score["refusal_patterns"]), 3)


if __name__ == "__main__":
    unittest.main()
