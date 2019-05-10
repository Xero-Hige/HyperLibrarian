####################################### Resources ###########################################
import sys


class Queue:

    def __init__(self):
        self.queue = []

    def push(self, value):
        self.queue.append(value)

    def pop(self):
        if not self.queue:
            raise ValueError("Empty queue")

        return self.queue.pop(0)

    def head(self):
        if not self.queue:
            raise ValueError("Empty queue")
        return self.queue[0]

    def empty(self):
        return self.queue != []


######################################## Import #############################################

import skeleton

################################ Inject Resources ###########################################

skeleton.Queue = Queue  # Class injection


################################# Test Definitions ###########################################

def test_upload():
    u = skeleton.Uploader()
    u.enqueue("a")
    assert u.uploaded_files() == 0
    u.enqueue("f")
    u.flush()
    assert u.uploaded_files() == 2


##################################### Test Runner ###########################################

def test_runner(test, testname):
    stdout = sys.stdout  # Prevents executing code to mess with the tests outputs
    try:
        sys.stdout = sys.stderr
        test()
        sys.stdout = stdout
        print(f"{testname}: OK")
    except Exception as e:
        sys.stdout = stdout
        print(f"{testname}: ERROR")
    finally:
        sys.stdout = stdout


# Test 01
test_runner(test_upload, "Test 01")
