from kivymd.uix.button import MDIconButton, MDRectangleFlatIconButton
from kivy.properties import StringProperty, NumericProperty

class CustomButton(MDIconButton):
    rounded_button = True
    _round_rad = 0
    _radius = 0
    _default_icon_pad=2
    