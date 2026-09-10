/*  CSV AUTO CLEANER - MAIN.JS
   Shared state + utilities + frontend API helper  */

window.appState = {
    sessionId: null,
    originalFilename: null,
    currentStats: null,
    beforeStats: null,
    qualityScore: null,
    selectedOperations: [],
    isProcessing: false
};


/* SHARED UTILITIES */

window.CleanerUtils = {

    formatBytes(bytes) {
        if (bytes == null || Number.isNaN(Number(bytes))) {
            return "—";
        }

        bytes = Number(bytes);

        if (bytes < 1024) {
            return `${bytes} B`;
        }

        if (bytes < 1024 * 1024) {
            return `${(bytes / 1024).toFixed(1)} KB`;
        }

        if (bytes < 1024 * 1024 * 1024) {
            return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
        }

        return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
    },


    getExtension(filename) {
        if (!filename || typeof filename !== "string") {
            return "";
        }

        const parts = filename.split(".");

        if (parts.length < 2) {
            return "";
        }

        return parts.pop().toLowerCase();
    },


    escapeHtml(value) {
        const div = document.createElement("div");
        div.textContent = value == null ? "" : String(value);
        return div.innerHTML;
    },


    formatNumber(value) {
        if (value == null || Number.isNaN(Number(value))) {
            return "—";
        }

        return Number(value).toLocaleString();
    },

    formatPercent(value) {
    if (value == null || Number.isNaN(Number(value))) {
        return "—";
    }

    return `${Number(value).toFixed(2)}%`;
  }
};


/* SAFE JSON API HELPER */

window.apiJson = async function (url, options = {}) {

    const requestOptions = {
        credentials: "same-origin",
        ...options
    };

    if (
        requestOptions.body &&
        typeof requestOptions.body !== "string"
    ) {
        requestOptions.body = JSON.stringify(requestOptions.body);
    }

    requestOptions.headers = {
        ...(requestOptions.body
            ? { "Content-Type": "application/json" }
            : {}),
        ...(options.headers || {})
    };

    const response = await fetch(url, requestOptions);

    let data;

    try {
        data = await response.json();
    } catch (error) {
        throw new Error(
            `Server returned an invalid response (${response.status}).`
        );
    }

    if (!response.ok || data.success === false) {

        const error = new Error(
            data.error ||
            `Request failed with status ${response.status}.`
        );

        error.status = response.status;
        error.data = data;

        throw error;
    }

    return data;
};


/* SECTION CONTROL */

window.showSection = function (id) {

    document.querySelectorAll(".screen").forEach(section => {
        section.classList.add("hidden");
    });

    const target = document.getElementById(id);

    if (!target) {
        console.warn(`Section not found: ${id}`);
        return;
    }

    target.classList.remove("hidden");

    requestAnimationFrame(() => {
        target.classList.add("section-enter");
    });

    setTimeout(() => {
        target.classList.remove("section-enter");
    }, 450);

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
};


/* LOADING STATE */

window.setGlobalLoading = function (loading) {

    appState.isProcessing = Boolean(loading);

    document.body.classList.toggle(
        "app-loading",
        Boolean(loading)
    );
};


/* SESSION HELPERS */

window.setSession = function (sessionId, filename = null) {

    appState.sessionId = sessionId;

    if (filename) {
        appState.originalFilename = filename;
    }

    try {
        sessionStorage.setItem(
            "csvCleanerSessionId",
            sessionId
        );

        if (filename) {
            sessionStorage.setItem(
                "csvCleanerFilename",
                filename
            );
        }

    } catch (error) {
        console.warn(
            "Session storage unavailable."
        );
    }
};


window.restoreSession = function () {

    try {

        const sessionId =
            sessionStorage.getItem(
                "csvCleanerSessionId"
            );

        const filename =
            sessionStorage.getItem(
                "csvCleanerFilename"
            );

        if (sessionId) {
            appState.sessionId = sessionId;
        }

        if (filename) {
            appState.originalFilename = filename;
        }

    } catch (error) {
        console.warn(
            "Unable to restore session."
        );
    }
};


/* TOAST NOTIFICATION */

window.showToast = function (
    message,
    type = "info"
) {

    let container =
        document.getElementById(
            "toast-container"
        );

    if (!container) {

        container =
            document.createElement("div");

        container.id =
            "toast-container";

        container.className =
            "toast-container";

        document.body.appendChild(
            container
        );
    }

    const toast =
        document.createElement("div");

    toast.className =
        `toast toast-${type}`;

    toast.innerHTML = `
        <span class="material-symbols-outlined">
            ${
                type === "success"
                    ? "check_circle"
                    : type === "error"
                        ? "error"
                        : "info"
            }
        </span>

        <span>
            ${CleanerUtils.escapeHtml(message)}
        </span>
    `;

    container.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.add("toast-visible");
    });

    setTimeout(() => {

        toast.classList.remove(
            "toast-visible"
        );

        setTimeout(() => {
            toast.remove();
        }, 250);

    }, 3500);
};


/*  INITIALIZATION */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        restoreSession();

        document.body.classList.add(
            "app-ready"
        );

        console.log(
            "CSV Auto Cleaner frontend initialized."
        );
    }
);

/* THEME */
(function initTheme() {
    const key = "csvCleanerTheme";

    function applyTheme(theme) {
        const value = theme === "dark" ? "dark" : "light";
        document.documentElement.dataset.theme = value;
        const themeMeta = document.querySelector('meta[name="theme-color"]');
        if (themeMeta) themeMeta.setAttribute("content", value === "dark" ? "#0b1120" : "#2563eb");

        document.querySelectorAll(".theme-btn").forEach((button) => {
            const active = button.dataset.theme === value;
            button.classList.toggle("theme-btn-active", active);
            button.setAttribute("aria-pressed", String(active));
        });

        try { localStorage.setItem(key, value); } catch (_) {}
        document.dispatchEvent(new CustomEvent("themechange", { detail: { theme: value } }));
    }

    document.addEventListener("DOMContentLoaded", () => {
        let saved = "light";
        try { saved = localStorage.getItem(key) || "light"; } catch (_) {}
        applyTheme(saved);

        document.querySelectorAll(".theme-btn").forEach((button) => {
            button.addEventListener("click", () => applyTheme(button.dataset.theme));
        });
    });
})();
