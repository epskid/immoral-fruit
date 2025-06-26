# immoral fruit
bad apple on the TI84+ CE. it runs with a whopping 32x12 resolution at 8fps. the encoder and a sample decoder are written in python and can be found in the `encoder` directory. here's a preview:

<p align="center">
    <img src="./capture.gif" alt="helpful alt text">
    <br />
    <i>recorded with the <a href="https://github.com/CE-Programming/CEmu">CEmu emulator</a></i>
</p>

## faq
### why is it so bad?
nothing is bad when it's a learning experience. also the emulator was behaving funny -- those wierd visual glitches aren't there when ran on actual hardware.

## compilation
supply `bad_apple.mp4` into the encoder directory, and run `encoder.py`. copy `data.c` into the `src` directory, and then use the [CEDev toolchain](https://github.com/CE-Programming/toolchain) to compile.
