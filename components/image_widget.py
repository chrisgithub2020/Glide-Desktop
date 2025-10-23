from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image
from kivy.properties import NumericProperty


class CustomImageWidget(DragBehavior, Image):
    pass