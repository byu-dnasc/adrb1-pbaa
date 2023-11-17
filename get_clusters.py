import os

import pbaa

os.makedirs('execution', exist_ok=True)

# find samples for which clustering has not yet been performed
sample_names = [fn[:-6] for fn in os.listdir('fastq') if fn.endswith('.fastq')]
execution_names = [fn for fn in os.listdir('execution') if os.path.isdir('execution/'+fn)]
# exclude empty directories from executions
for directory in execution_names:
    if os.listdir('execution/'+directory) == []:
        execution_names.remove(directory)

to_analyze = [name for name in sample_names if name not in execution_names]

# verify that an index file exists for each sample
for sample_name in to_analyze:
    index_path = f'fastq/{sample_name}.fastq.fai'
    if not os.path.isfile(index_path):
        print(f'No index file found for {sample_name}, skipping.')
        to_analyze.remove(sample_name)

# handle case where no samples need to be analyzed
if not to_analyze:
    if sample_names:
        print('No samples found for which clusters have not been generated.')
    else:
        print('No samples found.')
    exit(1)

# run pbaa on each sample
print('Found', len(to_analyze), 'samples for which clustering analysis has not yet occurred:')
print(','.join(to_analyze))
failures = pbaa.process_samples(to_analyze)

# report results
if failures:
    for sample_name, error_message in failures:
        print('#### Error executing pbaa for', sample_name, '####')
        print(error_message)
else:
    print('Successfully executed pbaa for all samples.')