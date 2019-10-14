import sys
sys.path.append('../')
from flask import Flask, jsonify, request
from flask_cors import CORS
from similarity.image_similarity import from_base64_to_img, is_exactly_equal, get_similarity_score
from collage.collage_detection import detect_collage
from categorization.hotel_image_categorization import default_image_classifier
import json
app = Flask(__name__)
CORS(app)


@app.route('/api/v1/imageSimilarity', methods=['POST'])
def image_similarity():
    # TODO check request is valid or not

    encoded_image1_string = str(json.loads(request.get_data()).get('firstEncodedImage'))
    encoded_image2_string = str(json.loads(request.get_data()).get('secondEncodedImage'))

    img1 = from_base64_to_img(encoded_image1_string)
    img2 = from_base64_to_img(encoded_image2_string)

    is_exactly_same = is_exactly_equal(img1, img2)
    similarity_score = get_similarity_score(img1, img2)
    print(is_exactly_same)
    print(similarity_score)

    response_data = {'isExactlySame': is_exactly_same, 'similarityScore': similarity_score}
    response = jsonify(response_data)
    response.status_code = 200

    return response


@app.route('/api/v1/collage', methods=['POST'])
def collage():
    # TODO check request is valid or not

    encoded_image_string = str(json.loads(request.get_data()).get('encodedImage'))
    img = from_base64_to_img(encoded_image_string)
    response_data = {'isCollage': str(detect_collage(img))}
    response = jsonify(response_data)
    response.status_code = 200

    return response



@app.errorhandler(Exception)
def all_exception_handler(error):
    response_data = {'errorDesc': str(error)}
    response = jsonify(response_data)
    response.status_code = 500
    return response



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
