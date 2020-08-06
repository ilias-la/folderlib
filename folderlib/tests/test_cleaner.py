import unittest
import pytest
import tempfile

import os
import random
import shutil
from pathlib2 import Path

from folder_wonder.cleaner import Cleaner, EmptyFilesList


class TestCleanerBasic(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dirpath = Path(self.temp_dir.name)
        for i in range(16):
            with tempfile.NamedTemporaryFile(dir=self.temp_dirpath, delete=False):
                pass

    def test_cascades(self):
        """
        Instead of writing methods without return values, make them return self
        This allows cascading of methods
        """
        cleaner = Cleaner(self.temp_dirpath)
        is_enabled = cleaner.analyze_path().cleanup().is_file_enabled("midi")
        self.assertEqual(is_enabled, False)

        cleaner = Cleaner(self.temp_dirpath, files_supported={"audio": {"midi": "on"}})
        is_enabled = cleaner.analyze_path().cleanup().is_file_enabled("midi")
        self.assertNotEqual(is_enabled, False)

    def test_EmptyFilesList_error(self):
        with tempfile.TemporaryDirectory() as d:
            cleaner = Cleaner(d)
            with pytest.raises(EmptyFilesList):
                cleaner.analyze_path().cleanup()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
