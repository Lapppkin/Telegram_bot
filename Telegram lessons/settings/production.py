import os


# Путь до коренной папки `tele_bot`
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# TODO: вписать сюда токен от своего бота!!!
TG_TOKEN = "1054775144:AAGR0Pu07k2Ql7VdhleiKL1bl79J6keAEfA"

# На сервере не используем прокси-URL
TG_API_URL = 'https://telegg.ru/orig/bot'

# Валютная пара для уведомления
NOTIFY_PAIR = "USD-BTC"
# ID чата для уведомлений о курсе BTC
NOTIFY_USER_ID = 720951086

# ID чата для уведомлений о курсе $
USD_NOTIFY_USER_ID = -1001386305123

# ID чата (владельца канала) для получения отзывов/заявок
FEEDBACK_USER_ID = 50512389
