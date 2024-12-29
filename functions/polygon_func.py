import numpy as np
def is_in_polygon(point, vertices):
    """
    Checks if a point is inside a convex polygon using the dot product method.

    Parameters:
        point (tuple): Coordinates of the point to check (x, y).
        vertices (list): List of tuples representing the polygon vertices [(x1, y1), (x2, y2), ...] in clockwise order.

    Returns:
        bool: True if the point is inside or on the edge of the polygon, False otherwise.
    """
    px, py = point
    n = len(vertices)
    sign = None

    for i in range(n):
        # Current vertex and next vertex (wrapping around)
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]

        # Vector from point to current vertex
        vec_MPi = np.array([x1 - px, y1 - py])
        # Vector from current vertex to next vertex
        vec_PiPi1 = np.array([x2 - x1, y2 - y1])

        # Calculate the dot product
        scalar_product = np.dot(vec_MPi, vec_PiPi1)

        # Determine the sign of the scalar product
        current_sign = np.sign(scalar_product)

        # If this is the first sign, initialize it
        if sign is None:
            sign = current_sign
        # If the sign is inconsistent, the point is outside the polygon
        elif current_sign != 0 and current_sign != sign:
            return False

    # If all scalar products have the same sign (or are zero), the point is inside or on the edge
    return True
