import sys
import subprocess

# usage: python vtune-report-summary.py [result_dir] [report_output_file]

amplxe_args = [
    'amplxe-cl', '-report',
    'summary', '-csv-delimiter=tab',
    '-format', 'csv',
    # '-result-dir', ''
    # '-report-output', '' 
]

if __name__ == '__main__':
	if len(sys.argv) > 1:
		res_dir = sys.argv[1]
		amplxe_args += ['-result-dir', res_dir]
	if len(sys.argv) > 2:
		outfile = sys.argv[2]
		amplxe_args += ['-report-output', outfile]

	subprocess.call(amplxe_args)
