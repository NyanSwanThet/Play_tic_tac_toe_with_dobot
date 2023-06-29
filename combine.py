import cv2
import math
import numpy as np
import DobotDllType as dType
import time
import math

def draw_board(board):
    print("-------------")
    print("| {} | {} | {} |".format(board[0], board[1], board[2]))
    print("-------------")
    print("| {} | {} | {} |".format(board[3], board[4], board[5]))
    print("-------------")
    print("| {} | {} | {} |".format(board[6], board[7], board[8]))
    print("-------------")

# Function to check if a player has won
def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Function to check if the game is a tie
def check_tie(board):
    return " " not in board

# Function to evaluate the score of the board
def evaluate(board):
    if check_win(board, "X"):
        return 1
    elif check_win(board, "O"):
        return -1
    else:
        return 0

# Function to recursively search for the best move using minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(board, "X"):
        return 1
    elif check_win(board, "O"):
        return -1
    elif check_tie(board):
        return 0

    if is_maximizing:
        best_score = float("-inf")
        for i, spot in enumerate(board):
            if spot == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i, spot in enumerate(board):
            if spot == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

# Function to make the bot's move
def make_move(board):
    best_score = float("-inf")
    best_move = None

    for i, spot in enumerate(board):
        if spot == " ":
            board[i] = "X"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i

    board[best_move] = "X"
    
    print(f'best move is to {best_move}')
    
    return best_move

def side_to_board(high_coord, side_block_coord, coord):
    
    dType.SetQueuedCmdClear(api)
    
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, high_coord[0], high_coord[1], high_coord[2], high_coord[3], isQueued = 1)
    
    
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, side_block_coord[0], side_block_coord[1], side_block_coord[2], side_block_coord[3], isQueued = 1)
    
    dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, side_block_coord[0], side_block_coord[1], side_block_coord[2]+70, side_block_coord[3], isQueued = 1)
    
    #dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, high_coord[0], high_coord[1], high_coord[2], high_coord[3], isQueued = 1)
    
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, coord[0], coord[1], coord[2]+70, coord[3], isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, coord[0], coord[1], coord[2], coord[3], isQueued = 1)
    
    dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)
    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, high_coord[0], high_coord[1], high_coord[2], high_coord[3], isQueued = 1)[0]
    
    dType.SetQueuedCmdStartExec(api)
    
    print(lastIndex)
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
    
    dType.SetQueuedCmdStopExec(api)

def win_pose():
    dType.SetQueuedCmdClear(api)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, win1[0], win1[1], win1[2], win1[3], isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, win2[0], win2[1], win2[2], win2[3], isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, win1[0], win1[1], win1[2], win1[3], isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, win2[0], win2[1], win2[2], win2[3], isQueued = 1)
    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, win1[0], win1[1], win1[2], win1[3], isQueued = 1)[0]
    dType.SetQueuedCmdStartExec(api)
    
    print(lastIndex)
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
    
    dType.SetQueuedCmdStopExec(api)

def tie_pose():
    dType.SetQueuedCmdClear(api)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, tie1[0], tie1[1], tie1[2], tie1[3], isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, tie2[0], tie2[1], tie2[2], tie2[3], isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, tie1[0], tie1[1], tie1[2], tie1[3], isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, tie2[0], tie2[1], tie2[2], tie2[3], isQueued = 1)
    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, tie1[0], tie1[1], tie1[2], tie1[3], isQueued = 1)[0]
    dType.SetQueuedCmdStartExec(api)
    
    print(lastIndex)
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
    
    dType.SetQueuedCmdStopExec(api)

def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def generate_circle_points(center_x, center_y, radius, num_points):
    circle_points = []
    angle_increment = 2 * math.pi / num_points

    for i in range(num_points):
        angle = i * angle_increment
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        circle_points.append((x, y))

    return circle_points


