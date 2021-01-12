#!/bin/bash
#step2_intat_ltr_annotation.sh

#USAGE step2_intat_ltr_annotation.sh Arabidopsis_thaliana

display_usage() {
        echo  "\nUsage:\n$0 [species_name]\n"
}

# if less than one arguments supplied, display usage
        if [  $# -le 0 ]
        then
                display_usage
                exit 1
        fi

#setting
scripts=/*/*/interSP/bin
Viridiplantae=/*/*/interSP/Viridiplantae_v3.0
export PATH='/home/zshanshan/bin/last-963/bin/':$PATH

# ltrharvest
echo "running ltrharvest"
cd results/$1/ltrharvest
gt ltrharvest -index ../index/$1 -minlenltr 100 -maxlenltr 3000 -similar 80 \
-gff3 ltrharvest.gff -out ltrharvest.fa > ltrharvest.scn

# sort
gt gff3 -sort ltrharvest.gff > ltrharvest_sorted.gff

# ltrdigest
echo "running ltrdigest"
cd ../ltrdigest
gt ltrdigest -outfileprefix ltrdigest ../ltrharvest/ltrharvest_sorted.gff ../index/$1 > ltrdigest.gff

# REXdb (Viridiplantae v3.0)
echo "running Protein Domains Finder"
cd ../REXdb
python2 $scripts/extract_LTR-RT_inner_seqs.py ../index/$1.fasta \
../ltrdigest/ltrdigest_tabout.csv ltrdigest_inner.fasta

python3 $scripts/dante.py \
-nld False -q ltrdigest_inner.fasta -pdb $Viridiplantae/Viridiplantae_v3.0_ALL_protein-domains.fasta \
-cs $Viridiplantae/Viridiplantae_v3.0_ALL_classification -oug ltrdigest_inner_domains.gff -dir ./

python2 $scripts/Intact_gypsy_copia_REXdb.py ltrdigest_inner_domains.gff intact_REXdb.csv

