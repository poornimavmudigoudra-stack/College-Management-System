/* General UI behaviour shared by every page. */
document.addEventListener("DOMContentLoaded", () => {
    // Auto-dismiss success/info alerts after 5 seconds
    document.querySelectorAll(".messages .alert-success, .messages .alert-info").forEach((alert) => {
        setTimeout(() => bootstrap.Alert.getOrCreateInstance(alert).close(), 5000);
    });

    // Ask for confirmation before submitting forms marked with data-confirm
    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (!window.confirm(form.dataset.confirm)) event.preventDefault();
        });
    });

    // Attendance: "All Present" / "All Absent" buttons
    document.querySelectorAll("[data-mark-all]").forEach((button) => {
        button.addEventListener("click", () => {
            const value = button.dataset.markAll;
            document.querySelectorAll(`input[type="radio"][value="${value}"]`).forEach((radio) => {
                radio.checked = true;
            });
        });
    });

    // Show / hide password toggle on the login page
    document.querySelectorAll("[data-toggle-password]").forEach((button) => {
        button.addEventListener("click", () => {
            const input = document.getElementById(button.dataset.togglePassword);
            const show = input.type === "password";
            input.type = show ? "text" : "password";
            button.innerHTML = show ? '<i class="bi bi-eye-slash"></i>' : '<i class="bi bi-eye"></i>';
        });
    });

    // Live preview for student / faculty photo uploads
    const preview = document.getElementById("photo-preview");
    const photoInput = document.querySelector('input[type="file"][name$="photo"]');
    if (preview && photoInput) {
        photoInput.addEventListener("change", () => {
            const [file] = photoInput.files;
            if (!file) return preview.classList.add("d-none");
            preview.src = URL.createObjectURL(file);
            preview.classList.remove("d-none");
        });
    }

    // Marks entry: highlight marks below the pass mark
    document.querySelectorAll(".marks-input").forEach((input) => {
        const check = () => {
            const value = parseFloat(input.value);
            input.classList.toggle("below-pass", !Number.isNaN(value) && value < parseFloat(input.dataset.pass));
        };
        input.addEventListener("input", check);
        check();
    });
});
