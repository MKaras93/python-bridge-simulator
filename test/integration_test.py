from client.bridge import MS
import time


def test_server_responds():
    MS.cockpit.hyper_drive_percent = 10
    time.sleep(2)
    MS.cockpit.hyper_drive_percent = -10
