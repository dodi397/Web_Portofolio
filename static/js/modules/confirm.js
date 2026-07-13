export function initConfirmDialogs() {
    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (e) => {
            const message = form.getAttribute("data-confirm") || "Yakin ingin melanjutkan?";
            if (!window.confirm(message)) {
                e.preventDefault();
            }
        });
    });
}
