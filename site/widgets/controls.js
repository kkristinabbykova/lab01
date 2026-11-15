// Панель элементов управления в стиле прежнего сайта про шрифты: «таблетки», круглые списки, ползунки с подписью.
// spec: [{type: "seg"|"select"|"range"|"text"|"button"|"reset", name, label, ...}], значения в model.values.
function render({ model, el }) {
  const spec = model.get("spec");
  const init = JSON.parse(JSON.stringify(model.get("values")));
  let vals = JSON.parse(JSON.stringify(init));
  const nf = (v, d) => Number(v).toFixed(d).replace(".", ",").replace("-", "−");
  const decs = st => { const s = String(st); return s.includes(".") ? s.split(".")[1].length : 0; };
  let timer = null;
  const push = (now) => {
    clearTimeout(timer);
    const send = () => { model.set("values", JSON.parse(JSON.stringify(vals))); model.save_changes(); };
    if (now) send(); else timer = setTimeout(send, 90);
  };
  const root = document.createElement("div");
  root.className = "fctl";
  const refreshers = {};
  for (const c of spec) {
    const lab = document.createElement("label");
    if (c.wide) lab.classList.add("wide");
    if (c.grow) lab.style.flex = `${c.grow} 1 0`;
    const cap = document.createElement("span");
    cap.className = "cap";
    if (c.type === "seg") {
      cap.textContent = c.label || ""; lab.append(cap);
      const seg = document.createElement("span"); seg.className = "seg"; seg.setAttribute("role", "radiogroup");
      const btns = c.options.map(([text, v]) => {
        const b = document.createElement("button"); b.type = "button"; b.textContent = text; b.setAttribute("role", "radio");
        b.addEventListener("click", () => {
          if (c.sets) { vals[c.sets] = v; (refreshers[c.sets] || (() => {}))(); }
          else vals[c.name] = v;
          sync(); push(true);
        });
        seg.append(b); return [b, v];
      });
      const sync = () => btns.forEach(([b, v]) => {
        const on = c.sets ? Math.abs(Number(vals[c.sets]) - Number(v)) < 1e-9 : vals[c.name] === v;
        b.setAttribute("aria-checked", on);
      });
      refreshers[c.name] = sync;
      if (c.sets) { const prev = refreshers[c.sets]; refreshers["__after_" + c.sets] = sync; }
      sync(); lab.append(seg);
    } else if (c.type === "chips") {
      cap.textContent = c.label || ""; lab.append(cap);
      const box = document.createElement("span"); box.className = "chips";
      const btns = c.options.map(([text, v, color]) => {
        const b = document.createElement("button"); b.type = "button";
        if (color) { const dot = document.createElement("i"); dot.style.background = color; b.append(dot); }
        b.append(document.createTextNode(text));
        b.addEventListener("click", () => {
          const cur = new Set(vals[c.name] || []);
          if (cur.has(v)) cur.delete(v); else cur.add(v);
          vals[c.name] = c.options.map(o => o[1]).filter(x => cur.has(x));
          sync(); push(true);
        });
        box.append(b); return [b, v];
      });
      const sync = () => btns.forEach(([b, v]) => b.setAttribute("aria-pressed", (vals[c.name] || []).includes(v)));
      refreshers[c.name] = sync; sync(); lab.append(box);
    } else if (c.type === "select") {
      cap.textContent = c.label || ""; lab.append(cap);
      const sel = document.createElement("select"); sel.className = "fancy";
      const add = (parent, [text, v]) => { const o = document.createElement("option"); o.value = JSON.stringify(v); o.textContent = text; parent.append(o); };
      if (c.groups) for (const [g, opts] of c.groups) { const og = document.createElement("optgroup"); og.label = g; opts.forEach(o => add(og, o)); sel.append(og); }
      else c.options.forEach(o => add(sel, o));
      sel.value = JSON.stringify(vals[c.name]);
      sel.addEventListener("change", () => { vals[c.name] = JSON.parse(sel.value); push(true); });
      refreshers[c.name] = () => { sel.value = JSON.stringify(vals[c.name]); };
      lab.append(sel);
    } else if (c.type === "range") {
      const d = c.decimals ?? decs(c.step ?? 1);
      const out = document.createElement("output"); out.className = "val";
      const unit = c.unit ? ` ${c.unit}` : "";
      cap.append(document.createTextNode(`${c.label}: `), out, document.createTextNode(unit));
      const inp = document.createElement("input"); inp.type = "range";
      inp.min = c.min; inp.max = c.max; inp.step = c.step ?? 1; inp.value = vals[c.name];
      const show = () => { out.textContent = c.thousands ? Number(inp.value).toLocaleString("ru-RU") : nf(inp.value, d); };
      inp.addEventListener("input", () => { show(); vals[c.name] = Number(inp.value);
        (refreshers["__after_" + c.name] || (() => {}))(); if (c.live) push(false); });
      inp.addEventListener("change", () => { vals[c.name] = Number(inp.value); push(true); });
      refreshers[c.name] = () => { inp.value = vals[c.name]; show(); (refreshers["__after_" + c.name] || (() => {}))(); };
      show(); lab.append(cap, inp);
    } else if (c.type === "text") {
      cap.textContent = c.label || ""; lab.append(cap);
      const inp = document.createElement("input"); inp.type = "text"; inp.value = vals[c.name] ?? "";
      if (c.maxlength) inp.maxLength = c.maxlength;
      if (c.placeholder) inp.placeholder = c.placeholder;
      inp.addEventListener("input", () => { vals[c.name] = inp.value; push(false); });
      refreshers[c.name] = () => { inp.value = vals[c.name]; };
      lab.append(inp);
    } else if (c.type === "button" || c.type === "reset") {
      lab.classList.add("btn");
      const b = document.createElement("button"); b.type = "button"; b.className = "pill"; b.textContent = c.label;
      b.addEventListener("click", () => {
        if (c.type === "reset") { const keep = vals; vals = JSON.parse(JSON.stringify(init));
          for (const k in keep) if (!(k in vals)) vals[k] = keep[k];
          spec.filter(x => x.type === "button").forEach(x => { vals[x.name] = keep[x.name]; });
          Object.keys(refreshers).filter(k => !k.startsWith("__")).forEach(k => refreshers[k]()); }
        else vals[c.name] = (vals[c.name] || 0) + 1;
        push(true);
      });
      lab.append(b);
    }
    root.append(lab);
  }
  el.append(root);
}
export default { render };
