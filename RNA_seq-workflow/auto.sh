#！/bin/bash
#
#
#############################
#structural dir tree
#RNAseq
#|__sra_name1
#| |__*.log
#| |__sra_name.sra
#| |__fastq_data
#| |   |__sra_name1.sra_1.fastq
#| |   |__sra_name1.sra_2.fastq
#| |__fastqc_test
#| |   |
#| |__tophat_test
#| |   |__
#| |   |
#| |__result
#|    |__sra_name1.bam
#|    |__align_summary.txt 
#|
#|__sra_name2
#|  |
#|
#|
#
#############################
#
flag=$1
#
#
sra_name_file=$2
#the sra name file records sra index list line by line
#
#
dir_base=/root/tshan/
#dir_pi=/mnt/data/RNAseq/${sra_name}
#local dir to save sra file
#
#
#server_ip=10.2.42.11
#
#
#server_username=tshan
#
#
sra_fullname=${sra_name}.sra
#sra full name    e.m.   SRR8089950.sra
#
#
#dir_11=/home/tshan/data/RNAseq/${sra_name}
#dir where everything of the sra file is saved in 10.2.42.11
#
#
#dir_home=/home/tshan/
#
#
#genome gff file in 10.2.42.11
genome_gff=/home/tshan/data/genome/NBI_genome/NBI_Gossypium_hirsutum_v1.1.gene.gff
#
#
#genome index file in 10.2.42.11
genome_index=/home/tshan/data/genome/bowtie2index/NBI_Gih_v1.1
#
#
#file name after fastqdump
fastq_dumped_name=tshan_data_RNAseq_${sra_name}
#need correction !!!!!!!!!!!
#
#
#download sra file from NCBI ftp server
#recieve an argument as directory,which means this func can be used locally and remotely
function DownloadFromNCBI(){	

	local str1=${sra_name:0:6}
	#to make the target string.  example SRR808

	local str2=${sra_name}.sra
	#to make the target string.  example SRR8089950.sra
	
	local url="https://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/${str1}/${sra_name}/${str2}"
	#the url to donwload sra file
	
	sudo wget -P $1 ${url} 1>>$1/wget.log 2>>$1/wget_error.log
	#donwload the file. 
	
}
#
#
#make structural dir for donwloading
#recieve an argument as directory,which means this func can be used locally and remotely
function MakeDir(){

	if [ ! -d $1 ]
	then
		sudo mkdir $1
		#make a dir for sra file donwloading
		sudo mkdir $1/fastq_data
		#make dir for fastq-dump
		sudo mkdir $1/tophat_test
		#make dir for tophat
		sudo mkdir $1/fastqc_test
		#make dir for tophat
		sudo mkdir $1/result
	else
		sudo mkdir $1/fastq_data
		#make dir for fastq-dump
		sudo mkdir $1/tophat_test
		#make dir for tophat
		sudo mkdir $1/fastqc_test
		#make dir for tophat
	fi
}
#
#
#upload sra file to the server target dir from local host
#function UpLoad(){
#	
#	#make a dir in target server
#	sudo ssh ${server_username}@${server_ip} mkdir ${dir_11}
#	
#	#upload the file
#	sudo scp ${dir_pi}/${sra_fullname} ${server_username}@${server_ip}:${dir_11} 1>>${dir_pi}/scp.log 2>>${dir_pi}/scp_error.log
#	
#}
#
#
#download tophat output to local machine from server
#function DownloadResult(){
#
#	sudo scp tshan@10.2.42.11:${dir_11}/tophat_test/accepted_hits.bam ${dir_pi}/tophat_test/
#	#download tophat to local machine
#
#}
#
#
#
#################################################
#all the func below run on the server host
#################################################
#
#
#run fastq-dump
#accept an argument as directory,which means this func can be used locally and remotely
function FastqDump(){
	
	local str1=${fastq_dumped_name}_${sra_name}.sra_1.fastq
	
	local str2=${fastq_dumped_name}_${sra_name}.sra_1.fastq
	
	fastq-dump --split-3 -O $1/fastq_data/ -A $1/${sra_fullname} 1> $1/fastq_dump.log  2> $1/fastq_dump_error.log
	
	mv $1/fastq_data/${str1} $1/fastq_data/${sra_name}.sra_1.fastq
	
	mv $1/fastq_data/${str1} $1/fastq_data/${sra_name}.sra_2.fastq
}
#
#
#
#
#run tophat
#accept two argument,first as working directory,second as log directory,which means this func can be used locally and remotely
function Tophat(){

	tophat -p 6 -G ${genome_gff} -o $1/tophat_test/ ${genome_index} $1/fastq_data/${sra_name}.sra_1.fastq $1/fastq_data/${sra_name}.sra_2.fastq 1> ${dir_home}/tophat.log 2>$2/tophat_error.log

}
#
#
#clean useless files
#accept one argument as working directory, which means this func can be used locally and remotely
function Clean(){
	
	#target file name
	local str1=${sra_name}_accepted_hits.bam
	local str2=${sra_name}_align_summary.txt
	#sra file 
	local str3=${sra_name}.sra
	#move result to result dir
	mv $1/tophat_test/accepted_hits.bam $1/result/${str1}
	mv $1/tophat_test/align_summary.txt $1/result/${str2}
	
	#remove everything in tophat_test
	rm -rf $1/tophat_test/
	
	#remove fastq files
	rm -rf $1/fastq_data/

	#remove sra file
	rm -rf $1/${str3}
	
}
###########################################################
#main function entry
###########################################################
#
#
case ${flag} in

