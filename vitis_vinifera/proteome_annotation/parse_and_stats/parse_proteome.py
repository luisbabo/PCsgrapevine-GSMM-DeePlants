import csv
import sys

def parse_and_export_csv(input_csv, output_csv):
    levels = ["EC1", "EC2", "EC3", "EC4"]
    fieldnames = ["id", "EC1", "prob_EC1", "EC2", "prob_EC2", "EC3", "prob_EC3", "EC4", "prob_EC4"]

    with open(input_csv, 'r', encoding='utf-8') as fin, \
         open(output_csv, 'w', newline='', encoding='utf-8') as fout:
        
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            out_row = {"id": row.get("id", "").strip()}
            
            for level in levels:
                cell = row.get(level, "").strip()
                ecs = []
                probs = []
                
                if cell:
                    for entry in cell.split(";"):
                        if ":" in entry:
                            ec, prob = entry.split(":", 1)
                            ecs.append(ec.strip())
                            probs.append(prob.strip())
                
                out_row[level] = "|".join(ecs)
                out_row[f"prob_{level}"] = "|".join(probs)
                
            writer.writerow(out_row)

def main():
    if len(sys.argv) == 3:
        parse_and_export_csv(sys.argv[1], sys.argv[2])
    else:
        sys.exit("Uso: python parse_proteome.py <input.csv> <output.csv>")

if __name__ == "__main__":
    main()