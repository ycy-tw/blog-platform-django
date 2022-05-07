$(document).ready(function () {
    $('#dt').DataTable({
        "order": [[0, "desc"]],
        "lengthChange": false,
        "responsive": true,
        "columns": [
            { "width": "10%" },
            { "width": "40%" },
            { "width": "10%" },
            { "width": "10%" },
            { "width": "10%" },
            { "width": "10%" },
        ],
        "pageLength": 10,
    });
});

