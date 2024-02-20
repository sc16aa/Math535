# Discuss 2

import cv2
import numpy as np



def display_color_channels(image):
    # Split the image into its color channels (B, G, R)
    blue_channel, green_channel, red_channel = cv2.split(image)

    # Create windows for displaying the images
    cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Blue Channel', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Green Channel', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Red Channel', cv2.WINDOW_NORMAL)

    # Display the images in their respective windows
    cv2.imshow('Original Image', image)
    cv2.imshow('Blue Channel', cv2.merge([blue_channel, np.zeros_like(green_channel), np.zeros_like(red_channel)]))
    cv2.imshow('Green Channel', cv2.merge([np.zeros_like(blue_channel), green_channel, np.zeros_like(red_channel)]))
    cv2.imshow('Red Channel', cv2.merge([np.zeros_like(blue_channel), np.zeros_like(green_channel), red_channel]))

    # Wait for a key press and close all windows on key press
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def display_gray_image_and_planes(gray_image_path):
    # Read the grayscale image
    gray_image = cv2.imread(gray_image_path, cv2.IMREAD_GRAYSCALE)

    # Display the original grayscale image
    cv2.imshow('Original Grayscale Image', gray_image)
    cv2.waitKey(0)

    # Get the 8-bit planes
    planes = [np.bitwise_and(gray_image, 2**i) for i in range(9)]

    # Display each 8-bit plane in a separate window
    for i, plane in enumerate(planes):
        cv2.imshow(f'Bit Plane {i}', plane)
        cv2.waitKey(0)

    # Close all windows
    cv2.destroyAllWindows()


def intensity_profile_along_line(gray_image_path, start_pixel, end_pixel):
    # Read the grayscale image
    gray_image = cv2.imread(gray_image_path, cv2.IMREAD_GRAYSCALE)

    # Define the line parameters
    r1, c1 = start_pixel
    r2, c2 = end_pixel

    # Create a mask for the line
    mask = np.zeros_like(gray_image)
    cv2.line(mask, (c1, r1), (c2, r2), 255, 1)

    # Extract intensity values along the line using the mask
    intensity_profile = gray_image[mask != 0]

    # Display the original grayscale image
    cv2.imshow('Original Grayscale Image', gray_image)
    cv2.waitKey(0)

    # Display the line on the original image
    cv2.line(gray_image, (c1, r1), (c2, r2), 255, 1)
    cv2.imshow('Line on Grayscale Image', gray_image)
    cv2.waitKey(0)

    # Display the intensity profile
    intensity_profile_image = np.zeros_like(gray_image)
    intensity_profile_image[mask != 0] = 255
    cv2.imshow('Intensity Profile along Line', intensity_profile_image)
    cv2.waitKey(0)

    # Close all windows
    cv2.destroyAllWindows()

    # Print the intensity profile
    print("Intensity Profile along Line:", intensity_profile)





def main():
    print("Press 1 for color image, 2 for grayscale image, or 3 for intensity profile: ")
    choice = input()

    if choice == '1' :
        
        # Replace 'your_image.jpg' with the path to your image file
        image_path = 'Ondra_sampling.jpg'
        # Read the image
        original_image = cv2.imread(image_path)
        display_color_channels(original_image)
            
    elif choice == '2':
        # Example usage:
        gray_image_path = 'ondra_gray.jpg'
        
        #gray_image = cv2.imread(gray_image_path)
        display_gray_image_and_planes(gray_image_path)
        
    elif choice == '3':
        
       # Example usage:
        gray_image_path = 'ondra_gray.jpg'
        start_pixel = (140, 460)
        end_pixel = (457, 872)
        intensity_profile_along_line(gray_image_path, start_pixel, end_pixel)
        


if __name__ == "__main__":
    main()
