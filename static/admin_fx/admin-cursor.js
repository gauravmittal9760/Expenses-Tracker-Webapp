/* =========================================================
   SpendWise Admin Panel — Custom Animated Cursor
   Small dot glued to the real pointer + a glowing ring that
   trails behind it with smooth easing (lerp). Auto-disables
   itself on touch-only devices so mobile admins are unaffected.
   ========================================================= */
(function () {
    "use strict";

    // Skip entirely on touch/coarse-pointer devices (phones/tablets)
    var isTouch =
        window.matchMedia &&
        window.matchMedia("(hover: none), (pointer: coarse)").matches;

    if (isTouch) return;

    document.documentElement.classList.add("admin-cursor-active");

    var dot = document.createElement("div");
    dot.id = "admin-cursor-dot";

    var ring = document.createElement("div");
    ring.id = "admin-cursor-ring";

    document.addEventListener("DOMContentLoaded", function () {
        document.body.appendChild(dot);
        document.body.appendChild(ring);
    });

    // If the script is placed at the end of <body>, DOM is already ready
    if (document.readyState === "interactive" || document.readyState === "complete") {
        document.body.appendChild(dot);
        document.body.appendChild(ring);
    }

    var mouseX = window.innerWidth / 2;
    var mouseY = window.innerHeight / 2;

    // Ring position (lagging, eased)
    var ringX = mouseX;
    var ringY = mouseY;

    var EASE = 0.16; // lower = more lag/trail, higher = snappier

    window.addEventListener("mousemove", function (e) {
        mouseX = e.clientX;
        mouseY = e.clientY;

        dot.style.transform =
            "translate(-50%, -50%) translate(" + mouseX + "px," + mouseY + "px)";

        document.documentElement.classList.remove("admin-cursor-hidden");
    });

    window.addEventListener("mouseleave", function () {
        document.documentElement.classList.add("admin-cursor-hidden");
    });

    window.addEventListener("mousedown", function () {
        document.documentElement.classList.add("admin-cursor-down");
    });

    window.addEventListener("mouseup", function () {
        document.documentElement.classList.remove("admin-cursor-down");
    });

    function animateRing() {
        ringX += (mouseX - ringX) * EASE;
        ringY += (mouseY - ringY) * EASE;

        ring.style.transform =
            "translate(-50%, -50%) translate(" + ringX + "px," + ringY + "px)";

        requestAnimationFrame(animateRing);
    }

    requestAnimationFrame(animateRing);

    // Hover-grow effect over anything clickable
    var HOVER_SELECTOR =
        "a, button, input, select, textarea, label, [role='button'], .clickable, [onclick]";

    document.addEventListener(
        "mouseover",
        function (e) {
            if (e.target.closest && e.target.closest(HOVER_SELECTOR)) {
                document.documentElement.classList.add("admin-cursor-hover");
            }
        },
        true
    );

    document.addEventListener(
        "mouseout",
        function (e) {
            if (e.target.closest && e.target.closest(HOVER_SELECTOR)) {
                if (
                    !e.relatedTarget ||
                    !(e.relatedTarget.closest && e.relatedTarget.closest(HOVER_SELECTOR))
                ) {
                    document.documentElement.classList.remove("admin-cursor-hover");
                }
            }
        },
        true
    );
})();
