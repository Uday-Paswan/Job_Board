document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.querySelector(".nav-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });
    }

    function dismissToast(toast) {
        toast.classList.add("toast-hide");
        setTimeout(() => toast.remove(), 350);
    }

    document.querySelectorAll(".toast").forEach(function (toast) {
        // manual close button
        const closeBtn = toast.querySelector(".toast-close");
        if (closeBtn) {
            closeBtn.addEventListener("click", () => dismissToast(toast));
        }
        // auto-dismiss after 4s (matches the progress bar animation)
        setTimeout(() => dismissToast(toast), 4000);
    });
});