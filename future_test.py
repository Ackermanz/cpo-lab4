import threading
import unittest
import time

from future import MyProcessPoolExecutor, MyTimeoutException, CanceledException


def task(n, second):
    print("threadid: " + str(threading.current_thread()) + "running the task")
    time.sleep(second)
    return n ** 2


class TestFuture(unittest.TestCase):

    def test_IsDone(self):
        excutors = MyProcessPoolExecutor(4)
        f1 = excutors.submit(task, 2, 1)
        time.sleep(3)
        self.assertEqual(f1.IsDone(), True)
        f2 = excutors.submit(task, 2, 3)
        f3 = excutors.submit(task, 4, 10)
        self.assertEqual(f2.IsDone(), False)
        self.assertEqual(f3.IsDone(), False)
        time.sleep(5)
        self.assertEqual(f2.IsDone(), True)
        self.assertEqual(f3.IsDone(), False)

    def test_result(self):
        excutors = MyProcessPoolExecutor(4)
        f1 = excutors.submit(task, 1, 1)
        f1.Result()
        self.assertEqual(f1.result, 1)
        f2 = excutors.submit(task, 3, 4)
        self.assertEqual(f2.result, None)
        f2.Result()
        self.assertEqual(f2.result, 9)

    def test_timeout(self):
        excutors = MyProcessPoolExecutor(4)
        f1 = excutors.submit(task, 1, 1)
        f1.Result()
        self.assertEqual(f1.result, 1)
        try:
            f2 = excutors.submit(task, 3, 4)
            f2.Result(1)
        except MyTimeoutException:
            print("f2 raise MyTimeoutException")
        f3 = excutors.submit(task, 4, 5)
        f3.Result(10)

    def test_IsProgress(self):
        excutors = MyProcessPoolExecutor(4)
        f1 = excutors.submit(task, 1, 5)
        time.sleep(1)
        self.assertEqual(f1.IsProgress(), True)
        time.sleep(1)
        self.assertEqual(f1.IsProgress(), True)
        time.sleep(1)
        self.assertEqual(f1.IsProgress(), True)
        time.sleep(4)
        self.assertEqual(f1.IsProgress(), False)

    def test_Cancel(self):
        excutors = MyProcessPoolExecutor(4)
        f1 = excutors.submit(task, 1, 5)
        with self.assertRaises(CanceledException):
            f1.Cancel()
            f1.Result()
        f2 = excutors.submit(task, 2, 3)
        self.assertEqual(f2.Cancel(), True)
        f3 = excutors.submit(task, 3, 3)
        time.sleep(1)
        self.assertEqual(f3.Cancel(), False)
        f4 = excutors.submit(task, 4, 3)
        time.sleep(5)
        self.assertEqual(f4.Cancel(), False)

    def test_priority(self):
        excutors = MyProcessPoolExecutor(3)
        f1 = excutors.submit(task, 1, 5, priority=1)
        f2 = excutors.submit(task, 2, 5, priority=3)
        time.sleep(1)
        f3 = excutors.submit(task, 3, 5, priority=2)
        f4 = excutors.submit(task, 4, 5, priority=4)
        time.sleep(1)
        self.assertEqual(f1.IsProgress(), True)
        self.assertEqual(f2.IsProgress(), False)
        self.assertEqual(f4.IsProgress(), True)
        self.assertEqual(f3.IsProgress(), False)


if __name__ == '__main__':
    unittest.main()
