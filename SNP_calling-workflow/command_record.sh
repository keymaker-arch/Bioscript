参考基因组获取和索引：
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/237/485/GCA_002237485.1_Zm-PH207-REFERENCE_NS-UIUC_UMN-1.1

bowtie2-build PH207_genome_genebank.fna PH207

samtools faidx -f PH207_genome_genebank.fna


下载sra数据：
nohup prefetch -p -X 100G --option-file PH207_SRR.txt 1>prefetch.log 2>error.log &


sra数据解压和质控：
fastq-dump --split-files SRR1575346/SRR1575346.sra -O SRR1575346/

fastqc SRR1575346_1.fastq


bowtie2比对：
nohup bowtie2 -x ../../genome/PH207 -1 SRR1575346_1.fastq -2 SRR1575346_2.fastq -S out.sam -p 24 1>bowtie.log 2>error.log & 


sam文件排序和索引：
samtools view -@ 24 -bS out.sam | samtools sort -@ 24 -o out.bam.sorted
samtools index -@ 24 out.bam.sorted out.bam.sorted.indexed

nohup sh -c "view -@ 24 -bS out.sam | samtools sort -@ 24 -o out.bam.sorted" 1>samtools.log 2>1& &


使用bcftools进行snpcalling:
nohup bcftools mpileup --fasta-ref ../../genome/PH207_genome_genebank.fna out.bam.sorted -o mpileup.vcf 1>mpileup.log 2>&1 &
nohup bcftools call -cv -o raw_snp.vcf mpileup.vcf 1>bcftools.log 2>&1 &

nohup sh -c "bcftools mpileup --fasta-ref ../../genome/PH207_genome_genebank.fna out.bam.sorted -Ou | bcftools call -cv -o raw_snp.vcf" 1>bcftools.log 2>&1 &