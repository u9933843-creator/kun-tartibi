"""Kun Tartibi uchun avtomatik testlar.

Ishga tushirish:  python -m unittest tests -v
"""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import main


class TaskTests(unittest.TestCase):
    def setUp(self):
        # Haqiqiy tasks.json ga tegmaslik uchun vaqtinchalik fayl ishlatamiz
        self.tmp = tempfile.TemporaryDirectory()
        self.original = main.DATA_FILE
        main.DATA_FILE = Path(self.tmp.name) / "tasks.json"

    def tearDown(self):
        main.DATA_FILE = self.original
        self.tmp.cleanup()

    def run_quiet(self, func, *args):
        with contextlib.redirect_stdout(io.StringIO()):
            return func(*args)

    def test_add_task(self):
        self.run_quiet(main.add_task, "Git o'rganish")
        tasks = main.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Git o'rganish")
        self.assertFalse(tasks[0]["done"])

    def test_complete_task(self):
        self.run_quiet(main.add_task, "Python mashq")
        self.run_quiet(main.complete_task, 1)
        self.assertTrue(main.load_tasks()[0]["done"])

    def test_edit_task(self):
        self.run_quiet(main.add_task, "Eski matn")
        self.run_quiet(main.edit_task, 1, "Yangi matn")
        self.assertEqual(main.load_tasks()[0]["title"], "Yangi matn")

    def test_delete_task(self):
        self.run_quiet(main.add_task, "Birinchi")
        self.run_quiet(main.add_task, "Ikkinchi")
        self.run_quiet(main.delete_task, 1)
        tasks = main.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Ikkinchi")

    def test_invalid_number_exits(self):
        self.run_quiet(main.add_task, "Yagona")
        with self.assertRaises(SystemExit):
            self.run_quiet(main.edit_task, 5, "x")

    def test_empty_list(self):
        self.assertEqual(main.load_tasks(), [])


if __name__ == "__main__":
    unittest.main()
