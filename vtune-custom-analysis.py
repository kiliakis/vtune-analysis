import sys
import os
import subprocess

# usage: python vtune-custom-analysis.py ./exe exe_args (for binaries)
#        python vtune-custom-analysis.py python script.py exe_args (for python scripts)
# See the amplxe_args for the deafult args + this link:
# https://software.intel.com/en-us/vtune-amplifier-help-command-line-interface-reference


# These are the exact events collected by vtune18 for the haswell microarch
# to report the general-exploration (top-down analysis paper)

events = [
    'CPU_CLK_UNHALTED.THREAD:sa=2000000',
    'CPU_CLK_UNHALTED.REF_TSC:sa=2000000',
    'INST_RETIRED.ANY:sa=2000000',
    'ARITH.DIVIDER_UOPS',
    'BACLEARS.ANY',
    'BR_MISP_RETIRED.ALL_BRANCHES_PS',
    'CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE:sa=10003',
    'CPU_CLK_UNHALTED.REF_XCLK:sa=10003',
    'CPU_CLK_UNHALTED.THREAD_P',
    'CYCLE_ACTIVITY.CYCLES_NO_EXECUTE',
    'CYCLE_ACTIVITY.STALLS_L1D_PENDING',
    'CYCLE_ACTIVITY.STALLS_L2_PENDING',
    'CYCLE_ACTIVITY.STALLS_LDM_PENDING',
    'DSB2MITE_SWITCHES.PENALTY_CYCLES',
    'DTLB_LOAD_MISSES.STLB_HIT',
    'DTLB_LOAD_MISSES.WALK_DURATION',
    'DTLB_STORE_MISSES.STLB_HIT',
    'DTLB_STORE_MISSES.WALK_DURATION',
    'ICACHE.IFDATA_STALL',
    'IDQ.ALL_DSB_CYCLES_4_UOPS',
    'IDQ.ALL_DSB_CYCLES_ANY_UOPS',
    'IDQ.ALL_MITE_CYCLES_4_UOPS',
    'IDQ.ALL_MITE_CYCLES_ANY_UOPS',
    'IDQ.DSB_UOPS',
    'IDQ.MITE_UOPS',
    'IDQ.MS_SWITCHES',
    'IDQ.MS_UOPS',
    'IDQ_UOPS_NOT_DELIVERED.CORE',
    'IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE',
    'ILD_STALL.LCP',
    'INST_RETIRED.PREC_DIST',
    'INT_MISC.RECOVERY_CYCLES',
    'ITLB_MISSES.STLB_HIT',
    'ITLB_MISSES.WALK_COMPLETED',
    'ITLB_MISSES.WALK_DURATION',
    'L1D_PEND_MISS.PENDING',
    'L1D_PEND_MISS.REQUEST_FB_FULL:cmask=1',
    'L2_RQSTS.RFO_HIT',
    'LD_BLOCKS.NO_SR',
    'LD_BLOCKS.STORE_FORWARD',
    'LD_BLOCKS_PARTIAL.ADDRESS_ALIAS',
    'LSD.CYCLES_4_UOPS',
    'LSD.CYCLES_ACTIVE',
    'LSD.UOPS',
    'MACHINE_CLEARS.COUNT',
    'MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM_PS',
    'MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT_PS',
    'MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS_PS',
    'MEM_LOAD_UOPS_L3_MISS_RETIRED.LOCAL_DRAM_PS',
    'MEM_LOAD_UOPS_L3_MISS_RETIRED.REMOTE_DRAM_PS',
    'MEM_LOAD_UOPS_L3_MISS_RETIRED.REMOTE_FWD_PS',
    'MEM_LOAD_UOPS_L3_MISS_RETIRED.REMOTE_HITM_PS',
    'MEM_LOAD_UOPS_RETIRED.HIT_LFB_PS',
    'MEM_LOAD_UOPS_RETIRED.L1_HIT_PS',
    'MEM_LOAD_UOPS_RETIRED.L1_MISS',
    'MEM_LOAD_UOPS_RETIRED.L2_HIT_PS',
    'MEM_LOAD_UOPS_RETIRED.L3_HIT_PS',
    'MEM_LOAD_UOPS_RETIRED.L3_MISS_PS',
    'MEM_UOPS_RETIRED.ALL_STORES_PS',
    'MEM_UOPS_RETIRED.LOCK_LOADS_PS',
    'MEM_UOPS_RETIRED.SPLIT_LOADS_PS',
    'MEM_UOPS_RETIRED.SPLIT_STORES_PS',
    'MEM_UOPS_RETIRED.STLB_MISS_LOADS_PS',
    'MEM_UOPS_RETIRED.STLB_MISS_STORES_PS',
    'OFFCORE_REQUESTS_BUFFER.SQ_FULL',
    'OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD:cmask=6',
    'OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DATA_RD',
    'OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO',
    'OTHER_ASSISTS.ANY_WB_ASSIST',
    'RESOURCE_STALLS.SB',
    'RS_EVENTS.EMPTY_CYCLES',
    'RS_EVENTS.EMPTY_END',
    'UOPS_DISPATCHED_PORT.PORT_0',
    'UOPS_DISPATCHED_PORT.PORT_1',
    'UOPS_DISPATCHED_PORT.PORT_2',
    'UOPS_DISPATCHED_PORT.PORT_3',
    'UOPS_DISPATCHED_PORT.PORT_4',
    'UOPS_DISPATCHED_PORT.PORT_5',
    'UOPS_DISPATCHED_PORT.PORT_6',
    'UOPS_DISPATCHED_PORT.PORT_7',
    'UOPS_EXECUTED.CORE:cmask=1',
    'UOPS_EXECUTED.CORE:cmask=2',
    'UOPS_EXECUTED.CORE:cmask=3',
    'UOPS_ISSUED.ANY',
    'UOPS_RETIRED.RETIRE_SLOTS',
    'OFFCORE_RESPONSE:request=DEMAND_RFO:response=LLC_HIT.HITM_OTHER_CORE',
    'OFFCORE_RESPONSE:request=DEMAND_RFO:response=LLC_MISS.REMOTE_HITM'
]


# Consider setting the -user-data-dir to store the raw results in 
# separate directory
amplxe_args = [
    'amplxe-cl',
    '-collect-with', 'runsa',
    '-knob', 'event-config=' +  ','.join(events),
    '-knob', 'enable-user-tasks=true',
    '-knob', 'analyze-openmp=true',
    '-cpu-mask=0-13,14-27,28-41,42-55',
    '-discard-raw-data',
    '-start-paused'
    # '-user-data-dir=',
    # '-app-working-dir=', app_working_dir,
]


def run_custom_exploration(exe, exe_options):
    arg_list = amplxe_args + ['--', exe] + exe_options
    print(arg_list)
    subprocess.call(arg_list)


if __name__ == '__main__':
	exe = sys.argv[1]
	exe_options = sys.argv[2:]
	run_custom_exploration(exe, exe_options)



# To report
# amplxe-cl -R summary -result-dir r004ge0/ 
# -csv-delimiter=tab -format csv -quiet 
# -report-output report.csv