### Documention
<KnownGenesToBed>(https://github.com/lindenb/jvarkit/wiki/KnownGenesToBed

### How to use

```shell
curl -s "http://hgdownload.cse.ucsc.edu/goldenPath/mm10/database/knownGene.txt.gz" | gunzip -c | java -jar kg2bed.jar
```
#### Example

```shell
curl -s "http://hgdownload.cse.ucsc.edu/goldenPath/mm10/database/knownGene.txt.gz" |  gunzip -c |  java -jar kg2bed.jar -t -x -o CDS_UTR_INTRON.csv
```
