#!/bin/bash


for i in {8..20};
do
    echo $i
    chrom=$i
    bcftools=/tscc/projects/ps-palmer/software/local/src/bcftools-1.14/bcftools
    plink=/tscc/projects/ps-palmer/software/local/src/plink-1.90/plink
    infile=/tscc/projects/ps-palmer/samuckadam/code/10.3/r10.3.2
    out1=/tscc/projects/ps-palmer/samuckadam/code/10.3/chroms/c${chrom}
    # out1=/projects/ps-palmer/samuckadam/code/compare/round10c${chrom}/c${chrom}

    # source activate lof
    source /home/samuckadam/miniconda3/bin/activate lof

    # use plink to get chr# from round10 genotypes
    ${plink} --bfile ${infile} --chr ${chrom}  --make-bed --out ${out1}

    # convert chr genotypes to vcf format
    ${plink} --bfile ${out1} --recode vcf-iid --out ${out1}

    dir_path=/tscc/projects/ps-palmer/samuckadam/code/10.3/chroms
    cd $dir_path

    #call to filtering python script
    # python transform.py ${chrom} 

    cut -f 1-9 c${chrom}.vcf > c${chrom}_filt.vcf

    # /projects/ps-palmer/software/local/src/plink-1.90/plink --bfile /projects/ps-palmer/samuckadam/code/round10 --extract /projects/ps-palmer/samuckadam/code/lof_list.txt --make-bed --out lof_bfile

    #call to snpeff
    # java -Xms40g -Xmx40g -jar /projects/ps-palmer/gwas/GWAS-pipeline/snpEff/snpEff.jar mRatBN7.2.105 -v c${chrom}_filt.vcf > c${chrom}_filt.ann.vcf

done