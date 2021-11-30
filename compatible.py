"""
# First Thoughts:
Being a rectangular polygon I can respresent that as a matrix of 0s and 1s where 0s is it being outside of the boundary and 1 being within the boundary
Need to create matrix from coordinates
When I have matrix I can then build an algorithm to determine if the house fits.

## Things to think about and assumptions:
- Are length and width integers? (will start with assuming so for simplicity, can easy scale everything later)
- Assuming rectangular verticies provided are integers
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

----------------------------------

## In real life, lots are unfortunately not rectilinear - they can be of any general shape. With this in mind, how would you change your approach 
# to determine where a home could fit on a lot?

Some of the assumptions I ended up making was that length/width as well as the verticies provided where provided in integers. One way to handle this is
to create a constant(k) such that when multipled by length/width and the verticies would become integers. You would then scale everything else by constant(k) including the
steps you take when iterating through the matrix. Why does this matter or how does it apply to this question? Ever played with Photoshop and zoomed deep into an image?
In a rastor file you can think of different polygons as actually being rectangular polygons if you zoom in enough. This would also need to be handled for the case in which a setback
is given in a different unit than the lot boundaries or house footprint. This not be the optimal solution however it would work in theory with a few modifications to ensure that you are
ensuring space is a bit greater than your width to just acount for weird edges.

Thinking through a different alogorithm I would take inspiration from (https://web.archive.org/web/20150221185554/https://d3plus.org/blog/behind-the-scenes/2014/07/08/largest-rect/)
where you first smooth the edges of the polygon. From there you can implement almost the same algorithm except your aspect ratio would be fixed as you have the length and width of the house.
In a convex shape, one alternative you can do is draw lines (vector) between each vertex then take the longest line check if the line length is greater than the max(length,width) if it is
then you can iterate over that line as a vector checking in orthoginal(perpendicular) direction to determine if the width will fit. This doesn't work as well in a non-convex shape as not all verticies
can touch via a straight line by definition, I figure in this case you can likely draw you lines between verticies and in the case that is crosses a boundary move it so the line only touches one vertex and 
touches the outer boundary of the shape and ends at the furthest boundry it can.

As a last next step following the above I would read through: https://www.cs.princeton.edu/~chazelle/pubs/PolygContainmentProb.pdf to get a better understanding of that was done here and see if implementing
this would be a better solution when only having to account for a rectangle (which is an easier problem)


--------------------------------
# Thank you!

Thank you Matt and the Atmos team! This is far from my best work and definitely doesn't represent me ability well. However it is a reflection of how long it's been since I have had to 
code my own solution to something from scratch. I had plenty of fun thinking about the problem and it reminded me again why I not only miss being
more of an individual contributor but also why I NEED to go back and code more to keep my skills sharp. I hope my explanations and understanding of
the problem make up for my poor code and it can be considered along with the rest of the strengths I may bring to the team with my lessons learned scaling a business and team.
Regardless I thank you for the opportunity and the problem, it's been a blast to think about and solve.

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
