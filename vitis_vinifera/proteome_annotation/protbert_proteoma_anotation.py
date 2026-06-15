from plants_sm.pathway_prediction.ec_numbers_annotator_utils.prot_bert_prediction import predict_with_protbert_from_fasta

predict_with_protbert_from_fasta(
    fasta_path="PN40024_v41_REF_proteins.fasta",
    output_path="Results_VitisVinifera/predictions_PN40024_v41_protbert_fasta.csv",
    device="cuda:2"
)