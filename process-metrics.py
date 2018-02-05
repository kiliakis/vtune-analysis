import numpy as np
import sys
import csv
import argparse

parser = argparse.ArgumentParser(
    description='Post-process of collected hw-events', 
    usage='process-metrics.py infile -o outfile')

parser.add_argument('infile', action='store', type=str,
                    help='The input file that contains the hw-events values.')

parser.add_argument('-o', '--outfile', type=str, default='metrics.csv',
                    help='The output file to write the calculated metrics'
                    ' Default: metrics.csv')


metrics = {
    # 'mpki': '1000 * self.mem_load_uops_retired.l3_hit_ps / self.inst_retired.any',
    'time(s)' : 'self.task_time',
    'time.contribution%' :'100 * self.task_time / total.task_time',
    'calls' : 'self.task_count',
    'cpi': 'self.cpu_clk_unhalted.thread / self.inst_retired.any',
    'ipc': 'self.inst_retired.any / self.cpu_clk_unhalted.thread',
    'front_bound%': '100 * self.idq_uops_not_delivered.core / (4 * self.cpu_clk_unhalted.thread)',
    'front_bound.contribution%': '(self.cpu_clk_unhalted.thread/ total.cpu_clk_unhalted.thread) * 100 * self.idq_uops_not_delivered.core / (4 * self.cpu_clk_unhalted.thread)',
    'be_bound%': '100 * (1 - (self.idq_uops_not_delivered.core + self.uops_issued.any + 4 * self.int_misc.recovery_cycles) / (4 * self.cpu_clk_unhalted.thread))',
    'be_bound.contribution%': 'self.cpu_clk_unhalted.thread / total.cpu_clk_unhalted.thread * 100 * (1 - (self.idq_uops_not_delivered.core + self.uops_issued.any + 4 * self.int_misc.recovery_cycles) / (4 * self.cpu_clk_unhalted.thread))',
    'core_bound%': '100 * (1 - (self.idq_uops_not_delivered.core + self.uops_issued.any + 4 * self.int_misc.recovery_cycles) / (4 * self.cpu_clk_unhalted.thread)) - 100 * self.cycle_activity.stalls_ldm_pending / self.cpu_clk_unhalted.thread',
    'core_bound.contribution%': '(self.cpu_clk_unhalted.thread / total.cpu_clk_unhalted.thread) * (100 * (1 - (self.idq_uops_not_delivered.core + self.uops_issued.any + 4 * self.int_misc.recovery_cycles) / (4 * self.cpu_clk_unhalted.thread)) - 100 * self.cycle_activity.stalls_ldm_pending / self.cpu_clk_unhalted.thread)',
    'mem_bound%': '100 * self.cycle_activity.stalls_ldm_pending / self.cpu_clk_unhalted.thread',
    'mem_bound.contribution%': '(self.cpu_clk_unhalted.thread/ total.cpu_clk_unhalted.thread) * 100 * self.cycle_activity.stalls_ldm_pending / self.cpu_clk_unhalted.thread',
    'l1_bound%': '100 * (self.cycle_activity.stalls_ldm_pending - self.cycle_activity.stalls_l1d_pending) / self.cpu_clk_unhalted.thread',
    'l3_latency%' : '(41 * ( self.mem_load_uops_retired.l3_hit_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps)))/self.cpu_clk_unhalted.thread)',
    'l3_latency.contribution%' : '(41 * ( self.mem_load_uops_retired.l3_hit_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps)))/total.cpu_clk_unhalted.thread)',
    'l3_data_sharing%' : '(43 * ( self.mem_load_uops_l3_hit_retired.xsnp_hit_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps)))/self.cpu_clk_unhalted.thread)',
    'l3_data_sharing.contribution%' : '(43 * ( self.mem_load_uops_l3_hit_retired.xsnp_hit_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps)))/total.cpu_clk_unhalted.thread)',
    'l3_contested_accesses%' : '(60 * ((self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps ) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps))) + (self.mem_load_uops_l3_hit_retired.xsnp_miss_ps * ( 1 + self.mem_load_uops_retired.hit_lfb_ps / ((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps ) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps)))) / self.cpu_clk_unhalted.thread)',
    'l3_contested_accesses.contribution%' : '(60 * ((self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps ) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps))) + (self.mem_load_uops_l3_hit_retired.xsnp_miss_ps * ( 1 + self.mem_load_uops_retired.hit_lfb_ps / ((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps ) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps)))) / total.cpu_clk_unhalted.thread)',
    'store_bound%': '100 * self.resource_stalls.sb / self.cpu_clk_unhalted.thread', 
    'store_bound.contribution%': '100 * self.resource_stalls.sb / total.cpu_clk_unhalted.thread', 
    'local_dram_bound%' : '100 * (200 * (self.mem_load_uops_l3_miss_retired.local_dram_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps))) / total.cpu_clk_unhalted.thread)',
    'local_dram_bound.contribution%' : '100 * (200 * (self.mem_load_uops_l3_miss_retired.local_dram_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps))) / self.cpu_clk_unhalted.thread)',
    'remote_dram_bound%' : '100 * (310 * (self.mem_load_uops_l3_miss_retired.remote_dram_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps))) / total.cpu_clk_unhalted.thread)',
    'remote_dram_bound.contribution%' : '100 * (310 * (self.mem_load_uops_l3_miss_retired.remote_dram_ps * (1 + self.mem_load_uops_retired.hit_lfb_ps /((self.mem_load_uops_retired.l2_hit_ps + self.mem_load_uops_retired.l3_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hit_ps + self.mem_load_uops_l3_hit_retired.xsnp_hitm_ps + self.mem_load_uops_l3_hit_retired.xsnp_miss_ps) + self.mem_load_uops_l3_miss_retired.local_dram_ps + self.mem_load_uops_l3_miss_retired.remote_dram_ps + self.mem_load_uops_l3_miss_retired.remote_hitm_ps + self.mem_load_uops_l3_miss_retired.remote_fwd_ps))) / self.cpu_clk_unhalted.thread)',
    'bad_speculation%': '100 * ((self.uops_issued.any - self.uops_retired.retire_slots + 4 * self.int_misc.recovery_cycles)/(4 * self.cpu_clk_unhalted.thread))',
    'bad_speculation.contribution%': '(self.cpu_clk_unhalted.thread/ total.cpu_clk_unhalted.thread) * 100 * ((self.uops_issued.any - self.uops_retired.retire_slots + 4 * self.int_misc.recovery_cycles)/(4 * self.cpu_clk_unhalted.thread))',
    'retiring%': '100 * (self.uops_retired.retire_slots/(4 * self.cpu_clk_unhalted.thread))',
    'retiring.contribution%': '(self.cpu_clk_unhalted.thread / total.cpu_clk_unhalted.thread) *  100 * (self.uops_retired.retire_slots/(4 * self.cpu_clk_unhalted.thread))',
    'be_bound_at_exe%': '100 * (self.cycle_activity.cycles_no_execute + self.uops_executed.core:cmask=1 - self.uops_executed.core:cmask=2)/ (self.cpu_clk_unhalted.thread)',
    
    # 'l2_bound%': '100 * (self.cycle_activity.stalls_l1d_pending - self.cycle_activity.stalls_l2_pending) / self.cpu_clk_unhalted.thread',
    # 'l3_bound%': '',
    # 'dram_bound%:' '',
    # 'uncore_bound': '100 * self.cycle_activity.stalls_l2_pending / self.cpu_clk_unhalted.thread'
    # 'resource_stalls_cost%': '100 * self.resource_stalls.any / self.cpu_clk_unhalted.thread'
    '':''
}


