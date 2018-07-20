import sys
import argparse
import requests
from PIL import Image, ImageFilter,ImageDraw

API_URL = 'https://kapi.kakao.com/v1/vision/face/detect'
MYAPP_KEY = 'd97c1cf5443f691563adec0e826bc64a'

def detect_face(filename):
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}

    try:
        files = { 'file' : open(filename, 'rb')}
        resp = requests.post(API_URL, headers=headers, files=files)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(str(e))
        sys.exit(0)

def rantangle(filename, detection_result):
    image = Image.open(filename)

    for face in detection_result['result']['faces']:
        x = int(face['x']*image.width)
        w = int(face['w']*image.width)
        y = int(face['y']*image.height)
        h = int(face['h']*image.height)
        # box = image.crop((x,y,x+w, y+h))
        # box = box.resize((20,20), Image.NEAREST).resize((w,h), Image.NEAREST)
        # image.paste(box, (x,y,x+w, y+h))
        draw_rectangle=ImageDraw.Draw(image)
        draw_rectangle.rectangle(((x,y),(x+w,y+h)),outline="#ff8888")
    return image



if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Mosaic faces.')
    # parser.add_argument('image_file', type=str, nargs='?', default="./images/05.jpg",
    #                     help='image file to hide faces')

    # args = parser.parse_args()

    image_file='DR0LKDqV4AA-V31.jpg'
    detection_result = detect_face(image_file)
    image = mosaic(image_file, detection_result)
    image.show()