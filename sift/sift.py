import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def run_sift(
        n_features,
        n_octave_layers,
        contrast_threshold,
        edge_threshold,
        sigma,
        ratio,
        percentage,
        file1,
        file2
):
    img1 = cv.imread(file1, cv.IMREAD_GRAYSCALE)  # queryImage
    img2 = cv.imread(file2, cv.IMREAD_GRAYSCALE)  # trainImage

    # Initiate SIFT detector
    sift = cv.SIFT_create(
        nfeatures=n_features,
        nOctaveLayers=n_octave_layers,
        contrastThreshold=contrast_threshold,
        edgeThreshold=edge_threshold,
        sigma=sigma
    )

    # find key points and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # BFMatcher with default params
    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    count = 0
    for i, (m, n) in enumerate(matches):
        # print(f'Point {i}, min match {m.distance}, next {n.distance}')
        if m.distance/n.distance <= ratio:
            count += 1
            good.append([m])

    print(f'{count} good matches.')

    # cv.drawMatchesKnn expects list of lists as matches.
    result = cv.drawMatchesKnn(
        img1,
        kp1,
        img2,
        kp2,
        good,
        None,
        matchColor=(255, 0, 0),
        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    Image.fromarray(result).resize((1600, 800)).show()

    key_points_image = cv.drawKeypoints(
        img1,
        kp1,
        None,
        color=(255, 0, 0),
        flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    Image.fromarray(key_points_image).resize((500, 500)).show()

    if count/len(matches) >= percentage:
        return f'SAME - ({round(count/len(matches), 2)}) - {count} out of {len(matches)}.'
    else:
        return f'NOT SAME - ({round(count/len(matches), 3)}) - {count} out of {len(matches)}.'
