import sys
import re


pattern_1 = '(\d+) reads; of these:'
pattern_2 = '(\d+) \((\d.*?)\) were paired; of these:'
pattern_5 = '(\d+) \((\d.*?)\) aligned concordantly >1 times'
pattern_15 = '(.*?) overall alignment rate'

def get_align_info(f_bowtie):
    _out_list = []
    for line in f_bowtie:
        match = re.search(pattern_1, line)
        if match:
            _out_list.append(match.group(1))
            continue

        match = re.search(pattern_2, line)
        if match:
            _out_list.append(match.group(1))
            _out_list.append(match.group(2))
            continue

        match = re.search(pattern_5, line)
        if match:
            _out_list.append(match.group(1))
            _out_list.append(match.group(2))
            continue

        match = re.search(pattern_15, line)
        if match:
            _out_list.append(match.group(1))
            continue
    return _out_list


if __name__=='__main__':
    srr_acc_file = sys.argv[1]
    output_file = sys.argv[2]
    f_output = open(output_file, 'w')
    f_output.write('SRR_acc\tpaired_reads\trate\talign>1\trate\toverrall_align\n')

    srr_acc_list = []
    with open(srr_acc_file, 'r') as fp:
        for line in fp:
            srr_acc_list.append(line.replace('\n', ''))

    for srr_acc in srr_acc_list:
        bowtie_file = srr_acc+'/'+'bowtie.log'
        f_bowtie = open(bowtie_file, 'r')
        num_list = get_align_info(f_bowtie)
        f_bowtie.close()
        f_output.write(srr_acc+'\t')
        for num in num_list:
            f_output.write(num+'\t')
        f_output.write('\n')

    f_output.close()
