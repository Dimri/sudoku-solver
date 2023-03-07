import cv2
import numpy as np
import copy

from sudoku import utils, app


WIDTH_IMG = 450
HEIGHT_IMG = 450
model = utils.prediction_model()


def prepare_image(IMAGE_PATH):
    """Prepare image and resize to given width and height"""
    img = cv2.imread(IMAGE_PATH)
    img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
    imgBlank = np.zeros(img.shape, np.uint8)
    imgThreshold = utils.preProcess(img)
    return img, imgBlank, imgThreshold


def find_contours(imgThreshold):
    """Find all the contours in the image"""
    imgThresholdcopy = copy.deepcopy(imgThreshold)
    contours, _ = cv2.findContours(
        imgThresholdcopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    return contours


def biggest_contour(contours, imgBigContour):
    """Find biggest contours and use it as sudoku"""
    biggest, _ = utils.biggestContour(contours)
    # reorder points
    biggest = utils.reorder(biggest)
    # draw contour
    # cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 10)

    pts1 = np.float32(biggest)
    pts2 = np.float32(
        [[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]]
    )

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return matrix


def split_image(imgWarpColored):
    """Split the image and find digits"""
    # imgSolvedDigits = imgBlank.copy()
    boxes = utils.splitBoxes(imgWarpColored)
    numbers = utils.get_prediction(boxes, model)
    return np.array(numbers)
    # imgDetectedDigits = utils.displaynums(imgDetectedDigits, numbers, color=(255,0,255))
    # showimage('1', np.concatenate((imgDetectedDigits, img), axis=1))


def digit_matrix(image_path):
    """Given image of sudoku find the digits in it."""
    print(image_path)
    img, imgBlank, imgThreshold = prepare_image(image_path)
    imgBigContour = copy.deepcopy(img)

    # get all contours
    contours = find_contours(imgThreshold)

    # visualize contours in image
    # imgContour = copy.deepcopy(img)
    # cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 3)
    # utils.showimage("contours", imgContour)

    # find biggest contour in the image
    matrix = biggest_contour(contours, imgBigContour)
    # cv2.imwrite(app.config["UPLOAD_FOLDER"] + "big-contour.png", imgBigContour)
    # utils.showimage("big", imgBigContour)
    # warp the sudoku frame to occupy full img
    imgWarpColored = cv2.warpPerspective(img, matrix, (WIDTH_IMG, HEIGHT_IMG))
    cv2.imwrite(app.config["UPLOAD_FOLDER"] + "warped-contour.png", imgWarpColored)
    # imgDetectedDigits = imgBlank.copy()

    # grayscale it
    imgWarpColored = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)

    # get numbers from the image
    numbers = split_image(imgWarpColored)

    return numbers.reshape((9, 9))
