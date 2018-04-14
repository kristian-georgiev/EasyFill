# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# from kivy.core.image import Image as CoreImage
# from kivy.uix.image import Image
# import time
# Builder.load_string('''
# <CameraClick>:
#     orientation: 'vertical'
#     Camera:
#         id: camera
#         resolution: (640, 480)
#         play: False
#     ToggleButton:
#         text: 'Play'
#         on_press: camera.play = not camera.play
#         size_hint_y: None
#         height: '48dp'
#     Button:
#         text: 'Capture'
#         size_hint_y: None
#         height: '48dp'
#         on_press: root.capture()
# ''')


# class CameraClick(BoxLayout):
#     def capture(self):
#         '''
#         Function to capture the images and give them the names
#         according to their captured time and date.
#         '''
#         camera = self.ids['camera']
#         timestr = time.strftime("%Y%m%d_%H%M%S")
#         camera.export_to_png("IMG_" + timestr)
#         print("Saved")
#         return Image(source = "IMG_" + timestr)


# class TestCamera(App):

#     def build(self):
#         return CameraClick()
# TestCamera().run() 

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty

import time
import threading


class ScreenOne(Screen):

    pass


class ScreenTwo(Screen):
    health_points = NumericProperty(100)

    def __init__(self, **kwargs):
        print("reachered here")
        super(ScreenTwo, self).__init__(**kwargs)

    def on_health_points(self, instance, value):
        if value < 1:
            self.changeScreen()

    def on_enter(self, *args):
        thread = threading.Thread(target=self.bleed)
        thread.daemon = True
        thread.start()

    def bleed(self, *args):
        while self.health_points > 0:
            self.health_points -= 5
            time.sleep(0.1)

    def displayScreenThenLeave(self):
        self.changeScreen()

    def changeScreen(self):
        if self.manager.current == 'screen1':
            self.manager.current = 'screen2'
        else:
            self.manager.current = 'screen1'


class Manager(ScreenManager):

    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)


class ScreensApp(App):

    def build(self):
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    ScreensApp().run()