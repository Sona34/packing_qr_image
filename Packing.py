import Parameters
import glob
import cv2
import numpy as np
from rectpack import newPacker
import random
import time
import os
import itertools

from PIL import Image
from pyzbar.pyzbar import decode
 
import rectpack.packer as packer
import rectpack.maxrects as maxrects

def get_qrcode_info(image_path = Parameters.WorkSpacePath["qrcode_image_path"]):
    
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

        if w == qrcode_image.shape[0]:
            qrcode_image = cv2.rotate(qrcode_image, cv2.ROTATE_90_CLOCKWISE)
        

        try:
            # packing qrcode_image
            output_image[y:y+h, x:x+w] = qrcode_image
        except ValueError:
            return output_image

    return output_image


if __name__ == "__main__":

    #decode_time = int()

    # packer = newPacker()
    packer = newPacker(mode=packer.PackingMode.Offline, bin_algo=packer.PackingBin.Global, 
pack_algo=maxrects.MaxRectsBssf, sort_algo=packer.SORT_AREA)

    # get bin_shape (width & height)
    bin_width = int(Parameters.parameters["bin_width"])
    bin_height = int(Parameters.parameters["bin_height"])

    # add bin info to packer
    packer.add_bin(bin_width, bin_height, bid=0)
    
    # start_time = time.time()
    i = int()
    # iter loop
    for i in itertools.count():
        # update qrcode info
        qrcode_images, qrcode_items = get_qrcode_info()

        # add rect info to packer
        for index, item in enumerate(qrcode_items):
            packer.add_rect(item[0], item[1], rid=index)
        
        # packing
        packer.pack()

        rect_lists = list()

        # append rect elements to rect_lists
        for r in packer.rect_list():
            # index, x, y, w, h
            rect_lists.append((r[5], r[1], r[2], r[3], r[4]))
        

        # Image placement from calculated values
        output_image = placement_qrcode_images(qrcode_images, rect_lists, bin_width, bin_height)
        output_image_dir = Parameters.WorkSpacePath["output_image_dir"]

        # # save image to different dir
        #output_image_path = os.path.join(output_image_dir, "output_{0:02}.png".format(i + 1))
        #cv2.imwrite(output_image_path, output_image)

        # # save image to same dir
        output_image_path = os.path.join(output_image_dir, "output.png")
        cv2.imwrite(output_image_path, output_image)

        # decode
        decode_start_time = time.time()
        data = decode(Image.open(output_image_path))
        decode_end_time = time.time()

        if len(data) != 0:
            url = str(data)
            break
        # else:
            # print("data is none")
            
        decode_time = decode_end_time - decode_start_time

    # end_time = time.time()
    # Wprocess_time = end_time - start_time

    # get elements
    device_id = Parameters.parameters["device_id"]
    cut_tag = Parameters.parameters["cut_tag"]

    # カットした画像群と使用したデバイスを出力
    print("%s,%d,%d" % (cut_tag, device_id, i + 1))   