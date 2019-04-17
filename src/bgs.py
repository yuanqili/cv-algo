import cv2
import numpy as np
import sqlalchemy
import sys

if __name__ == '__main__':

    video_path = sys.argv[1]

    # Opens a video
    cap = cv2.VideoCapture(video_path)

    # Kernel for object detection
    kernel_dil = np.ones((20, 20), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))

    # Reads the video
    _, first_frame = cap.read()
    background_reference = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    background_reference = cv2.GaussianBlur(background_reference, (5, 5), 0)

    # Sets up running average background
    avg = np.float32(first_frame)

    frame_index = 0
    while True:
        frame_index += 1
        ret, frame = cap.read()
        if not ret:
            cv2.imwrite(f'avgframe{frame_index}.png', avg)
            break

        cv2.accumulateWeighted(frame, avg, 0.00056)

        background_reference = cv2.convertScaleAbs(avg)
        background_reference = cv2.cvtColor(background_reference, cv2.COLOR_BGR2GRAY)
        background_reference = cv2.GaussianBlur(background_reference, (5, 5), 0)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        # if frame_index % 24 == 0:
        #     background_reference = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     background_reference = cv2.GaussianBlur(background_reference, (5, 5), 0)

        difference = cv2.absdiff(background_reference, gray_frame)
        # If pixel value is greater than a threshold value, it is assigned one value (maybe white), else it is assigned
        # another value (maybe black).
        # The first argument is the source image, which should be a grayscale image.
        # The second argument is the threshold value which is used to classify the pixel vlaues.
        # The third argument is the maxVal which represents the value to be given if pixel value is more than
        #     (sometimes less than) the threshold value.
        # OpenCV provides different styles of thresholding and it is decided by the forth parameter of the function.
        #     - cv2.THRESH_BINARY[_INV]
        #     - cv2.THRESH_TRUNC
        #     - cv2.THRESH_TOZERO[_INV]
        _, difference = cv2.threshold(difference, 32, 255, cv2.THRESH_BINARY)

        difference = cv2.morphologyEx(difference, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(difference, kernel_dil, iterations=1)

        # if frame_index % 30 != 0:
        #     continue

        (contours, hierarchy) = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_index = 0
        for pic, contour in enumerate(contours):
            contour_index += 1
            area = cv2.contourArea(contour)
            if area > 1600:
                x, y, w, h = cv2.boundingRect(contour)
                # cv2.imwrite(f'outputs/chaweng/{frame_index}-{contour_index}.png', frame[y:y+h, x:x+w])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(difference, (x, y), (x + w, y + h), (255, 255, 255), 2)

        if frame_index % 24 == 0:
            print(frame_index)

        if frame_index % 2400 == 0:
            cv2.imwrite(f'avgframe{frame_index}.png', avg)

        cv2.imshow('frame', frame)
        cv2.imshow('difference', difference)
        cv2.imshow('background reference', background_reference)

        # mask = subtractor.apply(frame)
        # cv2.imshow('Frame', frame)
        # cv2.imshow('mask', mask)

        if cv2.waitKey(30) == 27:
            cv2.imwrite(f'avgframe{frame_index}.png', avg)
            break


    cap.release()
    cv2.destroyAllWindows()