#	-d)
#		MakeDirLocal
#		;;
#	-u)
#		UpLoad
#		;;
#	-du)
#		MakeDirLocal
#		DownloadFromNCBI
#		UpLoad
#		;;
#	-m)
#		MakeDirLocal
#		;;
#	-dr)
#		MakeDirLocal
#		DownloadResult
#		;;
#	-M)
#		MakeDirRemote
#		;;
#	-F)
#		MakeDirRemote
#		FastqDump
#		;;
#	-FD)
#		FastqDump
#		;;
#	-FC)
#		Fastqc
#		;;
#	-T)
#		Tophat
#		;;
#	-A)
#		MakeDirRemote
#		DOWNLOAD
#		FastqDump
#		Tophat
#		;;
	-A)
		for sra_name in `cat sra_name_file`
		do

		dir=${dir_base}${sra_name}
		MakeDir ${dir}
		DownloadFromNCBI ${dir}
		FastqDump ${dir}
		Tophat ${dir}
		Clean ${dir}

		done
	;;
		


	-h)
		echo "auto-run V1.0 "
		echo "[usage]: "
		echo "auto-run -[option] [sra_name_file]"
		echo "		example : auto-run -A to_run.txt"
		echo "		option run locally is in lower case while option run on server is in upper case"
		echo ""
		echo "	options:"
		echo "options run on local machine:"
		echo ""
		echo "	-d create the dir and donwload sra file to it "
		echo "	-u create the dir in server and upload sra file to it"
		echo "	-du create the dir locally and donwload sra file to it and upload to server"
		echo "	-m create the local dir in local machine only"
		echo "	-dr download bam result from server"
		echo "options run on server"
		echo ""
		echo "	-M create structural dir in server"
		echo "	-F run fastq-dump for sra file and run fastqc. the dirs should be already made"
		echo "	-FD run fastq-dump only . dirs should be already made"
		echo "	-FC run fastqc only. dirs should be already made"
		echo "	-T run tophat "
		echo ""
		echo ""
		echo "example:"
		echo "	by running command: "
		echo "		./auto-run -du SRR8089950"
		echo "on local machine, the dir /mnt/data/RNAseq/SRR8089950/ will be created and SRR8089950.sra will be downloaded to it, and uploaded to dir /home/tshan/data/test/SRR8089950/ on server during this procedure"
		echo ""
		echo ""
		echo "#######################################"
		echo "#	for a common situation, run         " 
		echo "#	./auto-run -du [sra_name]       "
		echo "#	on local machine, then run          "
		echo "#	./auto-run -F [sra_name]        "
		echo "#	on server                           "
		echo "#######################################"
		echo ""
		echo "for splited files "
		echo "run "
		echo "	./auro_run -S [sra_name]"
		echo "to split file to 6G each one"
		echo "run ./auto-run -TP [sra_name] [index] to tophat one part of the splited file"
		echo "run ./auto-run -C [sra_name] to remove all the useless file of one sra data/RNAseq/$"
		echo ""
		echo ""
		echo ""
		echo ""
		echo ""
		echo ""
		echo "for more detailed information, please check the source code of this script."
		echo ""
		;;
	*)
		echo "please type -h for a simple instruction"
		;;
esac