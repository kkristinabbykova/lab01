// Большая чёрная кнопка-«таблетка», как на прежнем сайте. Каждый щелчок увеличивает count.
function render({ model, el }) {
  const b = document.createElement("button");
  b.className = "pill"; b.type = "button"; b.textContent = model.get("label");
  b.addEventListener("click", () => { model.set("count", model.get("count") + 1); model.save_changes(); });
  el.append(b);
}
export default { render };
