from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import BooleanProperty, NumericProperty
from kivy.graphics import Color, Rectangle

class DrawingArea(MDBoxLayout):
    init_x = NumericProperty(0)
    init_y = NumericProperty(0)
    def touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            touch.grab(self)
            self.init_x = touch.x
            self.init_y = touch.y
            return True
        
    
    def touch_move(self, touch):
        if self.collide_point(touch.x, touch.y) and touch.grab_current == self:
            with self.canvas:
                Color(1,0,0,1)
                self.draw_rectangle(touch.x-self.init_x, touch.y-self.init_y)
                
            return True
        
        return False
        
    def touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            return True
        

    def draw_rectangle(self, width, height):
        self.rect = Rectangle(pos=(self.init_x, self.init_y), size=(width,height))