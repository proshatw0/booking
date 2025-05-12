document.addEventListener('DOMContentLoaded', () => {
    const openModalBtn = document.getElementById('open-modal-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const modalOverlay = document.getElementById('modal-overlay');

    if (openModalBtn && closeModalBtn && modalOverlay) {
        openModalBtn.addEventListener('click', () => {
            modalOverlay.classList.add('active');
        });

        closeModalBtn.addEventListener('click', () => {
            modalOverlay.classList.remove('active');
        });

        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                modalOverlay.classList.remove('active');
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', () => {
    const editModalOverlay = document.getElementById('edit-modal-overlay');
    const closeEditModalBtn = document.getElementById('close-edit-modal-btn');
    
    const editButtons = document.querySelectorAll('.edit-btn');
    
    editButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const userId = e.target.getAttribute('data-user-id');  
            
            fetch(`/brewmaster-secret/staff/edit/${userId}`, {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                if (data && data.id !== undefined) {
                    document.querySelector('[name="last_name_edit"]').value = data.last_name || ''; 
                    document.querySelector('[name="first_name_edit"]').value = data.first_name || ''; 
                    document.querySelector('[name="middle_name_edit"]').value = data.middle_name || ''; 
                    document.querySelector('[name="login_edit"]').value = data.login || '';  
                    document.querySelector('[name="position_id_edit"]').value = data.position_id || ''; 

                    document.querySelector('#user_id_edit').value = data.id;

                    editModalOverlay.classList.add('active');
                } else {
                    console.error('Невалидные данные для пользователя', data);
                }
            })
            .catch(error => {
                console.log('Ошибка:', error);
            });
        });
    });

    if (closeEditModalBtn) {
        closeEditModalBtn.addEventListener('click', () => {
            editModalOverlay.classList.remove('active');
        });
    }

    editModalOverlay.addEventListener('click', (e) => {
        if (e.target === editModalOverlay) {
            editModalOverlay.classList.remove('active');
        }
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const deleteBtns = document.querySelectorAll('.delete-btn');
    const modalOverlay = document.getElementById('delete-modal-overlay');
    const confirmText = document.getElementById('delete-confirm-text');
    const deleteConfirmBtn = document.getElementById('delete-confirm-btn');
    const deleteCancelBtn = document.getElementById('delete-cancel-btn');
    let userIdToDelete = null;
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', (event) => {
            event.preventDefault();
            const userId = event.target.getAttribute('data-user-id');
            const userName = event.target.getAttribute('data-user-name');
            
            confirmText.textContent = `Подтвердить удаление пользователя ${userName}`;

            userIdToDelete = userId;
            
            modalOverlay.classList.add('active');
        });
    });
    deleteConfirmBtn.addEventListener('click', () => {
        if (userIdToDelete !== null) {
            fetch(`/brewmaster-secret/staff/delete/${userIdToDelete}`, {
                method: 'POST',
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = response.url;
                } else {
                    alert('Не удалось удалить пользователя');
                }
            })
            .catch(error => {
                alert('Ошибка при удалении пользователя');
            });
        }
    });
    deleteCancelBtn.addEventListener('click', () => {
        modalOverlay.classList.remove('active');
    });
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.classList.remove('active');
        }
    });
});