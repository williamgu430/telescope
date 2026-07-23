import unittest
from unittest.mock import MagicMock, patch

from clusterloader2.utils import run_cl2_command


class TestRunClusterLoader2Command(unittest.TestCase):
    @patch("clusterloader2.utils.DockerClient")
    def test_nonzero_exit_raises(self, mock_docker_client):
        container = MagicMock()
        container.logs.return_value = []
        container.wait.return_value = {"StatusCode": 1}
        mock_docker_client.return_value.run_container.return_value = container

        with self.assertRaisesRegex(
            RuntimeError,
            "clusterloader2 exited with a non-zero status code 1",
        ):
            run_cl2_command(
                kubeconfig="/tmp/kubeconfig",
                cl2_image="clusterloader2:test",
                cl2_config_dir="/tmp/config",
                cl2_report_dir="/tmp/results",
                provider="gcp",
            )

    @patch("clusterloader2.utils.DockerClient")
    def test_zero_exit_succeeds(self, mock_docker_client):
        container = MagicMock()
        container.logs.return_value = []
        container.wait.return_value = {"StatusCode": 0}
        mock_docker_client.return_value.run_container.return_value = container

        run_cl2_command(
            kubeconfig="/tmp/kubeconfig",
            cl2_image="clusterloader2:test",
            cl2_config_dir="/tmp/config",
            cl2_report_dir="/tmp/results",
            provider="gcp",
        )


if __name__ == "__main__":
    unittest.main()
