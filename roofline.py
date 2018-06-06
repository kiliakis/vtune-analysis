import sys
import os
import subprocess
import argparse
from datetime import datetime

# usage: python vtune-custom-analysis.py ./exe exe_args (for binaries)
#        python vtune-custom-analysis.py python script.py exe_args (for python scripts)
# See the amplxe_args for the deafult args + this link:
# https://software.intel.com/en-us/vtune-amplifier-help-command-line-interface-reference


# These are the exact events collected by vtune18 for the haswell microarch
# to report the general-exploration (top-down analysis paper)


# Consider setting the -user-data-dir to store the raw results in
# separate directory

timestr = datetime.now().strftime('%d%b%y.%H-%M-%S')
custom_template = './custom.tmpl'

parser = argparse.ArgumentParser(description='Collect and report the metrics needed '
                                 'to plot the roofline model.',
                                 usage='python roofline.py -r [raw_dir] -o [csv_dir] -e /usr/bin/ls -l')

parser.add_argument('-r', '--rawdir', type=str,
                    default='roofline-'+timestr,
                    help='The directory to store the roofline related raw data.'
                    ' Default: roofline-date.time')


parser.add_argument('-o', '--outdir', type=str, default='roofline-'+timestr,
                    help='The directory to store the calculated metrics.'
                    ' Default: roofline-date.time')

parser.add_argument('-e','--exe', type=str, nargs=argparse.REMAINDER,
                    help='The executable together with its arguments.')

parser.add_argument('-report-only', '--report-only', action='store_true', default=False,
                    help='Do not run the roofline analysis, only report.'
                    ' Default: Run the analysis and report')

parser.add_argument('-t', '--template', type=str, default=custom_template,
                    help='Custom report template for the flops report.'
                    ' Default: %s' % custom_template)





if __name__ == '__main__':
    args = parser.parse_args()
    custom_template = args.template

    advixe1_args = ['advixe-cl', '-collect',
                    'survey', '-quiet', '-project-dir']

    advixe2_args = ['advixe-cl', '-collect',
                    'tripcounts', '-flop',
                    '-ignore-app-mismatch', '-project-dir']

    advixe3_args = ['advixe-cl', '-report', 'custom', '-format=csv',
                    '--report-template', custom_template, '-report-output', '',
                    '-project-dir']

    advixe4_args = ['advixe-cl', '-report', 'roofs', '-format=csv',
                    '-report-output', '', '-project-dir']
    print(args)
    if not args.exe and args.report_only==False:
        print('You need to provide the executable to be profiled with -e or --exe')
        sys.exit(-1)

    advixe3_args[-2] = args.outdir + '/flops.csv'
    advixe4_args[-2] = args.outdir + '/roofs.csv'
    print(advixe3_args)
    print(advixe4_args)
    if not os.path.exists(args.rawdir):
        os.makedirs(args.rawdir)
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    if not args.report_only:
        subprocess.call(advixe1_args + [args.rawdir, '--'] + args.exe)
        subprocess.call(advixe2_args + [args.rawdir, '--'] + args.exe)
        subprocess.call(advixe4_args + [args.rawdir])
    subprocess.call(advixe3_args + [args.rawdir])

