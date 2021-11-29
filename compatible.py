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
    return True


if __name__ == "__main__":
    result = isCompatible([5, 2], [(1, 1), (5, 1), (5, 9), (3, 2), (1, 1)])
    print("Your house is compatible with this lot: ", result)
