import Parameters
import glob
import cv2
import numpy as np
from rectpack import newPacker
import random

from PIL import Image

def get_qrcode_images(image_path = Parameters.WorkSpacePath["qrcode_image_path"]):
    
    # get file path
    qrcode_image_files = glob.glob(image_path + "/*.*")

    # random shuffle file path
    random.shuffle(qrcode_image_files)

    qrcode_images = list()
    qrcode_shapes = list()

    for f in qrcode_image_files:
        img = cv2.imread(f)
        
        # (width, height)
        qrcode_shape = (img.shape[1], img.shape[0])

        # append conntents
        qrcode_images.append(img)
        qrcode_shapes.append(qrcode_shape)
    
    return qrcode_images, qrcode_shapes

def placement_qrcode_images(qrcode_images, rect_lists, bin_width, bin_height):
    
    # create empty bin
    output_image = np.zeros((bin_width, bin_height, 3), dtype=np.uint8)
    
    # get elements from rect_lists
    for rect_list in rect_lists:
        index, x, y, w, h = rect_list
        qrcode_image = qrcode_images[index]
        
        # packing qrcode_image
        output_image[y:y+h, x:x+w] = qrcode_image

    return output_image


if __name__ == "__main__":

    # 新しいパッカーオブジェクトの生成
    packer = newPacker()

    images, items = get_qrcode_images()

    # get bin_shape (width & height)
    bin_width = int(Parameters.parameters["bin_width"])
    bin_height = int(Parameters.parameters["bin_height"])

    # add bin info to packer
    packer.add_bin(bin_width, bin_height, bid=0)

    # add rect info to packer
    for index, item in enumerate(items):
        packer.add_rect(item[0], item[1], rid=index)

    # packing calcurate
    packer.pack()

    rect_lists = list()

    # append rect elements to rect_lists
    for r in packer.rect_list():
        # index, x, y, w, h
        rect_lists.append((r[5], r[1], r[2], r[3], r[4]))
    
    # Image placement from calculated values
    output_image = placement_qrcode_images(images, rect_lists, bin_width, bin_height)

    output_image_path = Parameters.WorkSpacePath["output_image_path"]
    cv2.imwrite(output_image_path, output_image)
    
    
    # # 計測開始時間
    # start_time = time.time()

    # # 試行回数の取得
    # try_steps = Parameters.parameters["try_steps"]

    # for i in range(try_steps):

    #     # decode
    #     decode_start_time = time.time()
    #     data = decode(Image.open())
    #     decode_end_time = time.time()
    
    # # 計測終了時間
    # end_time = time.time()

    # process_time = end_time - start_time