document.addEventListener('DOMContentLoaded', () => {
    const clearBtn = document.getElementById('clear-filters-btn');
    const form = document.querySelector('.filter-data');

    clearBtn.addEventListener('click', () => {
        form.querySelectorAll('input, select').forEach(el => {
            if (el.type === 'select-one' || el.type === 'text' || el.type === 'date' || el.type === 'time') {
                el.value = '';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('reservation-modal-overlay');
    const openBtn = document.getElementById('open-reservation-modal-btn');
    const closeBtn = document.getElementById('close-reservation-modal-btn');

    openBtn.addEventListener('click', () => {
        modal.classList.add('active');
    });

    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('reservation-modal-overlay-edit');
    const closeBtn = document.getElementById('close-reservation-modal-btn-edit');
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
    document.querySelectorAll('.clickable-row').forEach(function(row) {
        row.addEventListener('click', function() {
            const reservationId = this.getAttribute('data-id');
            openEditModal(reservationId);
        });
    });
    document.querySelectorAll('.clickable-row').forEach(function(row) {
        row.addEventListener('click', function() {
            const reservationId = this.getAttribute('data-id');
            openEditModal(reservationId); 
        });
    });
    function openEditModal(reservationId) {
        fetch(`/brewmaster-secret/reservations/edit/${reservationId}`)
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    document.getElementById('reservation-id').value = data.id;
                    document.getElementById('reservation-name').value = data.name;
                    document.getElementById('reservation-date').value = data.date;
                    document.getElementById('reservation-start-time').value = data.start_time;
                    document.getElementById('reservation-end-time').value = data.end_time;
                    document.getElementById('reservation-table').value = data.table_number;
                    document.getElementById('reservation-num-people').value = data.num_people;
                    document.getElementById('reservation-phone').value = data.phone;
                    document.getElementById('reservation-email').value = data.email;
                    document.getElementById('reservation-special-requests').value = data.special_requests;
    
                    const statusSelect = document.getElementById('reservation-status');
                    statusSelect.innerHTML = '';
                    data.statuses.forEach(status => {
                        const option = document.createElement('option');
                        option.value = status.id;
                        option.textContent = status.name;
                        if (status.id === data.status_id) {
                            option.selected = true;
                        }
                        statusSelect.appendChild(option);
                    });

                    document.getElementById('reservation-created-at').textContent = `Создано: ${data.created_at}`;
                    document.getElementById('reservation-responsible').textContent = data.responsible ? `Ответственный: ${data.responsible}` : 'Ответственный: —';
    
                    document.getElementById('reservation-modal-overlay-edit').classList.add('active');
                }
            })
            .catch(err => {
                console.error('Ошибка загрузки данных о брони:', err);
            });
    }
});

let filterTimeout = null;

document.querySelectorAll('.filter-data input, .filter-data select').forEach(elem => {
    elem.addEventListener('input', () => {
        clearTimeout(filterTimeout);
        filterTimeout = setTimeout(fetchFilteredReservations, 2000);
    });
});

document.getElementById('clear-filters-btn').addEventListener('click', () => {
    document.querySelectorAll('.filter-data input, .filter-data select').forEach(elem => {
        if (elem.type === 'select-one' || elem.type === 'text' || elem.type === 'date')
            elem.value = '';
    });
    fetchFilteredReservations();
});

function fetchFilteredReservations() {
    const params = new URLSearchParams(new FormData(document.querySelector('.filter-data')));
    
    fetch(`/brewmaster-secret/reservations/filter?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('.reservation-body tbody');
            tbody.innerHTML = '';

            data.forEach(res => {
                const tr = document.createElement('tr');
                tr.classList.add('clickable-row');
                tr.setAttribute('data-id', res.id);
                tr.innerHTML = `
                    <td>${res.name}</td>
                    <td>${res.status}</td>
                    <td>${res.date}</td>
                    <td>${res.start_time}–${res.end_time}</td>
                    <td>${res.num_people}</td>
                    <td>${res.table_name}</td>
                `;
                tbody.appendChild(tr);
            });
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const removeBtn = document.getElementById('remove-reservation-btn');

    if (removeBtn) {
        removeBtn.addEventListener('click', () => {
            const reservationId = document.getElementById('reservation-id').value;

            if (confirm('Вы уверены, что хотите удалить эту бронь?')) {
                fetch(`/brewmaster-secret/reservations/remove/${reservationId}`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json',
                    },
                    credentials: 'same-origin'
                })
                .then(response => {
                    if (response.redirected) {
                        window.location.href = response.url;
                    } else {
                        alert('Бронь удалена');
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Ошибка при удалении брони:', error);
                    alert('Ошибка сервера при удалении');
                });
            }
        });
    }
});