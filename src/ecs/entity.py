class Entity:
	def __init__(self, id):
		self.id = id
		self.components = {}

	def add_component(self, component):
		self.components[component.__class__] = component

	def get_component(self, component_type):
		return self.components.get(component_type)
