function count() {
        // Инициализировать новый запрос
        const request = new XMLHttpRequest();
        var TaskId = task_id.getAttribute('About');
        var Url = `/script_runner/expect_execution_task/${TaskId}`;
        request.open('POST', Url);
        // Функция обратного вызова, когда запрос завершен
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.state != 'PENDING'){
                window.location.replace(`/script_runner/task_status/${TaskId}`);
                }
            }
        // Добавить данные для отправки с запросом
          const data = new FormData();
        // Послать запрос
        request.send();
        return false;
}

let timerId = setInterval(() => count(), 1000);