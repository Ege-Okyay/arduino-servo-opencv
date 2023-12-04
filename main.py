import cv2
import math

from pyfirmata import Arduino, SERVO
from hand_tracking import HandTracker

# Set the Arduino board's port (COM4 in this example)
PORT = 'COM4'

# Set the Arduino board's servo pin (PIN 9 in this example)
PIN = 9

# Initialize the Arduino board
board = Arduino(PORT)

# Set the servo pin as an output for servo control
board.digital[PIN].mode = SERVO

# Define a function to calculate the distance between two points
def calculate_distance(x1, x2, y1, y2):
    # Calculate the distance using the Pythagorean theorem
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    # Round the distance to the nearest whole number
    return round(distance)

# Define a function to set the servo motor's angle
def rotate_servo(value):
    # Set the servo motor's angle based on the input value
    board.digital[PIN].write(value)

# Main function
def main():
    # Initialize the video capture device
    cap = cv2.VideoCapture(0)

    # Initialize the HandTracker class
    tracker = HandTracker()

    # Main loop
    while True:
        # Read a frame from the video capture device
        ret, image = cap.read()

        # Check if the frame was read successfully
        if not ret:
            print("No ret")
            break

        # Apply hand tracking to the image
        image = tracker.handFinder(image)

        # Find the hand landmarks (x, y coordinates)
        lm_list = tracker.positionFinder(image)

        # Check if there are hand landmarks
        if len(lm_list) != 0:
            # Get the coordinates of the index and thumb fingers
            index_x = lm_list[8][1]
            index_y = lm_list[8][2]

            thumb_x = lm_list[4][1]
            thumb_y = lm_list[4][2]

            # Calculate the distance between the index and thumb fingers
            distance = calculate_distance(index_x, thumb_x, index_y, thumb_y)

            # Map the distance to a range of 20 to 250
            distance = max(20, min(distance, 250))

            # Set the servo motor's angle based on the calculated distance
            rotate_servo(distance)

            # Print the distance
            print(f"Distance: {distance}")

        # Display the video frame with overlaid hand landmarks
        cv2.imshow("Video", cv2.flip(image, 1))

        # Exit the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close the window
    cap.release()
    cv2.destroyAllWindows()

# Run the main function
if __name__ == "__main__":
    main()
    