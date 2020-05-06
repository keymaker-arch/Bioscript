import re
import os
import sys


pattern_input = 'Input:  (.*?)\n'
pattern_mapped = 'Mapped:  (.*?) of input'
pattern_overall = '^(.*?) overall'
pattern_pair = 'Aligned pairs:  (.*?)\n'
pattern_concordant = '^(.*?) concordant pair'
pattern_srr = '(SRR\d{7})'


def get_summary(SRR_id ,align_file, target_file):
    f_source = open(align_file, 'r')
    f_target = open(target_file, 'a')

    f_target.write(SRR_id+'\t')

    for line in f_source:
        match = re.search(pattern_input, line)
        if match:
            input = match.group(1)
            f_target.write(input+'\t')
            continue


        match = re.search(pattern_mapped, line)
        if match:
            mappd = match.group(1)
            f_target.write(mappd+')\t')
            continue


        match = re.search(pattern_overall, line)
        if match:
            ovrl = match.group(1)
            f_target.write(ovrl+'\t')
            continue


        match = re.search(pattern_pair, line)
        if match:
            pair = match.group(1)
            f_target.write(pair+'\t')
            continue


        match = re.search(pattern_concordant, line)
        if match:
            con = match.group(1)
            f_target.write(con+'\n')
            continue

    f_target.close()
    f_source.close()

# 使用字典进行存储时键发生冲突，应该为列表嵌套列表的格式存储
# 19/11/16 通过检测键值是否存在，若存在则在当前键后加'_'以，仅支持分割为两个文件的情况，应重构为列表嵌套列表
def get_align_file(file_root):
    result_dict = {}
    file_list = []
    for root, dirs, files in os.walk(file_root):
        for file_name in files:
            if 'align_summary' in file_name:
                file_list.append(os.path.join(root, file_name))

    for strs in file_list:
        match = re.search(pattern_srr, strs)
        if match:
            key = match.group(1)
            if key in result_dict:
                key = key+"_"
                result_dict[key] = strs
            else:
                result_dict[key] = strs

    return result_dict


if __name__=='__main__':
    dir = sys.argv[1]
    summary_file = sys.argv[2]

    file_dict = get_align_file(dir)

    for key, value in file_dict.items():
       get_summary(key, value, summary_file)
