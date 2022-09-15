import numpy as np
import cv2

def AR_landmark():
    # define an empty custom dictionary with 
    aruco_dict = cv2.aruco.custom_dictionary(0, 5, 1)
    # add empty bytesList array to fill with 3 markers later
    aruco_dict.bytesList = np.empty(shape = (15, 4, 4), dtype = np.uint8)

    # Marker 1
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [0,0,1,1,0],
                    [1,1,1,0,1]], dtype = np.uint8)
    aruco_dict.bytesList[0] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 2
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [1,0,1,1,0],
                    [1,0,1,1,0]], dtype = np.uint8)
    aruco_dict.bytesList[1] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 3
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [0,1,1,1,1],
                    [1,0,1,0,0]], dtype = np.uint8)
    aruco_dict.bytesList[2] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 4
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [0,1,1,1,0],
                    [0,1,1,1,0]], dtype = np.uint8)
    aruco_dict.bytesList[3] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 5
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [1,0,1,1,1],
                    [0,1,1,0,0]], dtype = np.uint8)
    aruco_dict.bytesList[4] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 6
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [0,0,1,1,1],
                    [0,0,1,1,1]], dtype = np.uint8)
    aruco_dict.bytesList[5] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 7
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [1,1,1,1,0],
                    [0,0,1,0,1]], dtype = np.uint8)
    aruco_dict.bytesList[6] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 8
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [0,0,1,0,1],
                    [1,1,1,1,0]], dtype = np.uint8)
    aruco_dict.bytesList[7] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 9
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [1,1,1,0,0],
                    [1,1,1,0,0]], dtype = np.uint8)
    aruco_dict.bytesList[8] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 10
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [0,1,1,0,0],
                    [1,0,1,1,1]], dtype = np.uint8)
    aruco_dict.bytesList[9] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 11
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [1,0,1,0,1],
                    [1,0,1,0,1]], dtype = np.uint8)
    aruco_dict.bytesList[10] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 12
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [1,0,1,0,0],
                    [0,1,1,1,1]], dtype = np.uint8)
    aruco_dict.bytesList[11] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 13
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [0,1,1,0,1],
                    [0,1,1,0,1]], dtype = np.uint8)
    aruco_dict.bytesList[12] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 14
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [1,1,1,0,1],
                    [0,0,1,1,0]], dtype = np.uint8)
    aruco_dict.bytesList[13] = cv2.aruco.Dictionary_getByteListFromBits(mybits)
    # Marker 15
    mybits = np.array([[1,1,0,1,1],
                    [1,1,0,1,1],
                    [1,0,1,0,1],
                    [0,0,1,0,0],
                    [0,0,1,0,0]], dtype = np.uint8)
    aruco_dict.bytesList[14] = cv2.aruco.Dictionary_getByteListFromBits(mybits)

    return (aruco_dict)
    