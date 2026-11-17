export const $ = (id) => document.getElementById(id);

export function renderResult(latest) {
  $("tasks").replaceChildren();
  for (const task of latest.result.tasks) {
    const card = document.createElement("div");
    card.className = "task";
    for (const [tag, text] of [
      ["h3", task.task],
      [
        "p",
        `Ответственный: ${task.owner ?? "не указан"} · Срок: ${task.deadline ?? "не указан"}`,
      ],
      ["blockquote", task.evidence],
    ]) {
      const el = document.createElement(tag);
      el.textContent = text;
      card.append(el);
    }
    $("tasks").append(card);
  }
  if (!latest.result.tasks.length)
    $("tasks").textContent = "Явных задач в заметках не найдено.";
  $("stats").textContent =
    `${latest.model} · ${latest.seconds} с · ${latest.tokens_per_second ?? "—"} токенов/с · попыток: ${latest.attempts}`;
  $("json").textContent = JSON.stringify(latest, null, 2);
  $("output").hidden = false;
}
