from kivymd.uix.textfield import MDTextFieldRect
from kivy.uix.behaviors import DragBehavior
from kivy.uix.scatterlayout import ScatterLayout, Scatter


class CustomTextWidget(DragBehavior, MDTextFieldRect):
    size_hint = (.35,.08)
    def __init__(self,pos, **kwargs, ):
        super().__init__(**kwargs)
        self.pos = (pos[0], pos[1]-self.height//2)