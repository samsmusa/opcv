import math
import cv2
import numpy as np
import json

DETECT_CORNER_POINT = 1
DETECT_INNER_BOX = 2
PERCENT = 1
TRUE_FALSE = 2


def get_convex_hull(contour):
    return cv2.convexHull(contour)


def get_contour_area_by_hull_area(contour):
    return (cv2.contourArea(contour) /
            cv2.contourArea(get_convex_hull(contour)))


def get_contour_area_by_bounding_box_area(contour):
    return (cv2.contourArea(contour) /
            cv2.contourArea(get_bounding_rect(contour)))


def get_contour_perim_by_hull_perim(contour):
    return (cv2.arcLength(contour, True) /
            cv2.arcLength(get_convex_hull(contour), True))


def get_contour_perim_by_bounding_box_perim(contour):
    return (cv2.arcLength(contour, True) /
            cv2.arcLength(get_bounding_rect(contour), True))


def get_full_height_by_contour_height(contour, full_height):
    (x, y, w, h) = cv2.boundingRect(contour)
    return full_height / float(h)


def get_full_width_by_contour_width(contour, full_width):
    (x, y, w, h) = cv2.boundingRect(contour)
    return full_width / float(w)


def get_bounding_rect_aspect_ratio(contour):
    (x, y, w, h) = cv2.boundingRect(contour)
    return h / float(w)


def get_important_contour_featues(contour, img):
    (x, y, w, h) = cv2.boundingRect(contour)
    full_width = img.shape[1]
    full_height = img.shape[0]

    try:
        return {
            "hull_area_ratio": get_contour_area_by_hull_area(contour),
            "bounding_area_ratio": get_contour_area_by_bounding_box_area(contour),
            "hull_perim_ratio": get_contour_perim_by_hull_perim(contour),
            "hull_bounding_perim_ratio": get_contour_perim_by_bounding_box_perim(contour),
            "image_height_ratio": h / float(full_height),
            "image_width_ratio": w / float(full_width),
            "aspect_ratio": h / float(w),
            "height": h,
            "width": w
        }
    except ZeroDivisionError:
        return {
            "hull_area_ratio": float("inf"),
            "bounding_area_ratio": float("inf"),
            "hull_perim_ratio": float("inf"),
            "hull_bounding_perim_ratio": float("inf"),
            "image_height_ratio": float("inf"),
            "image_width_ratio": float("inf"),
            "aspect_ratio": float("inf"),
            "height": float("inf"),
            "width": float("inf"),
        }
        # return 7 * [np.inf]


def get_bounding_rect(contour):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    return np.int0(box)


def features_distance(f1, f2):
    f1 = np.array(f1)
    f2 = np.array(f2)
    return np.linalg.norm(f1 - f2)


# Default mutable arguments should be harmless here
def draw_point(point, img, radius=5, color=(0, 0, 255)):
    cv2.circle(img, tuple(point), radius, color, -1)


def draw_text(img, draw_str, pt, padd=0):
    cv2.putText(img, "[" + draw_str + "]", (pt[0] + padd, pt[1] + padd), cv2.FONT_HERSHEY_PLAIN, .7, (0, 0, 200))


def draw_corners(c_img, points):
    (top_left, top_right, bottom_right, bottom_left) = points

    cv2.circle(c_img, tuple(top_left), 5, (10, 200, 20), -1)
    cv2.circle(c_img, tuple(top_right), 5, (10, 200, 20), -1)
    cv2.circle(c_img, tuple(bottom_right), 5, (10, 200, 20), -1)
    cv2.circle(c_img, tuple(bottom_left), 5, (10, 200, 20), -1)
    print("outmost points: ", top_left, top_right, bottom_right, bottom_left)


def get_centroid(contour):
    m = cv2.moments(contour)
    x = int(m["m10"] / m["m00"])
    y = int(m["m01"] / m["m00"])
    return x, y


def normalize(im):
    return cv2.normalize(im, np.zeros(im.shape), 0, 255, norm_type=cv2.NORM_MINMAX)


def get_approx_contour(contour, tol=.01):
    """Get rid of 'useless' points in the contour"""
    epsilon = tol * cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, epsilon, True)


def get_contours(image_gray, mode=cv2.RETR_TREE):
    im2, contours, hierarchy = cv2.findContours(
        image_gray, mode, cv2.CHAIN_APPROX_SIMPLE)

    return [get_approx_contour(cnt) for cnt in contours]
    # return map(get_approx_contour, contours)


def order_points(points):
    """Order points counter-clockwise-ly."""
    origin = np.mean(points, axis=0)

    def positive_angle(p):
        x, y = p - origin
        ang = np.arctan2(y, x)
        return 2 * np.pi + ang if ang < 0 else ang

    return sorted(points, key=positive_angle)


