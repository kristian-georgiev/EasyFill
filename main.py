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

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
from tesserocr import PyTessBaseAPI, PSM, RIL



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
        filename = "IMG_" + timestr
        return Image(source = "IMG_" + timestr)


class ControlScreen(Screen):

    def __init__(self, **kwargs):
        super(ControlScreen, self).__init__(**kwargs) 

    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------

    # Scan

    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------



    def scan(self, filename):
        # import the necessary packages

        def order_points(self, pts):
            # initialzie a list of coordinates that will be ordered
            # such that the first entry in the list is the top-left,
            # the second entry is the top-right, the third is the
            # bottom-right, and the fourth is the bottom-left
            rect = np.zeros((4, 2), dtype="float32")

            # the top-left point will have the smallest sum, whereas
            # the bottom-right point will have the largest sum
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            # now, compute the difference between the points, the
            # top-right point will have the smallest difference,
            # whereas the bottom-left will have the largest difference
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            # return the ordered coordinates
            return rect

        def four_point_transform(self, image, pts):
            # obtain a consistent order of the points and unpack them
            # individually
            rect = self.order_points(pts)
            (tl, tr, br, bl) = rect

            # compute the width of the new image, which will be the
            # maximum distance between bottom-right and bottom-left
            # x-coordiates or the top-right and top-left x-coordinates
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))

            # compute the height of the new image, which will be the
            # maximum distance between the top-right and bottom-right
            # y-coordinates or the top-left and bottom-left y-coordinates
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))

            # now that we have the dimensions of the new image, construct
            # the set of destination points to obtain a "birds eye view",
            # (i.e. top-down view) of the image, again specifying points
            # in the top-left, top-right, bottom-right, and bottom-left
            # order
            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype="float32")

            # compute the perspective transform matrix and then apply it
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
            # return the warped image
            return warped


        # construct the argument parser and parse the arguments
        # ap = argparse.ArgumentParser()
        # ap.add_argument("-i", "--image", required=True,
        #                 help="Path to the image to be scanned")
        # args = vars(ap.parse_args())

        # load the image and compute the ratio of the old height
        # to the new height, clone it, and resize it
        image = cv2.imread(filename)
        ratio = 1
        # ratio = image.shape[0] / 500.0
        # orig = image.copy()
        # image = imutils.resize(image, height=500)

        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(image, 170, 200)

        # show the original image and the edge detected image
        # print("STEP 1: Edge Detection")
        # cv2.imshow("Image", image)
        # cv2.imshow("Edged", edged)
        # cv2.waitKey(10)
        # cv2.destroyAllWindows()


        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        im2, contours, hierarchy = cnts
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break

        # show the contour (outline) of the piece of paper
        # print("STEP 2: Find contours of paper")
        # cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
        # cv2.imshow("Outline", image)
        # cv2.waitKey(10)
        # cv2.destroyAllWindows()

        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = self.four_point_transform(image, screenCnt.reshape(4, 2) * ratio)

        # convert the warped image to grayscale, then threshold it
        # to give it that 'black and white' paper effect
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        T = threshold_local(warped, 11, offset=10, method="gaussian")
        warped = (warped > T).astype("uint8") * 255

        # show the original and scanned images
        # print("STEP 3: Apply perspective transform")
        # cv2.imshow("Original", imutils.resize(orig, height=650))
        # cv2.imshow("Scanned", imutils.resize(warped, height=650))
        # cv2.waitKey(10)
        return warped

    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------

    # Text blocks init

    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------


    def create_blocks_of_text(self, filename):


        THRESHOLD_VALUE = 200

        filename = "fake_form.jpg"
        image = Image.open(filename)
        image = image.convert("L")
        # image.show()

        # imgData = np.asarray(image)
        # img = (imgData > THRESHOLD_VALUE) * 1.0

        with PyTessBaseAPI(psm=PSM.AUTO_OSD) as api:
            api.SetImage(image)
            api.Recognize()

            it = api.AnalyseLayout()
            orientation, direction, order, deskew_angle = it.Orientation()
            print("Orientation: {:d}".format(orientation))

        image = image.rotate(90 * orientation)

        blocks = {}
        with PyTessBaseAPI() as api:
            api.SetImage(image)
            boxes = api.GetComponentImages(RIL.TEXTLINE, True)
            print('Found {} textline image components.'.format(len(boxes)))
            for i, (im, box, _, _) in enumerate(boxes):
                # im is a PIL image object
                # box is a dict with x, y, w and h keys
                api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
                ocrResult = api.GetUTF8Text()
                blocks[ocrResult] = box
                conf = api.MeanTextConf()
                print((u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, " "confidence: {1}, text: {2}").format(
                    i, conf, ocrResult, **box))
        return blocks


    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------

    # Blank init

    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------



    def is_white(self, pixel_val):
        """tuple with (r, g, b) values"""
        return pixel_val > 250  # allow a small noise for white

    def inside_image(self, coords):
        global img
        global width
        global height
        return (coords[0] >= 0 and coords[1] >= 0) and (coords[0] < width and coords[1] < height)

    def extend_dir(self, coords, direction):
        global img
        global width
        global height
        temp_coords = coords
        for magnitude in range(max(width, height) + 2):
            if not self.inside_image(temp_coords):
                return magnitude
            if self.is_white(img[temp_coords]):
                return magnitude
            temp_coords = (temp_coords[0] + direction[0],
                        temp_coords[1] + direction[1])
        return width

    def extend_up(self, coords):
        high = coords[1]
        low = 0
        ans = coords[1]

        while low <= high:
            med = (low + high) // 2
            if self.white_pixels(med, coords[0], coords[1], coords[0]) <= 0:
                high = med - 1
                ans = min(ans, med)
            else:
                low = med + 1
        return coords[1] - ans

    def extend_down(self, coords):
        global height
        low = coords[1]
        high = height - 1
        ans = coords[1]

        while low <= high:
            med = (low + high) // 2
            if self.white_pixels(coords[1], coords[0], med, coords[0]) <= 0:
                low = med + 1
                ans = max(ans, med)
            else:
                high = med - 1
        return ans - coords[1]

    def extend_left(self, coords):
        high = coords[0]
        low = 0
        ans = coords[0]

        while low <= high:
            med = (low + high) // 2
            if self.white_pixels(coords[1], med, coords[1], coords[0]) <= 0:
                high = med - 1
                ans = min(ans, med)
            else:
                low = med + 1
        return coords[0] - ans

    def extend_right(self, coords):
        global width
        low = coords[0]
        high = width - 1
        ans = coords[0]

        while low <= high:
            med = (low + high) // 2
            if self.white_pixels(coords[1], coords[0], coords[1], med) <= 0:
                low = med + 1
                ans = max(ans, med)
            else:
                high = med - 1
        return ans - coords[0]

    def border_distance(self, coords):
        return min(self.extend_up(coords), self.extend_down(coords), self.extend_left(coords), self.extend_right(coords))

    def max_distance_pixel(self):
        global width
        global height
        max_border_distance = 0
        candidate_pixel = (1, 1)
        for i in range(0, width, 7):
            for j in range(0, height, 3):
                pixel_distance = self.border_distance((i, j))
                if pixel_distance > max_border_distance:
                    max_border_distance = pixel_distance
                    candidate_pixel = (i, j)
        return candidate_pixel

    def expand_rectangle_dp(self, pixel):
        best_area = 0
        best_coords = (0, 0, 0, 0)

        for i in range(height):
            for j in range(height):
                # up will be at pixel[1] - i
                # down will be at pixel[1] + j
                up = pixel[1] - i
                down = pixel[1] + j
                if (not self.inside_image((pixel[0], up))):
                    break
                if (not self.inside_image((pixel[0], down))):
                    continue
                if self.white_pixels(up, pixel[0], down, pixel[0]) != 0:
                    continue

                left = self.get_left(pixel[0], up, down)
                right = self.get_right(pixel[0], up, down)

                new_area = (right - left + 1) * (i + j + 1)
                if new_area > best_area:
                    best_area = new_area
                    best_coords = (pixel[0] - left, right - pixel[0], i, j)

        return best_coords

    def get_left(self, right, up, down):
        high = right
        low = 0
        ans = right

        while low <= high:
            med = (low + high) // 2
            if self.white_pixels(up, med, down, right) == 0:
                high = med - 1
                ans = min(ans, med)
            else:
                low = med + 1
        return ans

    def get_right(self, left, up, down):
        global width
        high = width - 1
        low = left
        ans = left

        while low <= high:
            med = (low + high) // 2
            if self.white_pixels(up, left, down, med) == 0:
                low = med + 1
                ans = max(ans, med)
            else:
                high = med - 1
        return ans

    def expand_strategy(self, pixel, strategy):
        up = 0
        down = 0
        left = 0
        right = 0
        expanded = True
        while expanded:
            expanded = False

            for move in strategy:
                if move == 0:  # 0 is left
                    if self.expand_left_right(pixel[1] - up, pixel[1] + down, pixel[0] - left - 1):
                        expanded = True
                        left += 1

                elif move == 1:  # 1 is right
                    if self.expand_left_right(pixel[1] - up, pixel[1] + down, pixel[0] + right + 1):
                        expanded = True
                        right += 1

                elif move == 2:  # 2 is up
                    if self.expand_up_down(pixel[0] - left, pixel[0] + right, pixel[1] - up - 1):
                        expanded = True
                        up += 1

                else:  # 3 is down
                    if self.expand_up_down(pixel[0] - left, pixel[0] + right, pixel[1] + down + 1):
                        expanded = True
                        down += 1

        return (left, right, up, down)

    def expand_rectangle(self, pixel):
        best_area = 0
        best_coords = (0, 0, 0, 0)

        strategies = [(0, 0, 1, 1, 2, 2, 3, 3), (3, 3, 2, 2, 0, 0, 1, 1), (0, 2, 1, 3),
                    (2, 0, 3, 1), (0, 0, 1, 1, 2, 3), (3, 3, 2, 2, 0, 1)]

        for strategy in strategies:
            new_coords = self.expand_strategy(pixel, strategy)
            new_area = (new_coords[1] + new_coords[0]) * \
                (new_coords[2] + new_coords[3])
            if new_area > best_area:
                best_area = new_area
                best_coords = new_coords

        return best_coords

    def expand_up_down(self, left, right, line):
        global img
        for i in range(left, right + 1):
            if not self.inside_image((i, line)) or self.is_white(img[(i, line)]):
                return False  # cannot expand
        return True

    def expand_left_right(self, up, down, line):
        global img
        for i in range(up, down + 1):
            if not self.inside_image((line, i)) or self.is_white(img[(line, i)]):
                return False  # cannot expand
        return True

    def fill_white(self, ul, lr):  # fill in rectangle from upper-left to lower-right
        global img
        for col in range(ul[0], lr[0] + 1):
            for row in range(ul[1], lr[1] + 1):
                img[col, row] = 255  # make everything green!

    def fill_box(self, ul, lr):  # fill in rectangle from upper-left to lower-right
        global img
        for col in range(ul[0], lr[0] + 1):
            for row in range(ul[1], lr[1] + 1):
                img[col, row] = 255  # make everything white!


    # get number of white pixels in rectangle from upper-left to lower-right
    def white_pixels(self, up, left, down, right):
        global dp
        answer = dp[right][down]
        if up != 0:
            answer -= dp[right][up - 1]
        if left != 0:
            answer -= dp[left - 1][down]
        if up != 0 and left != 0:
            answer += dp[left - 1][up - 1]
        return answer

    def preprocess_dp(self):
        global dp
        global img
        global width
        global height
        dp = []
        dp.append([])
        for i in range(height):
            dp[0].append(int(self.is_white(img[0, i])))
        for i in range(1, width):
            for j in range(height):
                if j == 0:
                    dp.append([])
                    dp[i].append(int(self.is_white(img[i, j])))
                else:
                    dp[i].append(int(dp[i - 1][j] + dp[i][j - 1] -
                                    dp[i - 1][j - 1] + int(self.is_white(img[i, j]))))

    def find_blank(self, num_points=5):
        boxes = []
        for num in range(num_points):
            self.preprocess_dp()
            point = self.max_distance_pixel()
            print(point)
            (left, right, up, down) = self.expand_rectangle_dp(point)
            self.fill_white((point[0] - left, point[1] - up),
                    (point[0] + right, point[1] + down))
            boxes.append(((point[0] - left, point[1] - up),
                        (point[0] + right, point[1] + down)))
            #fill_box((point[0]-10, point[1]-10), (point[0]+10, point[1]+10))
        return boxes

    def blank_init(self, filename):
        im = Image.open(filename)
        im1 = im.filter(ImageFilter.FIND_EDGES)
        im2 = im1.filter(ImageFilter.MaxFilter(size=7))
        rgb_im1 = im2.convert('L')
        #rgb_im1.show()
        global img
        global dp
        global width
        global height
        width, height = rgb_im1.size
        #print(width)
        #print(height)
        img = rgb_im1.load()
        poullas = self.find_blank()
        #rgb_im1.show()
        return poullas


    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------

    # Blank matching

    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------

    def match(self,instruction, blanks):
        """
        Procedure that returns the coordinates of the box that is best linked to the specific instruction
        Ideas: Check upper left coordinate, or lower right coordinate
        """
        return self.closestK(instruction, blanks, k=1)


    def get_center(self,coords):
        return ((coords[0][0] + coords[1][0]) / 2, (coords[0][1] + coords[1][1]) / 2)


    def get_upper_left(self,coords):
        return coords[0]


    def get_lower_right(self,coords):
        return coords[1]


    def get_area(self,coords):
        """Returns area of blank space"""
        return (coords[1][0] - coords[0][0] + 1) * (coords[1][1] - coords[0][1] + 1)


    def euclidean(self,instruction, blank):
        """is waiting two tuples"""
        """we will add bias such that entries lower or to the right are favored"""
        bias = instruction[0] - blank[0] + instruction[1] - blank[1]
        return (instruction[0] - blank[0])**2 + (instruction[1] - blank[1])**2 + bias


    def manhattan(self,instruction, blank):
        """is waiting two tuples"""
        return abs(instruction[0] - blank[0]) + abs(instruction[1] - blank[1])


    def closestK(self,instruction, blanks, k=3):
        blank_dist = []
        for idx in range(len(blanks)):
            blank_dist.append(
                (self.euclidean(instruction, self.get_center(blanks[idx])), idx))
        blank_dist.sort()

        best_area = 0
        best_idx = 0
        for i in range(k):
            new_area = self.get_area(blanks[blank_dist[i][1]])
            if new_area > best_area:
                best_area = new_area
                best_idx = blank_dist[i][1]

        return best_idx


    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------

    # Actually init something here

    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------

    scan = self.scan(filename)
    blocks = self.create_blocks_of_text(filename)
    blanks = self.blank_init(filename)

    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------

    # Button functions

    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------
    # ------------------------

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
    def print_end(self):
        print("print")
        # implement print
    def test(self):
        # engine = pyttsx3.init()
        # engine.say('Sally sells seashells by the seashore.')
        # engine.say('The quick brown fox jumped over the lazy dog.')
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
