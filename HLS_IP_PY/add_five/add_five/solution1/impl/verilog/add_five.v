// ==============================================================
// RTL generated by Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC
// Version: 2014.1
// Copyright (C) 2014 Xilinx Inc. All rights reserved.
// 
// ===========================================================

`timescale 1 ns / 1 ps 

(* CORE_GENERATION_INFO="add_five,hls_ip_2014_1,{HLS_INPUT_TYPE=cxx,HLS_INPUT_FLOAT=0,HLS_INPUT_FIXED=0,HLS_INPUT_PART=xc7z020clg484-1,HLS_INPUT_CLOCK=10.000000,HLS_INPUT_ARCH=others,HLS_SYN_CLOCK=2.440000,HLS_SYN_LAT=0,HLS_SYN_TPT=none,HLS_SYN_MEM=0,HLS_SYN_DSP=0,HLS_SYN_FF=0,HLS_SYN_LUT=0}" *)

module add_five (
        ap_start,
        ap_done,
        ap_idle,
        ap_ready,
        input_r,
        output_r,
        ap_return
);

parameter    ap_const_logic_1 = 1'b1;
parameter    ap_const_logic_0 = 1'b0;
parameter    ap_const_lv32_5 = 32'b101;
parameter    ap_const_lv32_0 = 32'b00000000000000000000000000000000;

input   ap_start;
output   ap_done;
output   ap_idle;
output   ap_ready;
input  [31:0] input_r;
output  [31:0] output_r;
output  [31:0] ap_return;




assign ap_done = ap_start;
assign ap_idle = ap_const_logic_1;
assign ap_ready = ap_start;
assign ap_return = ap_const_lv32_0;
assign output_r = (input_r + ap_const_lv32_5);


endmodule //add_five

