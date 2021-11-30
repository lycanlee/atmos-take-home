"""
# First Thoughts:
Being a rectangular polygon I can respresent that as a matrix of 0s and 1s where 0s is it being outside of the boundary and 1 being within the boundary
Need to create matrix from coordinates
When I have matrix I can then build an algorithm to determine if the house fits.

## Things to think about and assumptions:
- Are length and width integers? (will start with assuming so for simplicity, can easy scale everything later)
- Going to start by assuming that boundaries and rectangular polygon will be parallel (no rotation required)
- Assuming length and width are supplied in the same unit of measurement
- Assuming coordinates will fit into the 2D grid provided and I do not need to scale the grid

# Questions:

## What improvements would you make if you were to start over again?

Well first off my solution is not that well coded (or documented) and makes a ton of assumptions ignoring edgecases above.
So I would start there. If I am to put that to the side for a moment, largely my solution is solving the problem
through bruteforce which was largely done just as my first implementation through so I could better understand the problem
before jumping into how others have already solved this mathematically as I beleive trying to solve the problem first can provide
a deeper understanding to solutions later. Let's talk about how I would handle iterating my code in an agile fashion.
First let's start by simply pruning my bruteforce method a bit and then discuss an alternative algorithm for solving this (Which really
should have been my first solution). So first one of the problems with my bruteforce method for searching is that if I do not
find a fitting rectangle in my first pass through the X-axis (fist vector) then I end up iterating over the same space multiple times
as I am only ever incrementing the Y axis by one. There are a few ways that can be solved, one is to store the indexs where I read 0
last row and only check those index's in the next row since I would have already checked for consequetive 1s upwards and stopped at a 0.
Another obvious thing to check which I forgot to do where was right away looking at width and height of the rectangle and determining if it
will even fit in the square matrix once reduced to smallest sub matrix that would contain all the 1s. Ontop of checking that right away I
can also as I am iterating through the rows and columns to stop iterating if the min(length,width) is greater than the number of indexs I
have left in that vector. 

Implementing a different algorithm: Taking inspiration from (https://www.geeksforgeeks.org/maximum-size-sub-matrix-with-all-1s-in-a-binary-matrix/)
We can create a second matrix where each index we store a tuple (or make it a 3d matrix) and in each index we can store consequetive 1s below and to the 
left by iterating through in a similar fashion and adding 1 to the cooresponding value in the touple. Then checking if any of the touples have values greater
or equal to width/length like in the solution I have created.



 


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
