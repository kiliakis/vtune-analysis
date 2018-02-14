import sys
import subprocess
import argparse

# usage: python report.py -r [summary | hw-events] -i [indir] -o [outfile]

parser = argparse.ArgumentParser(description='Generate a report from the input raw data.',
                                 usage='python report.py -r [summary | hw-events] -i [indir] -o [outfile]')

parser.add_argument('-r', '--report', type=str, default='hw-events',
                    help='The report type. (summary or hw-events)'
                    ' Default: hw-events')

parser.add_argument('-o', '--outfile', type=str, default=None,
                    help='The file to save the report.'
                    ' Default: None (print to the stdout)')

parser.add_argument('-i', '--indir', type=str, default=None,
                    help='The directory containing the collected data.'
                    ' Default: None (print to the stdout)')


amplxe_args = [
    'amplxe-cl', '-report',
    '', '-csv-delimiter=tab',
    '-format', 'csv'
]

if __name__ == '__main__':
    args = parser.parse_args()
    amplxe_args[2] = args.report
    if args.report == 'hw-events':
        amplxe_args += ['-group-by', 'task']
    if args.outfile:
        amplxe_args += ['-report-output', args.outfile]
    if args.indir:
        amplxe_args += ['-result-dir', args.indir]
    subprocess.call(amplxe_args)
