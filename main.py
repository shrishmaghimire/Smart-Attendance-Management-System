## Import necessary packages
import os
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast.kivytoast.kivytoast import toast
from kivy.utils import get_hex_from_color
import sqlite3

from kivymd.uix.dialog import  MDDialog
# NavigationDrawer
from kivy.properties import StringProperty

from kivymd.uix.list import OneLineAvatarListItem

class ContentNavigationDrawer(BoxLayout):
    pass

class NavigationItem(OneLineAvatarListItem):
    icon = StringProperty()


class RootWidget(BoxLayout):
    pass

## This is the main app.

class MainApp(MDApp):

    def __init__(self, **kwargs):
        self.title = "Attendance Management System"
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.theme_style="Light"
        super().__init__(**kwargs)
    
    
    def build(self):
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor() 
        c.execute("""CREATE TABLE if not exists students(
            name text
            )""")

        conn.commit()
        conn.close()
        return RootWidget()
    
    def back_to_home_screen(self):
        self.root.ids.student_name.text = ""
        self.root.ids.student_id.text = ""
        self.root.ids.screen_manager.current = "HomeScreen"
    
    def show_ExitDialog(self):
        dialog = MDDialog(
            title="Attendance Management System", 
            text = "Are you [color=%s][b]sure[/b][/color] ?"
            % get_hex_from_color(self.theme_cls.primary_color), 
            size_hint=[.5, .5],
        events_callback=self.stopApp,
        text_button_ok="Exit",
        text_button_cancel="Cancel"
        )
        dialog.open()
    
    def stopApp(self, text_of_selection, popup_widget):
        
        if text_of_selection == "Exit":
            self.stop()
        else:
            pass
    
    def performAttendance(self):
        os.system("python3 faceRecognition.py")
    
    def captureTrainingImages(self, student_name, student_id, screen_manager):
        
        print(len(student_name), len(student_id))
        if len(student_name) > 0 and len(student_name) <= 23 and len(student_id) > 0 and len(student_id) <= 6:
            os.system("python3 captureTrainingImages.py {} {}".format(student_name, student_id))
            toast("Training Images Collected.")
            screen_manager.current = "HomeScreen"
        else:
            toast("Please Enter Correct Details.")
        
    def show_records(self):
        print("Showing Records")
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("Select * from students")
        records = c.fetchall()

        word = ''
        for record in records:
            word = f'{word}\n{record[0]}'
            print(word)
            self.root.ids.word_label.text = f'{word}'
        conn.commit()

        conn.close()
    
MainApp().run()
