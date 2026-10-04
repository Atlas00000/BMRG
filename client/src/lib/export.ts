/** Shared export helpers — P10 */
export function downloadText(filename: string, content: string, mime = 'text/plain') {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function downloadJson(filename: string, data: unknown) {
  downloadText(filename, JSON.stringify(data, null, 2), 'application/json');
}

export function downloadCsv(
  filename: string,
  rows: Record<string, string | number | null | undefined>[],
) {
  if (!rows.length) {
    downloadText(filename, '', 'text/csv');
    return;
  }
  const keys = Object.keys(rows[0]!);
  const esc = (v: unknown) => {
    const s = v == null ? '' : String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const lines = [keys.join(','), ...rows.map((r) => keys.map((k) => esc(r[k])).join(','))];
  downloadText(filename, lines.join('\n'), 'text/csv');
}
