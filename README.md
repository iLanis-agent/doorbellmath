# Doorbell math

How many days a battery doorbell really runs between charges, whether the old transformer in the wall has headroom for a video bell, and what charging versus wiring costs in a year. Exact arithmetic in the browser, every borrowed number labeled - the headroom verdict is a planning estimate, not an electrical ruling.

Live site: https://ilanis-agent.github.io/doorbellmath/

## The three tools

- **Battery plan** - `batteryPlan(capMah, usablePct, ringsDay, activeMa, activeSec, standbyMa)`: days between charges and charges per year.
- **Transformer plan** - `transformerPlan(va, bellVa, chimeVa)`: total draw, headroom percent and a labeled margin verdict.
- **Power plan** - `powerPlan(capMah, volts, chargesYear, watts, priceCents)`: charging cost versus wired cost per year.

## Labeled norms (illustrative references, not specs)

- Pack: 6000 mAh at 80% usable. Ring: 300 mA for 20 seconds, 8 a day, 2.5 mA standby. Transformer: 10 VA. Grid price: 15 cents a kWh. The bell maker's rating and a qualified electrician decide what is safe to wire.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (12 cases, 57 checks)

Regenerate the oracle expectations: `python3 oracle.py`
