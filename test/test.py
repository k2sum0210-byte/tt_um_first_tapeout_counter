# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


async def wait_clock_and_settle(dut, cycles=1):
    """Wait for clock edges and allow nonblocking assignments to settle."""
    await ClockCycles(dut.clk, cycles)
    await Timer(1, unit="ns")


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 4-bit up/down counter test")

    # 10 us period = 100 kHz
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Initialize inputs
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await wait_clock_and_settle(dut, 2)

    actual = int(dut.uo_out.value)
    assert actual == 0, f"Reset failed: expected 0, got {actual}"

    dut.rst_n.value = 1
    await Timer(1, unit="ns")

    # Test up-counting
    dut._log.info("Test up-counting")

    dut.ui_in.value = 0
    dut.ena.value = 1

    for expected in range(1, 6):
        await wait_clock_and_settle(dut)

        actual = int(dut.uo_out.value) & 0x0F
        assert actual == expected, (
            f"Up-count failed: expected {expected}, got {actual}"
        )

    # Test hold
    dut._log.info("Test enable hold")

    dut.ena.value = 0
    held_value = int(dut.uo_out.value) & 0x0F

    await wait_clock_and_settle(dut, 3)

    actual = int(dut.uo_out.value) & 0x0F
    assert actual == held_value, (
        f"Hold failed: expected {held_value}, got {actual}"
    )

    # Test down-counting
    dut._log.info("Test down-counting")

    dut.ui_in.value = 1
    dut.ena.value = 1

    for expected in [4, 3, 2, 1, 0]:
        await wait_clock_and_settle(dut)

        actual = int(dut.uo_out.value) & 0x0F
        assert actual == expected, (
            f"Down-count failed: expected {expected}, got {actual}"
        )

    # Test downward wraparound: 0 -> 15
    dut._log.info("Test downward wraparound")

    await wait_clock_and_settle(dut)

    actual = int(dut.uo_out.value) & 0x0F
    assert actual == 15, (
        f"Downward wraparound failed: expected 15, got {actual}"
    )

    # Test upward wraparound: 15 -> 0
    dut._log.info("Test upward wraparound")

    dut.ui_in.value = 0
    await wait_clock_and_settle(dut)

    actual = int(dut.uo_out.value) & 0x0F
    assert actual == 0, (
        f"Upward wraparound failed: expected 0, got {actual}"
    )

    # Upper output bits must remain zero
    assert (int(dut.uo_out.value) & 0xF0) == 0, (
        "Unused output bits uo_out[7:4] are not zero"
    )

    dut._log.info("All counter tests passed")
