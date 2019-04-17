import cv2
import numpy as np

lut_u = np.array([[[i, 255-i, 0] for i in range(256)]], dtype=np.uint8)
lut_v = np.array([[[0, 255-i, i] for i in range(256)]], dtype=np.uint8)

if __name__ == '__main__':
    # Opens a video
    cap = cv2.VideoCapture('video/webcam-greenwood-ave.mp4')

    # Kernel for object detection
    kernel_dil = np.ones((20, 20), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # Reads the video
    _, first_frame = cap.read()
    background_reference = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    background_reference = cv2.GaussianBlur(background_reference, (5, 5), 0)

    # Others
    avg = np.float32(first_frame)
    fgbg = cv2.createBackgroundSubtractorMOG2(128, cv2.THRESH_BINARY, 1)

    frame_index = 0
    while True:
        frame_index += 1
        ret, frame = cap.read()
        if not ret:
            break

        masked_image = fgbg.apply(frame)
        masked_image = cv2.morphologyEx(masked_image, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(masked_image, kernel_dil, iterations=1)
        (contours, hierarchy) = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 1600:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                roi_vehicle = frame[y:y - 10 + h + 5, x:x - 8 + w + 10]

        cv2.imshow('masked frame', masked_image)

        if cv2.waitKey(30) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
