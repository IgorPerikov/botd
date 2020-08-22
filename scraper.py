import csv
from typing import Dict, Set


class BotdData:
    mapping: Dict[str, int] = {}
    users: Set[str] = set()

    def get_mapping(self) -> Dict[str, int]:
        return self.mapping

    def get_users(self) -> Set[str]:
        return self.users

    def get_max_affinity(self) -> int:
        return sorted(self.mapping.values(), reverse=True)[0]

    def add(self, botd_author: str, song_sender: str) -> None:
        self.users.add(botd_author)
        self.users.add(song_sender)
        key = botd_author + '|' + song_sender if botd_author > song_sender else song_sender + '|' + botd_author
        if key in self.mapping:
            self.mapping[key] = self.mapping[key] + 1
        else:
            self.mapping[key] = 1


def scrape(path_to_file: str) -> BotdData:
    data = BotdData()
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
                    data.add(current_botd_author, row['user'])
                    already_added.add(row['user'])
    return data
