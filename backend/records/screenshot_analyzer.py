import cv2
import numpy as np
from easyocr import Reader
from Levenshtein import distance
from json import dumps, JSONDecodeError
from sys import stderr
from subprocess import run

template = cv2.imread('/backend/records/template.png')
height, width = template.shape[:-1]
target_ratio = width / height

# reader = Reader(lang_list=["en"], gpu=False, verbose=False, model_storage_directory='/easyocr/models')


def skin_rectangles(image, ratio):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)

    _, binary = cv2.threshold(contrast, 127, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(contrast, 80, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rects = list()
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h

        if abs(aspect_ratio - ratio) < 0.2 and (200 < w < 300) and (100 < h < 200):
            rects.append(np.array([np.array([x, y]), np.array([x + w, y]),
                                   np.array([x + w, y + h]), np.array([x, y + h])]))

    return rects


def boundaries_from_rectangle(rectangle):
    p1, p2, p3, p4 = rectangle

    x1 = min(p1[0], p2[0], p3[0], p4[0])
    x2 = max(p1[0], p2[0], p3[0], p4[0])
    y1 = min(p1[1], p2[1], p3[1], p4[1])
    y2 = max(p1[1], p2[1], p3[1], p4[1])

    return x1, y1, x2, y2


def info_images(img, rect):
    x1, y1, x2, y2 = boundaries_from_rectangle(rect)
    w = abs(x2 - x1)
    h = abs(y2 - y1)

    y3 = y2 - int(0.34 * h)
    y4 = y2 - int(0.34 * 0.5 * h)

    name_img = img[y3:y4, x1:x2]

    x3 = x1 + int(0.2 * w)
    x4 = x1 + int(0.6 * w)

    count_img = img[y4:y2, x1:x3]
    price_img = img[y4:y2, x4:x2]

    return name_img, count_img, price_img


def price_str(price: str):
    price_str_list = list()
    for el in price:
        if el in '0123456789.,':
            price_str_list.append(el.replace(',', '.'))
    return ''.join(price_str_list)


def count_int(count: str):
    count_str_list = list()
    for el in count:
        if el.isdigit():
            count_str_list.append(el)
    return int(''.join(count_str_list))


def name_str(name: str):
    names = list()
    with open('/backend/records/skins.txt', 'r', encoding='utf-8') as names_file:
        for name_line in names_file:
            name_line = name_line.split(',')[0].strip()
            if name_line:
                names.append(name_line)
    if not names:
        raise PermissionError('Skins list appeared to be empty.')
    return min(names, key=lambda x: distance(name, x))


def analyze_screenshot(path: str) -> list:
    skins = list()

    image = cv2.imread(path)

    global target_ratio

    rectangles = skin_rectangles(image, target_ratio)
    # new = np.copy(image)
    # cv2.drawContours(new, rectangles, -1, (0, 255, 0), 2)
    # cv2.imwrite('result.png', new)

    hi, wi = image.shape[:2]
    image = cv2.resize(image, (wi, hi), interpolation=cv2.INTER_LINEAR)

    # global reader

    # for rectangle in rectangles:
        # name_image, count_image, price_image = info_images(image, rectangle)

        # try:
            # price_res = reader.readtext(price_image, allowlist='G0123456789.,')
            # if price_res[0][-1] < 0.6:
                # raise ValueError(str(price_res))
            # price = price_str(price_res[0][-2])

            # count_res = reader.readtext(count_image)
            # if count_res[0][-1] < 0.6:
                # raise ValueError(str(count_res))
            # count = count_int(count_res[0][-2])

            # name_res = reader.readtext(name_image)
            # if name_res[0][-1] < 0.6:
                # raise ValueError(str(name_res))
            # name = name_str(name_res[0][-2])

            # skins.append({
                # 'name': name,
                # 'price': price,
                # 'count': count
            # })
        # except Exception as e:
            # print(f'Exception in item: {e}', file=stderr)

    return skins


if __name__ == '__main__':
    from sys import argv

    if len(argv) != 2:
        exit(2)

    try:
        skins_list = analyze_screenshot(argv[1])
        skins_dump = dumps(skins_list)
        print(skins_dump)
    except JSONDecodeError:
        exit(3)
    except Exception as ex:
        print(str(ex), file=stderr)
        exit(4)
