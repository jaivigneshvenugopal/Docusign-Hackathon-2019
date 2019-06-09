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


def envelope_color(image, threshold):
    rgb_green = (71, 140, 20)
    # Get size
    width, height = image.size

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()
    boolean_2d_array = [[0 for i in range(height)] for j in range(width)]
    # embed()

    pixel_hist = []

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
            if i > width/2:
                # Get Pixel
                pixel = get_pixel(image, i, j)
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]
                gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)
                distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(rgb_green, pixel)]))
                if boolean_2d_array[i][j] == 0 and distance < threshold:
                    pixels[i, j] = (int(gray), int(gray), int(gray))
                    pixel_hist.append((i, j))
                    boolean_2d_array[i][j] = 2
                elif boolean_2d_array[i][j] == 1 and distance < threshold/2:
                    pixels[i, j] = (int(gray), int(gray), int(gray))
                    pixel_hist.append((i, j))
                    boolean_2d_array[i][j] = 2
    # Return new image
    return new, pixel_hist


def whiten_image(image, pixel_hist):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    # Get ground colour
    for i in range(width):
        for j in range(height):
            pixels[i, j] = get_pixel(image, i, j)
            # if bounding_box[0] < i < bounding_box[2] and bounding_box[1] < j < bounding_box[3]:
            #     boolean_2d_array[i][j] = 1

    # Remap whites
    for i in range(len(pixel_hist)):
        pixels[pixel_hist[i][0], pixel_hist[i][1]] = (255, 255, 255)

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
    image_name = 'sample6.jpg'
    image_path = '/Users/jaivignesh/Desktop/docusign/image_processing_backend/' + image_name
    print('Running person detection algo...')
    # bounding_box = ml_part(image_name)
    image = open_image(image_path)
    threshold = 10
    modified_images = []
    history_pixel_change = []

    print('Processing image...')
    for i in range(40):
        new_frame, hist = envelope_color(image, threshold)
        modified_images.append(new_frame)
        history_pixel_change.append(hist)
        threshold += 5

    # white_images = []
    # for i in range(len(history_pixel_change)):
    #     white_images.append(whiten_image(modified_images[-1], history_pixel_change[i]))
    # modified_images += white_images

    print('Generating gif...')
    modified_images[0].save(image_name.split('.')[0] + '.gif', save_all=True, append_images=modified_images, duration=150, loop=0)
