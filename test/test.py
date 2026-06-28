# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 4-bit up/down counter test")

    # 10 us period = 100 kHz clock
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Initialize inputs
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Reset counter
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)

    assert int(dut.uo_out.value) == 0, \
        f"Reset failed: expected 0, got {int(dut.uo_out.value)}"

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # -------------------------------------------------
    # Test up-counting
    # ui_in[0] = 0 means count up
    # -------------------------------------------------
    dut._log.info("Test up-counting")

    dut.ui_in.value = 0
    dut.ena.value = 1

    for expected in range(1, 6):
        await ClockCycles(dut.clk, 1)

        actual = int(dut.uo_out.value) & 0x0F

        assert actual == expected, \
            f"Up-count failed: expected {expected}, got {actual}"

    # -------------------------------------------------
    # Test hold operation
    # ena = 0 means hold current value
    # -------------------------------------------------
    dut._log.info("Test enable hold")

    dut.ena.value = 0
    held_value = int(dut.uo_out.value) & 0x0F

    await ClockCycles(dut.clk, 3)

    actual = int(dut.uo_out.value) & 0x0F

    assert actual == held_value, \
        f"Hold failed: expected {held_value}, got {actual}"

    # -------------------------------------------------
    # Test down-counting
    # ui_in[0] = 1 means count down
    # -------------------------------------------------
    dut._log.info("Test down-counting")

    dut.ui_in.value = 1
    dut.ena.value = 1

    for expected in [4, 3, 2, 1, 0]:
        await ClockCycles(dut.clk, 1)

        actual = int(dut.uo_out.value) & 0x0F

        assert actual == expected, \
            f"Down-count failed: expected {expected}, got {actual}"

    # -------------------------------------------------
    # Test downward wraparound: 0 -> 15
    # -------------------------------------------------
    dut._log.info("Test downward wraparound")

    await ClockCycles(dut.clk, 1)

    actual = int(dut.uo_out.value) & 0x0F

    assert actual == 15, \
        f"Downward wraparound failed: expected 15, got {actual}"

    # -------------------------------------------------
    # Test upward wraparound: 15 -> 0
    # -------------------------------------------------
    dut._log.info("Test upward wraparound")

    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 1)

    actual = int(dut.uo_out.value) & 0x0F

    assert actual == 0, \
        f"Upward wraparound failed: expected 0, got {actual}"

    # Verify unused upper output bits remain zero
    assert (int(dut.uo_out.value) & 0xF0) == 0, \
        "Unused output bits uo_out[7:4] are not zero"

    dut._log.info("All counter tests passed")
