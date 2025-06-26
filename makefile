# ----------------------------
# Makefile Options
# ----------------------------

NAME = BADAPPLE
ICON = icon.png
DESCRIPTION = "Bad Apple."
COMPRESSED = YES
COMPRESSED_MODE = zx0

CFLAGS = -Wall -Wextra -Oz
CXXFLAGS = -Wall -Wextra -Oz

# ----------------------------

include $(shell cedev-config --makefile)
