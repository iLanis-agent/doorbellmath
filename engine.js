(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function money(c) { return "$" + Math.floor(c / 100) + "." + ("0" + (c % 100)).slice(-2); }

  function batteryPlan(capMah, usablePct, ringsDay, activeMa, activeSec, standbyMa) {
    if (!(capMah > 0) || !(usablePct > 0) || !(ringsDay > 0) || !(activeMa > 0) || !(activeSec > 0) || !(standbyMa > 0)) return { error: "capacity, usable, rings, current, seconds and standby must be positive" };
    var daily = standbyMa * 24 + ringsDay * activeSec * activeMa / 3600;
    var days = Math.floor(capMah * usablePct / 100 / daily);
    var charges = Math.ceil(365 / days);
    return { days: days, charges: charges };
  }

  function transformerPlan(va, bellVa, chimeVa) {
    if (!(va > 0) || !(bellVa > 0) || !(chimeVa > 0)) return { error: "transformer, bell and chime must be positive" };
    var load = bellVa + chimeVa;
    var headroom = Math.round((va - load) / va * 100);
    var verdict = headroom >= 30 ? "comfortable" : (headroom >= 10 ? "tight" : "undersized");
    return { load: load, headroom: headroom, verdict: verdict };
  }

  function powerPlan(capMah, volts, chargesYear, watts, priceCents) {
    if (!(capMah > 0) || !(volts > 0) || !(chargesYear > 0) || !(watts > 0) || !(priceCents > 0)) return { error: "capacity, volts, charges, watts and price must be positive" };
    var batteryCents = Math.round(capMah * volts / 1000000 * chargesYear * priceCents);
    var wiredKwh = watts * 8760 / 1000;
    var wiredCents = Math.round(wiredKwh * priceCents);
    return { batteryCents: batteryCents, wiredKwh: wiredKwh, wiredCents: wiredCents };
  }

  function renderBattery(r, capMah, usablePct, ringsDay, activeMa, activeSec, standbyMa) {
    return "A labeled " + capMah + " mAh pack at " + usablePct + "% usable, " + plural(ringsDay, "ring") + " a day at " + activeMa + " mA for " + plural(activeSec, "second") + " each and a " + standbyMa + " mA standby draw, lasts about " + plural(r.days, "day") + " - " + plural(r.charges, "charge") + " a year.";
  }

  function renderTransformer(r, va, bellVa, chimeVa) {
    var phrase = r.verdict === "comfortable" ? "a comfortable margin" : (r.verdict === "tight" ? "a tight margin" : "undersized for the load");
    return "A transformer rated " + va + " VA, a bell drawing " + bellVa + " VA and a chime drawing " + chimeVa + " VA: total " + r.load + " VA, headroom " + r.headroom + "% - " + phrase + ".";
  }

  function renderPower(r, capMah, volts, chargesYear, watts, priceCents) {
    return "Charging the pack costs about " + money(r.batteryCents) + " a year at " + priceCents + " cents a kWh; a wired bell sipping " + watts + " W uses " + r.wiredKwh + " kWh, about " + money(r.wiredCents) + " a year.";
  }

  var api = { batteryPlan: batteryPlan, transformerPlan: transformerPlan, powerPlan: powerPlan, renderBattery: renderBattery, renderTransformer: renderTransformer, renderPower: renderPower };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.DoorbellMath = api;
})(this);
