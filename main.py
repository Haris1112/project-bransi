from Model import Model
from View import View
from Controller import Controller

model = Model()
view = View(model)
controller = Controller(model, view)