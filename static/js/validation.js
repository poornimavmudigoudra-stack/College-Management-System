/* Client-side validation helpers. The server always re-validates; this is just faster feedback. */
document.addEventListener("DOMContentLoaded", () => {
    const PHONE_PATTERN = /^\+?[0-9\s-]{7,15}$/;

    const showError = (input, message) => {
        input.classList.add("is-invalid");
        let feedback = input.parentElement.querySelector(".js-feedback");
        if (!feedback) {
            feedback = document.createElement("div");
            feedback.className = "invalid-feedback d-block js-feedback";
            input.insertAdjacentElement("afterend", feedback);
        }
        feedback.textContent = message;
    };

    const clearError = (input) => {
        input.classList.remove("is-invalid");
        input.parentElement.querySelector(".js-feedback")?.remove();
    };

    const validate = (input) => {
        clearError(input);
        const value = input.value.trim();
        if (input.required && !value && input.type !== "file") {
            showError(input, "This field is required.");
            return false;
        }
        if (value && input.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
            showError(input, "Enter a valid email address.");
            return false;
        }
        if (value && /phone/i.test(input.name) && !PHONE_PATTERN.test(value)) {
            showError(input, "Enter a valid phone number (7-15 digits).");
            return false;
        }
        if (value && input.type === "number") {
            const number = parseFloat(value);
            if (input.min !== "" && number < parseFloat(input.min)) { showError(input, `Minimum value is ${input.min}.`); return false; }
            if (input.max !== "" && number > parseFloat(input.max)) { showError(input, `Maximum value is ${input.max}.`); return false; }
        }
        if (input.name.endsWith("password2")) {
            const password1 = input.form.querySelector('input[name$="password1"]');
            if (password1 && password1.value !== input.value) {
                showError(input, "The two passwords do not match.");
                return false;
            }
        }
        return true;
    };

    document.querySelectorAll("form.needs-validation").forEach((form) => {
        const fields = form.querySelectorAll("input:not([type=hidden]):not([type=checkbox]):not([type=radio]), select, textarea");
        fields.forEach((field) => field.addEventListener("blur", () => validate(field)));

        form.addEventListener("submit", (event) => {
            let valid = true;
            fields.forEach((field) => { if (!validate(field)) valid = false; });
            if (!valid) {
                event.preventDefault();
                form.querySelector(".is-invalid")?.focus();
            }
        });
    });
});
