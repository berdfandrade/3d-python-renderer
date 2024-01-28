# A Python 3D Modeller

An impletation of [Erick Dransch's Python 3D Modeller](https://aosabook.org/en/500L/a-3d-modeller.html)

### Introduction

Humans are innately creative. We continuously design and build novel, useful, and interesting things. In modern times, we write software to assist in the design and creation process. Computer-aided design (CAD) software allows creators to design buildings, bridges, video game art, film monsters, 3D printable objects, and many other things before building a physical version of the design.

At their core, CAD tools are a method of abstracting the 3-dimensional design into something that can be viewed and edited on a 2-dimensional screen. To fulfill that definition, CAD tools must offer three basic pieces of functionality. Firstly, they must have a data structure to represent the object that's being designed: this is the computer's understanding of the 3-dimensional world that the user is building. Secondly, the CAD tool must offer some way to display the design on the user's screen. The user is designing a physical object with 3 dimensions, but the computer screen has only 2 dimensions. The CAD tool must model how we perceive objects, and draw them to the screen in a way that the user can understand all 3 dimensions of the object. Thirdly, the CAD tool must offer a way to interact with the object being designed. The user must be able to add to and modify the design in order to produce the desired result. Additionally, all tools would need a way to save and load designs from disk so that users can collaborate, share, and save their work.

A domain-specific CAD tool offers many additional features for the specific requirements of the domain. For example, an architecture CAD tool would offer physics simulations to test climate stresses on the building, a 3D printing tool would have features that check whether the object is actually valid to print, an electrical CAD tool would simulate the physics of electricity running through copper, and a film special effects suite would include features to accurately simulate pyrokinetics.

However, all CAD tools must include at least the three features discussed above: a data structure to represent the design, the ability to display it to the screen, and a method to interact with the design.

With that in mind, let's explore how we can represent a 3D design, display it to the screen, and interact with it, in 500 lines of Python.

### Rendering as a Guide

The driving force behind many of the design decisions in a 3D modeller is the rendering process. We want to be able to store and render complex objects in our design, but we want to keep the complexity of the rendering code low. Let us examine the rendering process, and explore the data structure for the design that allows us to store and draw arbitarily complex objects with simple rendering logic. 