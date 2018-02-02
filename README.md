# vtune-analysis
A collection of python scripts to collect hw events and analyze via the command line

# Contents

1. vtune-custom-analysis.py: Collect all the required events to recreate the top-down analysis (or general-exploration) on a haswell processor
1. vtune-report-hw-events.py: Group the collected results by task (which are indicated in the code using the intel itt API).
1. vtune-report-summary.py: The top-down analysis summary for the whole code.
1. process-metrics.py: Data analysis script, used to calculate user defined metrics combining the collected hw events.
1. example1.py: A very simple example that demonstrates the usage of the itt API. 
