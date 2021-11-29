"""
First Thoughts:
Being a rectangular polygon I can respresent that as a matrix of 0s and 1s where 0s is it being outside of the boundary and 1 being within the boundary
Need to create matrix from coordinates
When I have matrix I can then build an algorithm to determine if the house fits.

Things to think about and assumptions:
- Are length and width integers? (will start with assuming so for simplicity, can easy scale everything later)
- Going to start by assuming that boundaries and rectangular polygon will be parallel (no rotation required)
- Assuming length and width are supplied in the same unit of measurement
- Assuming coordinates will fit into the 2D grid provided and I do not need to scale the grid

"""
import numpy as np
from PIL import Image, ImageDraw


def isCompatible(homeFootprint, lotBoundaries):
    matrix = constructMatrix(lotBoundaries)
    # TODO: Implement setBack by changing 1s to 0s at border of poperty
    # TODO: Cont: Assume that units are same measurement otherwise need to scale
    result = bruteForceAttempt(matrix, homeFootprint[0], homeFootprint[1])
    return result


# This was taken from https://stackoverflow.com/questions/3654289/scipy-create-2d-polygon-mask
# TODO: Replace with your own function that is not using libraries
def constructMatrix(coordinates):
    width = 100  # default to 100 units as specific in initial problem statement
    height = 100  # default to 100 units as specific in initial problem statement
    img = Image.new("L", (width, height), 0)
    ImageDraw.Draw(img).polygon(coordinates, outline=1, fill=1)
    mask = np.array(img)

    return np.asarray(
        mask
    )  # TODO: reduce the matrix to smallest matrix that will contain all the index's with value 1


# Where to write initial algorithm code as brute force to better understand the problem
def bruteForceAttempt(matrix, width, length):
    """
    First lets assume that the matrix being input in already a submatrix
    of the original matrix such that it contains all of the 1s and some 0s
    to fill the boundary where it would not be 1 due to being not a square
    or retangal and rather a rectangular polygon
    
    Start with the first row in the matrix find the first 1
    count the number of consequetive 1s horizontally then vertically
    check if rectangle will fit given consequetive 1s
    if not then continue horizontally starting from the next 0
    for simplicity sake    
    """
    rows = len(matrix)
    columns = len(matrix[0])
    i = 0
    while i < rows:
        j = 0
        while j < columns:
            countHorizontal = 0
            countVertical = 0
            if matrix[i][j] == 1:
                countHorizontal = getConsecutiveOnesHorizontal(
                    i, j, columns, countHorizontal, matrix
                )
                countVertical = getConsecutiveOnesVertical(
                    i, j, rows, countVertical, matrix
                )

            # Check if criteria met
            if (
                countHorizontal != 0
                and countVertical != 0
                and isCriteriaMet(countHorizontal, countVertical, width, length)
            ):
                return True

            # determine horizontal move
            j = determineHorizontalMovement(countHorizontal, width, length, j)

        i += 1
    return False


# this and function below are similar consider refactoring again.
def getConsecutiveOnesHorizontal(x, y, columns, countHorizontal, matrix):
    while y < columns:
        if matrix[x][y] == 1:
            countHorizontal += 1
        else:
            break
        y += 1
    return countHorizontal

# CountVertical likely doesn't need to be passed in because it will always be 0.
# Same comment applies to getConsecutiveOnesHorizontal function
def getConsecutiveOnesVertical(x, y, rows, countVertical, matrix):
    while x < rows:
        if matrix[x][y] == 1:
            countVertical += 1
        else:
            break
        x += 1
    return countVertical


def determineHorizontalMovement(countHorizontal, width, length, index):
    if (countHorizontal == 0) or (countHorizontal - 1 >= min(width, length)):
        index += 1
        return index

    index += countHorizontal
    return index


def isCriteriaMet(countHorizontal, countVertical, width, length):
    print("comparison made ", countHorizontal, countVertical, width, length)
    if (countHorizontal >= width and countVertical >= length) or (
        countHorizontal >= length and countVertical >= width
    ):
        return True
    return False


if __name__ == "__main__":
    result = isCompatible([5, 2], [(1, 1), (5, 1), (5, 9), (3, 2), (1, 1)])
    print("Your house is compatible with this lot: ", result)
