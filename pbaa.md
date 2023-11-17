# `pbAA` haplotype analysis

This repository contains code for detecting the haplotypes present in reads 
sequenced from amplicons of the ADRB1 ORF. It uses [`pbAA`](https://github.com/PacificBiosciences/pbAA) 
to phase reads and identify variants, followed by custom python code to 
determine the haplotypes present in the input samples.

## PacBio Amplicon Analysis (`pbAA`)

`pbAA` is a method which is particularly useful for variant discovery.

`pbAA` produces a set of unique consensus sequences assembled by clustering
reads which map to a guide sequence. `pbAA` executes in several stages (see 
diagram in README from [GitHub repo](https://github.com/PacificBiosciences/pbAA))
and accomplishes several tasks along the way.

The `pbAA` pipeline includes error correction and consensus sequence generation.

### Guide sequence

The sequence of the ADRB1 ORF (NC_000010.11:114044133-114045566) is used effectively 
to filter out any off-target reads.

### Clustering and consensus sequence generation

One important task performed by `pbAA` is clustering. During the clustering stage, 
reads which aligned to a guide sequence are subdivided into groups by similarity. A
consensus sequence is generated for each cluster. Several metrics are generated for 
each cluster which are used to filter all clusters into one of two files, one for 
'passed' clusters, and another for 'failed'.

### Multiple clusters

In theory, `pbAA` should create a consensus sequences for each true molecular sequence
which was created during the PCR amplification. `pbAA` is sensitive to all types of 
variation. From a small sample of ADRB1 amplicon sequences, I have observed clusters 
which are identical to the reference, some with single substitutions, deletions, and more.

## Identifying haplotypes from `pbAA` clusters

The aim of this analysis is to determine the haplotype(s) present in the samples
used as inputs. Two loci are used to define the haplotypes, a SNP located at position
145 of the guide sequence mentioned above, and another SNP at position 1165.
The samples chosen for sequencing and analysis are known to be heterozygous for at least
one of these loci.

The variation present in the amplified sequences used as input will cause multiple 
clusters to form. However, the consensus sequences created from these clusters are
derived from one or the other chromosome. After the clusters are obtained by running
`pbAA`, the results are analyzed to determine the sample's haplotypes. This analysis
includes counting the total number of reads which came from each chromosome, i.e.
the number of reads which represent each haplotype.

### Handling chimeric sequences

Artifical PCR chimeras can occur if the sample is a double heterozygote. These sequences
form their own clusters. `pbAA` runs the UCHIME algorithm on each cluster to compute the 
likelihood that the cluster represents a chimeric sequence. A score of -1 indicates an 
infinitesimal probability that a cluster represents a chimeric sequence. Therefore, only 
clusters with a uchime score of -1 are used for identifying the haplotypes. The logic for 
this is implemented in `fromfile.get_clusters`.

### Output file

Each row in the output file presents analysis results with respect to a single sample.  
- **total_reads** is the number of reads sequenced.  
- **reads_passing_qc** is the number of reads which `pbAA` uses. There are several factors
which can affect this number, but the main ones are read quality scores (default 
is >20) and the max reads per guide (default is 500, but I've set the value to 1,000,000
in this analysis so that the true number of reads in each haplotype is computed).

## Troubleshooting

In the event that this analysis detected zero reads for any of the four haplotypes,
a number of things could have gone wrong. The first thing to do is to look at the
files `pbAA` created, which should be located under the directory 'execution'.
This analysis uses the file with suffix 'passed_cluster_sequences.fasta' to find the
haplotypes present in the sample. This file should contain at least two lines which
make up a record for a single cluster. If it is empty, check 
'failed_cluster_sequences.fasta'. As long as there are clusters in the 'passed' file,
then the analysis should be able to detect haplotypes.
