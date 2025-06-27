import time
import itertools

def play(data, fps, width, height, bit):
    try:
        for frame in data:
            print("\x1b[2J\x1b[H")
            show_frame(itertools.takewhile(lambda x: x != 0, frame), width, height, bit)
            time.sleep(1 / fps)
    except KeyboardInterrupt:
        print("interrupted, exiting...")

def show_frame(frame, width, height, bit):
    expanded = []
    for compressed in frame:
        expanded += ['#' if compressed & (1 << bit) else ' ' for _ in range(compressed & ~(1 << bit))]
    rows = [expanded[i:i + width] for i in range(0, len(expanded), width)]
    for row in rows:
        print("".join(row))
