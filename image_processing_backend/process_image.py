# Imported PIL Library from PIL import Image
from PIL import Image
import math
from imageai.Detection import ObjectDetection
import os
from IPython import embed


# Open an Image
def open_image(path):
    newImage = Image.open(path)
    return newImage


# Save Image
def save_image(image, path):
    image.save(path, 'png')


# Create a new image with the given size
def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image


# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel


# Create a Grayscale version of the image
def convert_grayscale(image):
    # Get size
    width, height = image.size

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()

    # Transform to grayscale
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = get_pixel(image, i, j)

            # Get R, G, B values (This are int from 0 to 255)
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            # Transform to grayscale
            gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

            # Set Pixel in new image
            pixels[i, j] = (int(gray), int(gray), int(gray))

    # Return new image
    return new


def envelope_color(image, threshold, bounding_box):
    rgb_green = (71, 140, 20)
    # Get size
    width, height = image.size

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()
    boolean_2d_array = [[0 for i in range(height)] for j in range(width)]
    # embed()

    # Get ground colour
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixels[i, j] = get_pixel(image, i, j)
            # if bounding_box[0] < i < bounding_box[2] and bounding_box[1] < j < bounding_box[3]:
            #     boolean_2d_array[i][j] = 1

    # Remap greens
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = get_pixel(image, i, j)
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)
            distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(rgb_green, pixel)]))
            if boolean_2d_array[i][j] == 0:
                if distance < threshold:
                    pixels[i, j] = (int(gray), int(gray), int(gray))
            elif boolean_2d_array[i][j] == 1:
                if distance < threshold/2:
                    pixels[i, j] = (int(gray), int(gray), int(gray))
            boolean_2d_array[i][j] = 2
    # Return new image
    return new


def remove_greens(original_image, black_and_white_image, threshold):
    rgb_green = (71, 140, 20)
    width, height = original_image.size

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()
    boolean_2d_array = [[0 for i in range(height)] for j in range(width)]
    # embed()

    # Get ground colour
    for i in range(width):
        for j in range(height):
            pixels[i, j] = get_pixel(black_and_white_image, i, j)

    # Remap greens
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = get_pixel(original_image, i, j)
            white = 255
            distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(rgb_green, pixel)]))
            if boolean_2d_array[i][j] == 0:
                if distance < threshold:
                    pixels[i, j] = (int(white), int(white), int(white))
            elif boolean_2d_array[i][j] == 1:
                if distance < threshold/2:
                    pixels[i, j] = (int(white), int(white), int(white))
            boolean_2d_array[i][j] = 2
    # Return new image
    return new


def ml_part(image_name):
    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, image_name),
                                                 output_image_path=os.path.join(execution_path, 'new_' + image_name))

    for eachObject in detections:
        if eachObject["name"] == 'person':
            bounding_box = eachObject["box_points"]

    return bounding_box


if __name__ == '__main__':
    image_name = 'sample5.jpg'
    image_path = '/Users/jaivignesh/Desktop/docusign/image_processing_backend/' + image_name
    print('Running person detection algo...')
    bounding_box = ml_part(image_name)
    image = open_image(image_path)
    threshold = 10
    modified_images = []

    print('Processing image...')
    for i in range(30):
        modified_images.append(envelope_color(image, threshold, bounding_box))
        threshold += 15

    for i in range(30):
        modified_images.append(remove_greens(image, modified_images[-1], threshold))
        threshold += 15

    print('Generating gif...')
    modified_images[0].save(image_name.split('.')[0] + '.gif', save_all=True, append_images=modified_images, duration=100, loop=0)
