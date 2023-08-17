import cv2
import numpy as np
import time

def getDigits(image, model):
    """
    Takes in an image captured by BattleAnalysis class and extracts the digits
    in the image

    image should have 3 channels normally

    Returns the number in integer form
    """

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper HSV thresholds for yellow color
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])

    # Create a binary mask for yellow pixels - black and white image of it with yellows as white
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

    digits = strip_black_columns(yellow_mask)

    enemies_defeated = ""
    for digit in digits:
        result_image = np.column_stack(digit)
        #cv2.imshow("resultimag", result_image)
        #cv2.waitKey(0)

        # Prepare to resize to a 25x25
        target_size = (25, 25)
        resized_image = resize_with_padding(result_image, target_size)
        if resized_image is None:
            continue

        # Pass digit image into model and get prediction as a string
        category = model_predict(resized_image, model)
        if category == "10":
            # Skip commas
            continue
        elif category == "11":
            # Category 11 represents an image with two nums. Split image into two and predict with model again
            left, right = split(resized_image)
            enemies_defeated += model_predict(left, model)
            enemies_defeated += model_predict(right, model)
        else:
            enemies_defeated += category
        

    return int(enemies_defeated)



def model_predict(image, model):
    # Add batch and channel dimensions
    img_array = np.expand_dims(image, axis=0)
    img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension
    predictions = model.predict(img_array, verbose=0)
    best_prediction_index = np.argmax(predictions)

    # labels
    #class_labels = ['class_0', 'class_1', 'class_2', ...]  # List of class labels in the same order as during training
    #best_prediction_label = class_labels[best_prediction_index]

    return(str(best_prediction_index))



def resize_with_padding(image, target_size):
    """ Resizes a smaller image to 25x25 by filling the left and rights with black pixels """
    # Create a new black canvas of the target size
    new_image = np.zeros(target_size, dtype=np.uint8)
    
    # Calculate the position to paste the original image
    y_start = (target_size[0] - image.shape[0]) // 2
    x_start = (target_size[1] - image.shape[1]) // 2
    
    # Paste the original image onto the canvas
    try:
        new_image[y_start:y_start+image.shape[0], x_start:x_start+image.shape[1]] = image
    except Exception as e:
        print(f"[x] Error in getDigits.py -> resize_with_padding(image, target_size): {e}")
        return None
    
    return new_image



def split(image):
    """ Takes in an 11 category photo (photos that displays two nums) and splits them apart, pads them, and returns them """

    # Get the width and height of the image
    _, width = image.shape

    # Calculate the midpoint along the width
    midpoint = width // 2

    # Split the image vertically in half
    left_half = image[:, :midpoint]
    right_half = image[:, midpoint:]

    # Strip black columns
    left_half = strip_black_columns(left_half)[0]
    right_half = strip_black_columns(right_half)[0]

    left_half = np.column_stack(left_half)
    right_half = np.column_stack(right_half)

    print("lefthalf shape", left_half.shape)
    print("righthalf shape", right_half.shape)

    # Reconstruct left half and right half to center the number
    target_size = (25, 25)

    left_image = resize_with_padding(left_half, target_size)
    right_image = resize_with_padding(right_half, target_size)

    return left_image, right_image



def strip_black_columns(yellow_mask):
    """ Takes in a binary mask for yellows pixels and returns a list of digits separated by black space """

    # Extract digits
    digits = []
    selected_columns = []

    # Go through each column in the picture
    for col in range(yellow_mask.shape[1]):

        # If column has yellow, save the column
        column_mask = yellow_mask[:, col]
        if np.any(column_mask):

            # Use image[:, col:col+1, :] if dont want to use yellow_mask
            selected_columns.append(yellow_mask[:, col])

        # If no yellow in column, then it is space between numbers. If selected_columns not empty, then we can save the number
        elif selected_columns:
            result_image = np.column_stack(selected_columns)
            digits.append(list(selected_columns))
            selected_columns.clear()

        else:
            continue

    # If remaining digit left
    if selected_columns:
        digits.append(selected_columns)

    return digits