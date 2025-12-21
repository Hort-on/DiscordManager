import random

class RandomSelector:
    def __init__(self):
        self.selected_channel = None

    def ask_channel(self, interaction):

    def ask_quantity_of_teams(self, interaction):

    def command_distribution(self, interaction, members, team_count):
        random.shuffle(members)

        teams = [[] for _ in range(team_count)]

        for i, member in enumerate(members):
            teams[i % team_count].append(member)

        return teams #TODO: запитатись як краще викликати функцію чи через return чи просто як звичайний виклик

    def send_the_result(self, teams, interaction):
