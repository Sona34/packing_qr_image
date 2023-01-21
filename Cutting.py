import cv2
import cutParameters
import os
import numpy as np

# [height, width] の四角形の情報をもとにカットラインを作成, その後画像を保存
def clip_line_array(qrcode, cutline):

    height, width, channels = qrcode.shape
    
    output_img_dir = cutParameters.WorkSpacePath["OUTPUT_IMG_DIR_PATH"]
    img = np.full((height, width, 3), 255, np.uint8)

    for i in range(len(cutline)):
        clip = qrcode[cutline[i, 0, 0]:cutline[i, 0, 1], cutline[i, 1, 0]:cutline[i, 1, 1]]
        output_img = os.path.join(output_img_dir, "fragment0{}_{}.png".format((len(cutline)),(i+1)))
        cv2.imwrite(output_img, clip)

        # red で四角を描写
        red = (0, 0, 255)
        cv2.rectangle(img, (cutline[i, 1, 0], cutline[i, 0, 0]), (cutline[i, 1, 1], cutline[i, 0, 1]), red, thickness=1, lineType=cv2.LINE_8, shift=0)
        # print((cutline[i, 1, 0], cutline[i, 0, 0]), (cutline[i, 1, 1], cutline[i, 0, 1]))

    test_img = os.path.join("./img/test_img/", "fragment0{}_test.png".format(len(cutline)))
    cv2.imwrite(test_img, img)

def clip9(qrcode):

    height, width, channels = qrcode.shape  
    # print(width, height, channels)

    # 9rect, cut
    for i in range(3):
        for j in range(3):
            clip = qrcode[
                (i * width // 3) : ((i+1) * width // 3), 
                (j * height // 3) : ((j+1) * height // 3)
            ]
            
            tag = (3 * i) + j + 1
            output_img_dir = cutParameters.WorkSpacePath["OUTPUT_IMG_DIR_PATH"]
            output_img = os.path.join(output_img_dir, "fragment09_{}.png".format(tag))

            cv2.imwrite(output_img, clip)

if __name__ == "__main__":
    source_img_path = cutParameters.WorkSpacePath["SOURCE_IMG_PATH"]
    qrcode = cv2.imread(source_img_path)
    cv2.imwrite("qrcode.png", qrcode)
  
    # cutline = np.array([
    # [[0, 200],[0, 300]],
    # [[200, 300],[0, 300]],
    # [[300, 500],[0, 150]],
    # [[0, 150],[100, 400]],
    # [[150, 300], []],
    # [[300, 500], []],
    # [[300, 500], []],
    # [[300, 500], []],

    # qrcode 6
    # cutline = np.array([
    #     [[0, 300], [0, 200]],
    #     [[0, 300],[200, 400]],
    #     [[0, 300],[400, 600]],
    #     [[300, 600],[0, 200]],
    #     [[300, 600],[200, 400]],
    #     [[300, 600],[400, 600]],
    # ])

    # rand-7 400x400
    # cutline = np.array([
    #     [[0, 100], [0, 230]],
    #     [[0, 300], [230, 400]],
    #     [[100, 400], [0, 120]],
    #     [[300, 400], [120, 330]],
    #     [[100, 220], [120, 230]],
    #     [[300, 400], [330, 400]],
    #     [[220, 300], [120, 230]],
    # ])

    # 400x400
    cutline = np.array([
        [[0, 200], [0, 100]],
        [[200, 400], [0, 100]],
        [[0, 200],[100, 300]],
        [[200, 300],[100, 300]],
        [[300, 400],[100, 300]],
        [[0, 400],[300, 400]],
    ])

    cutline = np.array([
        [[0, 200], [0, 200]],
        [[200, 300], [0, 200]],
        [[300, 400],[0, 200]],
        [[0, 400],[200, 300]],
        [[0, 200],[300, 400]],
        [[200, 400],[300, 400]],
    ])

    cutline = np.array([
        [[0, 600],[0, 100]],
        [[0, 600],[100, 200]],
        [[0, 600],[200, 300]],
        [[0, 600],[300, 400]],
        [[0, 600],[400, 500]],
        [[0, 600],[500, 600]],
    ])

    clip_line_array(qrcode, cutline)
    
    # clip9(qrcode)
    