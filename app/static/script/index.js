document.addEventListener('DOMContentLoaded', () => {
    const startSelect = document.getElementById('time_start');
    const endSelect = document.getElementById('time_end');
    const dateInput = document.getElementById('date');
    const peopleInput = document.getElementById('people');

    const staticMinStart = "12:00";
    const maxEnd = "23:00";
    const stepMinutes = 15;

    // Функция для преобразования времени в минуты
    function timeToMinutes(time) {
        const [h, m] = time.split(":").map(Number);
        return h * 60 + m;
    }

    // Функция для преобразования минут обратно в время
    function minutesToTime(mins) {
        const h = String(Math.floor(mins / 60)).padStart(2, '0');
        const m = String(mins % 60).padStart(2, '0');
        return `${h}:${m}`;
    }

    // Получаем текущее серверное время
    function getNowFromServer() {
        return fetch('/api/time/now')
            .then(response => response.json())
            .then(data => {
                const date = new Date(`${data.date}T${data.time}:00`);
                return date;
            });
    }

    // Округляем время до следующего шага
    function roundToNextStep(minutes, step) {
        return Math.ceil(minutes / step) * step;
    }

    // Устанавливаем минимальное время начала брони для выбранной даты
    function getMinStartTimeForDate(dateStr, nowNSK) {
        const todayStr = nowNSK.toISOString().split('T')[0];

        if (dateStr === todayStr) {
            const minsNow = nowNSK.getHours() * 60 + nowNSK.getMinutes();
            const rounded = roundToNextStep(minsNow + stepMinutes, stepMinutes);
            return minutesToTime(Math.max(rounded, timeToMinutes(staticMinStart)));
        }

        return staticMinStart;
    }

    // Заполнение доступных вариантов для времени начала
    function fillStartOptions(nowNSK) {
        startSelect.innerHTML = '';
        const selectedDate = dateInput.value;
        const minStart = getMinStartTimeForDate(selectedDate, nowNSK);
        const start = timeToMinutes(minStart);
        const end = timeToMinutes(maxEnd) - 60;

        for (let t = start; t <= end; t += stepMinutes) {
            const time = minutesToTime(t);
            startSelect.add(new Option(time, time));
        }

        fillEndOptions(startSelect.value);
    }

    // Заполнение доступных вариантов для времени окончания
    function fillEndOptions(startTime) {
        endSelect.innerHTML = '';
        const start = timeToMinutes(startTime) + 60;
        const maxByLimit = timeToMinutes(startTime) + 180;
        const end = Math.min(maxByLimit, timeToMinutes(maxEnd));

        for (let t = start; t <= end; t += stepMinutes) {
            const time = minutesToTime(t);
            endSelect.add(new Option(time, time));
        }
    }

    // Устанавливаем ограничения на выбор даты
    function setupDateLimits(nowNSK) {
        const minDate = new Date(nowNSK);
        minDate.setDate(minDate.getDate()); // Оставляем текущий день

        // Если время больше 21:30, добавляем 1 день
        const currentTime = nowNSK.getHours() * 60 + nowNSK.getMinutes();
        if (currentTime > timeToMinutes("21:30")) {
            minDate.setDate(minDate.getDate() + 1); // Переходим на следующий день
        }

        const minDateStr = minDate.toISOString().split('T')[0];
        
        // Устанавливаем минимальную и максимальную дату
        const maxDate = new Date(nowNSK);
        maxDate.setDate(maxDate.getDate() + 30); // Максимум 30 дней вперед
        const maxDateStr = maxDate.toISOString().split('T')[0];

        dateInput.min = minDateStr;
        dateInput.max = maxDateStr;

        dateInput.value = minDateStr;  // Устанавливаем минимальную дату как выбранную
    }

    // Получаем текущее время с сервера и выполняем необходимые действия
    getNowFromServer().then(nowNSK => {
        setupDateLimits(nowNSK);
        fillStartOptions(nowNSK);

        // Добавляем обработчики для обновления времени начала и окончания
        dateInput.addEventListener('change', () => fillStartOptions(nowNSK));
        startSelect.addEventListener('change', () => fillEndOptions(startSelect.value));

        fetchAvailableTables();  // Обновляем доступные столы
    });

    // Получаем доступные столы для бронирования
    function fetchAvailableTables() {
        const date = dateInput.value;
        const timeStart = startSelect.value;
        const timeEnd = endSelect.value;
        const people = parseInt(peopleInput.value);

        if (!date || !timeStart || !timeEnd || !people) return;

        fetch(`/reservations/get?date=${date}&time_start=${timeStart}&time_end=${timeEnd}&people=${people}`)
            .then(response => response.json())
            .then(data => {
                const filteredTables = data.filter(table => {
                    if (table.name === "34" && people < 10) {
                        return false;
                    }
                    return true;
                });

                const availableTableIds = filteredTables.map(table => `table-${table.name.replace(/\./g, '-')}`);

                const allTableButtons = document.querySelectorAll('button[id^="table-"]');

                allTableButtons.forEach(button => {
                    if (availableTableIds.includes(button.id)) {
                        button.style.backgroundColor = '#4750FB';
                        button.disabled = false;
                        button.style.border = 'none';
                        button.style.color = '#F5F7FA';
                        button.style.borderRadius = '8px';
                        button.style.cursor = 'pointer';
                    } else {
                        button.style.backgroundColor = '#D6D6D6';
                        button.disabled = true;
                        button.style.border = 'none';
                        button.style.borderRadius = '8px';
                        button.style.cursor = 'not-allowed';
                    }
                });
            })
            .catch(error => console.error("Ошибка при получении данных:", error));
    }

    [peopleInput, dateInput, startSelect, endSelect].forEach(el => {
        el.addEventListener('change', fetchAvailableTables);
    });
});


