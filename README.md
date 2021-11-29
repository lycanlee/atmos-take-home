# Project Instructions

Atmos has to find out where we will place a home on a lot in our 3D models. The first part of this process is checking whether the home fits on the lot at all. In this challenge, we want to know whether a given home and a given lot are "compatible", ie. whether the home can fit within the lot.
 
Imagine a 2D grid with a width and length of 100 units.
Homes have a rectangular "building footprint" of the form: "[width, length]".
Lots have "boundaries", an array of coordinates that form a rectilinear polygon (straight lines and right angles only) of the form: "[(x, y), (x, y), ...]".
 
Create a function `isCompatible()` that receives a home's footprint and a lot's boundaries, and returns whether the home is compatible with the lot.
 
The prompt may be ambiguous on some parts - that's intentional! We want you to make reasonable assumptions when faced with ambiguity. We won't judge you on the details; we're more interested in seeing your general approach. Also, feel free to search up anything you'd like; as a hint, there are general mathematical solutions to this problem and its variants.
 
## Bonus

In real life, lots have "setbacks", which are buffer zones within a lot's boundaries that determine how much space must exist between the lot boundaries and the home. Think of them as "padding" in CSS.
 
Assuming setbacks are the same for every side of a lot, specified as an integer in units, incorporate setbacks into the `isCompatible()` function.
 
# How to Submit

Upload your code
Upload your completed project (feel free to make a Gist) to your GitHub, and then paste a link to the repository or Gist below in the form along with any comments you have about your solution.
 
## Questions

Please answer the following questions in your submission:
What improvements would you make if you were to start over again?
In real life, lots are unfortunately not rectilinear - they can be of any general shape. With this in mind, how would you change your approach to determine where a home could fit on a lot?
