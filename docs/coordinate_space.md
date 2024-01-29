# Coordinate Space

Before we dive into the `render` function, we should discuss a little bit of linear algebra

### Cordinate Space 

For our purposes, a Coordinate Space is a origin point and a set of 3 basis vector, usually the $x, y$ $z$ axes.

### Point 

Any point in 3 dimensions can be represented as an offset in the $x, y$ and $z$ directions from the origin point. The representation of a point is relative to the coordinate space that the point is in. The smae point has differente representations in different coordinate spaces. Any point in 3 dimensions can be representd in any 3-dimensional coordinate space.

### Vector

A vector is an $x, y$ and $z$ value representing the difference between two points in the $x, y$ and $z$ axes, respectively. 