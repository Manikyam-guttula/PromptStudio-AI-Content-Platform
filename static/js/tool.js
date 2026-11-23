
document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("aiToolForm");

    if (!form) return;

    const button = document.getElementById("generateButton");
    const loading = document.getElementById("loadingMessage");
    const resultSection = document.getElementById("resultSection");
    const resultOutput = document.getElementById("resultOutput");
    const errorMessage = document.getElementById("errorMessage");
    const copyButton = document.getElementById("copyButton");
    const regenerateButton = document.getElementById("regenerateButton");

    let lastPayload = null;

    async function submitPayload(payload) {

        errorMessage.hidden = true;
        loading.hidden = false;

        button.disabled = true;
        button.textContent = "Generating...";

        try {

            const response = await fetch(form.dataset.endpoint, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)

            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "Something went wrong.");
            }

            resultOutput.textContent = data.result || data.response || "";

            resultSection.hidden = false;

            resultSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        } catch (error) {

            errorMessage.textContent = error.message;
            errorMessage.hidden = false;

        } finally {

            loading.hidden = true;

            button.disabled = false;
            button.textContent = "Generate Result ✦";

        }

    }

    form.addEventListener("submit", event => {

        event.preventDefault();

        lastPayload = Object.fromEntries(
            new FormData(form).entries()
        );

        submitPayload(lastPayload);

    });

    if (copyButton) {

        copyButton.addEventListener("click", async () => {

            try {

                await navigator.clipboard.writeText(
                    resultOutput.textContent
                );

                copyButton.textContent = "Copied!";

                setTimeout(() => {
                    copyButton.textContent = "Copy Result";
                }, 1500);

            } catch {

                errorMessage.textContent =
                    "Unable to copy automatically. Please select and copy the result.";

                errorMessage.hidden = false;

            }

        });

    }

    if (regenerateButton) {

        regenerateButton.addEventListener("click", () => {

            if (lastPayload) {
                submitPayload(lastPayload);
            }

        });

    }

});
