# Flipper Zero NFC file converter

Converts F0 HEX in dump files into Integers, Binary and ASCII data for further investigation.
Usage is controlled with params.
Inspired by https://github.com/evilpete/flipper_toolbox/blob/main/nfc_hexdump.py

Note:
"Bare binary" was added as a helper to only output the binary values without
prepending the original data. This is useful is you intend to print these
values because it saves time removing original data to fit everything on a page.
