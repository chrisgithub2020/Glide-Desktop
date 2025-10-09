from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDColorPicker
from typing import Union
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window

## custom widgets
from components.button import CustomButton
from components.drawing_area import DrawingArea
from kivymd.uix.widget import MDWidget



class MainApp(MDApp):
    is_maximized = BooleanProperty(False)
    is_in_drawing_area = BooleanProperty(False)
    active_tool = StringProperty("pencil")
    statusbar_icon = StringProperty("draw-pen")
    statusbar_tool = StringProperty("Freehand")
    cursor_pos_x = NumericProperty(0)
    cursor_pos_y = NumericProperty(0)
    zoom_value = NumericProperty(50)

    def build(self):
        Window.bind(mouse_pos=self.update_cur_pos)
        self.title = "Glide"
        self.icon = "./ui/images/icon.png"
        self.color_picker = MDColorPicker()
        self.shapes_menu_item = [
                {"text": "Line","leading_icon":"vector-line", "on_release": lambda: self.menu_callback("Line", "vector-line")},
                {"text": "Triangle", "leading_icon": "triangle-outline", "on_release": lambda: self.menu_callback("Triangle", "triangle-outline")},
                {"text": "Square", "leading_icon": "square-outline","on_release": lambda: self.menu_callback("Square", "square-outline")},
                {"text": "Rounded Square", "leading_icon": "square-rounded-outline", "on_release": lambda: self.menu_callback("Rounded Square", "square-rounded-outline")},
                {"text": "Ellipse", "leading_icon":"ellipse-outline", "on_release": lambda: self.menu_callback("Ellipse", "ellipse-outline")},
                {"text": "Arc", "leading_icon":"vector-curve", "on_release": lambda: self.menu_callback("Arc", "vector-curve")}
        ]

        self.lines_menu_items = [
            {"text": "Freehand","leading_icon":"draw-pen", "on_release": lambda: self.menu_callback("Freehand", "draw-pen")},
            {"text": "Dotted","leading_icon":"dots-horizontal", "on_release": lambda: self.menu_callback("Dotted Line", "dots-horizontal")},
            {"text": "Bezier","leading_icon":"vector-bezier", "on_release": lambda: self.menu_callback("Bezier", "vector-bezier")},
        ]
        self.shapes_dropdown = MDDropdownMenu(items=self.shapes_menu_item, id="shapes_dropdown")
        self.lines_dropdown = MDDropdownMenu(items=self.lines_menu_items, id="line_dropdown")
        return Builder.load_file("./ui/main.kv")
    
    def open_dropdown(self, dropdown_type: str, instance):
        self.active_tool = dropdown_type
        if dropdown_type == "shape":
            self.shapes_dropdown.caller = instance
            self.shapes_dropdown.open()
        elif dropdown_type == "pencil":
            self.lines_dropdown.caller = instance
            self.lines_dropdown.open()


    def menu_callback(self, tool_type: str, tool_icon: str):
        ## updating the active tool
        self.statusbar_icon = tool_icon
        self.statusbar_tool = tool_type

        ## closing the dropdown
        self.shapes_dropdown.dismiss()
        self.lines_dropdown.dismiss()

    def open_color_picker(self):
        """Minimize window"""
        self.color_picker.open()
        self.color_picker.bind(
            on_select_color=self.set_color,
            on_release=self.get_selected_color,
        )

    def set_color(self,instance: MDColorPicker, color: list):
        """Maximize or restore window"""
        print(color)

    def get_selected_color(self, instance: MDColorPicker, color_format: str, selected_color: Union[list, str]):
        """Implement dragging of window"""
        print(color_format, selected_color)
        instance.dismiss()

    def update_cur_pos(self, window,  pos):
        """
            Do something when cursor is in drawing area
        """ 
        if self.root.ids["drawing_area"].collide_point(pos[0], pos[1]) and not (self.shapes_dropdown.collide_point(pos[0], pos[1]) or self.lines_dropdown.collide_point(pos[0], pos[1])):
            if not self.is_in_drawing_area:
                Window.set_system_cursor("crosshair")
                self.is_in_drawing_area = True
            self.cursor_pos_x = pos[0]
            self.cursor_pos_y = pos[1]
        else:
            if self.is_in_drawing_area:
                Window.set_system_cursor("arrow")
                self.is_in_drawing_area = False



if __name__ == "__main__":
    MainApp().run()