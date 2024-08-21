document.addEventListener('DOMContentLoaded', function() {
    const startPicker = flatpickr("#start", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true,
        locale: "ru",
        onChange: updateDuration
    });

    const endPicker = flatpickr("#end", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true,
        locale: "ru",
        onChange: updateDuration
    });

    function updateDuration() {
        const start = startPicker.selectedDates[0];
        const end = endPicker.selectedDates[0];

        if (start && end) {
            if (end < start) {
                alert("Время окончания не может быть раньше времени начала.");
                endPicker.clear();
                document.getElementById('duration_minutes').value = ''; // Очищаем поле, если дата некорректна
                return;
            }

            // Вычисление разницы во времени
            const duration = Math.floor((end - start) / 60000); // Разница в минутах

            // Убедимся, что результат - это число и не отрицательное значение
            if (!isNaN(duration) && duration >= 0) {
                document.getElementById('duration_minutes').value = duration;
            } else {
                document.getElementById('duration_minutes').value = ''; // Очистим значение, если оно некорректно
            }
        } else {
            document.getElementById('duration_minutes').value = ''; // Очистим значение, если одно из полей пустое
        }
    }
});
