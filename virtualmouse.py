import cv2 #cature video
import mediapipe as mp #recognise hand gesture
import pyautogui #action on different action


def window_down_minimize():
    pyautogui.hotkey('winleft', 'm')


def scroll_window(units):
    pyautogui.scroll(units)


def right_click(axis_x, axis_y):
    pyautogui.rightClick(axis_x, axis_y)



def virtualmouse():
    
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands() #hand detector
    drawing_utils = mp.solutions.drawing_utils #draw points on hand 
    screen_width, screen_height = pyautogui.size() #take height of window

    # variable declaration
    index_y = 0
    index_x = 0
    middle_finger_x = 0
    middle_finger_y = 0
    ring_finger_x = 0
    ring_finger_y = 0
    palm_bottom_x = 0
    palm_bottom_y = 0
    index_bottom_x = 0
    index_bottom_y = 0
    middle_finger_bottom_x = 0
    middle_finger_bottom_y = 0
    little_finger_x = 0
    little_finger_y = 0


    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*frame_width)
                    y = int(landmark.y*frame_height)
                    if id == 8: #tip of index finger
                        cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 255))
                        index_x = screen_width/frame_width*(x+5)
                        index_y = screen_height/frame_height*(y+5)

                    if id == 12: #tip of middle finger
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        middle_finger_x = screen_width/frame_width*(x+5)
                        middle_finger_y = screen_height/frame_height*(y+5)
                    
                    if id == 13: #ring_bottom
                        ring_bottom_x , ring_bottom_y = screen_width/frame_width*(x+5), screen_height/frame_height*(y+5)
                
                    if id == 16: #tip of ring finger
                        ring_finger_x = screen_width/frame_width*(x+5)
                        ring_finger_y = screen_height/frame_height*(y+5)
                        if abs(ring_bottom_y-ring_finger_y)<20:
                            pyautogui.screenshot('my_sc.png')

                    if id == 0: #bottom of palm
                        palm_bottom_x = screen_width/frame_width*(x+5)
                        palm_bottom_y = screen_height/frame_height*(y+5)

                    if id == 9:
                        middle_finger_bottom_x = screen_width/frame_width*(x+5)
                        middle_finger_bottom_y = screen_height/frame_height*(y+5)

                    if id == 5:  #bottom of index finger
                        index_bottom_x = screen_width/frame_width*(x+5)
                        index_bottom_y = screen_height/frame_height*(y+5)
                        if (abs(index_y - index_bottom_y)<50 or abs(middle_finger_y - index_bottom_y) <50 ):
                            scroll_window(-100) #for scroll down
                        elif abs(abs(index_y - palm_bottom_y) < 50 or abs(middle_finger_y - palm_bottom_y)<50):
                            scroll_window(100) # for scroll up
                    if id == 20: #little finger tip
                        little_finger_x = screen_width/frame_width*(x+5)
                        little_finger_y = screen_height/frame_height*(y+5)


                    if id == 4: #tip of thumb
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        thumb_x = screen_width/frame_width*(x+5)
                        thumb_y = screen_height/frame_height*(y+5)

                        #double click 
                        if abs(middle_finger_y-thumb_y)<50 and abs(index_y-thumb_y)<50 and abs(ring_finger_y-thumb_y)<50:
                            pyautogui.doubleClick(index_x,index_y)
                            pyautogui.sleep(1)

                        #left click
                        elif abs(middle_finger_y - thumb_y) < 50: 
                            pyautogui.click(index_x,index_y)
                            pyautogui.sleep(0.2)

                        #move cursor
                        elif abs(index_y - thumb_y) < 150: 
                            pyautogui.moveTo(index_x, index_y,tween = pyautogui.easeInOutQuad)

                        #right click 
                        elif abs(ring_finger_y - thumb_y) < 50:
                            right_click(index_x, index_y)
                            pyautogui.sleep(0.2)

        cv2.imshow('Virtual Mouse', frame)
        cv2.waitKey(1)

virtualmouse()