
document.addEventListener("DOMContentLoaded", () => {

    const sections = document.querySelectorAll(".page-section");
    const navButtons = document.querySelectorAll(".nav-btn");

    // Navigation
    function showSection(sectionId) {
        sections.forEach(section => {
            section.classList.toggle(
                "hidden",
                section.id !== sectionId
            );
        });

        navButtons.forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.section === sectionId
            );
        });

        if (sectionId === "history") loadHistory();
        if (sectionId === "analytics") loadAnalytics();
        if (sectionId === "dashboard") loadDashboard();
    }

    navButtons.forEach(button => {
        button.addEventListener("click", () => {
            showSection(button.dataset.section);
        });
    });

    document.querySelectorAll("[data-go]").forEach(button => {
        button.addEventListener("click", () => {
            showSection(button.dataset.go);
        });
    });

    // Common API request function
    async function sendRequest(url, data) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(data)
        });

        const raw = await response.text();

        let result;

        try {
            result = JSON.parse(raw);
        } catch {
            throw new Error(
                "Server returned an unexpected response. Check Flask terminal."
            );
        }

        if (!response.ok || !result.success) {
            throw new Error(result.error || "Request failed.");
        }

        return result;
    }

    // Show loading state
    function setLoading(button, loadingText, normalText) {
        button.disabled = loadingText !== null;
        button.textContent = loadingText || normalText;
    }

    // CONTENT GENERATOR
    const generateBtn = document.getElementById("generateBtn");

    generateBtn.addEventListener("click", async () => {
        const prompt = document.getElementById("prompt").value.trim();
        const tone = document.getElementById("tone").value;
        const contentType = document.getElementById("contentType").value;
        const output = document.getElementById("generateResult");

        if (!prompt) {
            output.textContent = "Please enter your prompt.";
            return;
        }

        setLoading(generateBtn, "Generating...", "Generate Content");
        output.textContent = "AI is generating your content...";

        try {
            const data = await sendRequest("/generate", {
                prompt: prompt,
                tone: tone,
                content_type: contentType
            });

            output.textContent = data.result;
            loadDashboard();

        } catch (error) {
            output.textContent = "Error: " + error.message;
        } finally {
            setLoading(generateBtn, null, "Generate Content");
        }
    });

    // TEXT SUMMARIZER
    const summarizeBtn = document.getElementById("summarizeBtn");

    summarizeBtn.addEventListener("click", async () => {
        const text = document.getElementById("summaryText").value.trim();
        const length = document.getElementById("summaryLength").value;
        const output = document.getElementById("summaryResult");

        if (!text) {
            output.textContent = "Please enter text to summarize.";
            return;
        }

        setLoading(summarizeBtn, "Summarizing...", "Generate Summary");
        output.textContent = "AI is summarizing your text...";

        try {
            const data = await sendRequest("/summarize", {
                text: text,
                length: length
            });

            output.textContent = data.summary;
            loadDashboard();

        } catch (error) {
            output.textContent = "Error: " + error.message;
        } finally {
            setLoading(summarizeBtn, null, "Generate Summary");
        }
    });

    // SENTIMENT ANALYZER
    const sentimentBtn = document.getElementById("sentimentBtn");

    sentimentBtn.addEventListener("click", async () => {
        const text = document.getElementById("sentimentText").value.trim();
        const output = document.getElementById("sentimentResult");

        if (!text) {
            output.textContent = "Please enter text to analyze.";
            return;
        }

        setLoading(sentimentBtn, "Analyzing...", "Analyze Sentiment");
        output.textContent = "AI is analyzing your text...";

        try {
            const data = await sendRequest("/sentiment", {
                text: text
            });

            output.textContent = data.sentiment;
            loadDashboard();

        } catch (error) {
            output.textContent = "Error: " + error.message;
        } finally {
            setLoading(sentimentBtn, null, "Analyze Sentiment");
        }
    });

    // COPY RESULT
    document.querySelectorAll("[data-copy]").forEach(button => {
        button.addEventListener("click", async () => {
            const target = document.getElementById(button.dataset.copy);
            const text = target.textContent.trim();

            if (!text) return;

            try {
                await navigator.clipboard.writeText(text);
                button.textContent = "Copied!";

                setTimeout(() => {
                    button.textContent = button.dataset.copy === "summaryResult"
                        ? "Copy Summary"
                        : "Copy Result";
                }, 1500);

            } catch {
                alert("Unable to copy. Please select and copy the text manually.");
            }
        });
    });

    // PROMPT HISTORY
    async function loadHistory() {
        const container = document.getElementById("historyList");
        container.textContent = "Loading history...";

        try {
            const response = await fetch("/history");
            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "Unable to load history.");
            }

            container.replaceChildren();

            if (!data.history.length) {
                container.textContent = "No prompt history available yet.";
                return;
            }

            data.history.forEach(item => {
                const card = document.createElement("article");
                card.className = "history-item";

                const heading = document.createElement("h3");
                heading.textContent = item.feature;

                const input = document.createElement("p");
                input.textContent = "Input: " + item.user_input;

                const result = document.createElement("p");
                result.textContent = "Result: " + item.result;

                const date = document.createElement("div");
                date.className = "history-date";

                const parsedDate = new Date(item.created_at);
                date.textContent = Number.isNaN(parsedDate.getTime())
                    ? item.created_at
                    : parsedDate.toLocaleString();

                card.append(heading, input, result, date);
                container.appendChild(card);
            });

        } catch (error) {
            container.textContent = "Error: " + error.message;
        }
    }

    // ANALYTICS
    async function loadAnalytics() {
        const totalElement = document.getElementById("analyticsTotal");
        const bars = document.getElementById("analyticsBars");

        totalElement.textContent = "Loading...";
        bars.replaceChildren();

        try {
            const response = await fetch("/analytics");
            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "Unable to load analytics.");
            }

            totalElement.textContent = data.total_activities;

            if (!data.feature_stats.length) {
                bars.textContent = "No analytics data available yet.";
                return;
            }

            const maxCount = Math.max(
                ...data.feature_stats.map(item => item.count),
                1
            );

            data.feature_stats.forEach(item => {
                const row = document.createElement("div");
                row.className = "analytics-row";

                const label = document.createElement("div");
                label.className = "analytics-label";

                const name = document.createElement("span");
                name.textContent = item.feature;

                const count = document.createElement("span");
                count.textContent = item.count;

                label.append(name, count);

                const track = document.createElement("div");
                track.className = "bar-track";

                const fill = document.createElement("div");
                fill.className = "bar-fill";
                fill.style.width = (item.count / maxCount * 100) + "%";

                track.appendChild(fill);
                row.append(label, track);
                bars.appendChild(row);
            });

        } catch (error) {
            totalElement.textContent = "0";
            bars.textContent = "Error: " + error.message;
        }
    }

    // DASHBOARD TOTAL
    async function loadDashboard() {
        try {
            const response = await fetch("/analytics");
            const data = await response.json();

            if (response.ok && data.success) {
                document.getElementById("totalActivities").textContent =
                    data.total_activities;
            }
        } catch (error) {
            console.error("Dashboard loading error:", error);
        }
    }

    // Initial dashboard data
    showSection("dashboard");
});