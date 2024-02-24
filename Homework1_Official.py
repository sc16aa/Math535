from PIL import Image
import numpy as np
import pandas as pd
np.set_printoptions(threshold=np.inf)

# Reading and Resizing the Image
coverorig = Image.open('grey.png')
cover = coverorig.resize((861, 689)) # Why do we resize the image?
#cover = cover1.convert('L')  # Convert to grayscale 

# Getting Size Information
M, N = cover.size

# Calculating Payload Capacity
capacity = int(np.ceil(np.log2(M * N)))
#print('Capacity:', capacity, 'bits')

# Setting Embedding Rate and Payload Length
rate = 0.10
K = round(rate * (M * N - capacity))
#print("First K: ", K)

# Generating Random Payload MUST PUT SEED HERE
seed_value = 42 # random seed answer to the universe
np.random.seed(seed_value)

payload = (np.round(np.random.rand(K))).astype(int) 
#print("Embed Payload: ", payload)   
# np.savetxt(payload, output_file1, delimiter=",")

#  Embeds a payload into the least significant bits of the cover image.

def LSBembed(cover, payload):

    cover_array = np.array(cover)
    M, N = cover.size
    print(cover_array.shape)

    capacity = int(np.ceil(np.log2(M * N)))
    rate = 0.10
    K = round(rate * (M * N - capacity))
    print("in function: ", K)
    
    
    # Flatten the cover image and convert it to a 1D array
    cover_flat = cover_array.flatten()    
    
    payload_length_bin = format(len(payload), '013b')
    print("Payload Length: ", len(payload_length_bin))

    # Embed the binary string of the payload length 
    for i in range(len(payload_length_bin)):
        cover_flat[i] = (cover_flat[i] & 0xFE) | int(payload_length_bin[i])

    K_bin = len(payload_length_bin)
    
    # Embed the actual payload
    for i in range(len(payload)):
        cover_flat[i + K_bin] = (cover_flat[i + K_bin] & 0xFE) | payload[i]

    # Reshape the 1D array back to the original image shape
    stego_array = cover_flat.reshape((N, M))

    # Create an Image with the stego image array
    stego = Image.fromarray(stego_array.astype('uint8'))

    return stego


stego = LSBembed(cover, payload)
stego.show()
stego.save('stego.png')  # to save the stego image


##NEXT STEP IS TO EXTRACT THE PAYLOAD FROM THE IMAGE

def LSBextract(stego):
    # Convert the stego image to a numpy array and flatten it
    stego_array = np.array(stego)
    print(stego_array.shape)
    
    # Flatten the image and convert it to a 1D array
    stego_flat = stego_array.flatten()

    # Extract the binary of the payload length 
    payload_length_bin = ""
    for i in range(16):
        payload_length_bin += str(stego_flat[i] & 0x1)

    # Convert the binary representation to an integer
    K = int(payload_length_bin, 2)
    print ("Extraction K: ", K)

    # Extract the payload from the least significant bits
    payload = np.zeros(K, dtype=int)
    for i in range(K):
        payload[i] = stego_flat[i + 13] & 0x1

    return payload


# Load the stego image
stego = Image.open('stego.png')
M, N = stego.size  # Get the dimensions of the stego image

# Extract the payload
extracted_payload = LSBextract(stego)
print("Extracted Payload: ", len(extracted_payload))
# Print the extracted payload
#print(extracted_payload)

if np.array_equal(payload, extracted_payload):
    print("Payloads Match")
else:    
    print("Payloads Do Not Match")
    
# Calculate the percentage of different bits
diff = np.sum(payload != extracted_payload)
total_bits = payload.size * 8  # Assuming 8 bits per element

percent_diff = int((diff / total_bits) * 100)

print(f"The percentage of different bits is {percent_diff}%")


