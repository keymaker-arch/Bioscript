#！/bin/bash
genome_ref="/sdd/hants/ZeaMays/PH207/genome/PH207"

function run1(){
    sra_acc=$1
    file_path=${sra_acc}"/"${sra_acc}".sra"
    if [ ! -f $file_path ]; then
        echo "no sra file found for: "${sra_acc}"/"${sra_acc}".sra"
        continue
    fi

    echo "Start processing: ${sra_acc}"
    echo "running fastq-dump for: ${sra_acc}/${sra_acc}.sra..."
    fastq-dump --split-files ${sra_acc}/${sra_acc}.sra -O ${sra_acc}/
    echo "fastq-dump done for: ${sra_acc}"

    if [ -f ${sra_acc}/${sra_acc}_1.fastq ]; then
        echo "running fastqc..."
        fastqc ${sra_acc}/${sra_acc}_1.fastq -o ${sra_acc}/
        echo "fastqc done for: ${sra_acc}" 
    elif [ -f ${sra_acc}/${sra_acc}.fastq ]; then
        echo "running fastqc..."
        nohup fastqc ${sra_acc}/${sra_acc}.fastq -o ${sra_acc}/
        echo "fastqc done for: ${sra_acc}" 
    fi
}

function run2(){
    sra_acc=$1
    echo "running bowtie for: ${sra_acc}"
    if [ -f "${sra_acc}/${sra_acc}_1.fastq" ]; then
        nohup bowtie2 -p 24 -x ${genome_ref} -1 ${sra_acc}/${sra_acc}_1.fastq -2 ${sra_acc}/${sra_acc}_2.fastq -S ${sra_acc}/out.sam 1>${sra_acc}/bowtie.log 2>&1
        echo "bowtie2 done for: ${sra_acc}"
    else
        nohup bowtie2 -p 24 -x ${genome_ref} -U ${sra_acc}/${sra_acc}.fastq -S ${sra_acc}/out.sam 1>${sra_acc}/bowtie.log 2>&1
        echo "bowtie2 done for: ${sra_acc}"
    fi
    
    echo "running samtools view sort index for: ${sra_acc}"
    samtools view -@ 24 -bS ${sra_acc}/out.sam | samtools sort -@ 24 -o ${sra_acc}/out.bam.sorted
    samtools index -@ 24 ${sra_acc}/out.bam.sorted ${sra_acc}/out.bam.sorted.indexed

    echo " "
    echo " "
}

function run3(){
    sra_acc=$1
    nohup sh -c "bcftools mpileup --fasta-ref ../genome/PH207_genome_genebank.fna ${sra_acc}/out.bam.sorted -Ou | bcftools call -cv -o ${sra_acc}/raw_snp.vcf" 1>bcftools.log 2>&1 &
}

for sra_acc1 in `cat $1`;do
	run2 ${sra_acc1}
done