const container = document.querySelector('.zoom-container');
const content = document.querySelector('.zoom-content');

let scale = 1;
let isDragging = false;
let startX, startY;
let offsetX = 0, offsetY = 0;

const MIN_SCALE = 0.3;
const MAX_SCALE = 3;

container.addEventListener('wheel', (e) => {
    e.preventDefault();

    const scaleFactor = 0.1;
    const mouseX = e.clientX - container.offsetLeft;
    const mouseY = e.clientY - container.offsetTop;

    const zoomIn = e.deltaY < 0;
    let newScale = zoomIn ? scale * (1 + scaleFactor) : scale / (1 + scaleFactor);
    newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, newScale));

    if (newScale !== scale) {
        const dx = mouseX - offsetX;
        const dy = mouseY - offsetY;

        offsetX -= dx * (newScale / scale - 1);
        offsetY -= dy * (newScale / scale - 1);

        scale = newScale;
        applyTransform();
    }
});

container.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.clientX - offsetX;
    startY = e.clientY - offsetY;
    content.style.cursor = 'grabbing';
});

container.addEventListener('mouseup', () => {
    isDragging = false;
    content.style.cursor = 'grab';
});

container.addEventListener('mouseleave', () => {
    isDragging = false;
    content.style.cursor = 'grab';
});

container.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    offsetX = e.clientX - startX;
    offsetY = e.clientY - startY;
    applyTransform();
});

container.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) {
        startX = e.touches[0].clientX - offsetX;
        startY = e.touches[0].clientY - offsetY;
    }
});

container.addEventListener('touchmove', (e) => {
    if (e.touches.length === 1) {
        offsetX = e.touches[0].clientX - startX;
        offsetY = e.touches[0].clientY - startY;
        applyTransform();
    } else if (e.touches.length === 2) {
        const dx = e.touches[1].clientX - e.touches[0].clientX;
        const dy = e.touches[1].clientY - e.touches[0].clientY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (!container.dataset.prevDist) {
            container.dataset.prevDist = distance;
            return;
        }

        const prevDist = parseFloat(container.dataset.prevDist);
        const delta = distance - prevDist;
        const pinchFactor = 0.005;

        let newScale = scale * (1 + delta * pinchFactor);
        newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, newScale));

        if (newScale !== scale) {
            scale = newScale;
            container.dataset.prevDist = distance;
            applyTransform();
        }
    }
});

container.addEventListener('touchend', () => {
    delete container.dataset.prevDist;
});

function applyTransform() {
    content.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;
}

