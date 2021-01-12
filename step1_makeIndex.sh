#!/bin/bash
#step1_makeIndex.sh

#USAGE step1_makeIndex.sh Arabidopsis_thaliana

display_usage() {
        echo  "\nUsage:\n$0 [species_name]\n"
}

# if less than one arguments supplied, display usage
        if [  $# -le 0 ]
        then
                display_usage
                exit 1
        fi

echo "make faidx"
samtools faidx results/$1/index/$1.fasta
echo "make blastdb"
makeblastdb -in results/$1/index/$1.fasta -dbtype nucl
echo "make ltrharvest index"
gt suffixerator -db results/$1/index/$1.fasta -indexname results/$1/index/$1 -tis -suf -lcp -des -ssp -sds -dna

