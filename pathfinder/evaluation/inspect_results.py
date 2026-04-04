import json

with open("evaluation/results.json", "r", encoding="utf-8") as f:
    d = json.load(f)

print("=== PROPOSED SYSTEM PVR VIOLATIONS ===")
for p in d["per_profile"]:
    if p["proposed"]["pvr_violated"]:
        print(f"\n{p['id']} ({p['category']}) budget={p['time_budget']}h")
        print(f"  Weak GT: {p['weak_topics_gt']}")
        print(f"  Roadmap: {p['proposed']['roadmap_topics']}")
        print(f"  TotalTime={p['proposed']['total_time']}")

print("\n=== B1 PVR VIOLATIONS ===")
for p in d["per_profile"]:
    if p["b1"]["pvr_violated"]:
        print(f"\n{p['id']} B1 roadmap: {p['b1']['roadmap_topics']}")
