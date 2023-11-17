import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_pbaa_cmd(sample_name):
    input_path = 'fastq/' + sample_name + '.fastq'
    if not os.path.isfile(input_path):
        raise ValueError(f'No fastq file for {sample_name}')
    # TODO: don't use path. expect pbaa executable to be on the system path
    pbaa_bin = '/home/aknaupp/.conda/envs/adrb1/bin/pbaa'
    cmd_fmt = pbaa_bin + ' cluster {options} {ref} {input_fastq} {output_prefix}'
    return cmd_fmt.format(
        options = '--max-reads-per-guide=1000000 --max-uchime-score=0.01',
        ref='adrb1.fa', 
        input_fastq=input_path,
        output_prefix=f'execution/{sample_name}/{sample_name}'
    )

def run_pbaa(sample_name):
    try:
        cmd = get_pbaa_cmd(sample_name)
    except ValueError as e:
        return str(e)
    os.makedirs(f'execution/{sample_name}', exist_ok=True)
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return sample_name, result

def process_samples(to_analyze):
    pbaa_executions = []
    with ThreadPoolExecutor() as executor:
        for sample_name in to_analyze:
            pbaa_executions.append(executor.submit(run_pbaa, sample_name))

    failures = []
    for pbaa_execution in as_completed(pbaa_executions):
        sample_name, result = pbaa_execution.result()
        # handle errors
        try:
            result.check_returncode()
        except subprocess.CalledProcessError:
            failures.append(sample_name, result.stderr.decode("utf-8"))
            continue
    return failures
