import math


def pos2angle(A, B, aspectRatio):
    """Calculate the angle between two points."""
    x = B[0] - A[0]
    y = B[1] - A[1]
    angle = math.atan2(-y, x / aspectRatio)
    return angle
