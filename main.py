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
import os
import pyttsx3



class CameraScreen(Screen):
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
        # self.changeScreen()
        return Image(source = "IMG_" + timestr)


class ControlScreen(Screen):

    def __init__(self, **kwargs):
        super(ControlScreen, self).__init__(**kwargs) 

    # def displayScreenThenLeave(self):
    #     self.changeScreen()
    def repeatSound(self):
        print("repeatSound")
        # implement repeatSOund
    def goBack(self):
        print("goBack")
        # implement goBack
    def goNext(self):
        print("goNext")
        # implement goNext
    def fill(self):
        print("fill")
        # implement fill
    def help(self):
        print("help")
        self.test()
        # implement help
    def print(self):
        print("print")
        # implement print
    def test(self):
        engine = pyttsx3.init()
        engine.say('Sally sells seashells by the seashore.')
        engine.say('The quick brown fox jumped over the lazy dog.')
        # engine.runAndWait()
        print("5")
        return 5





class PrintScreen(Screen):
    pass

class Manager(ScreenManager):

    camera_screen = ObjectProperty(None)
    control_screen = ObjectProperty(None)
    print_screen= ObjectProperty(None)

class ScreensApp(App):

    def build(self):
        manager = Manager()
        return manager


if __name__ == "__main__":
    ScreensApp().run()