def parse_input(infile):
    data = np.genfromtxt(infile, str, delimiter='\t')
    header = data[0]
    data = data[1:]
    header = [h.lower().replace(' ', '_').replace(
        'hardware_event_count:', '') for h in header]
    d = {}
    for row in data:
        key = row[0].lower().replace(' ', '_')
        if 'outside_any_task' in key:
            continue
        d[key] = {}
        for i in range(1, len(header)):
            if row[i].strip() != '':
                d[key][header[i]] = float(row[i].strip())
    return header, d


def evaluate_metric(header, data, dict_name, name, expression):
    result = [name]
    for task in sorted(data.keys()):
        string = expression.replace('self.', dict_name + '[\'' + task + '\']')
        string = string.replace('total.', dict_name + '[\'total\']')
        for h in sorted(header, reverse=True):
            string = string.replace(h, '[\'' + h.upper() + '\']')
            # print(h, string)
        try:
            result.append(round(eval(string.lower()), 3))
        except SyntaxError as se:
            print(string.lower(), ': Could not be evaluated')
            result.append('NaN')
    return result


if __name__ == '__main__':
    args = parser.parse_args()

    # if len(sys.argv) < 3:
    #     print("You must specify the input file and the output file")
    #     exit(-1)
    input_file = args.infile
    out_file = args.outfile
    header, data = parse_input(input_file)
    metrics_result = [['metric'] + sorted(data.keys())]
    for k, v in metrics.items():
        if k != '':
            metrics_result.append(evaluate_metric(header, data, 'data', k, v))

    writer = csv.writer(open(out_file, 'w'),
                        lineterminator='\n', delimiter='\t')
    writer.writerows(metrics_result)
