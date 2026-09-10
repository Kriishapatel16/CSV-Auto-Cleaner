(() => {
  "use strict";

  const $ = (id) =>
    document.getElementById(id);

  const root =
    $("results-section");

  const resultStyles = `
    <style id="results-inline-style">

      .results-page {
        max-width: 1400px;
        margin: 0 auto;
        padding: 32px 28px 60px;
      }

      .results-header {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        align-items: flex-start;
        margin-bottom: 24px;
      }

      .results-eyebrow {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: .12em;
        color: var(--primary);
        font-weight: 700;
      }

      .results-title {
        margin: 5px 0 6px;
        font-size: 30px;
        line-height: 1.15;
        color: var(--text-primary);
      }

      .results-subtitle {
        margin: 0;
        color: var(--text-secondary);
      }

      .results-grid {
        display: grid;
        grid-template-columns:
          repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin-bottom: 20px;
      }

      .result-stat,
      .result-panel {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow:
          0 2px 8px rgba(15,23,42,.04);
      }

      .result-stat {
        padding: 18px;
      }

      .result-stat-label {
        font-size: 12px;
        color: var(--text-secondary);
        display: block;
        margin-bottom: 7px;
      }

      .result-stat-value {
        font-size: 24px;
        font-weight: 750;
        color: var(--text-primary);
      }

      .result-compare {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 18px;
        margin-bottom: 20px;
      }

      .result-panel {
        padding: 20px;
      }

      .result-panel h3 {
        margin: 0 0 16px;
        font-size: 15px;
      }

      .result-panel-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .score {
        font-size: 34px;
        font-weight: 800;
      }

      .score.good {
        color: #16835b;
      }

      .score.warn {
        color: #b7791f;
      }

      .score.bad {
        color: #c24141;
      }

      .result-diff {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
      }

      .diff-box {
        padding: 14px;
        border-radius: 12px;
        background: var(--surface-soft);
        border: 1px solid var(--border);
      }

      .diff-label {
        font-size: 11px;
        color: var(--text-secondary);
      }

      .diff-value {
        display: block;
        margin-top: 5px;
        font-weight: 750;
        font-size: 18px;
      }

      .result-operations {
        margin-bottom: 20px;
      }

      .result-operation {
        display: flex;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid var(--border);
      }

      .result-operation:last-child {
        border-bottom: 0;
      }

      .result-operation
      .material-symbols-outlined {
        color: var(--success);
      }

      .result-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }

      .result-actions button {
        border: 1px solid var(--border);
        background: #fff;
        color: var(--text-primary);
        border-radius: 10px;
        padding: 11px 16px;
        font-weight: 650;
        cursor: pointer;
      }

      .result-actions .primary {
        background: var(--primary);
        border-color: var(--primary);
        color: #fff;
      }

      .result-actions button:disabled {
        opacity: .5;
        cursor: not-allowed;
      }

      .result-message {
        margin-top: 14px;
        color: var(--text-secondary);
        font-size: 13px;
      }

      .result-error {
        padding: 12px 14px;
        background: #fff3f3;
        border: 1px solid #fecaca;
        color: #b42318;
        border-radius: 10px;
        margin-bottom: 16px;
      }

      html[data-theme="dark"] .results-page {
        color: var(--text-primary);
      }

      html[data-theme="dark"] .result-stat,
      html[data-theme="dark"] .result-panel {
        background: #111827;
        border-color: #263449;
        box-shadow: 0 18px 46px rgba(0,0,0,.20);
      }

      html[data-theme="dark"] .result-stat-label,
      html[data-theme="dark"] .diff-label,
      html[data-theme="dark"] .result-message {
        color: #9aa9bd;
      }

      html[data-theme="dark"] .result-stat-value,
      html[data-theme="dark"] .result-panel h3,
      html[data-theme="dark"] .diff-value {
        color: #f8fafc;
      }

      html[data-theme="dark"] .diff-box {
        background: #141d2c;
        border-color: #2f4058;
      }

      html[data-theme="dark"] .result-actions button {
        background: #172033;
        border-color: #3a4a63;
        color: #f8fafc;
      }

      html[data-theme="dark"] .result-actions button:hover:not(:disabled) {
        background: #243249;
        border-color: #52709a;
      }

      html[data-theme="dark"] .result-actions .primary {
        background: #3b82f6;
        border-color: #60a5fa;
        color: #08111f;
      }

      html[data-theme="dark"] .result-actions .primary:hover:not(:disabled) {
        background: #60a5fa;
      }

      html[data-theme="dark"] .result-error {
        background: #321416;
        border-color: #6d2d34;
        color: #fca5a5;
      }

      html[data-theme="dark"] .score.good {
        color: #5ee7b7;
      }

      html[data-theme="dark"] .score.warn {
        color: #fbbf67;
      }

      html[data-theme="dark"] .score.bad {
        color: #fca5a5;
      }

      @media (max-width: 900px) {
        .results-grid {
          grid-template-columns:
            repeat(2, minmax(0, 1fr));
        }

        .result-compare {
          grid-template-columns: 1fr;
        }

        .results-header {
          flex-direction: column;
        }
      }

      @media (max-width: 560px) {
        .results-page {
          padding: 22px 16px 40px;
        }

        .results-grid {
          grid-template-columns: 1fr;
        }

        .results-title {
          font-size: 25px;
        }
      }

    </style>
  `;

  function fmt(value) {
    return window.CleanerUtils.formatNumber(
      value
    );
  }

  function pct(value) {
    return window.CleanerUtils.formatPercent(
      value
    );
  }

  function esc(value) {
    return window.CleanerUtils.escapeHtml(
      value
    );
  }

  function scoreClass(score) {

    const number =
      Number(score) || 0;

    if (number >= 85) {
      return "good";
    }

    if (number >= 65) {
      return "warn";
    }

    return "bad";
  }

  function statCard(
    label,
    value
  ) {

    return `
      <div class="result-stat">

        <span class="result-stat-label">
          ${esc(label)}
        </span>

        <span class="result-stat-value">
          ${esc(value)}
        </span>

      </div>
    `;
  }

  function renderResults(
    data = {}
  ) {

    if (!root) {
      return;
    }

    const before =
      data.before ||
      window.appState.beforeStats ||
      {};

    const after =
      data.after ||
      window.appState.currentStats ||
      {};

    const operations =
      data.operations ||
      window.appState.operationResults ||
      [];

    root.innerHTML =
      resultStyles +
      `
        <div class="results-page">

          <div class="results-header">

            <div>

              <span class="results-eyebrow">
                Cleaning complete
              </span>

              <h1 class="results-title">
                Your cleaned dataset is ready
              </h1>

              <p class="results-subtitle">
                ${esc(
                  window.appState.originalFilename ||
                  "Dataset"
                )}
                · Review the changes before downloading.
              </p>

            </div>

          </div>

          <div class="results-grid">

            ${statCard(
              "Remaining rows",
              fmt(after.rows)
            )}

            ${statCard(
              "Remaining columns",
              fmt(after.columns)
            )}

            ${statCard(
              "Missing values",
              `${fmt(after.missing)}
               (${pct(after.missing_percentage)})`
            )}

            ${statCard(
              "Duplicate rows",
              `${fmt(after.duplicates)}
               (${pct(after.duplicate_percentage)})`
            )}

          </div>

          <div class="result-compare">

            <section class="result-panel">

              <div class="result-panel-head">

                <h3>
                  Before cleaning
                </h3>

                <span
                  class="score ${scoreClass(
                    before.quality_score
                  )}"
                >
                  ${fmt(
                    before.quality_score
                  )}
                </span>

              </div>

              <div class="result-diff">

                <div class="diff-box">
                  <span class="diff-label">
                    Missing
                  </span>

                  <span class="diff-value">
                    ${fmt(before.missing)}
                  </span>
                </div>

                <div class="diff-box">
                  <span class="diff-label">
                    Duplicates
                  </span>

                  <span class="diff-value">
                    ${fmt(before.duplicates)}
                  </span>
                </div>

              </div>

            </section>

            <section class="result-panel">

              <div class="result-panel-head">

                <h3>
                  After cleaning
                </h3>

                <span
                  class="score ${scoreClass(
                    after.quality_score
                  )}"
                >
                  ${fmt(
                    after.quality_score
                  )}
                </span>

              </div>

              <div class="result-diff">

                <div class="diff-box">
                  <span class="diff-label">
                    Missing
                  </span>

                  <span class="diff-value">
                    ${fmt(after.missing)}
                  </span>
                </div>

                <div class="diff-box">
                  <span class="diff-label">
                    Duplicates
                  </span>

                  <span class="diff-value">
                    ${fmt(after.duplicates)}
                  </span>
                </div>

              </div>

            </section>

          </div>

          <section
            class="result-panel result-operations"
          >

            <h3>
              Operations applied
            </h3>

            ${
              operations.length
                ? operations
                    .map(
                      (item) => `
                        <div
                          class="result-operation"
                        >

                          <span
                            class="material-symbols-outlined"
                            aria-hidden="true"
                          >
                            check_circle
                          </span>

                          <span>
                            ${esc(
                              item.description ||
                              item.operation ||
                              "Operation completed"
                            )}
                          </span>

                        </div>
                      `
                    )
                    .join("")
                : `
                    <p class="result-message">
                      No operation details were returned.
                    </p>
                  `
            }

          </section>

          <section class="result-panel">

            <div class="result-actions">

              <button
                type="button"
                id="result-undo-btn"
              >
                Undo last round
              </button>

              <button
                type="button"
                id="result-reset-btn"
              >
                Reset dataset
              </button>

              <button
                type="button"
                id="result-more-btn"
              >
                Do more cleaning
              </button>

              <button
                type="button"
                class="primary"
                id="result-download-btn"
              >
                Download cleaned file
              </button>

              <button
                type="button"
                id="result-report-btn"
              >
                Generate PDF report
              </button>

            </div>

            <p
              id="result-message"
              class="result-message"
            >
              ${esc(
                data.message ||
                "Your processed dataset is ready."
              )}
            </p>

          </section>

        </div>
      `;

    bindResultActions();
  }

  function setMessage(
    text,
    error = false
  ) {

    const element =
      $("result-message");

    if (!element) {
      return;
    }

    element.textContent =
      text;

    element.classList.toggle(
      "result-error",
      error
    );
  }

  function bindResultActions() {

    $("result-more-btn")
      ?.addEventListener(
        "click",
        () => {

          window.Workspace
            ?.clearSelections?.();

          window.Workspace
            ?.refreshSummary?.();

          window.showSection(
            "workspace-section"
          );

        }
      );

    $("result-download-btn")
      ?.addEventListener(
        "click",
        () => {

          window.location.href =
            `/api/download/${encodeURIComponent(
              window.appState.sessionId
            )}`;

        }
      );

    $("result-report-btn")
      ?.addEventListener(
        "click",
        async () => {

          const button =
            $("result-report-btn");

          button.disabled =
            true;

          setMessage(
            "Generating your PDF report…"
          );

          try {

            const response =
              await fetch(
                `/api/report/${encodeURIComponent(
                  window.appState.sessionId
                )}`,
                {
                  credentials:
                    "same-origin",
                }
              );

            if (!response.ok) {

              const payload =
                await response
                  .json()
                  .catch(
                    () => null
                  );

              throw new Error(
                payload?.error ||
                "Unable to generate the report."
              );
            }

            const blob =
              await response.blob();

            const url =
              URL.createObjectURL(
                blob
              );

            const anchor =
              document.createElement(
                "a"
              );

            anchor.href =
              url;

            anchor.download =
              "csv_cleaning_report.pdf";

            document.body.appendChild(
              anchor
            );

            anchor.click();

            anchor.remove();

            URL.revokeObjectURL(
              url
            );

            setMessage(
              "PDF report generated successfully."
            );

          } catch (error) {

            setMessage(
              error.message,
              true
            );

          } finally {

            button.disabled =
              false;

          }

        }
      );

    $("result-undo-btn")
      ?.addEventListener(
        "click",
        async () => {

          const button =
            $("result-undo-btn");

          button.disabled =
            true;

          try {

            const result =
              await window.apiJson(
                `/api/undo/${encodeURIComponent(
                  window.appState.sessionId
                )}`,
                {
                  method:
                    "POST",
                }
              );

            window.appState.currentStats =
              result.stats;

            window.appState.beforeStats =
              null;

            window.appState.operationResults =
              [];

            renderResults({
              after:
                result.stats,

              operations:
                [],

              message:
                result.message,
            });

          } catch (error) {

            setMessage(
              error.message,
              true
            );

            button.disabled =
              false;
          }

        }
      );

    $("result-reset-btn")
      ?.addEventListener(
        "click",
        async () => {

          if (
            !confirm(
              "Reset the dataset to the original uploaded file?"
            )
          ) {
            return;
          }

          const button =
            $("result-reset-btn");

          button.disabled =
            true;

          try {

            const result =
              await window.apiJson(
                `/api/reset/${encodeURIComponent(
                  window.appState.sessionId
                )}`,
                {
                  method:
                    "POST",
                }
              );

            window.appState.currentStats =
              result.stats;

            window.appState.beforeStats =
              null;

            window.appState.operationResults =
              [];

            renderResults({
              after:
                result.stats,

              operations:
                [],

              message:
                result.message,
            });

          } catch (error) {

            setMessage(
              error.message,
              true
            );

            button.disabled =
              false;
          }

        }
      );
  }

  window.renderResults =
    renderResults;

})();