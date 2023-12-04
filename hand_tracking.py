import cv2
import mediapipe as mp

class HandTracker():
    def __init__(self, mode=False, max_hands=1, detection_con=0.5, model_complexity=1, track_con=0.5):
        # Initialize the HandTracker with the specified parameters
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.model_complexity = model_complexity
        self.track_con = track_con
        self.mp_hands = mp.solutions.hands
        # Initialize the hand tracking module from the Mediapipe library
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complexity,
                                         self.detection_con, self.track_con)
        self.mp_draw = mp.solutions.drawing_utils
    
    def handFinder(self, image, draw=True):
        # Convert the image to RGB format
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Process the image to detect hand landmarks
        self.results = self.hands.process(imgRGB)
        # Draw hand landmarks on the image if specified
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(image, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        # Return the image with overlaid hand landmarks
        return image
    
    def positionFinder(self, image, handNo=0, draw=False):
        lm_list = []
        # Check if hand landmarks are detected
        if self.results.multi_hand_landmarks:
            # Get the landmarks of the specified hand
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                h, w, c = image.shape
                # Get the pixel coordinates of the landmarks
                cx, cy = int(lm.x * w), int(lm.y * h)
                # Append the landmark id and coordinates to the list
                lm_list.append([id, cx, cy])
            # Draw a circle at the last landmark if specified
            if draw:
                cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        # Return the list of landmark ids and coordinates
        return lm_list
    