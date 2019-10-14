import cv2
import base64
import numpy as np
from PIL import Image
import io


def is_exactly_equal(image_base, image_to_compare):

    if image_base.shape == image_to_compare.shape:
        difference = cv2.subtract(image_base, image_to_compare)
        b, g, r = cv2.split(difference)

        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            return 1
        else:
            return 0

    return 0


def get_similarity_score(image_base, image_to_compare):

    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(image_base, None)
    kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(desc_1, desc_2, k=2)

    similar_points = []
    ratio = 0.5
    for m, n in matches:
        if m.distance < ratio * n.distance:
            similar_points.append(m)
    # print("Similarity points : " + str(len(similar_points)))
    # result = cv2.drawMatches(image_base, kp_1, image_to_compare, kp_2, similar_points, None)
    # cv2.imshow('test', result)
    # cv2.waitKey(0)
    return round(len(similar_points) / 20,2)
    # 20 similarity points show that these images are similar. So this similar point count divided by 20 to calculate score


def from_base64_to_img(encoded_string, return_type='cv'):
    decoded_string = base64.b64decode(encoded_string)
    image = Image.open(io.BytesIO(decoded_string))
    if return_type == 'pil':
        return image
    elif return_type == 'cv':
        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    else:
        raise IOError('Unknown return_type parameter: {}. return type should be either cv or pil'.format(
            return_type))

# img1_encoded_str = ''
# img2_encoded_str = ''
# print(is_exactly_equal(from_base64_to_img(img1_encoded_str),from_base64_to_img(img2_encoded_str)))
# print(get_similarity_point_count(from_base64_to_img(img1_encoded_str),from_base64_to_img(img2_encoded_str)))

# cv2.imshow('test',from_base64_to_img(img1_encoded_str))
# cv2.waitKey(0)
# cv2.destroyAllWindows()



