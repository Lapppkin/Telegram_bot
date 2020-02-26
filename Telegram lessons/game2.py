import time
import random


RSP = ['Камень', 'Ножницы', 'Бумага']
rch = random.choice(RSP)
cnt_User = 30
cnt_Comp = 30
Check = True
print('Привет!\n\nДавай поиграем в игру камень, ножницы, бумага!'
      '\nВведи цифру что ты хочешь вкинуть!')


while Check == True:
    rch = random.choice(RSP)
    print('\n1.Камень ☄️ \n2.Ножницы ✂️ ️\n3.Бумага 📃')
    ch1 = input('Ваш выбор >>> ')
    print('ЦУ-', sep=' ', end='')
    time.sleep(0.6)
    print('Е', sep=' ', end='')
    time.sleep(0.6)
    print('-ФА\n', sep=' ', end='')
    if rch == ('Камень'):
        if ch1 == '1':
            print('\n ☄️ против ☄️ ')
            print('\nУ меня камень ☄️ и у тебя камень ☄️! Ничья!')
            time.sleep(2)
            print(f"""
############################
Счет:
Вы {cnt_User} Bip Ⓜ️
Соперник {cnt_Comp} Bip Ⓜ️
############################
            """)
            time.sleep(2)

        elif ch1 == '2':
            print('\n ☄️ против ✂️ ')
            print('\nУ меня камень ☄️, а у тебя ножницы ✂️! Я выиграл!')
            time.sleep(2)
            cnt_User -= 10
            cnt_Comp += 10
            print(f"""
############################
Счет:
Вы {cnt_User} Bip Ⓜ️ (-10)
Соперник {cnt_Comp} Bip Ⓜ️ (+10)
############################
            """)
            time.sleep(2)

        elif ch1 == '3':
            print('\n ☄️ против 📃 ')
            print('\nУ меня камень ☄️, а у тебя бумага 📃! Ты выиграл!')
            time.sleep(2)
            cnt_Comp -= 10
            cnt_User += 10
            print(f"""
############################
Счет:
Вы {cnt_User} Bip Ⓜ️ (+10)
Соперник {cnt_Comp} Bip Ⓜ️ (-10)
############################
            """)
            time.sleep(2)

    elif rch == ('Ножницы'):
        if ch1 == '1':
            print('\n ✂️ против ☄️ ')
            print('\nУ меня ножницы ✂️, а у тебя камень ☄️! Ты выиграл!')
            time.sleep(2)
            cnt_Comp -= 10
            cnt_User += 10
            print(f"""
############################
Счет:
Вы {cnt_User} Bip Ⓜ️ (+10)
Соперник {cnt_Comp} Bip Ⓜ️ (-10)
############################
            """)
            time.sleep(2)

        elif ch1 == '2':
            print('\n ✂️ против ✂️ ')
            print('\nУ меня ножницы ✂️, а у тебя ножницы ✂️! Ничья!')
            time.sleep(2)
            print(f"""
############################
Счет:
Вы {cnt_User} Bip Ⓜ️
Соперник {cnt_Comp} Bip Ⓜ️
############################
            """)
            time.sleep(2)

        elif ch1 == '3':
            print('\n ✂️ против 📃️ ')
            print('\nУ меня ножницы ✂️, а у тебя бумага 📃! Я выиграл!')
            time.sleep(2)
            cnt_User -= 10
            cnt_Comp += 10
            print(f"""
############################
Счет:
Вы {cnt_User} Bip Ⓜ️ (-10)
Соперник {cnt_Comp} Bip Ⓜ️ (+10)
############################
            """)
            time.sleep(2)

    elif rch == ('Бумага'):
        if ch1 == '1':
            print('\n 📃️ против ☄️ ')
            print('\nУ меня бумага 📃, а у тебя камень ☄️! Я выиграл!')
            time.sleep(2)
            cnt_User -= 10
            cnt_Comp += 10
            print(f"""
############################
Счет:
Вы {cnt_User} Bip Ⓜ️ (-10)
Соперник {cnt_Comp} Bip Ⓜ️ (+10)
############################
            """)
            time.sleep(2)

        elif ch1 == '2':
            print('\n 📃️ против ✂️ ')
            print('\nУ меня бумага 📃, а у тебя ножницы ✂️! Ты выиграл!')
            time.sleep(2)
            cnt_Comp -= 10
            cnt_User += 10
            print(f"""
############################
Счет:
Вы {cnt_User} Bip Ⓜ️ (+10)
Соперник {cnt_Comp} Bip Ⓜ️ (-10)
############################
            """)
            time.sleep(2)

        elif ch1 == '3':
            print('\n 📃️ против 📃️ ')
            print('\nУ меня бумага 📃 и у тебя бумага 📃! Ничья!')
            time.sleep(2)
            print(f"""
############################
Счет:
Вы {cnt_User} Bip Ⓜ️
Соперник {cnt_Comp} Bip Ⓜ️
############################
            """)
            time.sleep(2)

    elif ch1 == str:
        print('Вводите цифры...')

    else:
        print('Прверьте правильность ввода...')

    if cnt_Comp == 0:
        User_benefit = cnt_User - 30
        print(f'Ура! ты победил в игре и заработал - {User_benefit} bip!')
        time.sleep(2)
        print('\n\nДавай еще сыграем?')
        print('1.Давай!\n2.Нет, не хочу')
        choose2 = input('>>> ')
        if choose2 == '1':
            continue
        elif choose2 == '2':
            print('Ну и ладно')
            time.sleep(2)
            quit()
    elif cnt_User == 0:
        User_loss = cnt_Comp - 30
        print(f'Увы( Вы проиграли в этой игре - {User_loss} bip!')
        time.sleep(2)
        print('\n\nДавай еще сыграем?')
        print('1.Давай!\n2.Нет, не хочу')
        choose2 = input('>>> ')
        if choose2 == '1':
            continue
        elif choose2 == '2':
            print('Ну и ладно')
            time.sleep(2)
            quit()

