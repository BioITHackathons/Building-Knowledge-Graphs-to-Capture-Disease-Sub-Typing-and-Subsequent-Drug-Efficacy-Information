# Varmovinator

![](raw=true)

## The world's best (and first) variant learning model validator (outside CAGI challenges).  

### For a given variant, this will pull basic information from standard bioinformatic databases such as 


* disease association <sup>1,2<sup>
* gene ontology <sup>2</sup>
* uniprot information <sup>2</sup>
* environmental factors that influence penetrance
* putative molecular consequences <sup>1</sup>
* putatative clinical consequences <sup>1</sup>
* population frequency <sup>1</sup>
* protein effects <sup>2<sup>
* gene <sup>2</sup>
  
1: opencravat
2: uniprot

  
### We have selected the following three models to test:
  
  1. BioGPT
  2. StabilityLM (Stable Vicuna 13-b)
  3. Fabric GEM
  
### We will come up with a model to
  * tag discrepant assertions
  * calculate a consistency score
