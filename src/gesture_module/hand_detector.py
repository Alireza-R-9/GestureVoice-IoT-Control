import cv2
import mediapipe as mp


class HandDetector:
    """
    Detect and track hands using MediaPipe.
    Provides methods to find hands in an image and return landmark coordinates.
    """

    def __init__(self, mode=False, maxHands=2, detectionCon=0.7, trackCon=0.7):
        """
        Initialize the hand detector.

        Args:
            mode (bool): Static image mode or video stream mode.
            maxHands (int): Maximum number of hands to detect.
            detectionCon (float): Minimum detection confidence [0.0, 1.0].
            trackCon (float): Minimum tracking confidence [0.0, 1.0].
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """
        Detect hands in an image and optionally draw landmarks.

        Args:
            img (numpy.ndarray): BGR image to process.
            draw (bool): Whether to draw hand landmarks on the image.

        Returns:
            numpy.ndarray: Image with or without drawn landmarks.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def get_landmarks(self, img):
        """
        Return landmarks for all detected hands in the image.

        Args:
            img (numpy.ndarray): BGR image used for scaling landmark coordinates.

        Returns:
            list: A list of hands, each hand is a list of tuples (id, cx, cy)
                  representing the landmark index and its pixel coordinates.
        """
        allHands = []
        if self.results.multi_hand_landmarks:
            h, w, c = img.shape
            for hand in self.results.multi_hand_landmarks:
                lmList = []
                for id, lm in enumerate(hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append((id, cx, cy))
                allHands.append(lmList)
        return allHands
