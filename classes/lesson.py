import os


class Lesson:
    def __init__(self, name):
        self.name = name

    def get(self):
        return list(os.walk(f"courses/{self.name}"))[0][1]

    def list(self, lname):
        return list(os.walk(f"courses/{self.name}/{lname}"))[0][2]

    def len(self, lname):
        return len(list(os.walk(f"courses/{self.name}/{lname}"))[0][2])
