(function () {

    "use strict";

    /* PROCESSING OVERLAY */

    function showProcessingState() {

        let overlay =
            document.getElementById(
                "processing-overlay"
            );

        if (!overlay) {

            overlay =
                document.createElement("div");

            overlay.id =
                "processing-overlay";

            overlay.className =
                "processing-overlay";

            overlay.innerHTML = `
                <div class="processing-card">

                    <div class="processing-spinner">
                        <span class="material-symbols-outlined">
                            sync
                        </span>
                    </div>

                    <h3>Cleaning your dataset</h3>

                    <p>
                        Applying the selected operations safely...
                    </p>

                    <div class="processing-progress">
                        <span></span>
                    </div>

                </div>
            `;

            document.body.appendChild(
                overlay
            );
        }

        requestAnimationFrame(() => {

            overlay.classList.add(
                "processing-visible"
            );
        });
    }


    function hideProcessingState() {

        const overlay =
            document.getElementById(
                "processing-overlay"
            );

        if (!overlay) {
            return;
        }

        overlay.classList.remove(
            "processing-visible"
        );

        setTimeout(() => {

            if (overlay.parentNode) {
                overlay.remove();
            }

        }, 250);
    }


    /* RESULT DISPLAY */

    function displayProcessingResult(
        result
    ) {

        appState.currentStats =
            result.after ||
            result.stats ||
            appState.currentStats;


        if (
            result.after &&
            typeof window.updateAnalysisStats ===
            "function"
        ) {

            window.updateAnalysisStats(
                result.after
            );
        }


        if (
            typeof window.renderResults ===
            "function"
        ) {

            window.renderResults(
                result
            );
        }


        if (
            typeof window.showSection ===
            "function"
        ) {

            const resultsSection =
                document.getElementById(
                    "results-section"
                );

            if (resultsSection) {
                showSection(
                    "results-section"
                );
            }
        }
    }


    /*  MAIN PROCESS FUNCTION  */

    async function processSelectedOperations(
        operations
    ) {

        if (!Array.isArray(operations) ||
            operations.length === 0) {

            showToast(
                "No cleaning operations selected.",
                "error"
            );

            return;
        }


        if (!appState.sessionId) {

            showToast(
                "Your dataset session is missing or expired.",
                "error"
            );

            return;
        }


        if (appState.isProcessing) {
            return;
        }


        appState.isProcessing = true;

        setGlobalLoading(true);

        showProcessingState();


        try {

            const payload = {
                operations: operations
            };


            const result =
                await apiJson(
                    `/api/operations/${encodeURIComponent(
                        appState.sessionId
                    )}`,
                    {
                        method: "POST",
                        body: payload
                    }
                );


            if (!result.success) {

                throw new Error(
                    result.error ||
                    "Dataset processing failed."
                );
            }


            displayProcessingResult(
                result
            );


            showToast(
                "Dataset cleaned successfully.",
                "success"
            );


        } catch (error) {

            console.error(
                "Processing error:",
                error
            );


            showToast(
                error.message ||
                "Unable to process the dataset.",
                "error"
            );


        } finally {

            hideProcessingState();

            appState.isProcessing =
                false;

            setGlobalLoading(
                false
            );


            if (
                window.workspace &&
                typeof window.workspace.updateProcessButton ===
                "function"
            ) {

                window.workspace
                    .updateProcessButton();
            }
        }
    }

    /*  PUBLIC API  */

    window.processSelectedOperations =
        processSelectedOperations;

    window.startProcessing =
        processSelectedOperations;


})();