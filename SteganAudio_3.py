import struct
import wave


def embed_into_audio(input_audio, file, output_audio):
    # get data from input files as bytes
    bytes_data = []
    with open(input_file, 'rb') as file:
        bytes_data = file.read()

    # get data from input audio file as bytes array
    waveObject = wave.open(input_audio, mode='rb')
    frameBytes = bytearray(list(waveObject.readframes(waveObject.getnframes())))    

    # add the length of the input file at the beginning of input bytes
    bytes_data = int_to_4bytes(len(bytes_data)) + bytes_data

    # embed input bytes to audio data by modifying 8th bit of the every byte in audio file
    bits = bytes_to_bits(bytes_data)
    for i, bit in enumerate(bits):
        frameBytes[i] = (frameBytes[i] & 254) | bit

    frameModified = bytes(frameBytes)
    
    # save modified bytes to output file
    with wave.open(output_audio,'wb') as output:
        output.setparams(waveObject.getparams())
        output.writeframes(frameModified)

    waveObject.close()

def extract_from_audio(input_audio, output_file):
    # get data from input audio file as bytes array
    waveObject = wave.open(input_audio, mode='rb')
    frameBytes = bytearray(list(waveObject.readframes(waveObject.getnframes())))

    # get hidden data length by reading 8th bit of the first 32 bytes of the audio file
    bits_len = [frameBytes[i] & 1 for i in range(4 * 8)]

    data_len = bytes_to_int(bits_to_bytes(bits_len))

    # extract data from audio file
    extracted = bits_to_bytes([frameBytes[i] & 1 for i in range(4 * 8, (data_len + 4) * 8)])
    
    # write output data to a file
    with open(output_file, 'wb') as file:
        file.write(extracted)


def bits_to_bytes(bits):
    # convert bits array to bytes
    bits += [0] * (8 - len(bits) % 8) if len(bits) % 8 != 0 else []
    byte_array = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        byte_array.append(byte)
    
    return bytes(byte_array)


def bytes_to_bits(byte_data):
    # convert bytes to bits array
    bit_list = []
    for byte in byte_data:
        for i in range(7, -1, -1):
            bit_list.append((byte >> i) & 1)
    return bit_list


def int_to_4bytes(value):
    # convert a number to 4 bytes
    return struct.pack('I', value)


def bytes_to_int(byte_array):
    # convert bytes to a number
    return struct.unpack('I', byte_array)[0]


if __name__=="__main__":
    option = input('[INPUT] Enter "0" to hide, "1" to extract: ')
    if option == "0":
        input_file = input('[INPUT] File to hide: ').replace('"', '')
        audio_input_file = input('[INPUT] Audio file: ').replace('"', '')
        audio_output_file = input('[INPUT] Output audio file: ').replace('"', '')
        embed_into_audio(audio_input_file, input_file, audio_output_file)
        print("Success")
    elif option == "1":
        audio_input_file = input('[INPUT] Audio file: ').replace('"', '')
        output_file = input('[INPUT] Output file: ').replace('"', '')
        extract_from_audio(audio_input_file, output_file)
        print("Success")
