import wave


def embed_into_audio(input_audio, message, output_audio):
    # append '\0' to the end of string
    message += '\0'
    
    # get data from message
    bytes_data = message.encode()

    # get data from input audio file as bytes array
    waveObject = wave.open(input_audio, mode='rb')
    frameBytes = bytearray(list(waveObject.readframes(waveObject.getnframes())))    

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

def extract_from_audio(input_audio):
    # get data from input audio file as bytes array
    waveObject = wave.open(input_audio, mode='rb')
    frameBytes = bytearray(list(waveObject.readframes(waveObject.getnframes())))

    # extract data from audio file
    extracted = []
    for i in range(len(frameBytes) // 8):
        # concat 8th bits from next 8 bytes of audio
        byte = bits_to_bytes([b & 1 for b in frameBytes[(i * 8):((i + 1) * 8)]])
        # break if end of a string
        if byte == b'\0':
            break
        extracted.append(byte)

    # return bytes as string
    return b''.join(extracted).decode('utf-8')


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


if __name__=="__main__":
    option = input('[INPUT] Enter "0" to hide, "1" to extract: ')
    if option == "0":
        input_msg = input('[INPUT] Message to hide: ')
        audio_input_file = input('[INPUT] Audio file: ').replace('"', '')
        audio_output_file = input('[INPUT] Output audio file: ').replace('"', '')
        embed_into_audio(audio_input_file, input_msg, audio_output_file)
        print("Success")
    elif option == "1":
        audio_input_file = input('[INPUT] Audio file: ').replace('"', '')
        msg = extract_from_audio(audio_input_file)
        print("Success")
        print(msg)
