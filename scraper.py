import csv
from typing import Dict, Set


class BotdData:
    DEFAULT_CONNECTION = -5
    STEP = 1

    mapping: Dict[str, int] = {}
    users: Set[str] = set()

    def get_mapping(self) -> Dict[str, int]:
        return self.mapping

    def get_users(self) -> Set[str]:
        return self.users

    def get_max_connection(self) -> int:
        return sorted(self.mapping.values(), reverse=True)[0]

    def add_connection(self, botd_author: str, song_sender: str) -> None:
        self.users.add(botd_author)
        self.users.add(song_sender)

        key = self.calculate_key(botd_author, song_sender)
        if key in self.mapping:
            if self.mapping[key] == self.DEFAULT_CONNECTION:
                self.mapping[key] = self.STEP
            else:
                self.mapping[key] = self.mapping[key] + self.STEP
        else:
            self.mapping[key] = self.STEP

    def add_fake_connection(self, user1: str, user2: str) -> None:
        if user1 == user2:
            return
        self.users.add(user1)
        self.users.add(user2)
        self.mapping[self.calculate_key(user1, user2)] = self.DEFAULT_CONNECTION

    @staticmethod
    def calculate_key(user1: str, user2: str) -> str:
        return user1 + '|' + user2 if user1 > user2 else user2 + '|' + user1


def scrape(path_to_file: str, apply_fake_connections: bool) -> BotdData:
    data = BotdData()
    if apply_fake_connections:
        with open(path_to_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            users = set()
            for row in reader:
                users.add(row['user'])
            for user1 in users:
                for user2 in users:
                    data.add_fake_connection(user1, user2)

    with open(path_to_file, newline='') as csvfile:
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
