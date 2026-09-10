(() => {
  "use strict";

  const $ = id =>
    document.getElementById(id);

  const MAX_SIZE =
    100 * 1024 * 1024;

  const ALLOWED =
    new Set([
      "csv",
      "xlsx",
      "xls",
      "json",
      "tsv"
    ]);

  const dropZone =
    $("drop-zone");

  const fileInput =
    $("file-input");

  const progressBox =
    $("upload-progress");

  const progressFill =
    $("progress-fill");

  const progressFilename =
    $("progress-filename");

  const progressStatus =
    $("progress-status");

  const errorBox =
    $("upload-error");

  const errorMessage =
    $("error-message");

  const analysisEmpty =
    $("analysis-empty");

  const analysisResults =
    $("analysis-results");

  const analysisFilename =
    $("analysis-filename");

  const statsEls = {

    rows: $("stat-rows"),

    columns: $("stat-columns"),

    cells: $("stat-cells"),

    missing: $("stat-missing"),

    missingPct:
      $("stat-missing-pct"),

    duplicates:
      $("stat-duplicates"),

    duplicatesPct:
      $("stat-duplicates-pct"),

    numeric:
      $("stat-numeric-cols"),

    text:
      $("stat-text-cols"),

    date:
      $("stat-date-cols"),

    memory:
      $("stat-memory"),

    size:
      $("stat-size"),

    filetype:
      $("stat-filetype"),

    encoding:
      $("stat-encoding"),

    delimiter:
      $("stat-delimiter")
  };

  const qualityRing =
    $("quality-ring");

  const qualityValue =
    $("quality-ring-value");

  let busy = false;


  /*
   * --------------------------------------------------
   * UI HELPERS
   * --------------------------------------------------
   */

  function setError(message) {

    if (errorMessage) {
      errorMessage.textContent =
        message;
    }

    errorBox?.classList.remove(
      "hidden"
    );

    dropZone?.classList.add(
      "upload-error-state"
    );
  }


  function clearError() {

    errorBox?.classList.add(
      "hidden"
    );

    dropZone?.classList.remove(
      "upload-error-state"
    );

    if (errorMessage) {
      errorMessage.textContent = "";
    }
  }


  function setProgress(
    percent,
    status
  ) {

    if (progressFill) {

      progressFill.style.width =
        `${Math.max(
          0,
          Math.min(
            100,
            percent
          )
        )}%`;

    }

    if (progressStatus) {

      progressStatus.textContent =
        status;

    }
  }


  function setQuality(score) {

    const safe =
      Math.max(
        0,
        Math.min(
          100,
          Number(score) || 0
        )
      );

    if (qualityRing) {

      qualityRing.style.background =
        `conic-gradient(
          var(--primary) ${safe}%,
          var(--border) 0
        )`;

    }

    if (qualityValue) {

      qualityValue.textContent =
        Math.round(safe);

    }
  }


  function resetAnalysis() {

    Object.values(statsEls)
      .forEach(element => {

        if (element) {
          element.textContent =
            "—";
        }

      });

    setQuality(0);

    analysisEmpty
      ?.classList.remove("hidden");

    analysisResults
      ?.classList.add("hidden");

  }


  /*
   * --------------------------------------------------
   * VALIDATION
   * --------------------------------------------------
   */

  function validateFile(file) {

    if (!file) {

      setError(
        "Please select a dataset first."
      );

      return false;
    }

    if (file.size === 0) {

      setError(
        "The selected file is empty."
      );

      return false;
    }

    if (file.size > MAX_SIZE) {

      setError(
        "This file is larger than the 100 MB limit."
      );

      return false;
    }

    const extension =
      window.CleanerUtils
        .getExtension(
          file.name
        );

    if (!ALLOWED.has(extension)) {

      setError(
        "Unsupported file type. Please use CSV, XLSX, XLS, JSON or TSV."
      );

      return false;
    }

    return true;
  }


  /*
   * --------------------------------------------------
   * ANALYSIS RENDERING
   * --------------------------------------------------
   */

  function updateAnalysis(
    stats,
    uploadInfo
  ) {

    const s =
      stats || {};

    const u =
      uploadInfo || {};

    if (analysisFilename) {

      analysisFilename.textContent =
        u.filename ||
        window.appState.originalFilename ||
        "Dataset";

    }

    const set =
      (element, value) => {

        if (element) {
          element.textContent =
            value;
        }

      };


    set(
      statsEls.rows,
      window.CleanerUtils
        .formatNumber(s.rows)
    );

    set(
      statsEls.columns,
      window.CleanerUtils
        .formatNumber(s.columns)
    );

    set(
      statsEls.cells,
      window.CleanerUtils
        .formatNumber(
          s.total_cells
        )
    );

    set(
      statsEls.missing,
      window.CleanerUtils
        .formatNumber(
          s.missing
        )
    );

    set(
      statsEls.missingPct,
      window.CleanerUtils
        .formatPercent(
          s.missing_percentage
        )
    );

    set(
      statsEls.duplicates,
      window.CleanerUtils
        .formatNumber(
          s.duplicates
        )
    );

    set(
      statsEls.duplicatesPct,
      window.CleanerUtils
        .formatPercent(
          s.duplicate_percentage
        )
    );

    set(
      statsEls.numeric,
      window.CleanerUtils
        .formatNumber(
          s.numeric_columns
        )
    );

    set(
      statsEls.text,
      window.CleanerUtils
        .formatNumber(
          s.text_columns
        )
    );

    set(
      statsEls.date,
      window.CleanerUtils
        .formatNumber(
          s.date_columns
        )
    );

    set(
      statsEls.memory,
      window.CleanerUtils
        .formatBytes(
          s.memory_bytes
        )
    );

    set(
      statsEls.size,
      window.CleanerUtils
        .formatBytes(
          u.size
        )
    );

    set(
      statsEls.filetype,
      String(
        u.extension || ""
      ).toUpperCase()
    );

    set(
      statsEls.encoding,
      s.encoding ||
      "Detected"
    );

    set(
      statsEls.delimiter,
      s.delimiter ||
      "Auto"
    );


    setQuality(
      s.quality_score
    );


    window.appState.currentStats =
      s;

    window.appState.qualityScore =
      s.quality_score;


    /*
     * Existing chart system
     */

    if (
      typeof window.renderDatasetInsights ===
      "function"
    ) {

      window.renderDatasetInsights({

        stats: s,

        columnTypeCounts:
          s.column_type_counts || {
            numeric:
              Number(
                s.numeric_columns || 0
              ),

            text:
              Number(
                s.text_columns || 0
              ),

            date:
              Number(
                s.date_columns || 0
              )
          },

        missingByColumn:
          s.missing_by_column || [],

        fileType:
          String(
            u.extension || ""
          ).toUpperCase(),

        fileSize:
          window.CleanerUtils
            .formatBytes(
              u.size
            ),

        encoding:
          s.encoding ||
          "Detected",

        estSeconds:
          s.estimated_processing_seconds ||
          1
      });

    }
  }


  /*
   * --------------------------------------------------
   * UPLOAD
   * --------------------------------------------------
   */

  async function uploadAndAnalyze(
    file
  ) {

    busy = true;

    window.appState.isUploading =
      true;

    clearError();

    resetAnalysis();

    dropZone?.classList.add(
      "is-busy"
    );

    progressBox
      ?.classList.remove(
        "hidden"
      );

    if (progressFilename) {

      progressFilename.textContent =
        file.name;

    }

    setProgress(
      10,
      "Preparing secure upload…"
    );


    try {

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );


      const response =
        await fetch(
          "/api/upload",
          {
            method: "POST",
            body: formData,
            credentials:
              "same-origin"
          }
        );


      let upload = null;

      try {

        upload =
          await response.json();

      } catch (_) {

        upload = null;

      }


      if (
        !response.ok ||
        !upload?.success
      ) {

        throw new Error(
          upload?.error ||
          "The server could not accept this file."
        );

      }


      window.appState.sessionId =
        upload.session_id;

      window.appState.originalFilename =
        upload.filename ||
        file.name;

      window.appState.extension =
        upload.extension ||
        window.CleanerUtils
          .getExtension(
            file.name
          );

      window.appState.workingExtension =
        upload.working_extension ||
        upload.extension ||
        window.appState.extension;

      window.appState.fileSize =
        upload.size ||
        file.size;


      setProgress(
        55,
        "Analyzing dataset structure…"
      );


      const analysis =
        await window.apiJson(
          `/api/analyze/${encodeURIComponent(
            upload.session_id
          )}`
        );


      window.appState.beforeStats =
        analysis.stats;

      updateAnalysis(
        analysis.stats,
        upload
      );


      setProgress(
        100,
        "Dataset ready"
      );


      analysisEmpty
        ?.classList.add(
          "hidden"
        );

      analysisResults
        ?.classList.remove(
          "hidden"
        );


      window.showToast(
        "Dataset analyzed successfully.",
        "success"
      );


      if (
        typeof window.Workspace
          ?.refreshSummary ===
        "function"
      ) {

        window.Workspace
          .refreshSummary();

      }

    } catch (error) {

      console.error(
        "Upload error:",
        error
      );

      window.appState.sessionId =
        null;

      window.appState.currentStats =
        null;

      window.appState.isUploading =
        false;

      setProgress(
        0,
        "Upload failed"
      );

      setError(
        error.message ||
        "Unable to upload this dataset."
      );


      window.showToast(
        error.message ||
        "Upload failed.",
        "error"
      );

    } finally {

      busy = false;

      window.appState.isUploading =
        false;

      dropZone?.classList.remove(
        "is-busy"
      );

    }
  }


  function handleFile(file) {

    if (busy) {
      return;
    }

    clearError();

    if (!validateFile(file)) {
      return;
    }

    uploadAndAnalyze(file);
  }


  /*
   * --------------------------------------------------
   * FILE INPUT
   * --------------------------------------------------
   */

  fileInput?.addEventListener(
    "change",
    event => {

      const file =
        event.target.files?.[0];

      if (file) {
        handleFile(file);
      }

      event.target.value = "";

    }
  );


  /*
   * --------------------------------------------------
   * DROP ZONE
   * --------------------------------------------------
   */

  dropZone?.addEventListener(
    "click",
    event => {

      if (busy) {
        return;
      }

      if (
        event.target.closest(
          "label"
        ) ||
        event.target.closest(
          "button"
        )
      ) {
        return;
      }

      fileInput?.click();

    }
  );


  dropZone?.addEventListener(
    "keydown",
    event => {

      if (busy) {
        return;
      }

      if (
        event.key === "Enter" ||
        event.key === " "
      ) {

        event.preventDefault();

        fileInput?.click();

      }

    }
  );


  [
    "dragenter",
    "dragover"
  ].forEach(type => {

    dropZone?.addEventListener(
      type,
      event => {

        event.preventDefault();

        if (!busy) {

          dropZone.classList.add(
            "drag-over"
          );

        }

      }
    );

  });


  [
    "dragleave",
    "drop"
  ].forEach(type => {

    dropZone?.addEventListener(
      type,
      event => {

        event.preventDefault();

        dropZone?.classList.remove(
          "drag-over"
        );

      }
    );

  });


  dropZone?.addEventListener(
    "drop",
    event => {

      if (busy) {
        return;
      }

      const file =
        event.dataTransfer
          ?.files?.[0];

      if (file) {
        handleFile(file);
      }

    }
  );

})();