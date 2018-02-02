# Download itt (https://github.com/NERSC/itt-python) and install
# If it fails to install try to add this line 
# self.vtune = '/path/to/vtune/directory'
# in the setup.py:finalize_options() function, before the assert statements
import itt
import numpy as np


size = int(1e6)
iters = 100

a = np.random.randn(size)
b = np.random.randn(size)

domain_one = itt.domain_create('dom1')
domain_two = itt.domain_create('dom2')
domain_three = itt.domain_create('dom3')
domain_total = itt.domain_create('domtotal')


itt.resume()

itt.task_begin(domain_total, 'domtotal')

for i in range(iters):    
    itt.task_begin(domain_one, 'dom1')
    c = a + b
    itt.task_end(domain_one)
    
    itt.task_begin(domain_two, 'dom2')
    d = a / b
    itt.task_end(domain_two)
    
    itt.task_begin(domain_three, 'dom3')
    e = np.sin(a) + np.cos(b)
    itt.task_end(domain_three)

itt.task_end(domain_total)
itt.detach()

print(np.mean(c), np.mean(d), np.mean(e))