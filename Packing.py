import Parameters
import glob
import cv2
import numpy as np
from rectpack import newPacker
import random
import time
import os
import itertools
import csv

from PIL import Image
from pyzbar.pyzbar import decode 

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
        
        # packing qrcode_image
        output_image[y:y+h, x:x+w] = qrcode_image

    return output_image


if __name__ == "__main__":

    decode_time = int()
    sum_of_count = int()

    # get try steps
    try_steps = Parameters.parameters["try_steps"]

    packer = newPacker()

    # get bin_shape (width & height)
    bin_width = int(Parameters.parameters["bin_width"])
    bin_height = int(Parameters.parameters["bin_height"])

    # add bin info to packer
    packer.add_bin(bin_width, bin_height, bid=0)
    
    start_time = time.time()
    
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
        # output_image_path = os.path.join(output_image_dir, "output_{0:02}.png".format(i + 1))
        # cv2.imwrite(output_image_path, output_image)

        # # save image to same dir
        output_image_path = os.path.join(output_image_dir, "output.png")
        cv2.imwrite(output_image_path, output_image)

        # decode
        decode_start_time = time.time()
        data = decode(Image.open(output_image_path))
        decode_end_time = time.time()

        if len(data) == 0:
            print("Data is none.")
        else:
            url = str(data)
            print("Data is %s" % url[16:38])

            print("%d trials left" % try_steps)
            try_steps -= 1

            if try_steps == 0:
                sum_of_count = i
                break
            
        decode_time = decode_end_time - decode_start_time

    end_time = time.time()
    process_time = end_time - start_time

    # get elements
    try_steps = Parameters.parameters["try_steps"]
    device_id = Parameters.parameters["device_id"]
    csv_path = Parameters.WorkSpacePath["csv_path"]

    # write data to csv
    with open(csv_path, 'a', newline="") as f:
        writer = csv.writer(f)

        l = list()
        l.append(device_id)
        l.append(try_steps)
        l.append(process_time)
        l.append(decode_time)
        l.append(sum_of_count)

        # write l to csv file
        writer.writerow(l)

    f.close()

    # print
    print("device_id : %d" % device_id)
    print("try_steps : %d" % try_steps)
    print("average of proc time : %f" % (process_time / try_steps))
    print("average of decode time : %f" % (decode_time / try_steps))
    print("average of try : %f" % (sum_of_count / try_steps))
    