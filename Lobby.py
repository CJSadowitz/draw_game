"""

"""
class Lobby:
    def __init__(self, seed, s_type, password=None):
        self.type = s_type
        self.seed = seed
        self.password = password
        self.player_list = []

    def get_player_list(self):
        return self.player_list
        
    def get_seed(self):
        return self.seed

    def get_password(self):
        return self.password

    def get_type(self):
        return self.type
        
    def add_player(self, player):
        return self.player_list.append(player)