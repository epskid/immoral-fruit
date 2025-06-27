# immoral fruit
bad apple on the TI84+ CE. it runs with a whopping 32x24 resolution at 8fps. the encoder and a sample decoder are written in python and can be found in the `encoder` directory. here's a preview:

<p align="center">
    <img src="./capture.gif" alt="helpful alt text">
    <br />
    <i>recorded with the <a href="https://github.com/CE-Programming/CEmu">CEmu emulator</a></i>
</p>

## faq
### why is it so bad?
nothing is bad when it's a learning experience (i suck at embedded programming).

## compilation
get the file you want to encode (such as bad apple) then run
```shell
./encode.sh <your file here>
```
then use the [CEDev toolchain](https://github.com/CE-Programming/toolchain) to compile.
