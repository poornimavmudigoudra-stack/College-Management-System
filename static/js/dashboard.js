/* Admin dashboard: "Students per Course" bar chart (data comes from json_script). */
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("courseChart");
    const dataElement = document.getElementById("course-chart-data");
    if (!canvas || !dataElement || typeof Chart === "undefined") return;

    const data = JSON.parse(dataElement.textContent);
    new Chart(canvas, {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Students",
                data: data.values,
                backgroundColor: "rgba(59, 91, 219, 0.75)",
                borderRadius: 6,
                maxBarThickness: 48,
            }],
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, ticks: { precision: 0 } },
                x: { grid: { display: false } },
            },
        },
    });
});
