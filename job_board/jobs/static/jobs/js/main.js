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
        const closeBtn = toast.querySelector(".toast-close");
        if (closeBtn) {
            closeBtn.addEventListener("click", () => dismissToast(toast));
        }
        setTimeout(() => dismissToast(toast), 4000);
    });

    // --- Custom logout confirmation modal ---
    const logoutForm = document.querySelector(".btn-logout")?.closest("form");
    const logoutModal = document.getElementById("logoutModal");
    const logoutCancel = document.getElementById("logoutCancel");
    const logoutConfirm = document.getElementById("logoutConfirm");

    if (logoutForm && logoutModal) {
        logoutForm.addEventListener("submit", function (e) {
            e.preventDefault(); // stop the real submit, show our modal instead
            logoutModal.classList.add("active");
        });

        logoutCancel.addEventListener("click", function () {
            logoutModal.classList.remove("active");
        });

        logoutConfirm.addEventListener("click", function () {
            logoutForm.submit(); // user confirmed, now actually submit the form
        });

        // also close if they click the dark overlay itself, outside the box
        logoutModal.addEventListener("click", function (e) {
            if (e.target === logoutModal) {
                logoutModal.classList.remove("active");
            }
        });
    }
});