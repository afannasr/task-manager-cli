import os
import tempfile
import unittest

from task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)
        self.manager = TaskManager(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add_task(self):
        task = self.manager.add("Learn Git")
        self.assertEqual(task.task_id, 1)
        self.assertFalse(task.done)

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add("   ")

    def test_complete_and_pending_filter(self):
        self.manager.add("A")
        self.manager.add("B")
        self.manager.complete(1)
        pending = self.manager.list_tasks(show_done=False)
        self.assertEqual([t.title for t in pending], ["B"])

    def test_delete_and_missing_id(self):
        self.manager.add("A")
        self.manager.delete(1)
        self.assertEqual(self.manager.list_tasks(), [])
        with self.assertRaises(KeyError):
            self.manager.find(99)

    def test_data_is_saved_to_file(self):
        self.manager.add("Saved task")
        reloaded = TaskManager(self.path)
        self.assertEqual(reloaded.list_tasks()[0].title, "Saved task")


if __name__ == "__main__":
    unittest.main()
  
