export function initReveals() {
    const reveals = document.querySelectorAll(".reveal");
    if (!reveals.length) return;

    requestAnimationFrame(() => {
        reveals.forEach((el) => el.classList.add("reveal-visible"));
    });
}
