SECRET_ADMIN_KEY = 'dev_secret_123'
ENDINGS_LIST = ['end_good','end_bad','end_third','end_four','end_five','end_six']

story = {
    "start": {"title":"Пробуждение","text":"Ты просыпаешься...","options":[{"text":"Начать","next":"loop"}]},
    "loop": {"title":"Петля","text":"Это петля.","options":[{"text":"Оглядеться","next":"floor"}]},
    "floor": {"title":"Пол","text":"Под ковром цифра 3.","options":[{"text":"В карман","next":"pocket"}],"fragment":{"key":"paper3","text":"3"}},
    "pocket": {"title":"Карманы","text":"В кармане бумага.","options":[{"text":"К пейджеру","next":"pager"}]},
    "pager": {"title":"Пейджер","text":"Сообщение: 'Не повторяй ошибку.'","options":[{"text":"К звуку","next":"voice"}]},
    "voice": {"title":"Шепот","text":"Шёпот...","options":[{"text":"Правда","next":"truth"}]},
    "truth": {"title":"Правда","text":"Голос: 'Ты создал петлю.'","options":[{"text":"Принять","next":"end_good"},{"text":"Отрицать","next":"end_bad"}]},
    "end_good": {"title":"Разрыв","text":"Ты свободен.","options":[]},
    "end_bad": {"title":"Бесконечность","text":"Петля держит тебя.","options":[]} 
}
