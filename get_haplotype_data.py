import os

import align
import fromfile

# analyze the clusters to get haplotype counts
execution_names = [fn for fn in os.listdir('execution')]
HAPLOTYPES = ('ag', 'ac', 'gc', 'gg')
adrb1 = align.get_adrb1()
aligner = align.get_aligner()
rows = []
cluster_rows = []

for sample_name in execution_names:
    ht_counts = dict.fromkeys(HAPLOTYPES, 0)
    for cluster_name, seq, read_count, freq, possibly_chimeric in fromfile.get_clusters(sample_name):
        if freq < 0.05:
            continue
        alignment = align.get_alignment(aligner, adrb1, seq)
        snp_1 = alignment[1,144]
        snp_2 = alignment[1,1164]
        haplotype = (snp_1+snp_2).lower()
        assert haplotype in HAPLOTYPES, f'haplotype {haplotype} not among possible haplotypes {HAPLOTYPES}'
        ht_counts[haplotype] += read_count
        cluster_rows.append((sample_name, cluster_name, haplotype))
    total_reads = fromfile.get_total_num_reads(sample_name)
    reads_passing_qc = fromfile.get_num_input_reads(sample_name)
    rows.append((sample_name, total_reads, reads_passing_qc) + tuple(ht_counts[ht] for ht in HAPLOTYPES))

with open('clusters_by_haplotype.json', 'w') as f:
    header = ('sample_name', 'cluster_name', 'haplotype')
    f.write(','.join(header) + '\n')
    for line in cluster_rows:
        f.write(','.join(line) + '\n')

# write the haplotype counts to a file
with open('haplotype_counts.tsv', 'w') as f:
    header = ('sample_name', 'total_reads', 'reads_passing_qc') + tuple('haplotype_' + ht + '_reads' for ht in HAPLOTYPES)
    f.write('\t'.join(header) + '\n')
    for row in rows:
        f.write('\t'.join(str(x) for x in row) + '\n')