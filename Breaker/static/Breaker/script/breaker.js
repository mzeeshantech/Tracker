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
//
//
//
//
//$(document).ready(function() {
//    $('tr[data-bs-toggle="collapse"]').click(function() {
//        var targetId = $(this).data('bs-target');
//        console.log(targetId)
//        var breakerId = targetId.replace('#detailsRow', '');
//        var startDate = $('#start_date').val();
//        var endDate = $('#end_date').val();
//        var location = $('#location').val();
//
//        var container = $(targetId);
//
//        $.ajax({
//            url: '/get-breaker-detail/', // The URL to the server
//            type: 'GET', // The HTTP method to use
//            data: {
//                breaker_id: breakerId,
//                start_date: startDate,
//                end_date: endDate,
//                location: location
//            },
//            success: function(response) {
////                $(targetId + ' .child-row').remove(); // Clear existing rows
//                 container.empty();
//                console.log(response);
//
//                response.data.forEach(function(item) {
//                    console.log(item);
//                    var rowHtml = `
//                        <tr id="detailsRow${item.breaker_id}" class="child-row">
//                            <td></td>
//                            <td>${item.breaker_id}</td>
//                            <td>${item.start_time || 'N/A'}</td>
//                            <td>${item.end_time || 'N/A'}</td>
//                            <td>${item.duration}</td>
//                            <td>${item.open_by_cmd ? '<i class="bi bi-check text-success"></i>' : '<i class="bi bi-x text-danger"></i>'}</td>
//                            <td>${item.close_by_cmd ? '<i class="bi bi-check text-success"></i>' : '<i class="bi bi-x text-danger"></i>'}</td>
//                        </tr>
//                    `;
////                    $(targetId).append(rowHtml); // Append new row
//                    container.append(rowHtml);
//                });
//
//                // Toggle icons for the collapse action
//                $(this).find('.toggle-icon').toggleClass('bi-plus-circle bi-minus-circle');
//            },
//            error: function(xhr, status, error) {
//                console.error("An error occurred: " + status + "\nError: " + error);
//            }
//        });
//    });
//});



$(document).ready(function() {
    $('tr[data-bs-toggle="collapse"]').click(function() {
        var targetId = $(this).data('bs-target');
        var breakerId = targetId.replace('#detailsRow', '');
        var startDate = $('#start_date').val();
        var endDate = $('#end_date').val();
        var location = $('#location').val();

        // Ensure we're targeting the correct place to append rows:
        var container = $(this); // Use 'this' to refer to the clicked row

        if (container.hasClass('close'))
        {
            $.ajax({
                url: '/get-breaker-detail/', // The URL to the server
                type: 'GET', // The HTTP method to use
                data: {
                    breaker_id: breakerId,
                    start_date: startDate,
                    end_date: endDate,
                    location: location
                },
                success: function(response) {
                    // Clear existing child rows that follow the container
                    container.nextAll('.child-row').remove();

                    response.data.forEach(function(item) {
                        var rowHtml = `
                            <tr id="detailsRow${item.breaker_id}" class="child-row">
                                <td></td>
                                <td>${item.breaker_id}</td>
                                <td>${item.start_time || 'N/A'}</td>
                                <td>${item.end_time || 'N/A'}</td>
                                <td>${item.duration}</td>
                                <td>${item.open_by_cmd ? '<i class="bi bi-check text-success"></i>' : '<i class="bi bi-x text-danger"></i>'}</td>
                                <td>${item.close_by_cmd ? '<i class="bi bi-check text-success"></i>' : '<i class="bi bi-x text-danger"></i>'}</td>
                            </tr>
                        `;
                        // Append new row directly after the container
                        container.after(rowHtml);
                    });

                    // Toggle icons for the collapse action
                    $(this).find('.toggle-icon').toggleClass('bi-plus-circle bi-minus-circle');
                    container.toggleClass('close open');
                },
                error: function(xhr, status, error) {
                    console.error("An error occurred: " + status + "\nError: " + error);
                }
            });
        } else {
            container.toggleClass('open close');

            var parentId = container.attr('id');

            // Output to console for verification

            // Construct the selector for child rows based on parent ID
            var childRowSelector = 'tr.child-row#' + parentId.replace('id_', '');

            // Find all child rows matching the selector
            var childRows = $(childRowSelector);

            childRows.remove();
        }
    });
});

//
//function updatePaginationControls(currentPage, totalPages) {
//    var pagination = $('#pagination-controls');
//    pagination.empty();  // Clear existing
//    // Add new controls
//    for (let i = 1; i <= totalPages; i++) {
//        var activeClass = i === currentPage ? 'active' : '';
//        var pageItem = `<li class="page-item ${activeClass}"><a class="page-link" href="#" onclick="fetchPageData(${i});">${i}</a></li>`;
//        pagination.append(pageItem);
//    }
//}
//
//function fetchPageData(page) {
//    $.ajax({
//        url: '/get_paginated_data/',
//        data: { page: page },
//        success: function(response) {
//            // Update your table or display area with the new data
//            updateTable(response.data);
//            updatePaginationControls(page, response.total_pages);
//        }
//    });
//}
//
//
//
//function updateTable(data) {
//    var table = $('#your-table-body-id');
//    table.empty();  // Clear existing data
//    data.forEach(function(item) {
//        var row = `<tr>
//            <td>${item.column1}</td>
//            <td>${item.column2}</td>
//            // Add more columns as needed
//        </tr>`;
//        table.append(row);
//    });
//}
//
//
//
//
//$(document).ready(function() {
//    fetchPageData(1);  // Load first page on page load
//});


$(document).ready(function() {
    $('#pagination-controls a.next-btn').click(function(e) {
        e.preventDefault(); // Prevent the default anchor behavior
        var page = $(this).data('page');
        var direction = $(this).data('direction');

        var currentPage = parseInt($('#current_page').val(), 1);

        var new_val = parseInt($('#current_page').val()) + 1
        $('#current_page').val(new_val);
        $('#locationForm').submit();
    });

    $('#pagination-controls a.back-btn').click(function(e) {
        e.preventDefault(); // Prevent the default anchor behavior
        var page = $(this).data('page');
        var direction = $(this).data('direction');

        var currentPage = parseInt($('#current_page').val(), 1);

        var new_val = parseInt($('#current_page').val()) - 1
        $('#current_page').val(new_val);
        $('#locationForm').submit();
    });

    document.getElementById('exportPdf').addEventListener('click', function() {
        var startDate = document.getElementById('start_date').value;
        var endDate = document.getElementById('end_date').value;
        var location = document.getElementById('location').value;
        var breaker = document.getElementById('breaker').value;

        var queryParams = new URLSearchParams({
            start_date: startDate,
            end_date: endDate,
            location: location,
            breaker: breaker
        });

        // Open the URL with the query parameters in a new tab
        var url = `/generate_pdf/?${queryParams.toString()}`;
        window.open(url, '_blank');
    });
});
