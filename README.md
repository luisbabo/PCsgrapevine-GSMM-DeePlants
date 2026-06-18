# Projeto Bioinformática

## Integration of Phenolic Secondary Metabolism into a Grapevine Genome-Scale Metabolic Model Using DeePlants


## Project Workflow
 
1. **Compound selection** — fourteen phenolic compounds present in *Vitis vinifera*
   but missing from the iMS7199 GSMM were selected (see `datasetpcs.csv`).
2. **Pathway classification** — each compound was classified against **KEGG** and
   **PlantCyc** using the DeePlants pathway classifier.
3. **Retrobiosynthetic (*de novo*) prediction** — biosynthetic routes were predicted
   with the **Retroformer** model via MCTS and A* algorithms and the reactions were rendered
   as images.
4. **Candidate-enzyme identification** — the grapevine reference proteome
   (**PN40024.v4**) was annotated with EC numbers using **ProtBERT**, to identify
   candidate enzymes for the predicted reactions.





### Author: Luís Babo
