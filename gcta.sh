#!/bin/bash
#PBS -q hotel
#PBS -l nodes=1:ppn=24
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -o gcta_log.out 
#PBS -e gcta_err.txt 

bcftools=/projects/ps-palmer/software/local/src/bcftools-1.14/bcftools
plink=/tscc/projects/ps-palmer/software/local/src/plink-1.90/plink
# bfile=/tscc/projects/ps-palmer/samuckadam/code/round10
bfile=round10
# out=/tscc/projects/ps-palmer/samuckadam/code/round10_extractedV3/round10_LOFextracts
out=round10_extractedV3/round10_LOFextracts
dominant=/projects/ps-palmer/samuckadam/code/round10_extractedV2/round10_ext_dom.vcf
dominantOut=/projects/ps-palmer/samuckadam/code/dominant/dominant
recessive=/projects/ps-palmer/samuckadam/code/round10_extractedV2/round10_ext_rec.vcf
recessiveOut=/projects/ps-palmer/samuckadam/code/recessive/recessive
gcta=/projects/ps-palmer/software/local/src/gcta/gcta64

cd /tscc/projects/ps-palmer/samuckadam/code
${plink} --bfile ${bfile}  --extract lof_list.txt --double-id --make-bed --out ${out} 
# cd ..
# cd ..

# cd projects/ps-palmer/samuckadam/code

${plink} --bfile ${out} --recode vcf-iid --out ${out}

# ${plink} --vcf ${dominant} --make-bed --out ${dominantOut}

# ${plink} --vcf ${recessive} --make-bed --out ${recessiveOut}

# for FILE in plink_phenotypes/*.phen
# do
#     BASE=`basename $FILE .phen`
#     	# ${gcta} --mlma --bfile ${recessiveOut} \
# 		# --grm /projects/ps-palmer/gwas/projects/Allrats/grm/AllchrGRM \
#         # --pheno $FILE --out gcta_recessive/$BASE --thread-num 24

#         ### Use for recessive and dominant models
#         # ${plink} --bfile ${out} --linear recessive --pheno $FILE --pheno-name $BASE --allow-no-sex --out plink_rec/$BASE --thread-num 24
        
#         ### Use for additive model
#         ${plink} --bfile ${out} --linear dominant --covar gcta_pca.eigenvec --pheno $FILE --pheno-name $BASE --allow-no-sex --out plink_pca_dom 1/$BASE --thread-num 24

# done



# ${gcta} --mlma --bfile ${out} --grm  --pheno $FILE --out results/phenotypes/$BASE

# making the pca's
# /projects/ps-palmer/software/local/src/gcta/gcta64 --grm-bin /projects/ps-palmer/gwas/projects/Allrats/grm/AllchrGRM --pca 3 --thread-num 20 --out gcta_pca
