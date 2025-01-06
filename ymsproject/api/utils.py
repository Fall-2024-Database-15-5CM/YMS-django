from math import sqrt

def calculate_distance(x1, y1, x2, y2):
    """
    두 slot 간 유클리드 거리 계산 함수

    Args:
    - x1, y1: 첫 번째 slot의 x, y 좌표 (float)
    - x2, y2: 두 번째 slot의 x, y 좌표 (float)

    Returns:
    - 두 slot 간의 거리 (float)
    """
    try:
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)
    except TypeError as e:
        raise ValueError(f"Invalid coordinates provided: {e}")
