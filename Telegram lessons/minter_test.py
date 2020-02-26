import mintersdk
from mintersdk.sdk.transactions import MinterSendCoinTx # Импортируем библиотеку для генерации транзакций
from mintersdk.minterapi import MinterAPI
from mintersdk.sdk.wallet import MinterWallet



minter = MinterAPI(api_url='https://api.minter.one') # API ноды

minter_wallet = mintersdk.sdk.wallet.MinterWallet

create = minter_wallet.create(mnemonic='flat regular cook pull hand swift dentist taxi miss used elevator treat')

private_key = ['private_key']

# print(private_key)

# nonce = minter.get_nonce(address='Mxfcbdfb79aead11c003c93cfe88ae2e57fd6c0288') # Адрес откуда отправляется монета
# tx = MinterSendCoinTx(coin='BIP', to='Mxe4b80d500ec39f136833bca4705e8041c24fe417', value=float(1), nonce=nonce, gas_coin='BIP')
#
# tx.sign(private_key='a5045c1cc7569cd01113acc9d41743d1c991569922978d77be196f6963bae4eb')
#
# send = minter.send_transaction(tx=tx.signed_tx) # Отправка транзакции
#
# hash = 'Mt'+send['result']['hash'].lower()

# balance = minter.get_balance(address='Mxe4b80d500ec39f136833bca4705e8041c24fe417')
# print(balance)


# list_trx = minter.get_transactions("tx.from='Mxe4b80d500ec39f136833bca4705e8041c24fe417' "
# #                                    "AND tx.type='01' AND tx.height=4650569")

# list_trx = minter.get_transactions("tx.from='Mxe4b80d500ec39f136833bca4705e8041c24fe417'"
#                                    "AND tx.type='01'")

# list_trx = minter.get_transactions("tx.from='Mxfcbdfb79aead11c003c93cfe88ae2e57fd6c0288'")

# list_trx = minter.get_transactions("tx.from='Mxe4b80d500ec39f136833bca4705e8041c24fe417' "
#                                    "AND tx.height=4650569")
# print(list_trx)

# print(minter.get_balance('Mxfcbdfb79aead11c003c93cfe88ae2e57fd6c0288'))
# print(minter.get_transaction(tx_hash=hash))
