from Bio.Align import PairwiseAligner
from Bio.Seq import Seq

def get_adrb1() -> str:
    with open('../adrb1.fa', 'r') as f:
        lines = f.read().split('\n')
        adbr1 = ''.join(lines[1:])
    return adbr1

def set_aligner_options(aligner, options):
    for key, value in options.items():
        setattr(aligner, key, value)

def get_aligner() -> PairwiseAligner:
    aligner = PairwiseAligner()
    set_aligner_options(aligner, {
        'match_score': 1,
        'mismatch_score': 0.9,
        'mode': 'local' # in case the sequences are not the same length
    })
    return aligner

def get_alignment(aligner, target, query):
    alignment = aligner.align(target, query)[0]
    rev_comp_alignment = aligner.align(target, Seq(query).reverse_complement())[0]
    if alignment.score < rev_comp_alignment.score:
        alignment = rev_comp_alignment
    return alignment