def win_pose1():
    center_x = 140
    center_y = -140
    distance = calculate_distance(140, -140, 100, -100)
    print("Distance:", distance)
    radius = distance
    num_points = 20
    
    points = generate_circle_points(center_x, center_y, radius, num_points)
    
    dType.SetQueuedCmdClear(api)
    dType.SetPTPCommonParams(api, 50, 50, isQueued = 1)
    for point in points:
        p1 = round(point[0],2)
        p2 = round(point[1], 2)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, p1, p2, 76, 0, isQueued = 1)
        print(p1, p2)
        
    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, high_coord[0], high_coord[1], high_coord[2], high_coord[3], isQueued = 1)[0]
    dType.SetQueuedCmdStartExec(api)
    
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
    
    dType.SetQueuedCmdStopExec(api)

def lose_pose():
    dType.SetQueuedCmdClear(api)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, -110, -30, 0, isQueued = 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, -110, 0, 0, isQueued = 1)
    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, -110, -30, 0, isQueued = 1)[0]
    dType.SetQueuedCmdStartExec(api)
    
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
    
    dType.SetQueuedCmdStopExec(api)

def num_to_move(move, turn_count):
    
    coord_dic = {
        0: coord_a,
        1: coord_b,
        2: coord_c,
        3: coord_d,
        4: coord_e,
        5: coord_f,
        6: coord_g,
        7: coord_h,
        8: coord_i
        }
    
    side_dic = {
        0:side_block_coord_1,
        1:side_block_coord_2,
        2:side_block_coord_3,
        3:side_block_coord_4
        }
    
    return coord_dic[move], side_dic[turn_count]




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
    cv2.imshow('frame', copy_frame)
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
    cap = cv2.VideoCapture(0)  # Change the parameter to a different number if you have multiple cameras
    
    player_turn = True
    bot_turn_count = 0
    
    while True:
        # Read a frame from the video capture
        print('r')
        ret, frame = cap.read()
        if ret:
            
            board = check_board(frame)
            draw_board(board)
            if check_win(board, "O"):
                draw_board(board)
                print("You win!")
                lose_pose()
                break
            
            if check_win(board, "X"):
                draw_board(board)
                print("Bot wins!")
                win_pose()
                break
            
            if check_tie(board):
                draw_board(board)
                print("It's a tie!")
                tie_pose()
                break
            
            if player_turn == True:
                print('player turn')
                
                input('press key after place\n')
                print('new board')
                board = check_board(frame)
                draw_board(board)
                
                if check_win(board, "O"):
                    draw_board(board)
                    print("You win!")
                    win_pose()
                    break

                if check_tie(board):
                    draw_board(board)
                    print("It's a tie!")
                    break
                
            else:
                
                
                print('bot turn')
                move_num = make_move(board)
                
                print('bot make a move at', move_num)
                
                coord, side = num_to_move(move_num, bot_turn_count)
                
                side_to_board(high_coord, side, coord)
                
                bot_turn_count += 1
                
                board = check_board(frame)
                draw_board(board)
                
                if check_win(board, "X"):
                    draw_board(board)
                    print("Bot wins!")
                    break
                
            player_turn = not(player_turn)
            board = check_board(frame)
            
            

        # Check if the user pressed the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
 
    
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll and get the CDLL object
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])




high_coord = [203, 33, 82, 0]

coord_a = [144, -12, -42, 0]
coord_b = [181, -13, -41, 0]
coord_c = [222, -17, -41, 0]

coord_d = [140, -41, -41, 0]
coord_e = [182, -45, -41, 0]
coord_f = [218, -50, -41, 0]

coord_g = [143, -71, -41, 0]
coord_h = [181, -74, -41, 0]
coord_i = [219, -78, -41, 0]


side_block_coord_1 = [150, 50, -43.5, 0]
side_block_coord_2 = [184, 52, -43.5, 0]
side_block_coord_3 = [143, 24, -43.5, 0]
side_block_coord_4 = [180, 24, -43.5, 0]

win1 = [213, -5, 37, 0]
win2 = [143, 0, 102, 0]

tie1 = [130, -150, 109, 0]
tie2 = [130, -150, 73, 0]

main()

#Disconnect Dobot
dType.DisconnectDobot(api)