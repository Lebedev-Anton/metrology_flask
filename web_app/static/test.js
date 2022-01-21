function count() {
        console.log('text');
        // Инициализировать новый запрос
        const request = new XMLHttpRequest();
        var TaskId = document.querySelector("#task_id").textContent;
        console.log(TaskId);
        var Url = `/script_runner/expect_execution_task/<${TaskId}>`;
        request.open('POST', Url);

        // Функция обратного вызова, когда запрос завершен
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            console.log(data.state)
            if (data.state != 'PENDING'){
                window.location.replace('/script_runner/task_status/<${task_id}>');
                }
            }
        // Добавить данные для отправки с запросом
          const data = new FormData();
        // Послать запрос
        request.send();
        return false;
}

let timerId = setInterval(() => count(), 4000);