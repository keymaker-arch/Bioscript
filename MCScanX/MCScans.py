import re


# take standard gff file as input, and output MCScanX format gff file.
# replace blank in gene id with '-'
def get_info(f_gff, f_result):
    pattern_cds = '\tCDS\t'
    pattern_loc = '^(.*?)\t'
    pattern_id = ';Name=(.*?);'
    pattern_begin_end = '\t(\d+)\t(\d+)\t'

    for line in f_gff:
        if '#' in line:
            continue

        match = re.search(pattern_cds, line)
        if match:
            match_loc = re.search(pattern_loc, line)
            match_id = re.search(pattern_id, line)
            match_begin_end = re.search(pattern_begin_end, line)

            str = match_loc.group(1)+'\t'+ match_id.group(1)+'\t'+match_begin_end.group(1)+'\t'+match_begin_end.group(2)+'\n'
            str = re.sub(' ', '-', str)

            f_result.write(str)

    f_result.close()
    f_gff.close()


