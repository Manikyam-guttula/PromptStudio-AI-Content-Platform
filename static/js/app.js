
document.addEventListener("DOMContentLoaded", () => {

    // ================= HISTORY =================

    const historyList = document.getElementById("historyList");
    const historyMessage = document.getElementById("historyMessage");

    if (historyList) {

        fetch("/api/history")

            .then(response => response.json())

            .then(data => {

                if (!data.success) {
                    throw new Error(data.error || "Unable to load history.");
                }

                historyMessage.textContent =
                    data.history.length ? "" : "No saved prompts yet.";

                data.history.forEach(item => {

                    const card = document.createElement("article");
                    card.className = "history-card";

                    const heading = document.createElement("div");
                    heading.className = "history-card-head";

                    const title = document.createElement("strong");
                    title.textContent = item.feature;

                    const date = document.createElement("span");
                    date.textContent = item.created_at;

                    heading.append(title, date);

                    const inputLabel = document.createElement("h4");
                    inputLabel.textContent = "Your Input";

                    const input = document.createElement("p");
                    input.textContent = item.user_input;

                    const outputLabel = document.createElement("h4");
                    outputLabel.textContent = "AI Result";

                    const output = document.createElement("p");
                    output.className = "history-output";
                    output.textContent = item.result;

                    const copy = document.createElement("button");
                    copy.className = "button secondary small";
                    copy.textContent = "Copy Result";

                    copy.addEventListener("click", async () => {

                        try {

                            await navigator.clipboard.writeText(
                                item.result || ""
                            );

                            copy.textContent = "Copied!";

                        } catch {

                            copy.textContent = "Copy unavailable";

                        }

                    });

                    card.append(
                        heading,
                        inputLabel,
                        input,
                        outputLabel,
                        output,
                        copy
                    );

                    historyList.appendChild(card);

                });

            })

            .catch(error => {

                historyMessage.textContent = error.message;

            });

    }


    // ================= ANALYTICS =================

    const analyticsList = document.getElementById("analyticsList");

    if (analyticsList) {

        fetch("/api/analytics")

            .then(response => response.json())

            .then(data => {

                if (!data.success) {
                    throw new Error(data.error || "Unable to load analytics.");
                }

                document.getElementById("analyticsTotal").textContent =
                    data.total_requests;

                document.getElementById("analyticsTools").textContent =
                    Object.keys(data.counts).length;

                analyticsList.replaceChildren();

                const entries = Object.entries(data.counts);

                if (entries.length === 0) {

                    analyticsList.textContent =
                        "No activity to display yet.";

                    return;

                }

                const maximum = Math.max(
                    ...entries.map(entry => entry[1]),
                    1
                );

                entries.forEach(([name, count]) => {

                    const row = document.createElement("div");
                    row.className = "analytics-row";

                    const label = document.createElement("div");
                    label.className = "analytics-label";

                    const title = document.createElement("span");
                    title.textContent = name;

                    const number = document.createElement("strong");
                    number.textContent = count;

                    label.append(title, number);

                    const track = document.createElement("div");
                    track.className = "progress-track";

                    const fill = document.createElement("div");
                    fill.className = "progress-fill";

                    fill.style.width =
                        `${(count / maximum) * 100}%`;

                    track.appendChild(fill);

                    row.append(label, track);

                    analyticsList.appendChild(row);

                });

            })

            .catch(error => {

                analyticsList.textContent = error.message;

            });

    }

});
