import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(n) + " " + (word if n == 1 else (form or word + "s"))
def money(c): return "$" + str(c // 100) + "." + str(c % 100).zfill(2)
def fmt(x): return str(jsnum(x))

def battery_plan(capMah, usablePct, ringsDay, activeMa, activeSec, standbyMa):
    if not (capMah > 0) or not (usablePct > 0) or not (ringsDay > 0) or not (activeMa > 0) or not (activeSec > 0) or not (standbyMa > 0):
        return {"error": "capacity, usable, rings, current, seconds and standby must be positive"}
    daily = standbyMa * 24 + ringsDay * activeSec * activeMa / 3600
    days = math.floor(capMah * usablePct / 100 / daily)
    return {"days": days, "charges": math.ceil(365 / days)}

def transformer_plan(va, bellVa, chimeVa):
    if not (va > 0) or not (bellVa > 0) or not (chimeVa > 0):
        return {"error": "transformer, bell and chime must be positive"}
    load = bellVa + chimeVa
    headroom = math.floor((va - load) / va * 100 + 0.5)
    verdict = "comfortable" if headroom >= 30 else ("tight" if headroom >= 10 else "undersized")
    return {"load": load, "headroom": headroom, "verdict": verdict}

def power_plan(capMah, volts, chargesYear, watts, priceCents):
    if not (capMah > 0) or not (volts > 0) or not (chargesYear > 0) or not (watts > 0) or not (priceCents > 0):
        return {"error": "capacity, volts, charges, watts and price must be positive"}
    battery_cents = math.floor(capMah * volts / 1000000 * chargesYear * priceCents + 0.5)
    wired_kwh = watts * 8760 / 1000
    return {"batteryCents": battery_cents, "wiredKwh": jsnum(wired_kwh), "wiredCents": math.floor(wired_kwh * priceCents + 0.5)}

def render_battery(r, capMah, usablePct, ringsDay, activeMa, activeSec, standbyMa):
    return ("A labeled " + fmt(capMah) + " mAh pack at " + fmt(usablePct) + "% usable, "
            + plural(ringsDay, "ring") + " a day at " + fmt(activeMa) + " mA for " + plural(activeSec, "second")
            + " each and a " + fmt(standbyMa) + " mA standby draw, lasts about " + plural(r["days"], "day")
            + " - " + plural(r["charges"], "charge") + " a year.")

def render_transformer(r, va, bellVa, chimeVa):
    phrase = "a comfortable margin" if r["verdict"] == "comfortable" else ("a tight margin" if r["verdict"] == "tight" else "undersized for the load")
    return ("A transformer rated " + fmt(va) + " VA, a bell drawing " + fmt(bellVa) + " VA and a chime drawing "
            + fmt(chimeVa) + " VA: total " + fmt(r["load"]) + " VA, headroom " + fmt(r["headroom"]) + "% - " + phrase + ".")

def render_power(r, capMah, volts, chargesYear, watts, priceCents):
    return ("Charging the pack costs about " + money(r["batteryCents"]) + " a year at " + fmt(priceCents)
            + " cents a kWh; a wired bell sipping " + fmt(watts) + " W uses " + fmt(r["wiredKwh"]) + " kWh, about "
            + money(r["wiredCents"]) + " a year.")

cases = []
for a in [(6000, 80, 8, 300, 20, 2.5), (4000, 85, 12, 250, 30, 3), (8000, 75, 4, 350, 15, 1.5), (0, 80, 8, 300, 20, 2.5)]:
    r = battery_plan(*a)
    cases.append({"fn": "batteryPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_battery(r, *a)})
for a in [(10, 5, 3), (16, 6, 4), (8, 5, 4), (0, 5, 3)]:
    r = transformer_plan(*a)
    cases.append({"fn": "transformerPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_transformer(r, *a)})
for a in [(6000, 5, 6, 2, 15), (4000, 3.7, 11, 3, 22), (8000, 5, 3, 1.5, 10), (6000, 5, 0, 2, 15)]:
    r = power_plan(*a)
    cases.append({"fn": "powerPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_power(r, *a)})

with open("expected.json", "w") as f:
    f.write(json.dumps(cases, separators=(",", ":")) + "\n")
print("wrote", len(cases), "cases")
