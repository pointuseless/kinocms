from datetime import timedelta


class Movie:

    def __init__(self, title: str, duration: timedelta):
        self.title = title
        self.duration = duration
