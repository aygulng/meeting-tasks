export async function api(path, options) {
  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok)
    throw Error(
      typeof data.detail === "string"
        ? data.detail
        : "Проверьте заполнение полей.",
    );
  return data;
}
