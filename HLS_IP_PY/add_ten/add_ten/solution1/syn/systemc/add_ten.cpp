// ==============================================================
// RTL generated by Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC
// Version: 2014.1
// Copyright (C) 2014 Xilinx Inc. All rights reserved.
// 
// ===========================================================

#include "add_ten.h"
#include "AESL_pkg.h"

using namespace std;

namespace ap_rtl {

const sc_logic add_ten::ap_const_logic_1 = sc_dt::Log_1;
const sc_logic add_ten::ap_const_logic_0 = sc_dt::Log_0;
const sc_lv<32> add_ten::ap_const_lv32_A = "1010";
const sc_lv<32> add_ten::ap_const_lv32_0 = "00000000000000000000000000000000";

add_ten::add_ten(sc_module_name name) : sc_module(name), mVcdFile(0) {

    SC_METHOD(thread_ap_done);
    sensitive << ( ap_start );

    SC_METHOD(thread_ap_idle);

    SC_METHOD(thread_ap_ready);
    sensitive << ( ap_start );

    SC_METHOD(thread_ap_return);
    sensitive << ( ap_start );

    SC_METHOD(thread_output_r);
    sensitive << ( ap_start );
    sensitive << ( input_r );

    SC_THREAD(thread_hdltv_gen);
    sensitive << ( ap_virtual_clock.pos() );

    static int apTFileNum = 0;
    stringstream apTFilenSS;
    apTFilenSS << "add_ten_sc_trace_" << apTFileNum ++;
    string apTFn = apTFilenSS.str();
    mVcdFile = sc_create_vcd_trace_file(apTFn.c_str());
    mVcdFile->set_time_unit(1, SC_PS);
    if (1) {
#ifdef __HLS_TRACE_LEVEL_PORT__
    sc_trace(mVcdFile, ap_start, "(port)ap_start");
    sc_trace(mVcdFile, ap_done, "(port)ap_done");
    sc_trace(mVcdFile, ap_idle, "(port)ap_idle");
    sc_trace(mVcdFile, ap_ready, "(port)ap_ready");
    sc_trace(mVcdFile, input_r, "(port)input_r");
    sc_trace(mVcdFile, output_r, "(port)output_r");
    sc_trace(mVcdFile, ap_return, "(port)ap_return");
#endif

    }
    mHdltvinHandle.open("add_ten.hdltvin.dat");
    mHdltvoutHandle.open("add_ten.hdltvout.dat");
}

add_ten::~add_ten() {
    if (mVcdFile) 
        sc_close_vcd_trace_file(mVcdFile);

    mHdltvinHandle << "] " << endl;
    mHdltvoutHandle << "] " << endl;
    mHdltvinHandle.close();
    mHdltvoutHandle.close();
}

void add_ten::thread_ap_done() {
    ap_done = ap_start.read();
}

void add_ten::thread_ap_idle() {
    ap_idle = ap_const_logic_1;
}

void add_ten::thread_ap_ready() {
    ap_ready = ap_start.read();
}

void add_ten::thread_ap_return() {
    ap_return = ap_const_lv32_0;
}

void add_ten::thread_output_r() {
    output_r = (!input_r.read().is_01() || !ap_const_lv32_A.is_01())? sc_lv<32>(): (sc_bigint<32>(input_r.read()) + sc_biguint<32>(ap_const_lv32_A));
}

void add_ten::thread_hdltv_gen() {
    const char* dump_tv = std::getenv("AP_WRITE_TV");
    if (!(dump_tv && string(dump_tv) == "on")) return;

    wait();

    mHdltvinHandle << "[ " << endl;
    mHdltvoutHandle << "[ " << endl;
    int ap_cycleNo = 0;
    while (1) {
        wait();
        const char* mComma = ap_cycleNo == 0 ? " " : ", " ;
        mHdltvinHandle << mComma << "{"  <<  " \"ap_start\" :  \"" << ap_start.read() << "\" ";
        mHdltvoutHandle << mComma << "{"  <<  " \"ap_done\" :  \"" << ap_done.read() << "\" ";
        mHdltvoutHandle << " , " <<  " \"ap_idle\" :  \"" << ap_idle.read() << "\" ";
        mHdltvoutHandle << " , " <<  " \"ap_ready\" :  \"" << ap_ready.read() << "\" ";
        mHdltvinHandle << " , " <<  " \"input_r\" :  \"" << input_r.read() << "\" ";
        mHdltvoutHandle << " , " <<  " \"output_r\" :  \"" << output_r.read() << "\" ";
        mHdltvoutHandle << " , " <<  " \"ap_return\" :  \"" << ap_return.read() << "\" ";
        mHdltvinHandle << "}" << std::endl;
        mHdltvoutHandle << "}" << std::endl;
        ap_cycleNo++;
    }
}

}

