Team Name     : Peterphancong
Affiliation   : National Cheng Kung University, Taiwan
Contact point : Peter Phan (peter.phancong@iir.csie.ncku.edu.tw / peter.phancong@gmail.com)
              : (886) 978114412
Team members  : Peter - Phan (PhD Student - National Cheng Kung University, Taiwan)
              : Celia - Ngo (Master student - National Cheng Kung University, Taiwan)
              : Ben - Phan (Master student - National Cheng Kung University, Taiwan)
Number of runs: 3
General method description: For the entity and identifier detection we build a probability model and fulfil method. First we extract and measure the co-occurence frequency of each pair of entity types as well as entity identifiers from the given data for training. Then we evaluate and fill in the missing entities with the highest frequency entities from available entities dataset. For the relation extraction, we use PubmedBERT with augmented data created by LLM
Run 1: Entity pairs are extracted from PubmedBERT without enhanced by probability model.
Run 2: Entity pairs from Run 1 with enhanced by appling probability model and fulfilment.
Run 3: Entity pairs from AIONER with fulfil method to detect identifiers.
Additional datasets: BioRED, GNormPlus, NLM-Gene, NCBI Disease, BC5CDR-Disease, Linnaeus, Species-800, BC5CDR-Chemical, NLM-Chem, tmVar3, BioID
