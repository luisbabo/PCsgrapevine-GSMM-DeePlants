import pandas as pd
from plants_sm.pathway_prediction.pathway_prediction import PlantPathwayClassifier

def prediction_PCs_pathway_missing_GSMM_VV(input, output):

    df = pd.read_csv(input, encoding='latin1', sep=',')
    classifier_kegg = PlantPathwayClassifier('KEGG')
    classifier_plantcyc = PlantPathwayClassifier('PlantCyc')
    list_pathway_plantcyc = []
    list_pathway_kegg = []
    for smiles in df['SMILES']:
        prediction_kegg = classifier_kegg.predict(smiles)
        list_pathway_kegg.append(prediction_kegg)

        prediction_plantcyc = classifier_plantcyc.predict(smiles)
        list_pathway_plantcyc.append(prediction_plantcyc)


    df['Pathway predictions KEGG'] = list_pathway_kegg
    df['Pathway predictions PlantCyc'] = list_pathway_plantcyc
    df.to_csv(output, index=False, sep=',')

prediction_PCs_pathway_missing_GSMM_VV('datasetpcs.csv', 'output_pathway_predict_pcs.csv')