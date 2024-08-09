document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('delete-button').addEventListener('click', function () {
        document.getElementById('confirmation-dialog').style.display = 'block';
    });

    document.getElementById('cancel-button').addEventListener('click', function () {
        document.getElementById('confirmation-dialog').style.display = 'none';
    });
});