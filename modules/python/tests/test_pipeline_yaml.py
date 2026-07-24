import os
import unittest


class TestPipelineYaml(unittest.TestCase):
    @staticmethod
    def _repo_path(*parts):
        return os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            *parts,
        )

    def test_competitive_job_stops_when_run_is_cancelled(self):
        pipeline_path = self._repo_path("jobs", "competitive-test.yml")

        with open(pipeline_path, "r", encoding="utf-8") as pipeline_file:
            pipeline = pipeline_file.read()

        self.assertIn(
            "condition: and(not(canceled()), "
            "or(eq(variables['Build.Reason'], 'Manual'), "
            "and(eq(variables['Build.Reason'], 'Schedule'), "
            "eq(variables['Build.SourceBranchName'], 'main'))))",
            pipeline,
        )
        self.assertIn("- template: /steps/pin-acr-endpoints.yml", pipeline)

    def test_variable_image_pull_pipeline_temporarily_pins_0722(self):
        pipeline_path = self._repo_path(
            "pipelines",
            "perf-eval",
            "ACR Benchmark",
            "image-pull-prefetch.yml",
        )

        with open(pipeline_path, "r", encoding="utf-8") as pipeline_file:
            pipeline = pipeline_file.read()

        self.assertIn("default: 20", pipeline)
        self.assertIn("max_pods: 8", pipeline)
        self.assertIn('pin_acr_0722: "true"', pipeline)
        self.assertIn("registry_pin_ip: 57.155.172.70", pipeline)
        self.assertIn("dataproxy_pin_ip: 57.155.172.73", pipeline)

        pin_step_path = self._repo_path("steps", "pin-acr-endpoints.yml")
        with open(pin_step_path, "r", encoding="utf-8") as pin_step_file:
            pin_step = pin_step_file.read()

        self.assertIn("kind: DaemonSet", pin_step)
        self.assertIn('cri-resource-consume: "true"', pin_step)
        self.assertIn("mountPath: /host/etc", pin_step)
        self.assertIn(
            "condition: and(succeeded(), eq(variables['pin_acr_0722'], 'true'))",
            pin_step,
        )

    def test_n10_pipeline_does_not_pin_0722(self):
        pipeline_path = self._repo_path(
            "pipelines",
            "perf-eval",
            "ACR Benchmark",
            "image-pull-prefetch-n10.yml",
        )

        with open(pipeline_path, "r", encoding="utf-8") as pipeline_file:
            pipeline = pipeline_file.read()

        self.assertNotIn("pin_acr_0722", pipeline)


if __name__ == "__main__":
    unittest.main()
