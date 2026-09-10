(() => {
  "use strict";

  const empty = document.getElementById("insights-empty");
  const results = document.getElementById("insights-results");
  const unavailable = document.getElementById("insights-unavailable");
  const $ = id => document.getElementById(id);
  const charts = {};

  function getColors() {
    const dark = document.documentElement.dataset.theme === "dark";
    return dark ? {
      primary: "#60A5FA",
      primarySoft: "rgba(96,165,250,.20)",
      success: "#34D399",
      successSoft: "rgba(52,211,153,.20)",
      warning: "#FBBF24",
      warningSoft: "rgba(251,191,36,.20)",
      border: "#334155",
      muted: "#A8B6CA",
      surface: "#111827",
      remaining: "#263449"
    } : {
      primary: "#2563EB",
      primarySoft: "rgba(37,99,235,.18)",
      success: "#059669",
      successSoft: "rgba(5,150,105,.18)",
      warning: "#F59E0B",
      warningSoft: "rgba(245,158,11,.18)",
      border: "#E2E8F0",
      muted: "#64748B",
      surface: "#FFFFFF",
      remaining: "#E2E8F0"
    };
  }

  function destroy(key) {
    if (charts[key]) charts[key].destroy();
    charts[key] = null;
  }

  function baseOptions(colors) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: colors.muted } } }
    };
  }

  function renderMissing(payload) {
    destroy("missing");
    const canvas = $("chart-missing-bar");
    if (!canvas || typeof Chart === "undefined") return;
    const colors = getColors();

    const rows = (payload.missingByColumn || [])
      .map(item => ({ name: String(item.column ?? "Unnamed"), missing: Number(item.missing || 0) }))
      .sort((a, b) => b.missing - a.missing)
      .slice(0, 8);

    charts.missing = new Chart(canvas, {
      type: "bar",
      data: {
        labels: rows.map(item => item.name.length > 16 ? `${item.name.slice(0, 15)}…` : item.name),
        datasets: [{
          data: rows.map(item => item.missing),
          backgroundColor: colors.primarySoft,
          borderColor: colors.primary,
          borderWidth: 1.5,
          borderRadius: 6
        }]
      },
      options: {
        ...baseOptions(colors),
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => ` ${c.parsed.y} missing` } } },
        scales: {
          x: { ticks: { color: colors.muted }, grid: { display: false } },
          y: { beginAtZero: true, ticks: { color: colors.muted, precision: 0 }, grid: { color: colors.border } }
        }
      }
    });
  }

  function renderTypes(payload) {
    destroy("types");
    const canvas = $("chart-type-pie");
    if (!canvas || typeof Chart === "undefined") return;
    const colors = getColors();
    const counts = payload.columnTypeCounts || { numeric: 0, text: 0, date: 0 };

    charts.types = new Chart(canvas, {
      type: "doughnut",
      data: { labels: ["Numeric", "Text", "Date"], datasets: [{ data: [Number(counts.numeric || 0), Number(counts.text || 0), Number(counts.date || 0)], backgroundColor: [colors.primary, "#94A3B8", colors.success], borderWidth: 0 }] },
      options: { ...baseOptions(colors), cutout: "66%", plugins: { legend: { position: "bottom", labels: { color: colors.muted, boxWidth: 10, usePointStyle: true } } } }
    });
  }

  function renderCompleteness(payload) {
    destroy("completeness");
    const canvas = $("chart-completeness");
    if (!canvas || typeof Chart === "undefined") return;
    const colors = getColors();
    const rows = Number(payload.stats?.rows || 0);
    const columns = Number(payload.stats?.columns || 0);
    const total = rows * columns;
    const missing = Math.min(total, Number(payload.stats?.missing || 0));
    const complete = Math.max(0, total - missing);

    charts.completeness = new Chart(canvas, {
      type: "doughnut",
      data: { labels: ["Complete", "Missing"], datasets: [{ data: [complete, missing], backgroundColor: [colors.success, colors.remaining], borderWidth: 0 }] },
      options: { ...baseOptions(colors), cutout: "68%", plugins: { legend: { position: "bottom", labels: { color: colors.muted, boxWidth: 10, usePointStyle: true } } } }
    });
  }

  function renderMissingShare(payload) {
    destroy("missingShare");
    const canvas = $("chart-missing-share");
    if (!canvas || typeof Chart === "undefined") return;
    const colors = getColors();
    const rows = (payload.missingByColumn || [])
      .map(item => ({ name: String(item.column ?? "Unnamed"), missing: Number(item.missing || 0) }))
      .filter(item => item.missing > 0)
      .sort((a, b) => b.missing - a.missing)
      .slice(0, 6);

    charts.missingShare = new Chart(canvas, {
      type: "polarArea",
      data: { labels: rows.length ? rows.map(item => item.name.length > 14 ? `${item.name.slice(0, 13)}…` : item.name) : ["No missing values"], datasets: [{ data: rows.length ? rows.map(item => item.missing) : [1], backgroundColor: ["rgba(37,99,235,.72)", "rgba(5,150,105,.72)", "rgba(245,158,11,.72)", "rgba(99,102,241,.72)", "rgba(14,165,233,.72)", "rgba(148,163,184,.72)"], borderWidth: 0 }] },
      options: { ...baseOptions(colors), scales: { r: { ticks: { display: false }, grid: { color: colors.border } } }, plugins: { legend: { position: "bottom", labels: { color: colors.muted, boxWidth: 10, usePointStyle: true } } } }
    });
  }

  function renderDuplicateShare(payload) {
    destroy("duplicateShare");
    const canvas = $("chart-duplicate-share");
    if (!canvas || typeof Chart === "undefined") return;
    const colors = getColors();
    const rows = Number(payload.stats?.rows || 0);
    const duplicates = Math.min(rows, Number(payload.stats?.duplicates || 0));
    const unique = Math.max(0, rows - duplicates);

    charts.duplicateShare = new Chart(canvas, {
      type: "pie",
      data: { labels: ["Unique", "Duplicate"], datasets: [{ data: [unique, duplicates], backgroundColor: [colors.primary, colors.warning], borderWidth: 0 }] },
      options: { ...baseOptions(colors), plugins: { legend: { position: "bottom", labels: { color: colors.muted, boxWidth: 10, usePointStyle: true } } } }
    });
  }

  function renderQualityScore(payload) {
    destroy("quality");
    const canvas = $("chart-quality-score");
    if (!canvas || typeof Chart === "undefined") return;
    const colors = getColors();
    const score = Math.max(0, Math.min(100, Number(payload.stats?.quality_score || 0)));

    charts.quality = new Chart(canvas, {
      type: "doughnut",
      data: { labels: ["Score", "Remaining"], datasets: [{ data: [score, 100 - score], backgroundColor: [colors.primary, colors.remaining], borderWidth: 0 }] },
      options: {
        ...baseOptions(colors),
        rotation: -90,
        circumference: 180,
        cutout: "72%",
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => c.dataIndex === 0 ? ` Quality ${score}/100` : ` Remaining ${100 - score}` } } }
      }
    });
  }

  function renderAttention(payload) {
    const list = $("column-attention-list");
    if (!list) return;
    const stats = payload.stats || {};
    const rows = Number(stats.rows || 0);
    const columns = (payload.missingByColumn || [])
      .map(item => { const missing = Number(item.missing || 0); return { name: String(item.column ?? "Unnamed"), missing, rate: rows ? (missing / rows) * 100 : 0 }; })
      .filter(item => item.missing > 0)
      .sort((a, b) => b.rate - a.rate)
      .slice(0, 5);

    if (!rows) { list.innerHTML = '<div class="column-attention-empty">No rows were detected in this dataset.</div>'; return; }
    if (!rows.length) { list.innerHTML = '<div class="column-attention-empty">All columns are complete. No missing-value hotspots were found.</div>'; return; }

    list.innerHTML = rows.map(item => {
      const width = Math.max(3, Math.min(100, item.rate));
      return `<div class="column-attention-row"><div class="column-attention-head"><span class="column-attention-name">${window.CleanerUtils.escapeHtml(item.name)}</span><span class="column-attention-count">${item.missing.toLocaleString()} missing · ${item.rate.toFixed(1)}%</span></div><div class="column-attention-track"><div class="column-attention-fill" style="width:${width}%"></div></div></div>`;
    }).join("");
  }

  function renderHealth(payload) {
    const list = $("health-summary-list");
    if (!list) return;
    const s = payload.stats || {};
    const missing = Number(s.missing_percentage || 0);
    const duplicate = Number(s.duplicate_percentage || 0);
    const status = (value, good, fair) => value <= good ? "good" : value <= fair ? "fair" : "poor";
    const labels = { good: "Good", fair: "Fair", poor: "Poor" };
    const rows = [["Completeness", status(missing, 2, 10)], ["Uniqueness", status(duplicate, 1, 5)], ["Dataset scale", Number(s.rows || 0) > 500000 ? "fair" : "good"]];
    list.innerHTML = rows.map(([label, state]) => `<div class="health-row"><span class="health-row-label">${window.CleanerUtils.escapeHtml(label)}</span><span class="health-pill health-pill-${state}">${labels[state]}</span></div>`).join("");
  }

  let lastPayload = null;

  window.renderDatasetInsights = function(payload) {
    if (!payload) {
      empty?.classList.remove("hidden");
      results?.classList.add("hidden");
      unavailable?.classList.add("hidden");
      return;
    }

    lastPayload = payload;
    empty?.classList.add("hidden");
    unavailable?.classList.add("hidden");
    results?.classList.remove("hidden");

    renderMissing(payload);
    renderTypes(payload);
    renderCompleteness(payload);
    renderMissingShare(payload);
    renderDuplicateShare(payload);
    renderQualityScore(payload);
    renderAttention(payload);
    renderHealth(payload);
  };

  document.addEventListener("themechange", () => {
    if (!lastPayload) return;
    renderMissing(lastPayload);
    renderTypes(lastPayload);
    renderCompleteness(lastPayload);
    renderMissingShare(lastPayload);
    renderDuplicateShare(lastPayload);
    renderQualityScore(lastPayload);
  });
})();
