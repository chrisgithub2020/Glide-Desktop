from kivy.uix.behaviors import DragBehavior
from kivymd.uix.fitimage import FitImage


class CustomImageWidget(DragBehavior, FitImage):
    size_hint=(None, None)
    size=(100, 100)