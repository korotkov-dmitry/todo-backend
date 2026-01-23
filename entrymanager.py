import os
from typing import List

from resources import Entry as Entry

class EntryManager:
    def __init__(self, data_path):
        self.data_path: str = data_path
        self.entries: List[Entry] = list()

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        list_dir = os.listdir(self.data_path)
        for entry in list_dir:
            if entry.endswith('.json'):
                content = Entry.load(os.path.join(self.data_path, entry))
                self.entries.append(content)

    def add_entry(self, title: str):
        self.entries.append(Entry(title))


# grocery_list = Entry('Products')