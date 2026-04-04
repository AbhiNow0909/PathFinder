import json

with open("evaluation/results.json", "r", encoding="utf-8") as f:
    d = json.load(f)

s = d["summary"]

print(f"B1 PVR {s['b1']['pvr']} TBA {s['b1']['tba']} WTC {s['b1']['wtc']} CWTC {s['b1']['constrained_wtc']}")
print(f"B2 PVR {s['b2']['pvr']} TBA {s['b2']['tba']} WTC {s['b2']['wtc']} CWTC {s['b2']['constrained_wtc']}")
print(f"Prop PVR {s['proposed']['pvr']} TBA {s['proposed']['tba']} WTC {s['proposed']['wtc']} CWTC {s['proposed']['constrained_wtc']}")

with open("summary_clean.txt", "w", encoding="utf-8") as f:
    f.write(f"B1 PVR {s['b1']['pvr']} TBA {s['b1']['tba']} WTC {s['b1']['wtc']} CWTC {s['b1']['constrained_wtc']}\n")
    f.write(f"B2 PVR {s['b2']['pvr']} TBA {s['b2']['tba']} WTC {s['b2']['wtc']} CWTC {s['b2']['constrained_wtc']}\n")
    f.write(f"Prop PVR {s['proposed']['pvr']} TBA {s['proposed']['tba']} WTC {s['proposed']['wtc']} CWTC {s['proposed']['constrained_wtc']}\n")
