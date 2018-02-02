import numpy as np
import sys
import csv


metrics = {
    'mpki': '1000 * self.mem_load_uops_retired.l3_hit_ps / self.inst_retired.any',
    'cpi': 'self.cpu_clk_unhalted.thread / self.inst_retired.any',
    'ipc': 'self.inst_retired.any / self.cpu_clk_unhalted.thread',
    'front_bound%': '100 * self.idq_uops_not_delivered.core / (4 * self.cpu_clk_unhalted.thread)',
    'bad_speculation%': '100 * ((self.uops_issued.any - self.uops_retired.retire_slots + 4 * self.int_misc.recovery_cycles)/(4 * self.cpu_clk_unhalted.thread))',
    'retiring%': '100 * (self.uops_retired.retire_slots/(4 * self.cpu_clk_unhalted.thread))',
    'mem_bound%': '100 * self.cycle_activity.stalls_ldm_pending / self.cpu_clk_unhalted.thread',
    'be_bound%': '100 * (1 - (self.idq_uops_not_delivered.core + self.uops_issued.any + 4 * self.int_misc.recovery_cycles) / (4 * self.cpu_clk_unhalted.thread))'
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
        result.append(round(eval(string.lower()), 3))
    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("You must specify the input file and the output file")
        exit(-1)
    input_file = sys.argv[1]
    out_file = sys.argv[2]
    header, data = parse_input(input_file)
    metrics_result = [['metric'] + sorted(data.keys())]
    for k, v in metrics.items():
        metrics_result.append(evaluate_metric(header, data, 'data', k, v))

    writer = csv.writer(open(out_file, 'w'),
                        lineterminator='\n', delimiter='\t')
    writer.writerows(metrics_result)
