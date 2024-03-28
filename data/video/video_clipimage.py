import cv2

def detect_and_save_faces(image_path, output_path):
    """Detects faces in the input image and saves them as 256x256 pixel images.
    
    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the detected face images.
    """
    # Load the pre-trained face cascade classifier
    face_cascade = cv2.CascadeClassifier('code/file/haarcascade_frontalface_default.xml')

    # Read the input image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Iterate over each detected face
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Resize the face region to 256x256 pixels
        face_crop = cv2.resize(img[y:y+h, x:x+w], (256, 256))
        
        # Save the face image
        cv2.imwrite(output_path, face_crop)

    # Display the image
    cv2.imshow('Image view', img)

    # Wait for 'q' key to be pressed
    while cv2.waitKey(0) & 0xFF != ord('q'):
        pass

    cv2.destroyAllWindows()

# Example usage
detect_and_save_faces('code/file/image.png', 'code/file/face_detected_256x256.png')
