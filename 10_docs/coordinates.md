# Module Design Document

## Module: coordinates

## Week: 1 – Day 1

## Author: Rodolfo

---

### 1. Purpose

Implement the foundational geometric operations of the rectangular coordinate system:

- Points
- Distance
- Midpoint
- Quadrants
- Basic utilities for later modules (lines, circles, graphs)

This module forms the base of the Week 1 Calculus package.

---

### 2. Mathematical Background

**Distance formula**
d = sqrt( (x2 - x1)^2 + (y2 - y1)^2 )

**Midpoint formula**
M = ( (x1 + x2)/2 , (y1 + y2)/2 )

**Slope formula**
m = (y2 - y1) / (x2 - x1)

**Point–slope form of a line**
y - y1 = m(x - x1)

**Slope–intercept form of a line**
y = mx + b

**Quadrants**

- Q1: x>0, y>0
- Q2: x<0, y>0
- Q3: x<0, y<0
- Q4: x>0, y<0

---

### 3. Data Structures

**Point representation**

- Tuple: (x, y)
- Later extension: class Point(x, y)

**Rationale**

- Tuples are lightweight and easy to use
- A class may be introduced later for richer behavior

---

### 4. Function List

**distance(p1, p2)**

- Inputs: p1=(x1,y1), p2=(x2,y2)
- Output: float
- Description: Euclidean distance

**midpoint(p1, p2)**

- Inputs: p1, p2
- Output: tuple
- Description: Midpoint of two points

**quadrant(p)**

- Input: p=(x,y)
- Output: integer 1–4 or 0 if on axis
- Description: Determine quadrant

---

### 5. Error Handling

- Non-numeric inputs → raise TypeError
- Points not length 2 → raise ValueError
- Points on axes → return 0 for quadrant

---

### 6. Dependencies

- Python `math` module
- No external libraries

---

### 7. Testing Strategy

- Test distance with known triangles
- Test midpoint with symmetric points
- Test quadrant boundaries
- Test invalid inputs

---

### 8. Future Extensions

- Point class with methods
- Vector operations
- N-dimensional generalization
