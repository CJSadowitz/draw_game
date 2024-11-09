class Hand:
	def __init__(self, list_cards=[]):
		self.cards = list_cards

class Score:
	def __init__(self, score=None):
		self.score = score

class Value:
	def __init(self, value=None):
		self.value = value

class Type:
	def __init__(self, card_type=None)
		self.card_type = card_type

class Turn:
	def __init__(self, type="number", count=0):
		self.type = type
		self.count = count

class Status:
	def __init__(self, status="alive"):
		self.status = status

class Renderable:
	def __init__(self, type="static", animation_curve=None, sprite_path=""):
		self.type = type
		self.animation_curve = animation_curve
		self.sprite_path = sprite_path

class Position:
	def __init__(self, position_tuple):
		self.pos_x


