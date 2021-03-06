# VK_api_xckd
Скрипт публикует случайный комикс с [xckd](https://xkcd.com/) в группе [VK](https://vk.com/public210037951).

### Как установить

Python3 должен быть установлен. Затем используйте pip (или pip3, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Объявление переменных окружения

Перед запуском скрипта в одном каталоге с файлом `main.py` необходимо создать файл для хранения переменных окружения 
с именем `.env` и следующим содержимым:
```
VK_ACCESS_TOKEN=[TOKEN]
VK_GROUP_ID=[ID]
```
В переменной `VK_ACCESS_TOKEN` хранится api-токен сгенерированный с помощью процедуры [Implict Flow](https://vk.com/dev/implicit_flow_user):
Для получения api-токена необходимо выполнить запрос на его получение к [api](https://oauth.vk.com/authorize) со следующими параметрами:
- `client_id` - Идентификатор вашего приложения (отображается в адресной строке, если нажать кнопку "Редактировать" для нового приложения).
- `scope` - [права доступа](https://vk.com/dev/permissions) для приложения. Вам потребуются следующие права:
photos, groups, wall, offline.
  
![Получение api-токена](https://sun9-70.userapi.com/impg/3_t3fjOxKeRWK010QvA79uBgGRPwsRJFJKhpXQ/1OA_DGjtLsg.jpg?size=971x31&quality=95&sign=fb923bae81aa498f0fd3c55df01826cc&type=album)
API-токен приходит в ответ на запрос и выглядит как строка наподобие `533bacf01e1165b57531ad114461ae8736d6506a3`, подписанная как `access_token`.

В переменной `VK_GROUP_ID` хранится идентификатор вашего сообщества Вконтакте для публикации комиксов.


### Инструкция

Для запуска скрипта используйте:
```
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе [Dvmn.org](https://dvmn.org/).
