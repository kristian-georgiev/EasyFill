# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# from kivy.core.image import Image as CoreImage
# from kivy.uix.image import Image
# import time

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

from gtts import gTTS


Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (1080, 540)
        play: True
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '60dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
    def changeScreen(self):
        if self.manager.current == 'camera_screen':
            self.manager.current = 'control_screen'
        else:
            self.manager.current = 'control_screen'

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_" + timestr)
        print("Saved")
        return Image(source = "IMG_" + timestr)
        self.changeScreen()

class TestCamera(App):

    def build(self):
        return CameraClick()
TestCamera().run()




class CameraScreen(Screen):
    pass


class ControlScreen(Screen):
    health_points = NumericProperty(100)

    def __init__(self, **kwargs):
        print("reached here")
        super(ControlScreen, self).__init__(**kwargs)




    def displayScreenThenLeave(self):
        self.changeScreen()



class PrintScreen(Screen):
    pass

class Manager(ScreenManager):

    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)


class ScreensApp(App):

    def build(self):
        m = Manager(transition=NoTransition())
        return m


if __name__ == "__main__":
    ScreensApp().run()
