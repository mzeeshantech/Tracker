document.getElementById("toggleFilterBtn").addEventListener("click", function () {
    const filterSection = document.getElementById("filterSection");
    if (filterSection.style.display === "none") {
        filterSection.style.display = "block";
    } else {
        filterSection.style.display = "none";
    }
});


document.querySelectorAll('.clickable').forEach(row => {
        row.addEventListener('click', function () {
            const icon = this.querySelector('.toggle-icon');
            if (icon.classList.contains('bi-plus-circle')) {
                icon.classList.remove('bi-plus-circle');
                icon.classList.add('bi-dash-circle');
            } else {
                icon.classList.remove('bi-dash-circle');
                icon.classList.add('bi-plus-circle');
            }
        });
    });