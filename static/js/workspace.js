(function () {
    const CATALOG = [
        {
            id: "missing",
            title: "Missing Values",
            icon: "rule",
            description: "Handle empty or null cells in your dataset.",
            ops: [
                {
                    id: "remove_missing_rows",
                    label: "Remove Missing Rows",
                    desc: "Delete rows that contain any missing values."
                },
                {
                    id: "remove_missing_columns",
                    label: "Remove Missing Columns",
                    desc: "Delete columns that contain any missing values."
                },
                {
                    id: "fill_missing_mean",
                    label: "Fill with Mean",
                    desc: "Replace missing numeric values with the column average."
                },
                {
                    id: "fill_missing_median",
                    label: "Fill with Median",
                    desc: "Replace missing numeric values with the column median."
                },
                {
                    id: "fill_missing_mode",
                    label: "Fill with Mode",
                    desc: "Replace missing values with the most frequent value."
                },
                {
                    id: "fill_missing_static",
                    label: "Fill with Static Value",
                    desc: "Replace missing values with a fixed value."
                },
                {
                    id: "forward_fill",
                    label: "Forward Fill",
                    desc: "Carry the previous row's value forward into gaps."
                },
                {
                    id: "backward_fill",
                    label: "Backward Fill",
                    desc: "Carry the next row's value backward into gaps."
                }
            ]
        },
        {
            id: "duplicates",
            title: "Duplicate Data",
            icon: "content_copy",
            description: "Find and remove repeated rows or columns.",
            ops: [
                {
                    id: "remove_duplicate_rows",
                    label: "Remove Duplicate Rows",
                    desc: "Delete rows that are exact duplicates."
                },
                {
                    id: "remove_duplicate_columns",
                    label: "Remove Duplicate Columns",
                    desc: "Delete columns whose values exactly match another column."
                },
                {
                    id: "remove_all_duplicate_groups",
                    label: "Remove All Duplicate Groups",
                    desc: "Remove every row belonging to a duplicate group."
                }
            ]
        },
        {
            id: "text",
            title: "Text Cleaning",
            icon: "text_fields",
            description: "Normalize and tidy up text values.",
            ops: [
                {
                    id: "trim_spaces",
                    label: "Trim Spaces",
                    desc: "Remove leading and trailing whitespace."
                },
                {
                    id: "remove_extra_spaces",
                    label: "Remove Extra Spaces",
                    desc: "Collapse multiple spaces into one space."
                },
                {
                    id: "lowercase",
                    label: "Convert to Lowercase",
                    desc: "Convert text values to lowercase."
                },
                {
                    id: "uppercase",
                    label: "Convert to Uppercase",
                    desc: "Convert text values to uppercase."
                },
                {
                    id: "title_case",
                    label: "Title Case",
                    desc: "Capitalize the first letter of every word."
                }
            ]
        },
        {
            id: "dates",
            title: "Date Operations",
            icon: "calendar_month",
            description: "Convert, validate and extract information from dates.",
            ops: [
                {
                    id: "convert_to_datetime",
                    label: "Convert to Date",
                    desc: "Convert date-like values into datetime format."
                },
                {
                    id: "remove_invalid_dates",
                    label: "Remove Invalid Dates",
                    desc: "Remove rows containing invalid date values."
                },
                {
                    id: "extract_year",
                    label: "Extract Year",
                    desc: "Extract the year from date values."
                },
                {
                    id: "extract_month",
                    label: "Extract Month",
                    desc: "Extract the month from date values."
                },
                {
                    id: "extract_day",
                    label: "Extract Day",
                    desc: "Extract the day from date values."
                }
            ]
        },
        {
            id: "formatting",
            title: "Formatting",
            icon: "tune",
            description: "Standardize columns and values.",
            ops: [
                {
                    id: "normalize_column_names",
                    label: "Normalize Column Names",
                    desc: "Make column names clean and consistent."
                },
                {
                    id: "standardize_missing_tokens",
                    label: "Standardize Missing Values",
                    desc: "Convert common missing-value tokens into proper missing values."
                },
                {
                    id: "convert_numeric_text",
                    label: "Convert Numeric Text",
                    desc: "Convert numeric-looking text into numbers."
                },
                {
                    id: "remove_empty_columns",
                    label: "Remove Empty Columns",
                    desc: "Delete columns containing no useful values."
                }
            ]
        },
        {
            id: "validation",
            title: "Validation",
            icon: "verified",
            description: "Check values against expected formats.",
            ops: [
                {
                    id: "remove_invalid_email_rows",
                    label: "Remove Invalid Emails",
                    desc: "Remove rows containing invalid email addresses."
                },
                {
                    id: "remove_invalid_date_rows",
                    label: "Remove Invalid Dates",
                    desc: "Remove rows containing invalid date values."
                }
            ]
        },
        {
            id: "transformation",
            title: "Data Transformation",
            icon: "swap_horiz",
            description: "Restructure and organize your dataset.",
            ops: [
                {
                    id: "remove_constant_columns",
                    label: "Remove Constant Columns",
                    desc: "Remove columns where every value is the same."
                },
                {
                    id: "sort_columns",
                    label: "Sort Columns",
                    desc: "Sort columns alphabetically."
                },
                {
                    id: "reset_row_index",
                    label: "Reset Row Index",
                    desc: "Reset the dataset row index."
                }
            ]
        }
    ];

    const selectedOps = new Set();
    let renderedOnce = false;

    const accordionRoot = document.getElementById("accordion-root");
    const recommendationsList = document.getElementById("recommendations-list");

    const sumRows = document.getElementById("sum-rows");
    const sumColumns = document.getElementById("sum-columns");
    const sumMissing = document.getElementById("sum-missing");
    const sumDuplicates = document.getElementById("sum-duplicates");
    const sumMemory = document.getElementById("sum-memory");
    const sumSize = document.getElementById("sum-size");
    const sumFiletype = document.getElementById("sum-filetype");
    const sumSession = document.getElementById("sum-session");
    const sumQualityRing = document.getElementById("sum-quality-ring");
    const sumQualityValue = document.getElementById("sum-quality-value");
    const sumSelectedCount = document.getElementById("sum-selected-count");
    const sumChangesList = document.getElementById("sum-changes-list");
    const sumEstTime = document.getElementById("sum-est-time");
    const processBtn = document.getElementById("process-btn");

    function escapeHtml(value) {
        const div = document.createElement("div");
        div.textContent = String(value ?? "");
        return div.innerHTML;
    }

    function escapeAttr(value) {
        return escapeHtml(value).replace(/"/g, "&quot;");
    }

    function renderAccordion() {
        if (!accordionRoot) {
            return;
        }

        accordionRoot.innerHTML = CATALOG.map(category => `
            <div class="accordion-item" data-cat="${category.id}">
                <button
                    type="button"
                    class="accordion-header"
                    data-toggle="${category.id}"
                >
                    <span
                        class="accordion-icon-wrap material-symbols-outlined"
                        aria-hidden="true"
                    >${category.icon}</span>

                    <span class="accordion-heading">
                        <span class="accordion-heading-title">
                            ${category.title}
                            <span class="accordion-op-count">
                                ${category.ops.length} operations
                            </span>
                        </span>

                        <span class="accordion-heading-desc">
                            ${category.description}
                        </span>
                    </span>

                    <span
                        class="material-symbols-outlined accordion-chevron"
                        aria-hidden="true"
                    >expand_more</span>
                </button>

                <div class="accordion-body-wrap">
                    <div class="accordion-body-inner">
                        <div class="accordion-body">
                            ${category.ops.map(operation => `
                                <label
                                    class="op-row"
                                    data-op="${operation.id}"
                                    title="${escapeAttr(operation.desc)}"
                                >
                                    <input
                                        type="checkbox"
                                        class="op-checkbox"
                                        data-op-checkbox="${operation.id}"
                                    >

                                    <span
                                        class="material-symbols-outlined op-icon"
                                        aria-hidden="true"
                                    >check_box_outline_blank</span>

                                    <span class="op-text">
                                        <span class="op-label">
                                            ${operation.label}
                                        </span>

                                        <p class="op-desc">
                                            ${operation.desc}
                                        </p>
                                    </span>

                                    <span
                                        class="material-symbols-outlined op-check-mark"
                                        aria-hidden="true"
                                    >check_circle</span>
                                </label>
                            `).join("")}
                        </div>
                    </div>
                </div>
            </div>
        `).join("");

        accordionRoot
            .querySelectorAll(".accordion-header")
            .forEach(header => {
                header.addEventListener("click", () => {
                    const item = header.closest(".accordion-item");

                    if (!item) {
                        return;
                    }

                    const wasOpen = item.classList.contains("open");

                    accordionRoot
                        .querySelectorAll(".accordion-item")
                        .forEach(other => {
                            other.classList.remove("open");
                        });

                    if (!wasOpen) {
                        item.classList.add("open");
                    }
                });
            });

        accordionRoot
            .querySelectorAll(".op-row")
            .forEach(row => {
                const checkbox = row.querySelector(".op-checkbox");

                if (!checkbox) {
                    return;
                }

                row.addEventListener("click", event => {
                    if (event.target === checkbox) {
                        return;
                    }

                    checkbox.checked = !checkbox.checked;
                    checkbox.dispatchEvent(new Event("change"));
                });

                checkbox.addEventListener("change", () => {
                    const operationId = row.dataset.op;

                    if (checkbox.checked) {
                        selectedOps.add(operationId);
                        row.classList.add("selected");
                    } else {
                        selectedOps.delete(operationId);
                        row.classList.remove("selected");
                    }

                    updateSummary();
                    syncRecommendationState();
                });
            });

        const first = accordionRoot.querySelector(".accordion-item");

        if (first) {
            first.classList.add("open");
        }
    }

    function estimateTextFor(operationId, stats) {
        const missing = stats?.missing;
        const duplicates = stats?.duplicates;

        const estimates = {
            remove_missing_rows:
                missing != null
                    ? `Remove rows containing ${missing.toLocaleString()} missing values`
                    : "Remove rows containing missing values",

            remove_missing_columns:
                "Remove columns that contain missing values",

            fill_missing_mean:
                missing != null
                    ? `Fill ${missing.toLocaleString()} missing values with column means`
                    : "Fill missing values with column means",

            fill_missing_median:
                missing != null
                    ? `Fill ${missing.toLocaleString()} missing values with column medians`
                    : "Fill missing values with column medians",

            fill_missing_mode:
                missing != null
                    ? `Fill ${missing.toLocaleString()} missing values with the most frequent value`
                    : "Fill missing values with the most frequent value",

            fill_missing_static:
                "Fill missing values with a fixed value",

            forward_fill:
                "Carry previous values forward into gaps",

            backward_fill:
                "Carry next values backward into gaps",

            remove_duplicate_rows:
                duplicates != null
                    ? `Remove ${duplicates.toLocaleString()} duplicate rows`
                    : "Remove duplicate rows",

            remove_duplicate_columns:
                "Remove duplicate columns",

            remove_all_duplicate_groups:
                "Remove all rows involved in duplicate groups",

            trim_spaces:
                "Trim leading and trailing whitespace",

            remove_extra_spaces:
                "Collapse extra internal spaces",

            lowercase:
                "Convert text to lowercase",

            uppercase:
                "Convert text to uppercase",

            title_case:
                "Apply title case to text",

            convert_to_datetime:
                "Convert date values into datetime format",

            remove_invalid_dates:
                "Remove rows containing invalid dates",

            extract_year:
                "Extract year from date values",

            extract_month:
                "Extract month from date values",

            extract_day:
                "Extract day from date values",

            normalize_column_names:
                "Normalize column names",

            standardize_missing_tokens:
                "Standardize missing-value tokens",

            convert_numeric_text:
                "Convert numeric-looking text into numbers",

            remove_empty_columns:
                "Remove empty columns",

            remove_invalid_email_rows:
                "Remove rows containing invalid email addresses",

            remove_invalid_date_rows:
                "Remove rows containing invalid dates",

            remove_constant_columns:
                "Remove columns containing only one unique value",

            sort_columns:
                "Sort columns alphabetically",

            reset_row_index:
                "Reset the dataset row index"
        };

        return estimates[operationId] || operationId;
    }

    function parseStatInt(element) {
        if (!element) {
            return 0;
        }

        const number = parseInt(
            String(element.textContent).replace(/,/g, ""),
            10
        );

        return Number.isNaN(number) ? 0 : number;
    }

    const RECOMMENDATION_RULES = [
        {
            test: context => context.missing > 0,
            icon: "report",
            text: context =>
                `Missing values detected (${context.missing.toLocaleString()})`,
            actionLabel: "Fill Missing Values",
            opId: "fill_missing_mean",
            catId: "missing"
        },
        {
            test: context => context.duplicates > 0,
            icon: "content_copy",
            text: context =>
                `Duplicate rows detected (${context.duplicates.toLocaleString()})`,
            actionLabel: "Remove Duplicates",
            opId: "remove_duplicate_rows",
            catId: "duplicates"
        },
        {
            test: context => context.dateCols > 0,
            icon: "calendar_month",
            text: context =>
                `${context.dateCols} date column${context.dateCols === 1 ? "" : "s"} detected`,
            actionLabel: "Convert Dates",
            opId: "convert_to_datetime",
            catId: "dates"
        },
        {
            test: context => context.textCols > 0,
            icon: "text_fields",
            text: context =>
                `${context.textCols} text column${context.textCols === 1 ? "" : "s"} detected`,
            actionLabel: "Trim Spaces",
            opId: "trim_spaces",
            catId: "text"
        }
    ];

    function getRecommendationContext() {
        const stats = window.appState?.currentStats || {};

        return {
            missing: Number(stats.missing || 0),
            duplicates: Number(stats.duplicates || 0),
            dateCols: parseStatInt(
                document.getElementById("stat-date-cols")
            ),
            textCols: parseStatInt(
                document.getElementById("stat-text-cols")
            )
        };
    }

    function renderRecommendations() {
        if (!recommendationsList) {
            return;
        }

        const context = getRecommendationContext();

        const matches = RECOMMENDATION_RULES.filter(
            rule => rule.test(context)
        );

        if (!matches.length) {
            recommendationsList.innerHTML =
                '<p class="recommendations-empty">No issues detected — this dataset looks clean.</p>';
            return;
        }

        recommendationsList.innerHTML = matches.map(rule => `
            <div
                class="recommendation-item"
                data-rec-op="${rule.opId}"
                data-rec-cat="${rule.catId}"
                tabindex="0"
                role="button"
                aria-label="Apply recommendation: ${escapeAttr(rule.actionLabel)}"
            >
                <span
                    class="material-symbols-outlined rec-icon"
                    aria-hidden="true"
                >${rule.icon}</span>

                <span class="recommendation-text">
                    ${escapeHtml(rule.text(context))}
                </span>

                <span class="recommendation-action">
                    ${rule.actionLabel}
                </span>
            </div>
        `).join("");

        recommendationsList
            .querySelectorAll(".recommendation-item")
            .forEach(item => {
                const applyRecommendation = () => {
                    const operationId = item.dataset.recOp;
                    const categoryId = item.dataset.recCat;

                    const category = accordionRoot?.querySelector(
                        `.accordion-item[data-cat="${categoryId}"]`
                    );

                    if (category) {
                        accordionRoot
                            .querySelectorAll(".accordion-item")
                            .forEach(other => {
                                other.classList.remove("open");
                            });

                        category.classList.add("open");
                    }

                    const row = accordionRoot?.querySelector(
                        `.op-row[data-op="${operationId}"]`
                    );

                    if (!row) {
                        return;
                    }

                    const checkbox = row.querySelector(".op-checkbox");

                    if (!checkbox) {
                        return;
                    }

                    if (!checkbox.checked) {
                        checkbox.checked = true;
                        checkbox.dispatchEvent(new Event("change"));
                    }

                    row.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });
                };

                item.addEventListener("click", applyRecommendation);

                item.addEventListener("keydown", event => {
                    if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        applyRecommendation();
                    }
                });
            });

        syncRecommendationState();
    }

    function syncRecommendationState() {
        if (!recommendationsList) {
            return;
        }

        recommendationsList
            .querySelectorAll(".recommendation-item")
            .forEach(item => {
                const operationId = item.dataset.recOp;

                item.classList.toggle(
                    "applied",
                    selectedOps.has(operationId)
                );
            });
    }

    function formatBytes(bytes) {
        if (window.CleanerUtils?.formatBytes) {
            return window.CleanerUtils.formatBytes(bytes);
        }

        if (!bytes || bytes < 0) {
            return "—";
        }

        const units = ["B", "KB", "MB", "GB"];
        let value = Number(bytes);
        let index = 0;

        while (value >= 1024 && index < units.length - 1) {
            value /= 1024;
            index++;
        }

        return `${value.toFixed(index === 0 ? 0 : 2)} ${units[index]}`;
    }

    function populateDatasetSummary() {
        const stats = window.appState?.currentStats;
        const filename = window.appState?.originalFilename;

        if (sumRows) {
            sumRows.textContent = stats
                ? Number(stats.rows || 0).toLocaleString()
                : "—";
        }

        if (sumColumns) {
            sumColumns.textContent = stats
                ? Number(stats.columns || 0).toLocaleString()
                : "—";
        }

        if (sumMissing) {
            sumMissing.textContent = stats
                ? Number(stats.missing || 0).toLocaleString()
                : "—";
        }

        if (sumDuplicates) {
            sumDuplicates.textContent = stats
                ? Number(stats.duplicates || 0).toLocaleString()
                : "—";
        }

        if (sumMemory) {
            const memory =
                stats?.memory_bytes ??
                stats?.estimatedMemoryBytes;

            sumMemory.textContent =
                memory != null ? formatBytes(memory) : "—";
        }

        if (sumFiletype) {
            sumFiletype.textContent = filename
                ? filename.split(".").pop().toUpperCase()
                : "—";
        }

        if (sumSession) {
            sumSession.textContent = "Preview mode";
        }

        const score = window.appState?.qualityScore;

        if (score != null) {
            if (sumQualityValue) {
                sumQualityValue.textContent = score;
            }

            if (sumQualityRing) {
                sumQualityRing.style.background =
                    `conic-gradient(var(--primary) ${score}%, var(--border) 0)`;
            }
        } else {
            if (sumQualityValue) {
                sumQualityValue.textContent = "—";
            }

            if (sumQualityRing) {
                sumQualityRing.style.background =
                    "conic-gradient(var(--border) 100%, var(--border) 0)";
            }
        }

        const sourceSize = document.getElementById("stat-size");

        if (sumSize) {
            sumSize.textContent =
                sourceSize && sourceSize.textContent !== "—"
                    ? sourceSize.textContent
                    : "—";
        }
    }

    function updateSummary() {
        const stats = window.appState?.currentStats;
        const count = selectedOps.size;

        if (sumSelectedCount) {
            sumSelectedCount.textContent = count;
        }

        if (processBtn) {
            processBtn.disabled = count === 0;
        }

        if (!sumChangesList) {
            return;
        }

        if (count === 0) {
            sumChangesList.innerHTML =
                '<p class="summary-changes-empty">Select an operation to see its estimated effect.</p>';
        } else {
            sumChangesList.innerHTML = Array.from(selectedOps)
                .map(operationId => `
                    <div class="summary-change-row">
                        <span
                            class="material-symbols-outlined"
                            aria-hidden="true"
                        >check_circle</span>

                        <span>
                            ${escapeHtml(
                                estimateTextFor(operationId, stats)
                            )}
                        </span>
                    </div>
                `)
                .join("");
        }

        const estimatedSeconds =
            count === 0 ? 0 : Math.round(1 + count * 0.4);

        if (sumEstTime) {
            sumEstTime.textContent =
                count === 0 ? "—" : `~${estimatedSeconds}s`;
        }
    }

    function clearSelections() {
        selectedOps.clear();

        accordionRoot
            ?.querySelectorAll(".op-checkbox")
            .forEach(checkbox => {
                checkbox.checked = false;
            });

        accordionRoot
            ?.querySelectorAll(".op-row.selected")
            .forEach(row => {
                row.classList.remove("selected");
            });

        updateSummary();
        syncRecommendationState();
    }

    async function processDataset() {
        if (!processBtn || processBtn.disabled) {
            return;
        }

        if (window.appState?.isProcessing) {
            return;
        }

        const operations = Array.from(selectedOps).map(id => ({
            id
        }));

        if (!operations.length) {
            return;
        }

        processBtn.disabled = true;

        try {
            if (window.ProcessingManager?.process) {
                const result =
                    await window.ProcessingManager.process(operations);

                if (window.renderResults) {
                    window.renderResults(result);
                }

                if (window.showSection) {
                    window.showSection("results-section");
                }

                window.showToast?.(
                    "Dataset processed successfully.",
                    "success"
                );

                return;
            }

            if (window.processSelectedOperations) {
                const result =
                    await window.processSelectedOperations(operations);

                if (window.renderResults) {
                    window.renderResults(result);
                }

                if (window.showSection) {
                    window.showSection("results-section");
                }

                return;
            }

            throw new Error("Processing module is not available.");
        } catch (error) {
            window.showToast?.(
                error.message || "Unable to process the dataset.",
                "error"
            );
        } finally {
            processBtn.disabled = selectedOps.size === 0;

            window.setTimeout(() => {
                window.ProcessingManager?.hide?.();
            }, 700);
        }
    }

    if (processBtn) {
        processBtn.addEventListener("click", processDataset);
    }

    const proceedBtn = document.getElementById("proceed-btn");

    if (proceedBtn) {
        proceedBtn.addEventListener("click", () => {
            if (!renderedOnce) {
                renderAccordion();
                renderedOnce = true;
            }

            populateDatasetSummary();
            updateSummary();
            renderRecommendations();

            if (window.showSection) {
                window.showSection("workspace-section");
            }
        });
    }

    window.clearWorkspaceSelections = clearSelections;
    window.getSelectedOperations = () =>
        Array.from(selectedOps).map(id => ({ id }));

    window.renderWorkspace = () => {
        renderAccordion();
        populateDatasetSummary();
        updateSummary();
        renderRecommendations();
        renderedOnce = true;
    };
})();