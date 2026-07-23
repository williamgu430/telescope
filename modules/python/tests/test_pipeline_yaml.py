import os
import unittest


class TestPipelineYaml(unittest.TestCase):
    def test_competitive_job_stops_when_run_is_cancelled(self):
        pipeline_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "jobs",
            "competitive-test.yml",
        )

        with open(pipeline_path, "r", encoding="utf-8") as pipeline_file:
            pipeline = pipeline_file.read()

        self.assertIn(
            "condition: and(not(canceled()), "
            "or(eq(variables['Build.Reason'], 'Manual'), "
            "and(eq(variables['Build.Reason'], 'Schedule'), "
            "eq(variables['Build.SourceBranchName'], 'main'))))",
            pipeline,
        )


if __name__ == "__main__":
    unittest.main()
