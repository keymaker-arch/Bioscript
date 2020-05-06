#！/bin/bash
function clean(){
    sra_acc=$1
    rm ${sra_acc}/${sra_acc}.sra
    rm ${sra_acc}/${sra_acc}_1.fastq
    rm ${sra_acc}/${sra_acc}_2.fastq
    rm ${sra_acc}/${sra_acc}.fastq
    rm ${sra_acc}/out.sam
}

function purge(){
    sra_acc=$1
    rm ${sra_acc}/${sra_acc}.sra
    rm ${sra_acc}/${sra_acc}_1.fastq
    rm ${sra_acc}/${sra_acc}_2.fastq
    rm ${sra_acc}/${sra_acc}.fastq
    rm ${sra_acc}/out.sam
    rm ${sra_acc}/out.bam.sorted
    rm ${sra_acc}/out.bam.sorted.indexed

}

for srr in `cat $1`;do
	purge $srr
done
