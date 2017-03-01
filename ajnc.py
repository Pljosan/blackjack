import random

cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
number_of_picked_cards = {'A':0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 'J':0, 'Q':0, 'K':0}

player_sum = 0
computer_sum = 0

indicator = 0
pick_for = 'player'

while indicator == 0:
    print "\nPicking for " + pick_for
    card = random.choice(cards)
    if number_of_picked_cards[card] == 4:
        continue
    print "Picked", card
    number_of_picked_cards[card] += 1

    if(pick_for == 'player'):
        if card == 'J' or card == 'Q' or card == 'K':
            player_sum += 10
        elif card == 'A':
            value = int(raw_input("Choose what suits you better, 1 or 11: "))
            player_sum += value
        else:
            player_sum += card
        print "Current player sum", player_sum
        if player_sum == 21:
            indicator = 1
            break
        elif player_sum > 21:
            indicator = 2
            break
        pick_for = 'computer'
    else:
        if card == 'J' or card == 'Q' or card == 'K':
            computer_sum += 10
        elif card == 'A':
            if computer_sum + 11 == 21:
                value = 11
            else:
                value = 1
            computer_sum += value
        else:
            computer_sum += card
        print "Current computer sum", computer_sum
        if computer_sum == 21:
            indicator = 2
            break
        elif computer_sum > 21:
            indicator = 1
            break
        pick_for = 'player'

if indicator == 1:
    print "\nYou won!"
else:
    print "\nThe computer won, sorry :("
