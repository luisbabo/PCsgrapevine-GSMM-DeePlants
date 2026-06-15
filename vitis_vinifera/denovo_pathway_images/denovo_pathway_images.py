import pandas as pd
from pathlib import Path
import io

from plants_sm.pathway_prediction.MCTS_A import MCTS_A
from plants_sm.pathway_prediction.entities import Molecule
from plants_sm.pathway_prediction.retroformer_reactor import Retroformer

from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image, ImageDraw, ImageFont

def predict_pathways(dataset_path: str, output_csv_path: str = "results_denovo_pathways.csv", device: str = 'cpu'):
    """
    Lê o dataset, executa a previsão de vias metabólicas e guarda os resultados num CSV.
    Retorna a lista de resultados (dicionários) para ser usada no desenho das reações.
    """
    df = pd.read_csv(dataset_path)
    searcher = MCTS_A(reactors=[Retroformer()], device=device)
    
    results = []
    for idx, row in df.iterrows():
        smiles = row["smiles"]
        name = row["METABOLITE NAME"]
        print(f"[{idx + 1}/{len(df)}] A processar: {name}")
        
        try:
            solution = searcher.search(molecule=Molecule.from_smiles(smiles))
            results.append({
                "name": name,
                "smiles": smiles,
                "solution": solution,
                "status": "success"
            })
        except Exception as e:
            print(f"  Erro ao processar {name}: {e}")
            results.append({
                "name": name,
                "smiles": smiles,
                "solution": None,
                "status": f"error: {e}"
            })

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv_path, index=False)
    print(f"\nResultados guardados em: {output_csv_path}")
    
    return results


def _draw_pathway_reactions(reactions, output_path=None, img_width=900, img_height=250):
    """
    Função auxiliar interna que desenha uma única via de reações.
    """
    if reactions and isinstance(reactions[0], list):
        reactions = [r for sublist in reactions for r in sublist]

    reaction_images = []
    for i, rxn_smarts in enumerate(reactions):
        try:
            rxn = AllChem.ReactionFromSmarts(rxn_smarts, useSmiles=True)
            if rxn is None:
                continue
            drawer = rdMolDraw2D.MolDraw2DCairo(img_width, img_height)
            drawer.drawOptions().padding = 0.15
            drawer.DrawReaction(rxn)
            drawer.FinishDrawing()
            png_data = drawer.GetDrawingText()
            img = Image.open(io.BytesIO(png_data)).convert("RGBA")
            labeled = Image.new("RGBA", (img_width, img_height + 30), (255, 255, 255, 255))
            labeled.paste(img, (0, 30))
            draw = ImageDraw.Draw(labeled)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except:
                font = ImageFont.load_default()
            draw.text((10, 5), f"Step {i + 1}", fill=(50, 50, 50), font=font)
            reaction_images.append(labeled)
        except Exception as e:
            print(f"Error drawing reaction {i+1}: {e}")
            continue

    if not reaction_images:
        raise ValueError("No valid reactions could be drawn.")

    total_height = sum(img.height for img in reaction_images)
    final_image = Image.new("RGBA", (img_width, total_height), (255, 255, 255, 255))
    y_offset = 0
    for img in reaction_images:
        final_image.paste(img, (0, y_offset))
        y_offset += img.height

    if output_path:
        final_image.convert("RGB").save(output_path)
        return None
    return final_image.convert("RGB")


def generate_reaction_images(results: list, output_dir: str = "pathway_images", img_width: int = 2400, img_height: int = 400):
    """
    Recebe os resultados da previsão e desenha as reações para cada molécula com sucesso.
    """
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)
    
    sucessos = 0
    for entry in results:
        if entry["status"] != "success":
            continue

        name = entry["name"]
        solution = entry["solution"]

        try:
            safe_name = name.replace("/", "_").replace("\\", "_").replace(":", "_")
            file_path = out_path / f"{safe_name}.png"
            _draw_pathway_reactions(
                solution.template, 
                output_path=file_path, 
                img_height=img_height, 
                img_width=img_width
            )
            sucessos += 1
        except Exception as e:
            print(f"Erro ao desenhar {name}: {e}")
            
    print(f"\nDesenho concluído. {sucessos} imagens geradas na pasta '{output_dir}'.")