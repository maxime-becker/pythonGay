import csv
import os
from datetime import datetime
from typing import NamedTuple

class GameStats(NamedTuple):
    name: str
    total_score: int
    timeplayed: datetime
    game_played: int
    score_per_game: int
    time_per_game: datetime

class CSVManager:
    def __init__(self, data_directory='data/'):
        self.data_directory = data_directory
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

    def read_csv(self, player_name: str) -> GameStats:
        file_name = os.path.join(self.data_directory, f"{player_name}.csv")
        if not os.path.exists(file_name):
            return self.create_new_player(player_name)
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            data = next(reader)
            return GameStats(
                name=data['name'],
                total_score=int(data['total_score']),
                timeplayed=datetime.strptime(data['timeplayed'], '%Y-%m-%d %H:%M:%S'),
                game_played=int(data['game_played']),
                score_per_game=int(data['score_per_game']),
                time_per_game=datetime.strptime(data['time_per_game'], '%Y-%m-%d %H:%M:%S')
            )

    def create_new_player(self, player_name: str) -> GameStats:
        default_stats = GameStats(
            name=player_name,
            total_score=0,
            timeplayed=datetime.now(),
            game_played=0,
            score_per_game=0,
            time_per_game=datetime.now()
        )
        self.overwrite_csv(player_name, default_stats)
        return default_stats

    def overwrite_csv(self, player_name: str, game_stats: GameStats):
        file_name = os.path.join(self.data_directory, f"{player_name}.csv")
        with open(file_name, mode='w', newline='') as file:
            fieldnames = ['name', 'total_score', 'timeplayed', 'game_played', 'score_per_game', 'time_per_game']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'name': game_stats.name,
                'total_score': game_stats.total_score,
                'timeplayed': game_stats.timeplayed.strftime('%Y-%m-%d %H:%M:%S'),
                'game_played': game_stats.game_played,
                'score_per_game': game_stats.score_per_game,
                'time_per_game': game_stats.time_per_game.strftime('%Y-%m-%d %H:%M:%S')
            })

    def update_field(self, player_name: str, field_name: str, new_value, row_name: str):
        file_name = os.path.join(self.data_directory, f"{player_name}.csv")
        rows = []
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] == row_name:
                    row[field_name] = new_value
                rows.append(row)
        with open(file_name, mode='w', newline='') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def delete_csv(self, player_name: str):
        file_name = os.path.join(self.data_directory, f"{player_name}.csv")
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            raise FileNotFoundError(f"The file {file_name} does not exist.")