def get_convex_hull_points(contours):
    all_points = np.concatenate(contours)
    hull_points = cv2.convexHull(all_points, False)
    npHull3d = np.array(hull_points)
    return npHull3d


def get_outmost_points_by_summation(hull_points):
    pts = hull_points[:, 0]
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


# image : grayscale image
# pts : 4 points arranged clockwisely
def four_point_transform(image, src):
    # obtain a consistent order of the points and unpack them
    # individually

    (tl, tr, br, bl) = src

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # print(rect, dst)
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


# def get_individual_omr_region(top_left_corners, ):
#     features_distance_for_box


def sort_points_manual(pts):
    tl, tr, br, bl = None, None, None, None

    if pts[0][0] < pts[1][0]:
        tl = pts[0]
        tr = pts[1]
    else:
        tl = pts[1]
        tr = pts[0]

    if pts[2][0] < pts[3][0]:
        bl = pts[2]
        br = pts[3]
    else:
        bl = pts[3]
        br = pts[2]

    return np.array([tl, tr, br, bl])


def get_omr_region(ori_img, debug=False, binaryThresh1=120):
    img = cv2.GaussianBlur(ori_img, (9, 9), 10)
    # img = cv2.bilateralFilter(ori_img, 9, 75, 75)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = normalize(img)
    # img = cv2.threshold(img, binaryThresh1, 255, cv2.THRESH_BINARY )[1]
    # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    edges_img = cv2.Canny(img, 50, 200, apertureSize=3, L2gradient=True)

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # edges_img = cv2.dilate(edges_img, kernel, iterations=1)
    # edges_img = cv2.erode(edges_img, kernel, iterations=1)

    # edges_img = cv2.morphologyEx(edges_img, cv2.MORPH_OPEN, kernel)
    contours = get_contours(edges_img)

    detected_contours = []
    for cnt in contours:
        cnt_feature = get_important_contour_featues(cnt, img)
        if 0.4 < cnt_feature["image_height_ratio"] < 1.0 and 0.6 < cnt_feature["image_width_ratio"] < 1.0:
            detected_contours.append(cnt)

    c_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if len(detected_contours) > 0:
        pixel_to_cut = 10
        hull_points = get_convex_hull_points(detected_contours)
        outmost_points = get_outmost_points_by_summation(hull_points)

        omr_region_img = four_point_transform(ori_img, outmost_points)
        omr_region_img = omr_region_img[pixel_to_cut:omr_region_img.shape[0] - pixel_to_cut, pixel_to_cut:omr_region_img.shape[1] - pixel_to_cut]
        if debug:
            draw_corners(c_img, outmost_points)
            cv2.drawContours(c_img, detected_contours, -1, (20, 10, 200), thickness=1)

        return omr_region_img, c_img, edges_img

    return None, c_img, edges_img


def is_a_circle_optimal(features):
    true_for = 0

    if .80 < features['hull_area_ratio'] <= 1:
        true_for += 1
    if .50 < features['bounding_area_ratio'] < 1:
        true_for += 1
    if 0.025 < features['image_height_ratio'] < 0.05:
        true_for += 1
    if 0.025 < features['image_width_ratio'] < 0.06:
        true_for += 1
    if .75 < features['aspect_ratio'] < 1.2:
        true_for += 1
    if 30 < features['height'] < 70:
        true_for += 1
    if 30 < features['width'] < 70:
        true_for += 1

    return true_for == 7


def is_a_circle_extreme(features):
    true_for = 0

    if .40 < features['hull_area_ratio'] <= 1:
        true_for += 1
    if .35 < features['bounding_area_ratio'] < 1:
        true_for += 1
    if 0.025 < features['image_height_ratio'] < 0.08:
        true_for += 1
    if 0.025 < features['image_width_ratio'] < 0.09:
        true_for += 1
    if .6 < features['aspect_ratio'] < 1.7:
        true_for += 1
    if 25 <= features['height'] <= 90:
        true_for += 1
    if 25 <= features['width'] <= 90:
        true_for += 1

    return true_for == 7


# return numpy 3d array of shape(n, 4, 2) or shape(0,) in case of invalid args
def arrange_points_according_to_question(point_group, is_debug=False, ori_img=None):
    if len(point_group) == 0:
        return np.array([])
    np_point_group = np.array(point_group)
    if np_point_group.shape[0] % 4 != 0:
        return np.array([])

    # sort points according to y coordinates
    np_point_group = np_point_group[np_point_group[:, 1].argsort()]

    # reshape the 2d array to 3d to arrange to blocks/circles according to question number
    shape1d = int(np_point_group.shape[0] / 4)
    np_point_group = np_point_group.reshape(shape1d, 4, 2)

    # now sort ponts in individual row according to the columns x coordinates
    i_length = np_point_group.shape[0]
    j_length = np_point_group.shape[1]
    for i in range(i_length):
        np_point_group[i] = np_point_group[i][np_point_group[i][:, 0].argsort()]
        if is_debug and ori_img is not None:
            for j in range(j_length):
                draw_text(ori_img, str(i + 1) + "/" + str(j + 1), np_point_group[i, j])

    return np_point_group


