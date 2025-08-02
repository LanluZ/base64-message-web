$(document).ready(function() {
    // Helper function to show alerts
    function showAlert(message, type = 'success') {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = [
            `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
            `   <div>${message}</div>`,
            '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
            '</div>'
        ].join('');
        document.querySelector('main').prepend(wrapper);
    }

    // Reload page after a delay
    function refreshPage() {
        location.reload();
    }

    // Add new message
    $('#saveMessageBtn').click(function() {
        const form = $('#addMessageForm');
        const url = form.data('url');
        const messageId = $('#messageId').val().trim();
        const content = $('#messageContent').val().trim();

        if (!messageId || !content) {
            showAlert('ID 和内容不能为空。', 'danger');
            return;
        }

        $.post(url, { id: messageId, content: content })
            .done(function(data) {
                if (data.success) {
                    $('#addMessageModal').modal('hide');
                    showAlert('消息添加成功！');
                    setTimeout(refreshPage, 1000);
                }
            })
            .fail(function(jqXHR) {
                showAlert(jqXHR.responseJSON.error || '发生未知错误。', 'danger');
            });
    });

    // Populate edit modal
    $('#editMessageModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        const id = button.data('id');
        const content = button.data('content');
        const modal = $(this);
        modal.find('#editMessageId').val(id);
        modal.find('#editMessageIdDisplay').val(id);
        modal.find('#editMessageContent').val(content);
    });

    // Update message
    $('#updateMessageBtn').click(function() {
        const form = $('#editMessageForm');
        const url = form.data('url');
        const id = $('#editMessageId').val();
        const content = $('#editMessageContent').val().trim();

        if (!content) {
            showAlert('内容不能为空。', 'danger');
            return;
        }

        $.post(url, { id: id, content: content })
            .done(function(data) {
                if (data.success) {
                    $('#editMessageModal').modal('hide');
                    showAlert('消息更新成功！');
                    setTimeout(refreshPage, 1000);
                }
            })
            .fail(function(jqXHR) {
                showAlert(jqXHR.responseJSON.error || '发生未知错误。', 'danger');
            });
    });

    // Populate delete modal
    $('#deleteConfirmModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        const id = button.data('id');
        const modal = $(this);
        modal.find('#deleteMessageId').text(id);
    });

    // Confirm delete
    $('#confirmDeleteBtn').click(function() {
        const url = $(this).data('url');
        const id = $('#deleteMessageId').text();

        $.post(url, { id: id })
            .done(function(data) {
                if (data.success) {
                    $('#deleteConfirmModal').modal('hide');
                    showAlert('消息删除成功！');
                    setTimeout(refreshPage, 1000);
                }
            })
            .fail(function(jqXHR) {
                showAlert(jqXHR.responseJSON.error || '发生未知错误。', 'danger');
            });
    });
});
