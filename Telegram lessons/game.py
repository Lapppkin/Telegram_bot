import random
import time


l1 = 3 #Жизни Игрока
l2 = 3 #Жизни Соперника

while l1 > 0 or l2 > 0:
    x = input('Ваш ход: ')
    y = random.choice(['Камень', 'Ножницы', 'Бумага'])
    print('Ход другого игрока ' + y)

    if ( x == 'Бумага' and y == 'Камень' ) or ( x == 'Ножницы' and y == 'Бумага' ) or ( x == 'Камень' and y == 'Ножницы' ):
        l2 -= 1 #Выиграл Игрок
        print( str(l1) + ' ' + str(l2) )

    elif ( x == 'Камень' and y == 'Бумага' ) or ( x == 'Ножницы' and y == 'Камень' ) or ( x == 'Бумага' and y == 'Ножницы' ):
        l1 -= 1 #Выиграл Соперник
        print( str(l1) + ' ' + str(l2) )
    else:
        print( str(l1) + ' ' + str(l2) ) #Ничья

        if l1 == 0:
            break  #Если жизни Игрока равны 0, то игра заканчивается
        if l2 == 0:
            break  #Если жизни Соперника равны 0, то игра заканчивается