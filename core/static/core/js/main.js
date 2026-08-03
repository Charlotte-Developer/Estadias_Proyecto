document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.querySelector(".sidebar");

    const toggle = document.getElementById("sidebarToggle");

    if (toggle) {

        toggle.addEventListener("click", function () {

            sidebar.classList.toggle("show");

        });

    }

});