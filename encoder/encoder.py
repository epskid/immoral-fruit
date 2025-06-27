# compresses bad_apple.mp4 (supplied by user due to being legally grey)

import ctypes
import decoder
import multiprocessing
import sys

try:
    import cv2
except ImportError:
    print("opencv2 is required")
    quit()

print(f"starting (opencv version {cv2.__version__})")

FPS = 8
FRAME_MS = 1000 // FPS
PIXEL_SIZE = 10
WIDTH = 320 // PIXEL_SIZE
HEIGHT = 240 // PIXEL_SIZE
MAX_COMPRESSED_FRAME_SIZE = WIDTH * HEIGHT // 2 # assume worst-case compression of 50%
W_INDICATOR_BIT = 7

frames = []

if len(sys.argv) != 2:
    print("please supply one file to encode")
    quit()
cap = cv2.VideoCapture(sys.argv[1])
original_fps = cap.get(cv2.CAP_PROP_FPS)
original_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1
print(f"original footage encoded at {int(original_fps)} fps with {int(original_frame_count)} frames")
frame_count = int((float(FPS) / original_fps) * original_frame_count) + 1
print(f"new footage will have {FPS} fps and {frame_count} frames")

frame_idx = 0
while True:
    cap.set(cv2.CAP_PROP_POS_MSEC, frame_idx * FRAME_MS)
    successful, frame = cap.read()
    if not successful:
        break
    print(f"[{frame_idx + 1}/{frame_count}] extracting frames...", end="\r")
    frames.append(cv2.resize(frame, (WIDTH, HEIGHT)))
    frame_idx += 1

print()
print("run length encoding frames...")

processed_frames = multiprocessing.Array(ctypes.c_uint8 * MAX_COMPRESSED_FRAME_SIZE, frame_count)

def process(processed_frames, frame_idx):
    python_data = []
    b_counter = 0
    w_counter = 0
    for row in range(HEIGHT):
        for col in range(WIDTH):
            is_white = frames[frame_idx][row, col][0] > 127
            if is_white:
                w_counter += 1
                if b_counter > 0:
                    python_data.append(b_counter)
                    b_counter = 0
            else:
                b_counter += 1
                if w_counter > 0:
                    python_data.append(w_counter + (1 << W_INDICATOR_BIT)) # flip bit to indicate it's white
                    w_counter = 0
        if b_counter > 0:
            python_data.append(b_counter)
            b_counter = 0
        elif w_counter > 0:
            python_data.append(w_counter + (1 << W_INDICATOR_BIT))
            w_counter = 0
    for i, elem in enumerate(python_data):
        processed_frames[frame_idx][i] = ctypes.c_uint8(elem)

processes = []
for frame_idx in range(frame_count):
    p = multiprocessing.Process(target=process, args=(processed_frames, frame_idx))
    processes.append(p)
    p.start()

for i, p in enumerate(processes):
    p.join()

with open("data.c", "w") as data:
    data.write("#include <stdint.h>\n")
    data.write("#include <stddef.h>\n")
    data.write(f"const uint16_t frames_mills = {FRAME_MS};\n")
    data.write(f"const uint24_t width = {WIDTH};\n")
    data.write(f"const uint8_t height = {HEIGHT};\n")
    data.write(f"const uint8_t pixel_size = {PIXEL_SIZE};\n")
    data.write(f"const uint8_t bit = {W_INDICATOR_BIT};\n")
    data.write("const uint8_t data[] = {")
    for frame_idx, frame in enumerate(processed_frames[:]):
        print(f"[{frame_idx + 1}/{frame_count}] writing to file...", end="\r")
        for i in range(MAX_COMPRESSED_FRAME_SIZE):
            if frame[i] == 0: # c arrays are terminated with NUL bytes
                break
            data.write(f"{hex(frame[i])},")
        data.write("0,")
    data.write("};\n")
    data.write("const size_t data_len = sizeof(data);")

print()

if input("play a preview? [y/n] ") == "y":
    decoder.play(processed_frames[:], FPS, WIDTH, HEIGHT, W_INDICATOR_BIT)
