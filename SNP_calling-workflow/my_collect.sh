#！/bin/bash
function collect(){
    srr_acc = $1
    mkdir logs/${srr_acc}
    cp ${srr_acc}/bowtie.log logs/${srr_acc}/
    cp ${srr_acc}/${srr_acc}_1_fastqc.zip logs/${srr_acc}/
    cp ${srr_acc}/${srr_acc}_fastqc.zip logs/${srr_acc}/
}

mkdir logs
for srr in `cat $1`;do
    collect $srr
    echo "collected:${srr}"
done

zip -r ${1}_log.zip logs
rm -rf logs