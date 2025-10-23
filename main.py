from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDColorPicker
from typing import Union
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ListProperty
from kivymd.uix.menu import MDDropdownMenu
from plyer import filechooser
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Line, Color

## custom widgets
from components.button import CustomButton
from components.drawing_area import DrawingArea
from components.text import CustomTextWidget
from components.image_widget import CustomImageWidget


   

class MainApp(MDApp):
    is_maximized = BooleanProperty(False)
    is_in_drawing_area = BooleanProperty(False)
    is_dropdown_opened = BooleanProperty(False)
    is_eraser_drawn = BooleanProperty(False)

    active_tool = StringProperty("pencil")
    statusbar_icon = StringProperty("draw-pen")
    statusbar_tool = StringProperty("Freehand")
    cursor_pos_x = NumericProperty(0)
    cursor_pos_y = NumericProperty(0)
    zoom_value = NumericProperty(50)
    dotted_line = BooleanProperty(False) ## everything is in dotted lines
    color_fill = BooleanProperty(False)##shapes are filled with colors
    pen_color = ListProperty([0,0,0,1])

    window_height = NumericProperty(Window.height)
    window_width = NumericProperty(Window.width)
    
    def build(self):
        Window.bind(mouse_pos=self.update_cur_pos)
        Window.bind(on_resize=self.on_resize_window)
        self.title = "Glide"
        self.icon = "./ui/images/icon.png"
        self.color_picker = MDColorPicker(size_hint=(0.4, 0.8))
        self.shapes_menu_item = [
                {"text": "Triangle", "leading_icon": "triangle-outline", "on_release": lambda: self.menu_callback("Triangle", "triangle-outline")},
                {"text": "Square", "leading_icon": "square-outline","on_release": lambda: self.menu_callback("Square", "square-outline")},
                {"text": "Rounded Square", "leading_icon": "square-rounded-outline", "on_release": lambda: self.menu_callback("Rounded Square", "square-rounded-outline")},
                {"text": "Ellipse", "leading_icon":"ellipse-outline", "on_release": lambda: self.menu_callback("Ellipse", "ellipse-outline")},
                {"text": "Arc", "leading_icon":"vector-curve", "on_release": lambda: self.menu_callback("Arc", "vector-curve")}
        ]

        self.lines_menu_items = [
            {"text": "Line","leading_icon":"vector-line", "on_release": lambda: self.menu_callback("Line", "vector-line")},
            {"text": "Freehand","leading_icon":"draw-pen", "on_release": lambda: self.menu_callback("Freehand", "draw-pen")},
            {"text": "Bezier","leading_icon":"vector-bezier", "on_release": lambda: self.menu_callback("Bezier", "vector-bezier")},
        ]
        self.shapes_dropdown = MDDropdownMenu(items=self.shapes_menu_item, id="shapes_dropdown")
        self.lines_dropdown = MDDropdownMenu(items=self.lines_menu_items, id="line_dropdown")
        return Builder.load_file("./ui/main.kv")
    
    def open_dropdown(self, dropdown_type: str, instance):
        self.active_tool = dropdown_type
        self.is_dropdown_opened = True
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

        self.is_dropdown_opened = False

    def open_color_picker(self, button):
        """Minimize window"""
        self.color_picker.open()
        self.color_picker.attach_to = button
        self.color_picker.bind(
            on_select_color=self.set_color,
            on_release=self.get_selected_color,
        )

    def file_manager_open(self, instance):
        image_filters = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.webp"]
        selected_files = filechooser.open_file(title="Choose an Image", multiple=True, filters=image_filters) # type: ignore

        if len(selected_files) > 0:
            for file in selected_files:
                image = CustomImageWidget(source=file)
                self.root.ids["drawing_area"].children[0].add_widget(image)       

    def set_color(self,instance: MDColorPicker, selected_color: list):
        """Maximize or restore window"""
        self.pen_color = selected_color

    def get_selected_color(self, instance: MDColorPicker, color_format: str, selected_color: Union[list, str]):
        """Implement dragging of window"""
        print(color_format, selected_color)
        if color_format == "HEX":
            self.pen_color = get_color_from_hex(selected_color)
        else:
            self.pen_color = selected_color
        instance.dismiss()

    def update_cur_pos(self, window,  pos):
        """
            Do something when cursor is in drawing area
        """ 
        ## is the cursor in the drawing area and no dropdown is open
        if self.root.ids["drawing_area"].collide_point(pos[0], pos[1]) and not self.is_dropdown_opened:
            ## draw a shape
            if not self.is_in_drawing_area and self.active_tool != "eraser" and self.active_tool != "text":
                Window.set_system_cursor("crosshair")
                self.is_in_drawing_area = True

            ## are we using eraser?
            if self.active_tool == "eraser":
                if not self.is_eraser_drawn:
                    ## draw eraser if not drawn
                    Window.show_cursor = False
                    with self.root.ids["drawing_area"].canvas.after:
                        Color(0,0,0,1)
                        self.eraser = Line(ellipse=(pos[0], pos[1], 25,25), width=1.5)
                    self.is_eraser_drawn = True
                else:
                    ## change position of eraser if drawn already
                    self.eraser.ellipse = (pos[0], pos[1], 25, 25)
            ## lets insert text
            elif self.active_tool == "text":
                Window.set_system_cursor("ibeam")

            ## update cursor position
            self.cursor_pos_x = pos[0]
            self.cursor_pos_y = pos[1]
        else:
            if self.is_in_drawing_area:
                self.is_in_drawing_area = False

            if self.is_eraser_drawn:
                ## remove the eraser
                self.root.ids["drawing_area"].canvas.after.remove(self.eraser)
                self.is_eraser_drawn = False
                Window.show_cursor = True

            ## bring back cursor to arrow
            Window.set_system_cursor("arrow")


    def on_resize_window(self, window, width, height):
        ## getting scale factor
        x_scale = width/self.window_width
        y_scale = height/self.window_height

        ##scaling content
        self.root.ids["drawing_area"].scale(x_scale, y_scale)

        self.window_height = height
        self.window_width = width

    def undo(self):
        self.root.ids["drawing_area"].undo()

    def redo(self):
        self.root.ids["drawing_area"].redo()




if __name__ == "__main__":
    MainApp().run()