def get_circle_block(np_array_points, contours_dic, img, row, col, is_debug=False):
    try:
        (cx, cy) = np_array_points[row - 1][col - 1]
        if is_debug:
            print("cx, cy: ", cx, cy)
        block14_contour = contours_dic[str(cx) + str(cy)]
        if block14_contour is not None:
            (x, y, w, h) = cv2.boundingRect(block14_contour)
            return img[y:y + h, x:x + w]

        return None
    except Exception:
        return None


# binarizatin of the omr circle region
def operate_on_circle_block(block, with_morphology=False):
    try:
        img = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        black_img = 255 - img
        if with_morphology:
            kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            black_img = cv2.erode(black_img, kernel_ellipse, iterations=1)

        # if with_morphology:
        #     kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #     black_img = cv2.erode(black_img, kernel_ellipse, iterations=2)
        #
        #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        #     black_img = cv2.dilate(black_img, kernel, iterations=3)

        #   kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        #   black_img = cv2.dilate(black_img, kernel, iterations=3)

        return black_img

    except Exception:
        return None


def preprocess_omr_region(ori_img):
    img = cv2.GaussianBlur(ori_img, (7, 7), 8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    black_img = 255 - img

    # morphology operation specially dilete
    dilete_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    black_img = cv2.dilate(black_img, dilete_kernel, iterations=3)

    return black_img, img


# ori_img should be resized to width = 1200 and the type of ori_img should be cv2 image
def get_omr_answers(ori_img, question_count=50, result_type=TRUE_FALSE):
    black_img, img = preprocess_omr_region(ori_img)

    c_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if question_count < 10 or question_count > 50:
        return None

    num_of_region = math.ceil(question_count / 20.0)
    region_width = int(img.shape[1] / num_of_region)

    left_region_right_x = region_width + 1
    middle_region_right_x = (2 * region_width) + 1

    contours = get_contours(black_img, cv2.RETR_EXTERNAL)

    all_detected_contours = {}
    left_points_group = []
    middle_points_group = []
    right_points_group = []

    contour_debug = False
    print_debug = False

    for cnt in contours:
        cnt_feature = get_important_contour_featues(cnt, black_img)
        if is_a_circle_extreme(cnt_feature):
            cx, cy = get_centroid(cnt)
            all_detected_contours[str(cx) + str(cy)] = cnt
            if cx < left_region_right_x:
                left_points_group.append([cx, cy])
            elif left_region_right_x < cx < middle_region_right_x:
                middle_points_group.append([cx, cy])
            elif middle_region_right_x < cx:
                right_points_group.append([cx, cy])
            if contour_debug:
                draw_point([cx, cy], c_img)

        elif print_debug and 30 < cnt_feature['height'] < 90:
            print("not found", cnt_feature)

    # print("left_points_group: ", len(left_points_group))
    # print("middle_points_group: ", len(middle_points_group))
    # print("right_points_group: ", len(right_points_group))

    print("all_detected_contours: ", len(all_detected_contours))

    final_np_array_points = np.array([])
    np3dArr1 = arrange_points_according_to_question(left_points_group)
    np3dArr2 = arrange_points_according_to_question(middle_points_group)
    np3dArr3 = arrange_points_according_to_question(right_points_group)

    if num_of_region == 3 and np3dArr1.shape[0] != 0 and np3dArr2.shape[0] != 0 and np3dArr3.shape[0] != 0:
        final_np_array_points = np.concatenate((np3dArr1, np3dArr2, np3dArr3))
    elif num_of_region == 2 and np3dArr1.shape[0] != 0 and np3dArr2.shape[0] != 0:
        final_np_array_points = np.concatenate((np3dArr1, np3dArr2))
    elif num_of_region == 2 and np3dArr1.shape[0] != 0 and np3dArr2.shape[0] != 0:
        final_np_array_points = np3dArr1

    print("final_np_array_points: ", final_np_array_points.shape)
    if final_np_array_points.shape[0] != 0 and final_np_array_points.shape[0] == question_count:

        answer_list = np.zeros((final_np_array_points.shape[0], final_np_array_points.shape[1]), dtype='float32')

        i_length = final_np_array_points.shape[0]
        j_length = final_np_array_points.shape[1]

        for i in range(i_length):
            for j in range(j_length):
                (cx, cy) = final_np_array_points[i][j]
                block14_contour = all_detected_contours[str(cx) + str(cy)]
                if block14_contour is not None:
                    (x, y, w, h) = cv2.boundingRect(block14_contour)
                    block = ori_img[y:y + h, x:x + w]
                    processed_img = operate_on_circle_block(block)

                    if processed_img is not None:
                        unique_vals, counts = np.unique(processed_img, return_counts=True)
                        index_dict = dict(zip(unique_vals, counts))
                        # mean_value = processed_img.mean()

                        total_pix = processed_img.shape[0] * processed_img.shape[1]
                        percent_of_white = ((index_dict[255] / float(total_pix)) * 100)

                        if result_type == TRUE_FALSE:
                            answer_list[i, j] = float(50 < percent_of_white)
                        else:
                            answer_list[i, j] = percent_of_white

                        if 50 < percent_of_white:
                            cv2.circle(c_img, (cx, cy), 20, (10, 200, 10), 3)

        # answer_list.around(decimals=1)
        return answer_list, c_img

    return None, c_img


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def preprocess_image_ori(ori_img):
    img = cv2.GaussianBlur(ori_img, (5, 5), 8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    black_img = 255 - img
    return black_img, img


def get_omr_answers_ori(ori_img, question_count=50, result_type=TRUE_FALSE):
    black_img, img = preprocess_image_ori(ori_img)

    if question_count < 10 or question_count > 50:
        return None

    num_of_region = math.ceil(question_count / 20.0)
    region_width = int(img.shape[1] / num_of_region)

    left_region_right_x = region_width + 1
    middle_region_right_x = (2 * region_width) + 1

    contours = get_contours(black_img, cv2.RETR_EXTERNAL)

    all_detected_contours = {}
    left_points_group = []
    middle_points_group = []
    right_points_group = []

    for cnt in contours:
        cnt_feature = get_important_contour_featues(cnt, black_img)
        if is_a_circle_optimal(cnt_feature):
            cx, cy = get_centroid(cnt)
            all_detected_contours[str(cx) + str(cy)] = cnt
            if cx < left_region_right_x:
                left_points_group.append([cx, cy])
            elif left_region_right_x < cx < middle_region_right_x:
                middle_points_group.append([cx, cy])
            elif middle_region_right_x < cx:
                right_points_group.append([cx, cy])

    final_np_array_points = np.array([])
    np3dArr1 = arrange_points_according_to_question(left_points_group)
    np3dArr2 = arrange_points_according_to_question(middle_points_group)
    np3dArr3 = arrange_points_according_to_question(right_points_group)

    if num_of_region == 3 and np3dArr1.shape[0] != 0 and np3dArr2.shape[0] != 0 and np3dArr3.shape[0] != 0:
        final_np_array_points = np.concatenate((np3dArr1, np3dArr2, np3dArr3))
    elif num_of_region == 2 and np3dArr1.shape[0] != 0 and np3dArr2.shape[0] != 0:
        final_np_array_points = np.concatenate((np3dArr1, np3dArr2))
    elif num_of_region == 2 and np3dArr1.shape[0] != 0 and np3dArr2.shape[0] != 0:
        final_np_array_points = np3dArr1

    if final_np_array_points.shape[0] != 0:
        answer_list = np.zeros((final_np_array_points.shape[0], final_np_array_points.shape[1], 3), dtype='float16')

        i_length = final_np_array_points.shape[0]
        j_length = final_np_array_points.shape[1]

        for i in range(i_length):
            for j in range(j_length):
                (cx, cy) = final_np_array_points[i][j]
                block14_contour = all_detected_contours[str(cx) + str(cy)]
                if block14_contour is not None:
                    (x, y, w, h) = cv2.boundingRect(block14_contour)
                    block = ori_img[y:y + h, x:x + w]
                    processed_img = operate_on_circle_block(block)

                    if processed_img is not None:
                        unique_vals, counts = np.unique(processed_img, return_counts=True)
                        index_dict = dict(zip(unique_vals, counts))
                        # mean_value = processed_img.mean()

                        total_pix = processed_img.shape[0] * processed_img.shape[1]
                        percet_of_white = (index_dict[255] / float(total_pix) * 100)
                        answer_list[i, j, 1] = float(cx)
                        answer_list[i, j, 2] = float(cy)
                        if result_type == TRUE_FALSE:
                            answer_list[i, j, 0] = float(50 < round(percet_of_white, 2))
                        else:
                            answer_list[i, j, 0] = round(percet_of_white, 2)

        return answer_list

    return None
