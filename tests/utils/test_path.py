import os
import tempfile
import unittest

from regent_rag.core.path import ensure_dir


class TestEnsureDir(unittest.TestCase):
    def setUp(self) -> None:
        # Create a temporary directory for testing
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_ensure_dir(self) -> None:
        # Test that ensure_dir creates the directory if it doesn't exist
        new_dir_path = os.path.join(self.test_dir.name, "new_dir")
        ensure_dir(new_dir_path)
        self.assertTrue(os.path.exists(new_dir_path))

        # Test that ensure_dir does not raise an error if the directory already exists
        try:
            ensure_dir(new_dir_path)
        # pylint: disable=broad-exception-caught
        except Exception as e:
            self.fail(f"ensure_dir raised an exception when called on an existing directory: {e}")


if __name__ == "__main__":
    unittest.main()
