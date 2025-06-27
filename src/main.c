#include "data.h"
#include "stdbool.h"
#include <graphx.h>
#include <stddef.h>
#include <sys/timers.h>

void render_frame(const uint8_t *frame, size_t len) {
  unsigned int x = 0;
  uint8_t y = 0;

  for (size_t idx = 0; idx < len; idx++) {
    const uint8_t chunk = frame[idx];
    const bool white = chunk & (1 << bit);
    const uint8_t length = chunk & ~(1 << bit);

    if (white)
      gfx_SetColor(0xFF);
    else
      gfx_SetColor(0);

    gfx_FillRectangle_NoClip(x * pixel_size, y * pixel_size,
                             length * pixel_size, pixel_size);

    x += length;
    if (x >= width) {
      x %= width;
      y += 1;
    }
  }
}

int main(void) {
  gfx_Begin();
  gfx_SetDrawBuffer();

  size_t start_slice = 0;
  for (size_t idx = 0; idx < data_len; idx++) {
    if (data[idx] == 0) {
      render_frame(data + start_slice, idx - start_slice);
      gfx_BlitBuffer();
      start_slice = idx + 1;
      delay(frames_mills);
    }
  }

  gfx_End();

  return 0;
}
