$(document).ready(function() {
    // 显示提示模态框的函数
    function showAlert(message, isError = false) {
        $('#alertModalBody').text(message);
        if (isError) {
            $('#alertModalLabel').text('错误').addClass('text-danger');
        } else {
            $('#alertModalLabel').text('成功').removeClass('text-danger').addClass('text-success');
        }
        const alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
        alertModal.show();
    }

    // 刷新页面的函数
    function refreshPage() {
        location.reload();
    }

    // 添加新消息
    $('#saveMessageBtn').click(function() {
        const messageId = $('#messageId').val().trim();
        const messageContent = $('#messageContent').val().trim();

        if (!messageId || !messageContent) {
            showAlert('请填写所有必填字段', true);
            return;
        }

        $.ajax({
            url: '/admin/add',
            type: 'POST',
            data: {
                id: messageId,
                content: messageContent
            },
            success: function(response) {
                if (response.success) {
                    showAlert('消息添加成功！');
                    $('#addMessageModal').modal('hide');
                    setTimeout(refreshPage, 1500);
                } else {
                    showAlert('添加失败: ' + response.error, true);
                }
            },
            error: function(xhr) {
                let errorMsg = '添加失败';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg += ': ' + xhr.responseJSON.error;
                }
                showAlert(errorMsg, true);
            }
        });
    });

    // 打开编辑模态框
    $(document).on('click', '.edit-btn', function() {
        const messageId = $(this).data('id');
        const messageContent = $(this).data('content');

        $('#editMessageId').val(messageId);
        $('#editMessageIdDisplay').val(messageId);
        $('#editMessageContent').val(messageContent);

        const editModal = new bootstrap.Modal(document.getElementById('editMessageModal'));
        editModal.show();
    });

    // 更新消息
    $('#updateMessageBtn').click(function() {
        const messageId = $('#editMessageId').val();
        const messageContent = $('#editMessageContent').val().trim();

        if (!messageContent) {
            showAlert('消息内容不能为空', true);
            return;
        }

        $.ajax({
            url: '/admin/update',
            type: 'POST',
            data: {
                id: messageId,
                content: messageContent
            },
            success: function(response) {
                if (response.success) {
                    showAlert('消息更新成功！');
                    $('#editMessageModal').modal('hide');
                    setTimeout(refreshPage, 1500);
                } else {
                    showAlert('更新失败: ' + response.error, true);
                }
            },
            error: function(xhr) {
                let errorMsg = '更新失败';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg += ': ' + xhr.responseJSON.error;
                }
                showAlert(errorMsg, true);
            }
        });
    });

    // 打开删除确认模态框
    $(document).on('click', '.delete-btn', function() {
        const messageId = $(this).data('id');
        $('#deleteMessageId').text(messageId);

        const deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
        deleteModal.show();
    });

    // 确认删除消息
    $('#confirmDeleteBtn').click(function() {
        const messageId = $('#deleteMessageId').text();

        $.ajax({
            url: '/admin/delete',
            type: 'POST',
            data: {
                id: messageId
            },
            success: function(response) {
                if (response.success) {
                    showAlert('消息删除成功！');
                    $('#deleteConfirmModal').modal('hide');
                    setTimeout(refreshPage, 1500);
                } else {
                    showAlert('删除失败: ' + response.error, true);
                }
            },
            error: function(xhr) {
                let errorMsg = '删除失败';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg += ': ' + xhr.responseJSON.error;
                }
                showAlert(errorMsg, true);
            }
        });
    });

    // 模态框关闭时重置表单
    $('#addMessageModal').on('hidden.bs.modal', function() {
        $('#messageId').val('');
        $('#messageContent').val('');
    });

    // 添加表格行动画效果
    $('#messageTableBody tr').addClass('fade-in');

    // 复制链接到剪贴板的功能
    $(document).on('click', '.copy-link', function(e) {
        e.preventDefault();
        const link = $(this).data('link');

        navigator.clipboard.writeText(window.location.origin + link).then(function() {
            showAlert('链接已复制到剪贴板！');
        }, function() {
            showAlert('复制失败，请手动复制链接', true);
        });
    });
});
