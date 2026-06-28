<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements a 4-bit synchronous up/down counter.

- When `rst_n` is low, the counter resets to `0000`.
- When `ena` is high, the counter changes on each rising edge of `clk`.
- When `ui_in[0]` is low, the counter counts upward.
- When `ui_in[0]` is high, the counter counts downward.
- The counter value is available on `uo_out[3:0]`.
- `uo_out[7:4]` is always `0`.

The counter wraps around automatically:

- Up-counting from `1111` produces `0000`.
- Down-counting from `0000` produces `1111`.

## How to test

1. Set `rst_n` low to reset the counter.
2. Set `rst_n` high.
3. Set `ena` high.
4. Set `ui_in[0]` low to count upward.
5. Apply clock pulses to `clk`.
6. Observe the counter value on `uo_out[3:0]`.
7. Set `ui_in[0]` high to count downward.
8. Set `ena` low and confirm that the counter holds its current value.

## External hardware

No external hardware is required for simulation.

For physical testing, the counter output can be observed using LEDs or the Tiny Tapeout development board.
