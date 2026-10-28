import argparse
import csv
import json

from .score import rank_companies


def main():
    ap = argparse.ArgumentParser(description="Rank companies by hiring signal from job postings.")
    ap.add_argument("--input", default="sample_data/postings.json")
    ap.add_argument("--target-tools", default="Clay,HubSpot,Salesforce,Apollo,n8n",
                    help="comma-separated tools your offer plugs into")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--out", help="write the full ranking to this CSV")
    a = ap.parse_args()

    postings = json.load(open(a.input))
    rows = rank_companies(postings, [t.strip() for t in a.target_tools.split(",") if t.strip()])
    print(f"{len(postings)} postings -> {len(rows)} companies\n")
    for r in rows[: a.top]:
        print(f"{r['score']:>3}  {r['company'][:28]:28}  {r['open_roles']} role(s)  {r['tools'][:60]}")
    if a.out:
        with open(a.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"\nwrote {len(rows)} rows to {a.out}")


if __name__ == "__main__":
    main()
