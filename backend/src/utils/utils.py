import cv2 as cv


def edge_detection(img):
    img_blur = cv.GaussianBlur(img, (3,3), SigmaX=0, SigmaY=0)
    edges = cv.Canny(image=img_blur, threshold1=100, threshold2=200)
    return edges


