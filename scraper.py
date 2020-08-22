import csv
from pathlib import Path
from typing import Dict, Set


class BotdData:
    DEFAULT_CONNECTION = -5
    STEP = 1

    def __init__(self):
        self._mapping: Dict[str, int] = {}
        self._users: Set[str] = set()

    def __str__(self):
        return "mapping: {0}, users: {1}".format(self._mapping, self._users)

    @property
    def mapping(self) -> Dict[str, int]:
        return self._mapping

    @property
    def users(self) -> Set[str]:
        return self._users

    def get_max_connection(self) -> int:
        return sorted(self._mapping.values(), reverse=True)[0]

    def add_connection(self, botd_author: str, song_sender: str) -> None:
        self._users.add(botd_author)
        self._users.add(song_sender)

        key = BotdData.calculate_key(botd_author, song_sender)
        if key in self._mapping:
            if self._mapping[key] == BotdData.DEFAULT_CONNECTION:
                self._mapping[key] = BotdData.STEP
            else:
                self._mapping[key] = self._mapping[key] + BotdData.STEP
        else:
            self._mapping[key] = BotdData.STEP

    def add_fake_connection(self, user1: str, user2: str) -> None:
        if user1 == user2:
            return
        self._users.add(user1)
        self._users.add(user2)
        self._mapping[BotdData.calculate_key(user1, user2)] = BotdData.DEFAULT_CONNECTION

    @staticmethod
    def calculate_key(user1: str, user2: str) -> str:
        return user1 + '|' + user2 if user1 > user2 else user2 + '|' + user1


def scrape(path_to_file: Path, apply_fake_connections: bool) -> BotdData:
    data = BotdData()
    if apply_fake_connections:
        with path_to_file.open(newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            users = set()
            for row in reader:
                users.add(row['user'])
            for user1 in users:
                for user2 in users:
                    data.add_fake_connection(user1, user2)

    with path_to_file.open(newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        current_botd_author = ''
        already_added = set()
        for row in reader:
            if row['#'] != '':
                current_botd_author = row['user']
                already_added = set()
            elif current_botd_author != row['user']:
                if row['user'] not in already_added:
                    data.add_connection(current_botd_author, row['user'])
                    already_added.add(row['user'])
    return data
