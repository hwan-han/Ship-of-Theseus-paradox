import csv
from pathlib import Path
from ship import Ship
from metrics import form_score, material_score, continuity_score, identity_score

def run_simulation(steps=50, k=2, out_csv="data/experiment_log.csv", alpha=0.4, beta=0.3, gamma=0.3):
    ship = Ship(n_parts=100, core_part_ids=set(range(0,5)))
    with open(out_csv, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["step","replaced_ratio","form","material","continuity","identity"])        
        for t in range(steps):
            ship.replace_parts(k=k, strategy="random")
            replaced_ratio = 1.0 - (sum(ship.original_flags)/ship.n_parts)
            form = form_score(structure_unchanged=True)
            material = material_score(ship.original_flags, core_ids=ship.core_part_ids)
            cont = continuity_score(ship.history["discontinuities"])
            ident = identity_score(form, material, cont, alpha, beta, gamma)
            wr.writerow([t+1, round(replaced_ratio,4), round(form,4), round(material,4), round(cont,4), round(ident,4)])
    return out_csv

if __name__ == "__main__":
    Path("data").mkdir(exist_ok=True, parents=True)
    csv_path = run_simulation()
    print(f"Wrote {csv_path}")