document.querySelectorAll('button[id^="table-"]').forEach(button => {
    button.addEventListener('click', () => {
        if (button.disabled) return;

        const tableId = button.id.replace('table-', '');
        const tableName = tableId.replace(/-/g, '.');

        fetch(`/table/${tableName}`)
            .then(response => response.json())
            .then(table => {
                const modalOverlay = document.getElementById('table-modal-overlay');
                const modalContent = modalOverlay.querySelector('.modal-content');

                modalContent.querySelector('h2').innerText = `Стол ${table.name}`;

                const oldBody = modalContent.querySelector('.modal-body');
                if (oldBody) oldBody.remove();

                const modalBody = document.createElement('div');
                modalBody.classList.add('modal-body');

                if (table.photo) {
                    const img = document.createElement('img');
                    const imgSrc = `/static/${table.photo.replace('app/static/', '')}`;
                    img.src = imgSrc;
                    img.alt = `Фото стола ${table.name}`;
                    img.style.maxWidth = '100%';
                    img.style.borderRadius = '12px';
                    modalBody.appendChild(img);
                }

                if (table.description) {
                    const desc = document.createElement('p');
                    desc.innerText = `Описание: ${table.description}`;
                    modalBody.appendChild(desc);
                }

                const dateInput = document.getElementById('date');
                const selectedDate = new Date(dateInput.value);
                const dayOfWeek = selectedDate.getDay();

                if ((dayOfWeek === 5 || dayOfWeek === 6) && table.deposit) {
                    const deposit = document.createElement('p');
                    deposit.innerText = `Депозит: ${table.deposit}₽`;
                    deposit.style.fontWeight = 'bold';
                    modalBody.appendChild(deposit);
                }

                const reserveButton = document.createElement('button');
                reserveButton.id = 'reserve-button';
                reserveButton.innerText = 'Продолжить';
                reserveButton.classList.add('reserve-button-class');
                reserveButton.addEventListener('click', () => {
                    const people = document.getElementById('people').value;
                    const date = document.getElementById('date').value;
                    const timeStart = document.getElementById('time_start').value;
                    const timeEnd = document.getElementById('time_end').value;

                    const reserveModal = document.getElementById('reserve-modal-overlay');
                    const reserveModalContent = reserveModal.querySelector('.modal-content');
                    const reserveModalBody = reserveModalContent.querySelector('.modal-body');

                    reserveModalBody.querySelector('#data-reserve-user').innerText = `Дата: ${date}`;
                    reserveModalBody.querySelector('#time-reserve-user').innerText = `Время: ${timeStart} - ${timeEnd}`;
                    reserveModalBody.querySelector('#table-reserve-user').innerText = `Стол: ${table.name}`;
                    
                    modalOverlay.classList.remove('active');

                    reserveModal.classList.add('active');
                });

                modalBody.appendChild(reserveButton);
                modalContent.appendChild(modalBody);
                modalOverlay.classList.add('active');
            })
            .catch(err => console.error('Ошибка при загрузке данных стола:', err));
    });
});

document.getElementById('close-table-modal-btn').addEventListener('click', () => {
    const modalOverlay = document.getElementById('table-modal-overlay');
    modalOverlay.classList.remove('active');
});

document.getElementById('submit-reservation-btn').addEventListener('click', () => {
    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const email = document.getElementById('email').value.trim();
    const specialRequests = document.getElementById('specialRequests').value.trim();

    const date = document.getElementById('date').value;
    const people = document.getElementById('people').value;
    const timeStart = document.getElementById('time_start').value;
    const timeEnd = document.getElementById('time_end').value;
    const tableName = document.getElementById('table-reserve-user').textContent.replace('Стол: ', '');

    if (!name || !phone || !date || !timeStart || !timeEnd || !people || !tableName) {
        alert('Пожалуйста, заполните все обязательные поля.');
        return;
    }

    const reservationData = {
        name,
        phone,
        email,
        specialRequests,
        date,
        time_start: timeStart,
        time_end: timeEnd,
        people,
        table: tableName
    };

    fetch('/reserve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reservationData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при бронировании');
        }
        return response.json();
    })
    .then(data => {
        if (data.reservation_id) {
            document.getElementById('reserve-modal-overlay').classList.remove('active');
            window.location.href = `/reservations/${data.reservation_id}`;
        } else {
            alert('Произошла ошибка при бронировании');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при бронировании.');
    });
});

document.getElementById('close-reserve-modal-btn').addEventListener('click', () => {
    const modalOverlay = document.getElementById('reserve-modal-overlay');
    modalOverlay.classList.remove('active');
});
