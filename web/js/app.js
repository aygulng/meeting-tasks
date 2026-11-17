import { api } from "./api.js";
import { $, renderResult } from "./ui.js";
let latest;
async function loadModels() {
  $("run").disabled = true;
  $("status").textContent = "Проверяем Ollama…";
  try {
    const data = await api("/api/models");
    $("model").replaceChildren(
      ...data.models.map((name) => new Option(name, name)),
    );
    $("run").disabled = !data.models.length;
    $("status").textContent = data.models.length
      ? "Ollama готова. Выберите модель."
      : "Локальных моделей нет. Выполните в терминале: ollama pull qwen3:4b";
  } catch (e) {
    $("status").textContent = e.message;
  }
}
$("refresh").onclick = loadModels;
$("sample").onclick = () => {
  $("notes").value =
    "Анна: Я подготовлю презентацию к пятнице.\nИгорь: Беру на себя проверку расчётов, закончу завтра.\nНужно обновить инструкцию для клиентов, ответственного пока не назначили.\nОбсудили новую цветовую схему, решение отложили.";
};
$("run").onclick = async () => {
  if (!$("notes").value.trim()) {
    $("status").textContent = "Добавьте текст встречи.";
    return;
  }
  $("output").hidden = true;
  for (const id of ["run", "refresh", "model", "sample", "notes"])
    $(id).disabled = true;
  $("status").textContent =
    "Модель разбирает заметки. Первый запуск может занять несколько минут…";
  try {
    latest = await api("/api/extract", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: $("notes").value,
        model: $("model").value,
      }),
    });
    renderResult(latest);
    $("status").textContent = "Готово.";
  } catch (e) {
    $("status").textContent = e.message;
  } finally {
    for (const id of ["run", "refresh", "model", "sample", "notes"])
      $(id).disabled = false;
  }
};
$("download").onclick = () => {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(latest, null, 2)], {
      type: "application/json",
    }),
  );
  const a = document.createElement("a");
  a.href = url;
  a.download = "meeting-tasks.json";
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
loadModels();
