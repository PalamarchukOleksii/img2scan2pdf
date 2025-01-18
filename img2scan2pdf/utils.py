import os

import cv2
import numpy as np
from PIL import Image


def resize_image(image, target_width=500):
    h, w, c = image.shape
    height = int((h / w) * target_width)
    return cv2.resize(image, (target_width, height))


def preprocess_image(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    blur = cv2.GaussianBlur(rgb, (5, 5), 1)
    edges = cv2.Canny(blur, 50, 150)
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(edges, kernel, iterations=1)
    return cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)


def find_document_contour(image):
    contours, _ = cv2.findContours(
        image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            return np.squeeze(approx)
    return None


def order_points(points):
    sorted_points = sorted(points, key=lambda p: p[0] + p[1])
    tl = sorted_points[0]
    br = sorted_points[3]

    if sorted_points[1][1] < sorted_points[2][1]:
        tr = sorted_points[1]
        bl = sorted_points[2]
    else:
        tr = sorted_points[2]
        bl = sorted_points[1]

    return np.array([tl, tr, br, bl], dtype="float32")


def get_result_size(tl, tr, br, bl):
    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    return np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32"), max_width, max_height


def wrap_image(image, four_points, size):
    multiplier_x = image.shape[1] / size[0]
    multiplier_y = image.shape[0] / size[1]
    multiplier = min(multiplier_x, multiplier_y)

    four_points_orig = four_points * multiplier

    rect = order_points(four_points_orig)
    (tl, tr, br, bl) = rect

    dst, max_width, max_height = get_result_size(tl, tr, br, bl)

    m = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, m, (max_width, max_height))

    return warped


def resize_image_to_a4(image, target_width=2480, target_height=3508, padding=10):
    h, w, c = image.shape
    aspect_ratio = w / h
    if aspect_ratio > 1:
        new_width = target_width - padding
        new_height = int((target_width - padding) / aspect_ratio)
    else:
        new_height = target_height - padding
        new_width = int((target_height - padding) * aspect_ratio)
    return cv2.resize(image, (new_width, new_height))


def process_image(image_path):
    image = cv2.imread(image_path)
    resized_image = resize_image(image)
    preprocessed_image = preprocess_image(resized_image)
    four_points = find_document_contour(preprocessed_image)
    if four_points is not None:
        wrapped_image = wrap_image(
            image, four_points, (500, int((500 / image.shape[1]) * image.shape[0])))
        return resize_image_to_a4(wrapped_image)
    return None


def get_image_paths_from_directory(input_dir):
    return [os.path.join(input_dir, filename) for filename in os.listdir(input_dir)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]


def convert_image_to_pil(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image_rgb)


def process_images_from_directory(input_dir, output_pdf_path):
    images_to_convert = []
    for image_path in get_image_paths_from_directory(input_dir):
        print(f"Processing: {image_path}")
        result_image = process_image(image_path)
        if result_image is not None:
            images_to_convert.append(convert_image_to_pil(result_image))

    if images_to_convert:
        images_to_convert[0].save(
            output_pdf_path, save_all=True, append_images=images_to_convert[1:])
        print(f"PDF saved at {output_pdf_path}")
    else:
        print("No valid images were processed.")
