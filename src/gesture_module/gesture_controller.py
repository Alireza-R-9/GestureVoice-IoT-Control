import math

class GestureController:
    """
    Handle hand gesture recognition using landmark points.
    Provides functions to detect finger count, gestures (FIST, FIVE, OK), and open/closed status.
    """

    def __init__(self):
        # Minimum and maximum distances (in pixels) for distance-based gestures
        self.min_distance = 50
        self.max_distance = 300

    def distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        x1, y1 = point1
        x2, y2 = point2
        return math.hypot(x2 - x1, y2 - y1)

    def get_distance_percentage(self, hand_landmarks):
        """
        Calculate distance between thumb tip and index tip as a percentage of min/max range.
        Returns a value between 0 and 100.
        """
        thumb = hand_landmarks[4][1:]
        index_finger = hand_landmarks[8][1:]
        dist = self.distance(thumb, index_finger)
        perc = (dist - self.min_distance) / (self.max_distance - self.min_distance) * 100
        return max(0, min(perc, 100))

    def get_hand_gesture(self, hand_landmarks):
        """
        Determine simple hand gestures:
        - "FIST" if no fingers are open
        - "FIVE" if all fingers are open
        - "UNKNOWN" otherwise
        """
        fingers = []
        tips = [4, 8, 12, 16, 20]

        # Thumb (x-axis comparison)
        if hand_landmarks[tips[0]][1] > hand_landmarks[tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers (y-axis comparison)
        for id in range(1, 5):
            if hand_landmarks[tips[id]][2] < hand_landmarks[tips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = sum(fingers)

        if totalFingers == 0:
            return "FIST"
        elif totalFingers == 5:
            return "FIVE"
        else:
            return "UNKNOWN"

    def count_fingers(self, hand_landmarks):
        """Count the number of fingers that are currently open"""
        fingers = []
        tips = [4, 8, 12, 16, 20]

        if hand_landmarks[tips[0]][1] > hand_landmarks[tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if hand_landmarks[tips[id]][2] < hand_landmarks[tips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    def is_four_fingers(self, hand_landmarks):
        """Check if exactly four fingers are open"""
        return self.count_fingers(hand_landmarks) == 4

    def get_open_fingers(self, hand_landmarks):
        """
        Return the status (open or closed) of each finger (Thumb → Pinky)
        Output: list of 5 boolean values [Thumb, Index, Middle, Ring, Pinky]
        """
        fingers = []
        tips = [4, 8, 12, 16, 20]

        # Thumb (x-axis comparison for right/left hand)
        if hand_landmarks[tips[0]][1] > hand_landmarks[tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers (y-axis comparison)
        for id in range(1, 5):
            if hand_landmarks[tips[id]][2] < hand_landmarks[tips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def is_ok_sign(self, hand_landmarks):
        """
        Detect 'OK' gesture (👌) — when thumb tip and index tip are very close.
        Returns True if distance < threshold.
        """
        thumb_tip = hand_landmarks[4][1:]
        index_tip = hand_landmarks[8][1:]
        distance = self.distance(thumb_tip, index_tip)
        return distance < 30  # Detection threshold (adjustable)
