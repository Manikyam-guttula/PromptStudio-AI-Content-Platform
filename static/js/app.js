
const $ = (id) => document.getElementById(id);

let activityChart = null;
let toastTimer = null;

function showToast(message) {
    const toast = $("toast");
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2500);
}

async function apiRequest(url, data = null) {
    const options = data === null
        ? {}
        : {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        };

    const response = await fetch(url, options);
    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || "Something went wrong.");
    }

    return result;
}

function navigate(page) {
    document.querySelectorAll(".page").forEach(section => {
        section.classList.toggle("active", section.id === page);
    });

    document.querySelectorAll(".nav-link").forEach(button => {
        button.classList.toggle("active", button.dataset.page === page);
    });

    const selected = document.querySelector(`.nav-link[data-page="${page}"]`);
    $("breadcrumb-title").textContent =
        selected ? selected.textContent.trim().replace(/^[^\w]+/, "") : page;

    if (page === "dashboard") loadDashboard();
    if (page === "history") loadHistory();
    if (page === "analytics") loadAnalytics();
}

document.querySelectorAll("[data-page]").forEach(button => {
    button.addEventListener("click", () => navigate(button.dataset.page));
});

document.querySelectorAll("[data-open]").forEach(button => {
    button.addEventListener("click", () => navigate(button.dataset.open));
});

async function generateContent() {
    const prompt = $("prompt").value.trim();

    if (!prompt) {
        showToast("Please enter a prompt first.");
        return;
    }

    const button = $("generate-btn");
    button.disabled = true;
    button.textContent = "Generating...";

    $("generate-result").textContent = "Creating your content. Please wait...";

    try {
        const data = await apiRequest("/api/generate", {
            prompt: prompt,
            content_type: $("content-type").value,
            tone: $("tone").value
        });

        $("generate-result").textContent = data.result;
        $("copy-generate").disabled = false;
        showToast("Content generated successfully!");
        loadDashboard();
    } catch (error) {
        $("generate-result").textContent = error.message;
        showToast(error.message);
    } finally {
        button.disabled = false;
        button.textContent = "✦ Generate Content →";
    }
}

async function summarizeText() {
    const text = $("summary-input").value.trim();

    if (!text) {
        showToast("Please enter text to summarize.");
        return;
    }

    const button = $("summarize-btn");
    button.disabled = true;
    button.textContent = "Summarizing...";

    $("summary-result").textContent = "Preparing your summary...";

    try {
        const data = await apiRequest("/api/summarize", { text });
        $("summary-result").textContent = data.result;
        $("copy-summary").disabled = false;
        showToast("Summary created successfully!");
        loadDashboard();
    } catch (error) {
        $("summary-result").textContent = error.message;
        showToast(error.message);
    } finally {
        button.disabled = false;
        button.textContent = "Summarize Text →";
    }
}

async function analyzeSentiment() {
    const text = $("sentiment-input").value.trim();

    if (!text) {
        showToast("Please enter text to analyze.");
        return;
    }

    const button = $("sentiment-btn");
    button.disabled = true;
    button.textContent = "Analyzing...";

    $("sentiment-result").textContent = "Analyzing your text...";

    try {
        const data = await apiRequest("/api/sentiment", { text });
        const result = data.result;

        $("sentiment-result").textContent =
            typeof result === "string" ? result : JSON.stringify(result, null, 2);

        showToast("Sentiment analysis completed!");
        loadDashboard();
    } catch (error) {
        $("sentiment-result").textContent = error.message;
        showToast(error.message);
    } finally {
        button.disabled = false;
        button.textContent = "Analyze Sentiment →";
    }
}

function copyResult(elementId) {
    const text = $(elementId).textContent;

    navigator.clipboard.writeText(text)
        .then(() => showToast("Copied to clipboard!"))
        .catch(() => showToast("Unable to copy. Please select the text manually."));
}

$("generate-btn").addEventListener("click", generateContent);
$("summarize-btn").addEventListener("click", summarizeText);
$("sentiment-btn").addEventListener("click", analyzeSentiment);

$("copy-generate").addEventListener("click", () => copyResult("generate-result"));
$("copy-summary").addEventListener("click", () => copyResult("summary-result"));

async function loadDashboard() {
    try {
        const data = await apiRequest("/api/history");
        const items = data.items || [];

        const generated = items.filter(item =>
            item.tool.toLowerCase().includes("generation")
        ).length;

        const summaries = items.filter(item =>
            item.tool.toLowerCase().includes("summar")
        ).length;

        const sentiments = items.filter(item =>
            item.tool.toLowerCase().includes("sentiment")
        ).length;

        $("total-operations").textContent = data.items.length;
        $("total-generated").textContent = generated;
        $("total-summaries").textContent = summaries;
        $("total-sentiments").textContent = sentiments;

        const recent = $("recent-activity");

        if (!items.length) {
            recent.textContent = "No activity yet. Start using your AI tools!";
        } else {
            recent.innerHTML = items.slice(0, 5).map(item => `
                <div class="recent-item">
                    <b>${escapeHTML(item.tool)}</b>
                    <small>${escapeHTML(item.created_at)}</small>
                </div>
            `).join("");
        }
    } catch (error) {
        console.error("Dashboard error:", error);
    }
}

async function loadHistory() {
    const container = $("history-list");
    container.textContent = "Loading history...";

    try {
        const data = await apiRequest("/api/history");
        const items = data.items || [];

        if (!items.length) {
            container.textContent = "No history available yet.";
            return;
        }

        container.innerHTML = items.map(item => `
            <div class="history-item">
                <b>${escapeHTML(item.tool)}</b>
                <small>${escapeHTML(item.created_at)}</small>
                <p>${escapeHTML(item.prompt.slice(0, 220))}</p>
            </div>
        `).join("");
    } catch (error) {
        container.textContent = error.message;
    }
}

async function loadAnalytics() {
    try {
        const data = await apiRequest("/api/analytics");

        $("analytics-total").textContent = data.total;

        const labels = data.by_tool.map(item => item.tool);
        const values = data.by_tool.map(item => item.count);

        const canvas = $("activity-chart");
        if (!canvas) return;

        if (activityChart) activityChart.destroy();

        activityChart = new Chart(canvas, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Number of activities",
                    data: values,
                    backgroundColor: "#8272e9",
                    borderRadius: 7,
                    maxBarThickness: 55
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    } catch (error) {
        console.error("Analytics error:", error);
    }
}

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[character]);
}

$("refresh-history").addEventListener("click", loadHistory);
$("refresh-analytics").addEventListener("click", loadAnalytics);

document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});
