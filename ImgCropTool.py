import argparse
import datetime
import os
import sys
import keyboard
import cv2

class Cropper:
    def __init__(self):
        self.p0 = [None, None]
        self.p1 = [None, None]
        self.p1s = [None, None]
        self.img = None
        self.img_org = None
        self.save_size = (640, 640)
        

    def make_squared(self):
        """Make a rectangle as a square by adjusting to the longer side."""
        if self.p0[0] is None or self.p1s[0] is None:
            return  # Do nothing if the points are not both defined.
        width = abs(self.p1s[0] - self.p0[0])
        height = abs(self.p1s[1] - self.p0[1])
        side_length = max(width, height)
        p1_x = self.p0[0] + side_length if self.p1s[0] > self.p0[0] else self.p0[0] - side_length
        p1_y = self.p0[1] + side_length if self.p1s[1] > self.p0[1] else self.p0[1] - side_length
        return  (p1_x, p1_y)

    def draw_box(self):
        """Draw box which selected by mouse dragging."""
        boxed = self.img.copy()
        _p1=self.make_squared()
        boxed = cv2.rectangle(boxed, tuple(self.p0), _p1, (0, 255, 0), 2)
        cv2.imshow('image', boxed)

    def save_box(self, _dir_out):
        """Save the boxed area as an image."""
        now = datetime.datetime.now()
        filename = now.strftime('%Y-%m-%d_%H-%M-%S')

        _p1=self.make_squared()
        x0 = int(min(self.p0[0], _p1[0]) // self.resize_ratio)
        y0 = int(min(self.p0[1], _p1[1]) // self.resize_ratio)
        x1 = int(max(self.p0[0], _p1[0]) // self.resize_ratio)
        y1 = int(max(self.p0[1], _p1[1]) // self.resize_ratio)
        img_boxed = self.img_org[y0:y1, x0:x1]
        print(img_boxed.shape)
        img_boxed = cv2.resize(img_boxed, self.save_size)
        cv2.imwrite(os.path.join(_dir_out, filename + '.Jpg'), img_boxed)

        print('Saved image ')

    def drag_box(self, event, x, y,_2,_3):
        """Mouse callback function - by mouse dragging."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.p0[0] = x
            self.p0[1] = y
            self.p1 = [None, None]
        elif event == cv2.EVENT_LBUTTONUP:
            if self.p0[0] == self.p1[0] and self.p0[1] == self.p1[1]:
                self.p0 = [None, None]
                self.p1 = [None, None]
            else:
                self.p1[0] = x
                self.p1[1] = y

        if self.p0[0] is not None and self.p1[0] is None:
            self.p1s=[x,y]
            self.draw_box()

    def process_images(self, dir_in, dir_out):
        """Process images in the input directory."""
        files = [os.path.join(dir_in, each) for each in os.listdir(dir_in) if os.path.isfile(os.path.join(dir_in, each))]
        files.sort()

        nums = len(files)
        idx = 0

        while nums > idx:
            self.img_org = cv2.imread(files[idx], cv2.IMREAD_COLOR)

            if self.img_org is None:
                idx += 1
                continue

            height = self.img_org.shape[0]
            if height > 1000:
                self.resize_ratio = (1000 / height) - 0.15
                self.img = cv2.resize(self.img_org, dsize=(0, 0), fx=self.resize_ratio, fy=self.resize_ratio, interpolation=cv2.INTER_AREA)
            else:
                self.img = self.img_org.copy()

            cv2.imshow('image', self.img)
            cv2.setMouseCallback('image', self.drag_box)
            print('[{}/{}] {}'.format(idx + 1, nums, files[idx]))

            while True:
                k = cv2.waitKey(100) & 0xFF
                if k == ord('q') or cv2.getWindowProperty('image', 0) == -1:
                    cv2.destroyAllWindows()
                    exit()
                elif k == ord('s'):
                    if self.p0[0] is not None and self.p1[0] is not None:
                        self.save_box(dir_out)
                        cv2.imshow('image', self.img)
                        self.p0 = self.p1 = [None, None]
                elif k == ord(' '):
                    idx += 1
                    break
                elif k == ord('b'):
                    idx -= 1
                    break
                elif self.p0[0] is not None and self.p1[0] is not None:
                    if keyboard.is_pressed("up"):
                        self.p0[1] -= 10
                        self.p1s[1] -= 10
                        self.draw_box()
                    elif keyboard.is_pressed("down"):
                        self.p0[1] += 10
                        self.p1s[1] += 10
                        self.draw_box()
                    elif keyboard.is_pressed("left"):
                        self.p0[0] -= 10
                        self.p1s[0] -= 10
                        self.draw_box()
                    elif keyboard.is_pressed("right"):
                        self.p0[0] += 10
                        self.p1s[0] += 10
                        self.draw_box()

        cv2.destroyAllWindows()

if __name__ == '__main__':
    # check and initialize
    input_directory="input"
    output_directory="output"
    if not os.path.isdir(input_directory):
        sys.exit('The input directory does not exist!!!')
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    # run main job for image cropping
    cropper = Cropper()
    cropper.process_images(input_directory, output_directory)