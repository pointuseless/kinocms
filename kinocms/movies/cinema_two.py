from __future__ import annotations


class Sector:

    def __init__(self, rows_type: str):
        self.type = rows_type
        self.rows = []

    def create_rows(self):

