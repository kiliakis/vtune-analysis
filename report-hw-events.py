import sys
import subprocess
import argparse

# usage: python vtune-report-hw-events.py [result_dir] [report_output_file]
parser = argparse.ArgumentParser(
    description='Report all the collected event counters',
    usage='report-hw-events.py -result-dir results/ -report-output hw-events.csv')


amplxe_args = [
    'amplxe-cl', '-report',
    'hw-events', '-csv-delimiter=tab',
    '-format', 'csv',
    '-group-by', 'task'
    # '-result-dir', ''
    # '-report-output', ''
]

if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #   res_dir = sys.argv[1]
    #   amplxe_args += ['-result-dir', res_dir]
    # if len(sys.argv) > 2:
    #   outfile = sys.argv[2]
    #   amplxe_args += ['-report-output', outfile]

    subprocess.call(amplxe_args + sys.argv[1:])
