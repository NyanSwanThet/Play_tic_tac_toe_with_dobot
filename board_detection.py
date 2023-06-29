import cv2
import math
import numpy as np


def draw_board(board):
    print("-------------")
    print("| {} | {} | {} |".format(board[0], board[1], board[2]))
    print("-------------")
    print("| {} | {} | {} |".format(board[3], board[4], board[5]))
    print("-------------")
    print("| {} | {} | {} |".format(board[6], board[7], board[8]))
    print("-------------")


def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def color_checker(image):
    
    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper bounds for the blue color
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    # Define the lower and upper bounds for the green color
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
    
    # Threshold the HSV image to get only blue colors
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    #blue_regions = cv2.bitwise_and(image, image, mask=blue_mask)
    
    
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    #green_regions = cv2.bitwise_and(image, image, mask=green_mask)
    
    # Check if any blue pixels are present
    has_blue = np.any(blue_mask)
    has_green = np.any(green_mask)
    
    if has_blue:
        return 'blue'
    elif has_green:
        return 'green'
    else:
        return 'blank'

def check_board(frame):
    
    copy_frame = frame.copy()
    x1, y1 = 155, 155
    x2, y2 = 388, 388
    
    
    cv2.line(copy_frame, (x1, y1), (x1, y2), 4)
    cv2.line(copy_frame, (x1, y1), (x2, y1), 4)
    cv2.line(copy_frame, (x2, y1), (x2, y2), 4)
    cv2.line(copy_frame, (x1, y2), (x2, y2), 4)
    
    d = calculate_distance(x1, y1, x2, y1)
    p = int(d/3)
    cv2.line(copy_frame, (x1+p, y1), (x1+p, y2), 4)
    cv2.line(copy_frame, (x1+p+p, y1), (x1+p+p, y2), 4)
    cv2.line(copy_frame, (x1, y1+p), (x2, y1+p), 4)
    cv2.line(copy_frame, (x1, y1+p+p), (x2, y1+p+p), 4)
    
    cv2.imshow('f', copy_frame)
    b_a = copy_frame[y1 : y1+p, x1 : x1+p]
    b_b = copy_frame[y1 : y1+p, x1+p : x1+p+p]
    b_c = copy_frame[y1 : y1+p, x1+p+p : x2]
    b_d = copy_frame[y1+p : y1+p+p, x1: x1+p]
    b_e = copy_frame[y1+p : y1+p+p, x1+p : x1+p+p]
    b_f = copy_frame[y1+p : y1+p+p, x1+p+p : x2]
    b_g = copy_frame[y1+p+p : y2, x1: x1+p]
    b_h = copy_frame[y1+p+p : y2, x1+p : x1+p+p]
    b_i = copy_frame[y1+p+p : y2, x1+p+p : x2]
    
    board_frame = [b_a, b_b, b_c,
            b_d, b_e, b_f,
            b_g, b_h, b_i]
    
    board = []
    for b in board_frame:
        color = color_checker(b)
        if color == 'green':
            board.append('O')
        elif color == 'blue':
            board.append('X')
        else:
            board.append(' ')
        
    
    return board
    
    
def main():
    # Open a video capture object
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Change the parameter to a different number if you have multiple cameras
    
    
    
    while True:
        # Read a frame from the video capture
        print('r')
        ret, frame = cap.read()
        if ret:
            
            board = check_board(frame)
            draw_board(board)
            
            

        # Check if the user pressed the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
 
    

main()