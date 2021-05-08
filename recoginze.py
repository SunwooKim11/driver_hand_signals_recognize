
import mediapipe as mp
import math

mp_hands = mp.solutions.hands

def hand_gesture(hand_landmarks):
  coeff = 1
  origin_landmarks_x = []
  origin_landmarks_y = []

  landmarks_x = []    #converted q
  landmarks_y = []

  for loc in mp_hands.HandLandmark:
    origin_landmarks_x.append(1-coeff*hand_landmarks.landmark[loc].x)
    origin_landmarks_y.append(1-coeff*hand_landmarks.landmark[loc].y)
    # print(tmp, ":  x: ", hand_landmarks.landmark[loc].x , "y: ", hand_landmarks.landmark[loc].y)
    # tmp+=1

  d0 = {'x': origin_landmarks_x[0], 'y': origin_landmarks_y[0]}
  d9 = {'x': origin_landmarks_x[9], 'y': origin_landmarks_y[9]}
  d9_from_d0 = {'x' : d9['x'] - d0['x'], 'y' : d9['y'] - d0['y']}

  r = math.sqrt((d9['x'] - d0['x'])**2 + (d9['y'] - d0['y'])**2)
  # get converted coordinate value x, y
  landmarks_x.append(origin_landmarks_x[0]), landmarks_y.append(origin_landmarks_y[0])

  for i in range(1, 9):
    landmarks_x.append(((origin_landmarks_x[i]-d0['x'])*d9_from_d0['y'] - (origin_landmarks_y[i] - d0['y']) * d9_from_d0['x']))
    landmarks_y.append(((origin_landmarks_x[i]-d0['x'])*d9_from_d0['x'] + (origin_landmarks_y[i] - d0['y']) * d9_from_d0['y']))

  landmarks_x.append(origin_landmarks_x[9]), landmarks_y.append(origin_landmarks_y[9])

  for i in range(9, 21):
    landmarks_x.append(((origin_landmarks_x[i]-d0['x'])*d9_from_d0['y'] - (origin_landmarks_y[i] - d0['y']) * d9_from_d0['x']))
    landmarks_y.append(((origin_landmarks_x[i]-d0['x'])*d9_from_d0['x'] + (origin_landmarks_y[i] - d0['y']) * d9_from_d0['y']))

  # get satatus of each finger (OPEN OR CLOSE)
  OPEN_THUMB = False
  OPEN_INDEX_FINGER = False
  OPEN_MIDDLE_FINGER = False
  OPEN_RING_FINGER = False
  OPEN_PINKY = False

  pesudoFixKeyPoint = landmarks_x[2]
  if(landmarks_x[3] > pesudoFixKeyPoint and landmarks_x[4] > pesudoFixKeyPoint):
    OPEN_THUMB = True

  pesudoFixKeyPoint = landmarks_y[6]
  if (landmarks_y[7] > pesudoFixKeyPoint and landmarks_y[8] > pesudoFixKeyPoint):
    OPEN_INDEX_FINGER = True

  pesudoFixKeyPoint = landmarks_y[10]
  if (landmarks_y[11] > pesudoFixKeyPoint and landmarks_y[12] > pesudoFixKeyPoint):
    OPEN_MIDDLE_FINGER = True

  pesudoFixKeyPoint = landmarks_y[14]
  if (landmarks_y[15] > pesudoFixKeyPoint and landmarks_y[16] > pesudoFixKeyPoint):
    OPEN_RING_FINGER = True

  pesudoFixKeyPoint = landmarks_y[18]
  if (landmarks_y[19] > pesudoFixKeyPoint and landmarks_y[20] > pesudoFixKeyPoint):
    OPEN_PINKY = True

  # get gesture
  gesture = "UNKNOWN"
  if(OPEN_INDEX_FINGER and OPEN_MIDDLE_FINGER and OPEN_RING_FINGER and OPEN_PINKY):
    m = d9_from_d0['y']/d9_from_d0['x']
    if(math.tan(2*math.pi/3) < m and m < math.tan(5*math.pi/6)):
      gesture = "Go first"
    else:
      gesture = "Thank you"
  if ((OPEN_THUMB) and (not OPEN_INDEX_FINGER) and (not OPEN_MIDDLE_FINGER) and (not OPEN_RING_FINGER) and (
  OPEN_PINKY)):
    gesture = "There is a pedesterian"


    # if ((OPEN_THUMB) and (OPEN_INDEX_FINGER) and (OPEN_MIDDLE_FINGER) and (OPEN_RING_FINGER) and (OPEN_PINKY)):
    #   gesture = "FIVE"
    #
    # if ((not OPEN_THUMB) and (OPEN_INDEX_FINGER) and (OPEN_MIDDLE_FINGER) and (not OPEN_RING_FINGER) and (
    # not OPEN_PINKY)):
    #   gesture = "TWO"
    #
    # if ((not OPEN_THUMB) and (OPEN_INDEX_FINGER) and (not OPEN_MIDDLE_FINGER) and (not OPEN_RING_FINGER) and (
    # not OPEN_PINKY)):
    #   gesture = "ONE"
    #
    # if ((not OPEN_THUMB) and (not OPEN_INDEX_FINGER) and (not OPEN_MIDDLE_FINGER) and (not OPEN_RING_FINGER) and (
    # not OPEN_PINKY)):
    #   gesture = "FIST"

  return gesture

