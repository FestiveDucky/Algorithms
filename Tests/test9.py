import cv2, pytesseract, keyboard, pyautogui, time
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\alexr\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

myconfig = r"--psm 11 --oem 3"

posx1, posy1 = None, None
while not keyboard.is_pressed('q'):
    if keyboard.is_pressed('+'):
        posx1, posy1 = pyautogui.position()
        time.sleep(0.1)
    if keyboard.is_pressed('-') and (posx1, posy1) != (None, None):
        posx2, posy2 = pyautogui.position()
        posx2 -= posx1
        posy2 -= posy1
        time.sleep(0.1)
        img = pyautogui.screenshot(region=(posx1, posy1, posx2, posy2))
        img.save('Image.png')
        img = cv2.imread("Image.png")

        height, width, _ = img.shape

        data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT)
        text = pytesseract.image_to_string(img)
        print(text)

        amount_boxes = len(data['text'])
        for i in range(amount_boxes):
            if float(data["conf"][i]) > 50:
                (x, y, width, height) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                img = cv2.rectangle(img, (x-5, y-5), (x + width + 5, y + height + 5), (255, 0, 0), 2)
                img = cv2.putText(img, data['text'][i], (x, y + height + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                  (255, 0, 0), 2,
                                  cv2.LINE_AA)

        cv2.imshow("img", img)
        cv2.waitKey(0)

        print((posx1, posy1, posx2, posy2))

        # print(" ".join(text.split()))
        screenshot = False
        posx1, posy1 = None, None
    elif keyboard.is_pressed('-') and (posx1, posy1) == (None, None):
        print("Selected a start point!")
        time.sleep(0.1)



