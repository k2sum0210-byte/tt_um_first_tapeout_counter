/*
 * Copyright (c) 2024 k2sum0210
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_k2sum0210_byte_counter (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    reg [3:0] count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 4'b0000;
        end else if (ena) begin
            if (ui_in[0])
                count <= count - 1'b1;
            else
                count <= count + 1'b1;
        end
    end

    assign uo_out  = {4'b0000, count};
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    wire _unused = &{uio_in, ui_in[7:1], 1'b0};

endmodule

`default_nettype wire
