from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from typing import Any
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty
from kivy.graphics import Color, Rectangle, Line, Triangle, RoundedRectangle, Ellipse
from kivy.utils import get_color_from_hex

from components.text import CustomTextWidget

class DrawingArea(MDFloatLayout):
    init_x = NumericProperty(0)
    init_y = NumericProperty(0)
    scale = NumericProperty(1)

    drawing_instructions = []
    redo_instruction = []
    tool = StringProperty("Freehand")
    shape = Any

    dotted_line = BooleanProperty(False) ## lines will be broken
    color_fill = BooleanProperty(False) ## shapes will be drawn with color fill
    pen_color = ListProperty([])
    def touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            touch.grab(self)
            self.init_x = touch.x
            self.init_y = touch.y
            with self.canvas:
                Color(self.pen_color[0],self.pen_color[1],self.pen_color[2],self.pen_color[3])
                match self.tool:
                    case "Square":
                        self.draw_rectangle(touch.x-self.init_x, touch.y-self.init_y)
                    case "Line":
                        self.draw_straight_line(touch)
                    case "Freehand":
                        self.draw_line(touch)
                    case "Triangle":
                        self.draw_triangle()
                    case "Rounded Square":
                        self.draw_rounded_rectangle(touch.x-self.init_x, touch.y-self.init_y)
                    case "Ellipse":
                        self.draw_ellipse(touch.x-self.init_x, touch.y-self.init_y)
                    case "Eraser":
                        c = get_color_from_hex("#f0f2f0ff")
                        Color(c[0], c[1], c[2], c[3])
                        self.erase(touch=touch)
            
            if self.tool == "text":
                text = CustomTextWidget((touch.x, touch.y))
                self.add_widget(text)
            
            return True
        
    
    def touch_move(self, touch):
        if self.collide_point(touch.x, touch.y) and touch.grab_current == self:
            if hasattr(self, "shape"):
                match self.tool:
                    case "Square":
                        if not self.color_fill:
                            self.shape.rectangle = (self.init_x, self.init_y, touch.x-self.init_x, touch.y-self.init_y)
                            print(self.shape.dash_length)
                            print(self.shape.dash_offset)
                        else:
                            self.shape.size = (touch.x-self.init_x, touch.y-self.init_y)
                    case "Freehand":
                        touch.ud["free-line"].points += [touch.x, touch.y]
                    case "Line":
                        touch.ud["line"].points = [self.init_x, self.init_y, touch.x, touch.y]
                    case "Triangle":
                        self.shape.points = [self.init_x, self.init_y, touch.x, touch.y, touch.x, self.init_y-(touch.y-self.init_y)]
                    case "Rounded Square":
                        if not self.color_fill:
                            self.shape.rounded_rectangle = (self.init_x, self.init_y, abs(touch.x-self.init_x), abs(touch.y-self.init_y), 20)
                        else:
                            self.shape.size = (touch.x-self.init_x, touch.y-self.init_y)
                    case "Ellipse":
                        if not self.color_fill:
                            self.shape.ellipse = (self.init_x, self.init_y, touch.x-self.init_x, touch.y-self.init_y)
                        else:
                            self.shape.size = (touch.x-self.init_x, touch.y-self.init_y)
                    case "Eraser":
                        touch.ud["eraser"].points += [touch.x, touch.y]
                
            return True
        
        return False
        
    def touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            return True
        
    def scale(self, x_scale: int, y_scale: int):
        """
            Scale all drawings to fit window when window size changes
        """
        for instruction in self.drawing_instructions:
            instruction.size = (instruction.size[0]*x_scale, instruction.size[1]*y_scale)
            instruction.pos = (instruction.pos[0]*x_scale, instruction.pos[1]*y_scale)
        
    def undo(self):
        if len(self.drawing_instructions) > 0:
            instruction = self.drawing_instructions.pop()
            self.canvas.remove(instruction)
            self.redo_instruction.append(instruction)
    
    def redo(self):
        if len(self.redo_instruction) > 0:
            instruction = self.redo_instruction.pop()
            self.canvas.add(instruction)
            self.drawing_instructions.append(instruction)

    def erase(self, touch):
        touch.ud["eraser"] = Line(width=7, points=[self.init_x, self.init_y, self.init_x, self.init_y])
        self.drawing_instructions.append(touch.ud["eraser"])

    def draw_rectangle(self, width, height):
        if not self.color_fill:
            self.shape = Line(rectangle=(self.init_x, self.init_y, width,height),dash_length=10 if self.dotted_line else 1, dash_offset=5 if self.dotted_line else 0 ,width=2 if not self.dotted_line else 1)
        else:
            self.shape = Rectangle(pos=(self.init_x, self.init_y), size=(width, height))
        self.drawing_instructions.append(self.shape)

    def draw_rounded_rectangle(self, width, height):
        if not self.color_fill:
            self.shape = Line(rounded_rectangle=(self.init_x, self.init_y, abs(width), abs(height), 20),dash_length=10 if self.dotted_line else 1, dash_offset=5 if self.dotted_line else 0 , width=2  if not self.dotted_line else 1)
        else:
            self.shape = RoundedRectangle(pos=(self.init_x, self.init_y), size=(width, height), radius=(20,))
        self.drawing_instructions.append(self.shape)

    def draw_straight_line(self, touch):        
        touch.ud["line"] = Line(width=2  if not self.dotted_line else 1, points=[self.init_x, self.init_y, self.init_x, self.init_y], dash_length=10 if self.dotted_line else 1, dash_offset=5 if self.dotted_line else 0)
        self.drawing_instructions.append(touch.ud["line"])

    def draw_line(self, touch):        
        touch.ud["free-line"] = Line(width=2  if not self.dotted_line else 1, points=[self.init_x, self.init_y], dash_length=10 if self.dotted_line else 1, dash_offset=5 if self.dotted_line else 0)
        self.drawing_instructions.append(touch.ud["free-line"])

    def draw_triangle(self):
        if not self.color_fill:
            self.shape = Line(points=[self.init_x, self.init_y, self.init_x, self.init_y, self.init_x, self.init_y],dash_length=10 if self.dotted_line else 1, dash_offset=5 if self.dotted_line else 0 , close=True, width=2  if not self.dotted_line else 1)
        else:
            self.shape = Triangle(points=[self.init_x, self.init_y, self.init_x, self.init_y, self.init_x, self.init_y])
        self.drawing_instructions.append(self.shape)

    def draw_ellipse(self, width, height):
        if not self.color_fill:
            self.shape = Line(ellipse=(self.init_x, self.init_y, width,height), dash_length=10 if self.dotted_line else 1, dash_offset=5 if self.dotted_line else 0 , width=2  if not self.dotted_line else 1)
        else:
            self.shape = Ellipse(pos=(self.init_x, self.init_y), size=(width, height))
        self.drawing_instructions.append(self.shape)