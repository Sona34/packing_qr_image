import Parameters
import glob
import cv2

from PIL import Image

def get_qrcode_images(image_path = Parameters.WorkSpacePath["qrcode_image_path"]):
    
    # get file path
    qrcode_image_files = glob.glob(image_path + "/*.*")

    qr_images = list()
    qr_shapes = list()

    for f in qrcode_image_files:
        img = cv2.imread(f)
        
        # (width, height)
        qr_shape = (img.shape[1], img.shape[0])

        # append conntents
        qr_images.append(img)
        qr_shapes.append(qr_shape)
    
    return qr_images, qr_shapes

if __name__ == "__main__":
    images, items = get_qrcode_images()

    cv2.imwrite('./test.png',images[2])
    print(items)