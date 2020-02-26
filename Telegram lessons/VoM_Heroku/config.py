bot_token = '940528045:AAExWjIAc-gKFoONBFI-XpGLc4uwHVwEfBo' # токен телеграм бота
channel = '@testVoM' # название канала в который будет происходить постинг (должен быть открыт) и бот должен быть админом

minter_api = 'https://mnt.funfasy.dev/v0/' # api funfasy
minter_api_headers = {'X-Project-Id':'193d36ff-8898-4dd5-96e2-164ca0a08123', 'X-Project-Secret':'c7dfa39baccf6c9944876ca97c6e9bbd'} # funfasy keys

address_for_listening = 'fcbdfb79aead11c003c93cfe88ae2e57fd6c0288' # адрес для транзакций (без Mx)

coin_for_limit = 'LAPKINLAB' # монета в которой принимаются транзакции

limit_delegator_coin = 0.5 # количество монет для определения пользователя делегатором

price_for_ordinary_message = 0.25 # количество монет для простого сообщения

price_for_delegator_message = 0.5 # количество монет для сообщения со ссылкой для делегатора

price_for_linked_messages = 1 # количество монет для сообщения со ссылкой для НЕ делегатора

price_for_pin_hour = 2 # количество монет для закрепления сообщения на час

price_for_pin_day = 3 # количество монет для закрепления сообщения на сутки


database = "/Users/arturyakushev/Documents/GitHub/Telegram_bot/Telegram lessons/VoM_Heroku/data_base.db" # путь к базе данных
# требуемые таблицы
# (CREATE TABLE `transactions` ( `hash` TEXT, `from` TEXT, `coin` TEXT, `value` REAL, `payload` TEXT, `status` TEXT )
# CREATE TABLE "pinned" ( `message_id` INTEGER, `time_unpin` TEXT )

link_explorer_delegations = 'https://explorer-api.apps.minter.network/api/v1/addresses/{}/delegations' # ссылка для определения делегатор ли пользователь

minterscan_icon_link = 'https://minterscan.pro/addresses/{}/icon' # ссылка для определения иконки кошелька

minterscan_address_link = 'https://minterscan.net/address/{}' # ссылка на адрес

explorer_transaction_link = 'https://explorer.minter.network/transactions/Mt{}' # ссылка на транзакцию
