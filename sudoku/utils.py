import cv2
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
from tensorflow import keras
from keras.models import load_model


def prediction_model():
    """load the trained model"""
    return load_model("sudoku/model/trained_model")


def showimage(title, img):
    """helper function to show image"""
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def preprocess(img):
    # convert image to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apply gaussian blur
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    # apply adaptive threshold
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
    return imgThreshold


def biggest_contour(contours):
    """find biggest contour with 4 vertices from list of contours"""
    biggest = np.array([])
    max_area = 0
    for contour in contours:
        # find contour area
        area = cv2.contourArea(contour)
        if area > 50:

            # find perimeter
            peri = cv2.arcLength(contour, True)
            # find number of vertices
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            # number of vertices is 4
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area

    return biggest, max_area


def reorder(points):
    """reorder points array as upper left, lower left, lower right, upper right"""
    # create a copy with zeros
    newpoints = np.zeros(points.shape, dtype=np.int32)
    # change shape (4,1,2) -> (4,2)
    points = points.reshape((4, 2))

    # sum along the rows
    add = points.sum(1)
    # min sum -> upper left corner
    newpoints[0] = points[np.argmin(add)]
    # max sum -> lower right corner
    newpoints[3] = points[np.argmax(add)]

    # difference along the rows (y-x)
    diff = np.diff(points, axis=1)
    # min diff -> lower left
    newpoints[1] = points[np.argmin(diff)]
    # max diff -> upper right
    newpoints[2] = points[np.argmax(diff)]

    # return ordered points
    return newpoints


def splitBoxes(img):
    """
    function to split the image into 81 boxes each having 1 digit
    """
    # vertically split into rows
    rows = np.vsplit(img, 9)
    boxes = []  # box image list
    for r in rows:
        # horizontally split rows into individual cells
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)
    return boxes


def get_prediction(boxes, model):
    """
    function to get numbers array from the sudoku photo
    """
    THRESHOLD = 0.8
    numbers = []
    # loop over digit images (sudoku box)
    for image in boxes:
        # preprocess image (same as train data)
        img = np.asarray(image)
        img = img[4 : img.shape[0] - 4, 4 : img.shape[1] - 4]
        img = cv2.resize(img, (28, 28))
        # make image black and white
        img = cv2.bitwise_not(img)
        # increase the contract and brightness
        img = cv2.convertScaleAbs(img, alpha=1.5, beta=5)
        # normalize
        img = img / 255
        # reshape it to the size that the model accepts
        img = img.reshape(1, 28, 28, 1)

        # predict the digit
        predictions = model.predict(img)
        class_index = np.argmax(predictions)  # digit
        prob_val = np.amax(predictions)  # probability value

        print(f"{class_index} {prob_val}")

        # if probability is greater than THRESHOLD add class_idx
        # else add 0 (no digit there)
        if prob_val > THRESHOLD:
            numbers.append(class_index)
        else:
            numbers.append(0)

    return numbers


def displaynums(img, numbers, color):
    """
    function to display the numbers list in 9x9 grid image
    """

    # section width and height
    secW = int(img.shape[0] / 9)
    secH = int(img.shape[1] / 9)

    for x in range(9):
        for y in range(9):
            if numbers[(y * 9) + x] != 0:
                cv2.putText(
                    img,
                    str(numbers[(y * 9) + x]),
                    ((x * secW + int(secW / 2) - 10), int(((y + 0.8) * secH))),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    2,
                    color,
                    2,
                    cv2.LINE_AA,
                )
            else:
                cv2.putText(
                    img,
                    "_",
                    ((x * secW + int(secW / 2) - 10), int(((y + 0.8) * secH))),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    2,
                    color,
                    2,
                    cv2.LINE_AA,
                )

    return img
