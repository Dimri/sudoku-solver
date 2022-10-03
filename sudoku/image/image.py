import cv2
import numpy as np
import copy

from sudoku import utils


WIDTH_IMG = 450
HEIGHT_IMG = 450
model = utils.prediction_model()


#### PREPARE THE IMAGE
img = cv2.imread('../sudoku_unsolved.png')
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgBlank = np.zeros(img.shape, np.uint8)
imgThreshold = utils.preProcess(img)    


#### FIND THE CONTOURS
imgContour = copy.deepcopy(img)
imgBigContour = copy.deepcopy(img)
imgThresholdcopy = copy.deepcopy(imgThreshold)
contours, hierarchy = cv2.findContours(imgThresholdcopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# visualize contours in image
cv2.drawContours(imgContour, contours, -1, (0,255,0), 3)
# showimage('contours', imgContour)


#### FIND THE BIGGEST CONTOURS AND USE IT AS SUDOKU
biggest, maxArea = utils.biggestContour(contours)
biggest = utils.reorder(biggest)
cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 10)
pts1 = np.float32(biggest)
pts2 = np.float32([[0,0],
                [WIDTH_IMG, 0],
                [0, HEIGHT_IMG],
                [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
# warp the sudoku frame to occupy full img
imgWarpColored = cv2.warpPerspective(img, matrix, (WIDTH_IMG, HEIGHT_IMG))
imgDetectedDigits = imgBlank.copy()
# grayscale it
imgWarpColored = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)


#### SPLIT THE IMAGE AND FIND DIGITS
imgSolvedDigits = imgBlank.copy()
boxes = utils.splitBoxes(imgWarpColored)
numbers = utils.get_prediction(boxes, model)
numbers = np.array(numbers)
imgDetectedDigits = utils.displaynums(imgDetectedDigits, numbers, color=(255,0,255))
# showimage('1', np.concatenate((imgDetectedDigits, img), axis=1))