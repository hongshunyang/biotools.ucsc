https://github.com/lindenb/jvarkit/wiki/KnownGenesToBed
curl -s "http://hgdownload.cse.ucsc.edu/goldenPath/mm10/database/knownGene.txt.gz" |\
  gunzip -c |\
  java -jar kg2bed.jar

3、curl -s "http://hgdownload.cse.ucsc.edu/goldenPath/mm10/database/knownGene.txt.gz" |  gunzip -c |  java -jar kg2bed.jar -t -x -o CDS_UTR_INTRON.csv
