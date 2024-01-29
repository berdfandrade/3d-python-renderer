# Coordinate Space

Before we dive into the `render` function, we should discuss a little bit of linear algebra

### Coordinate Space 

For our purposes, a Coordinate Space is a origin point and a set of 3 basis vector, usually the $x, y$ $z$ axes.

### Point 

Any point in 3 dimensions can be represented as an offset in the $x, y$ and $z$ directions from the origin point. The representation of a point is relative to the coordinate space that the point is in. The smae point has differente representations in different coordinate spaces. Any point in 3 dimensions can be representd in any 3-dimensional coordinate space.

### Vector

A vector is an $x, y$ and $z$ value representing the difference between two points in the $x, y$ and $z$ axes, respectively.

### Transformation Matrix

In computer graphics, it is convenient to use multiple differente coodinate spaces for different types of points. Transformation matrices convert points 
from on coordinate space to another coordinate space. To convert a vector $v$ from one coordinate space to another, we multiply by a transformation matrix $M:v = Mv.$ Some common transformation matrices are translations, scaling and rotations.

### Model, World, View, and Projection Coordinate Spaces

To draw an item to the screen, we need to convert between a few different coordinate spaces.

Conversion from eye space to homogeneous clop space is handle by `gluPerspective`, and conversion to normalized device space and viewposrt space is handled by `glViewport`. These two matrices are multiplied toghether and soroted as the `GL_PROJECTION` matrix. We don't need to know the terminoly or the details of how these matrices work for this (...)

We do, however, need to manede the lft hand side of the diagram ourselves. We define a matrix which converts points in the model (also called a mesh) from the model spaces into the world space, called the model matrix. We also define the view matrix, which converts from the world space into the eye space. In this project, we combine these two matrices to obtain the ModelView matrix.
