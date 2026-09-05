// Mobile nav toggle
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.querySelector(".nav-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });
    }

    // Auto-dismiss alerts after 4 seconds
    const alerts = document.querySelectorAll(".alert[data-auto-dismiss]");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = "opacity 0.4s ease";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });
});