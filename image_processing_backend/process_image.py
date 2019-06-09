# Imported PIL Library from PIL import Image
from PIL import Image
import math
import random
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
    rgb_ground = (139, 135, 90)
    # Get size
    width, height = image.size

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()
    boolean_2d_array = [[0 for i in range(height)] for j in range(width)]
    # embed()

    ground_color_map = []
    # Get ground colour
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = get_pixel(image, i, j)
            pixels[i, j] = pixel
            distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(rgb_ground, pixel)]))
            if distance < 35:
                boolean_2d_array[i][j] = 1
                ground_color_map.append(pixel)

    # Remap greens
    for i in range(width):
        for j in range(height):
            if boolean_2d_array[i][j] == 0:
                # Get Pixel
                pixel = get_pixel(image, i, j)
                distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(rgb_green, pixel)]))
                if distance < threshold:
                    # pixels[i, j] = random.choice(ground_color_map)
                    pixels[i, j] = rgb_ground
                boolean_2d_array[i][j] = 1

    # Return new image
    return new


if __name__ == '__main__':
    path = '/Users/jaivignesh/Desktop/docusign/image_processing_backend/naturepic.jpg'
    # path = '/Users/jaivignesh/Desktop/docusign/image_processing_backend/naturepic1.jpg'
    image = open_image(path)
    threshold = 10
    modified_images = []

    print('Processing image...')
    for i in range(30):
        modified_images.append(envelope_color(image, threshold))
        threshold += 5

    print('Generating gif...')
    modified_images[0].save("output.gif", save_all=True, append_images=modified_images, duration=100, loop=0)
    # for i in range(len(modified_images)):
    #     modified_images[i].show()
