import sys
import subprocess
import argparse

# usage: python vtune-report-summary.py [result_dir] [report_output_file]

parser = argparse.ArgumentParser(description='Generate the general-exploration'
                                 ' report summary')

# parser.add_argument('-', '--parallel',
#                     default=False, action='store_true',
#                     help='Produce Multi-threaded code. Use the environment'
#                     ' variable OMP_NUM_THREADS=xx to control the number of'
#                     ' threads that will be used.'
#                     ' Default: Serial code')

amplxe_args = [
    'amplxe-cl', '-report',
    'summary', '-csv-delimiter=tab',
    '-format', 'csv',
    # '-result-dir', ''
    # '-report-output', ''
]

if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     res_dir = sys.argv[1]
    #     amplxe_args += ['-result-dir', res_dir]
    # if len(sys.argv) > 2:
    #     outfile = sys.argv[2]
    #     amplxe_args += ['-report-output', outfile]

    subprocess.call(amplxe_args + sys.argv[1:])
