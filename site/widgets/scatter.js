// Точечный график шрифтов для marimo (anywidget): приближение, сдвиг, подсказки, щелчок по точке выбирает шрифт.
function render({ model, el }) {
  const NS = "http://www.w3.org/2000/svg", SW = 640, SH = 390, pad = { l: 58, r: 16, t: 14, b: 50 };
  const P = model.get("points"), CAT = model.get("cats");
  const XL = model.get("xlabel") || "x-height, доли кегля", YL = model.get("ylabel") || "толщина штриха, доли кегля";
  const XN = model.get("xname") || "x-height", YN = model.get("yname") || "штрих", ALWAYS = !!model.get("labels"), PICK = model.get("pickable") !== false;
  const nf = (v, d = 3) => v.toFixed(d).replace(".", ",");
  const mk = (tag, attrs = {}) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };
  const h = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt) e.textContent = txt; return e; };

  const root = h("div", "fsc");
  const bar = h("div", "zoombar");
  const bIn = h("button", "", "+"), bOut = h("button", "", "−"), bAll = h("button", "", "Весь график"), info = h("span", "note");
  bIn.title = "Приблизить"; bOut.title = "Отдалить";
  bar.append(bIn, bOut, bAll, info);
  const box = h("div", "box"), sc = mk("svg", { viewBox: `0 0 ${SW} ${SH}` }), tip = h("div", "tip"), hint = h("div", "hint", "Чтобы приблизить, держите Ctrl (⌘) и крутите колесо");
  box.append(sc, tip, hint);
  const legend = h("div", "legend");
  root.append(bar, box, legend);
  el.append(root);

  const xs = P.map(p => p.x), ys = P.map(p => p.s), xr = Math.max(...xs) - Math.min(...xs) || 1, yr = Math.max(...ys) - Math.min(...ys) || 1;
  const FULL = P.length ? { x: [Math.min(...xs) - xr * .04, Math.max(...xs) + xr * .04],
                            y: [Math.min(0, Math.min(...ys) - yr * .04), Math.max(...ys) + yr * .08] } : { x: [0, 1], y: [0, 1] };
  let V = { x: [...FULL.x], y: [...FULL.y] };
  const X = v => pad.l + (v - V.x[0]) / (V.x[1] - V.x[0]) * (SW - pad.l - pad.r);
  const Y = v => SH - pad.b - (v - V.y[0]) / (V.y[1] - V.y[0]) * (SH - pad.t - pad.b);
  const invX = px => V.x[0] + (px - pad.l) / (SW - pad.l - pad.r) * (V.x[1] - V.x[0]);
  const invY = py => V.y[0] + (SH - pad.b - py) / (SH - pad.t - pad.b) * (V.y[1] - V.y[0]);
  function niceTicks(a, b, n = 5) {
    const raw = (b - a) / n, p = 10 ** Math.floor(Math.log10(raw)), m = raw / p;
    const st = (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * p, out = [];
    for (let t = Math.ceil(a / st) * st; t <= b + 1e-12; t += st) out.push(+t.toFixed(10));
    return [out, Math.max(0, -Math.floor(Math.log10(st) + 1e-9))];
  }
  const zoomK = () => (FULL.x[1] - FULL.x[0]) / (V.x[1] - V.x[0]);
  function clampView() {
    ["x", "y"].forEach(a => { const w = Math.min(V[a][1] - V[a][0], FULL[a][1] - FULL[a][0]);
      const lo = Math.max(FULL[a][0], Math.min(V[a][0], FULL[a][1] - w)); V[a] = [lo, lo + w]; });
  }
  function zoomAt(f, px = (pad.l + SW - pad.r) / 2, py = (pad.t + SH - pad.b) / 2) {
    const cx = invX(px), cy = invY(py), minW = (FULL.x[1] - FULL.x[0]) / 40, minH = (FULL.y[1] - FULL.y[0]) / 40;
    const w = Math.max(minW, (V.x[1] - V.x[0]) / f), hh = Math.max(minH, (V.y[1] - V.y[0]) / f);
    const fx = (cx - V.x[0]) / (V.x[1] - V.x[0]), fy = (cy - V.y[0]) / (V.y[1] - V.y[0]);
    V = { x: [cx - fx * w, cx - fx * w + w], y: [cy - fy * hh, cy - fy * hh + hh] }; clampView(); draw();
  }
  function focusOn(name) {
    const p = P.find(q => q.f === name); if (!p) return;
    const w = (FULL.x[1] - FULL.x[0]) / 4, hh = (FULL.y[1] - FULL.y[0]) / 4;
    V = { x: [p.x - w / 2, p.x + w / 2], y: [p.s - hh / 2, p.s + hh / 2] }; clampView();
  }
  function axes() {
    const [xt, xd] = niceTicks(V.x[0], V.x[1]), [yt, yd] = niceTicks(V.y[0], V.y[1]);
    xt.filter(t => t > V.x[0] && t < V.x[1]).forEach(t => {
      sc.append(mk("line", { x1: X(t), x2: X(t), y1: pad.t, y2: SH - pad.b, stroke: "#e6e5e0" }));
      const tx = mk("text", { x: X(t), y: SH - pad.b + 18, "text-anchor": "middle", "font-size": 12, fill: "#5c6170" }); tx.textContent = nf(t, Math.max(2, xd)); sc.append(tx); });
    yt.filter(t => t >= V.y[0] && t < V.y[1]).forEach(t => {
      sc.append(mk("line", { x1: pad.l, x2: SW - pad.r, y1: Y(t), y2: Y(t), stroke: "#e6e5e0" }));
      const ty = mk("text", { x: pad.l - 8, y: Y(t) + 4, "text-anchor": "end", "font-size": 12, fill: "#5c6170" }); ty.textContent = nf(t, Math.max(2, yd)); sc.append(ty); });
    sc.append(mk("line", { x1: pad.l, x2: SW - pad.r, y1: SH - pad.b, y2: SH - pad.b, stroke: "#5c6170" }));
    const lx = mk("text", { x: (pad.l + SW - pad.r) / 2, y: SH - 8, "text-anchor": "middle", "font-size": 13, fill: "#1a1d24" }); lx.textContent = XL; sc.append(lx);
    const cy = (pad.t + SH - pad.b) / 2;
    const ly = mk("text", { x: 15, y: cy, "text-anchor": "middle", "font-size": 13, fill: "#1a1d24", transform: `rotate(-90 15 ${cy})` }); ly.textContent = YL; sc.append(ly);
  }
  function draw() {
    sc.replaceChildren(); tip.style.opacity = 0; axes();
    const defs = mk("defs"), cp = mk("clipPath", { id: "fscClip" });
    cp.append(mk("rect", { x: pad.l, y: pad.t, width: SW - pad.l - pad.r, height: SH - pad.t - pad.b })); defs.append(cp); sc.append(defs);
    const g = mk("g", { "clip-path": "url(#fscClip)" }); sc.append(g);
    const k = zoomK(), r = Math.min(10, 6 * Math.sqrt(Math.sqrt(k))), sel = model.get("selected");
    const vis = P.filter(p => p.x >= V.x[0] && p.x <= V.x[1] && p.s >= V.y[0] && p.s <= V.y[1]);
    vis.forEach(p => {
      const on = p.f === sel;
      const c = mk("circle", { cx: X(p.x), cy: Y(p.s), r: on ? r + 3 : r, fill: (CAT[p.c] || ["", "#999"])[1], "fill-opacity": .88,
        stroke: on ? "#1a1d24" : "#fff", "stroke-width": on ? 2.5 : 1.2, tabindex: 0, style: PICK ? "cursor:pointer" : "" });
      const show = () => { tip.textContent = `${p.f}: ${XN} ${nf(p.x)}, ${YN} ${nf(p.s)}` + (PICK ? " · нажмите, чтобы открыть" : "");
        const b = sc.getBoundingClientRect(), kk = b.width / SW;
        tip.style.left = `${X(p.x) * kk + 12}px`; tip.style.top = `${Y(p.s) * kk - 12}px`; tip.style.opacity = 1; };
      const hide = () => { tip.style.opacity = 0; };
      const pick = e => { if (!PICK) return; e.stopPropagation(); model.set("selected", p.f); model.save_changes(); draw(); };
      c.addEventListener("mouseenter", show); c.addEventListener("focus", show);
      c.addEventListener("mouseleave", hide); c.addEventListener("blur", hide);
      c.addEventListener("click", pick); c.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") pick(e); });
      c.addEventListener("pointerdown", e => e.stopPropagation());
      g.append(c);
    });
    const boxes = [];
    const labelled = (ALWAYS || (k > 1.5 && vis.length <= 30)) ? [...vis] : vis.filter(p => p.f === sel);
    labelled.sort((a, b) => (b.f === sel) - (a.f === sel) || b.s - a.s).forEach(p => {
      const t = mk("text", { x: X(p.x) + r + 4, y: Y(p.s) + 4, "font-size": p.f === sel ? 13 : 11, "font-weight": p.f === sel ? 650 : 400,
        fill: "#1a1d24", "pointer-events": "none", stroke: "#fff", "stroke-width": 3, "paint-order": "stroke" });
      t.textContent = p.f; g.append(t);
      const bb = t.getBBox(), hit = boxes.some(o => bb.x < o.x + o.width + 2 && o.x < bb.x + bb.width + 2 && bb.y < o.y + o.height && o.y < bb.y + bb.height);
      if (p.f !== sel && (hit || bb.x + bb.width > SW - pad.r)) t.remove(); else boxes.push(bb);
    });
    info.textContent = k > 1.02 ? `×${nf(k, 1)} · видно точек: ${vis.length} из ${P.length}` : `весь график · ${P.length} точек`;
    sc.style.cursor = k > 1.02 ? "grab" : "zoom-in";
    sc.style.touchAction = k > 1.02 ? "none" : "pan-y";
  }
  const svgPt = e => { const b = sc.getBoundingClientRect(); return [(e.clientX - b.left) * SW / b.width, (e.clientY - b.top) * SW / b.width]; };
  let hintT;
  sc.addEventListener("wheel", e => {
    if (!(e.ctrlKey || e.metaKey)) { hint.style.opacity = 1; clearTimeout(hintT); hintT = setTimeout(() => hint.style.opacity = 0, 1200); return; }
    e.preventDefault(); const [x, y] = svgPt(e); zoomAt(Math.exp(-e.deltaY * 0.002), x, y);
  }, { passive: false });
  sc.addEventListener("dblclick", e => { const [x, y] = svgPt(e); zoomAt(e.shiftKey ? 1 / 2 : 2, x, y); });
  const ptrs = new Map(); let pinch0 = null;
  sc.addEventListener("pointerdown", e => { ptrs.set(e.pointerId, svgPt(e));
    if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; pinch0 = Math.hypot(a[0] - b[0], a[1] - b[1]); }
    if (zoomK() > 1.02 || ptrs.size === 2) { sc.setPointerCapture(e.pointerId); sc.style.cursor = "grabbing"; } });
  sc.addEventListener("pointermove", e => {
    if (!ptrs.has(e.pointerId)) return; const prev = ptrs.get(e.pointerId), cur = svgPt(e); ptrs.set(e.pointerId, cur);
    if (ptrs.size === 2 && pinch0) { const [a, b] = [...ptrs.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]);
      zoomAt(d / pinch0, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2); pinch0 = d; return; }
    if (zoomK() <= 1.02) return;
    const dx = invX(prev[0]) - invX(cur[0]), dy = invY(prev[1]) - invY(cur[1]);
    V.x = V.x.map(v => v + dx); V.y = V.y.map(v => v + dy); clampView(); draw();
  });
  const up = e => { ptrs.delete(e.pointerId); if (ptrs.size < 2) pinch0 = null; sc.style.cursor = zoomK() > 1.02 ? "grab" : "zoom-in"; };
  sc.addEventListener("pointerup", up); sc.addEventListener("pointercancel", up);
  const med = a => { const b = [...a].sort((u, v) => u - v); return b[b.length >> 1]; };
  const MX = med(P.map(p => p.x)), MY = med(P.map(p => p.s));
  bIn.addEventListener("click", () => zoomK() > 1.02 ? zoomAt(1.6) : zoomAt(1.6, X(MX), Y(MY)));
  bOut.addEventListener("click", () => zoomAt(1 / 1.6));
  bAll.addEventListener("click", () => { V = { x: [...FULL.x], y: [...FULL.y] }; draw(); });
  const present = [...new Set(P.map(p => p.c))];
  legend.innerHTML = Object.entries(CAT).filter(([k]) => present.includes(k))
    .map(([k, [name, col]]) => `<span><i class="sw" style="background:${col}"></i>${name} (${P.filter(p => p.c === k).length})</span>`).join("");
  if (model.get("selected")) focusOn(model.get("selected"));
  model.on("change:selected", () => draw());
  draw();
}
export default { render };
