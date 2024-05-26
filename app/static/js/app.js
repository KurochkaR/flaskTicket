$(document).ready(function() {

    $(this).on('click', '.fa-pen', function() {
        var ticketId = $(this).closest('tr').find('.ticket-title').attr('data-id')
        var editUrl = '/tickets/edit/' + ticketId;
        window.location.href = editUrl;
    });
    $(this).on('click', '.fa-trash', function() {
        var ticketId = $(this).closest('tr').find('.ticket-title').attr('data-id')
        var deleteUrl = '/tickets/delete/' + ticketId;
        window.location.href = deleteUrl;
    });
});