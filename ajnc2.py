import random
import math
import time

#sending A's to the end of the list, so amount() would
#calculate them properly - if the sum of other elements is >= 10
#A is going to count as 1, else 11
#it has to be at the end, so we would know the complete sum of other elements
#not just first few
#for example, [4, 5, A, 6] - it would result in 26
#but using this function we would get [4, 5, 6, A] and the result = 16
def move_a_to_end(hand):
    br = 0
    for el in hand:
        if el == 'A':
            br += 1
    hand = filter(lambda a : a != 'A', hand)
    for i in range(br):
        hand.append('A')
    return hand

def amount(hand):
    amount = 0
    for el in hand:
        if el in picture: #J, Q, K count as 10
            amount += 10
        if el in number: #if it's a number, just add its values
            amount += el
        elif el == 'A':
            #if adding 11 to the current amount would go over 21, count A as 1
            if amount + 11 > 21:
                amount += 1
            else:
                amount += 11
    return amount

#all pictures
picture = ['J', 'Q', 'K']
#all number cards - i had no idea how to check if a variable is int, so this is
#the solution
number = [2, 3, 4, 5, 6, 7, 8, 9, 10]
#all possible cards
cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
#map of already dealt cards - value is how many have been dealt
number_of_picked_cards = {'A':0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 'J':0, 'Q':0, 'K':0}

total_player_wins = 0
total_computer_wins = 0

#while we still have at least 4 cards in deck:
while math.fsum(number_of_picked_cards.values()) < 48:
    print "========================================"
    print "\tStarting new game!!"
    print "     Cards left in deck: ", 52 - math.fsum(number_of_picked_cards.values())
    print "========================================"

    player_cards = []
    computer_cards = []

    #first player card
    card = random.choice(cards)
    player_cards.append(card)
    number_of_picked_cards[card] += 1

    #first computer card
    card = random.choice(cards)
    computer_cards.append(card)
    number_of_picked_cards[card] += 1

    #second player card
    card = random.choice(cards)
    player_cards.append(card)
    number_of_picked_cards[card] += 1
    #check if player got blackjack
    #TODO: is it over or does the computer pick cards hoping for a 'push'?
    if (player_cards[0] == 'A' and player_cards[1] in picture) or (player_cards[1] == 'A' and player_cards[0] in picture) or (player_cards[0] == 'A' and player_cards[1] == 10) or (player_cards[1] == 'A' and player_cards[0] == 10):
        print "Player blackjack!"
    print "Players hand", player_cards

    #second computer card
    card = random.choice(cards)
    computer_cards.append(card)
    number_of_picked_cards[card] += 1
    #check if computer got blackjack
    #TODO: is it over or does the player pick cards hoping for a 'push'?
    if (computer_cards[0] == 'A' and computer_cards[1] in picture) or (computer_cards[1] == 'A' and computer_cards[0] in picture) or (player_cards[0] == 'A' and player_cards[1] == 10) or (player_cards[1] == 'A' and player_cards[0] == 10):
        print "Computer blackjack!"
    print "Dealers hand", computer_cards

    #indicator telling us who won
    indicator = 0
    #current reciver of cards
    pick_for = 'player'

    #this one tells us whether the player chose to get a card or not
    #there was a problem that, near the end of the deck,
    #player would be asked 'Do you want a card?'
    #every time a card that has already been dealt 4 times gets
    #chosen by random.choice()
    #0 is no, 1 is yes
    choice = 0

    print "\nPicking for " + pick_for
    #calculate the sum of the 2 cards player got at the start
    player_sum = amount(player_cards)
    if pick_for == 'player':
        while indicator == 0: #while player hasn't stand-ed nor lost
            if choice == 0: #if the player hasn't said yes, write the question
                decision = raw_input("Do you want a card?[y/n] ")
            else: #else just pick a card, no questions asked
                decision = 'y'
            if decision == 'y':
                choice = 1
                card = random.choice(cards)
                if number_of_picked_cards[card] >= 4: #check if 4 cards of type card have been dealt
                    continue #if so, pick another
                player_cards.append(card) #add card to player hand
                player_cards = move_a_to_end(player_cards) #move A's to the end
                print "Current hand: ", player_cards
                player_sum = amount(player_cards) #calculate current amount
                print player_sum
                number_of_picked_cards[card] += 1 #edit the map value for the picked card

                #if player went over 21, he lost -> indicator = -1
                if amount(player_cards) > 21:
                    indicator = -1
                    pick_for = 'computer'
            else:
                #player chose not to get a card - stand -> indicator = 1
                indicator = 1
                pick_for = 'computer'
            choice = 0

    #we know that if indicator is -1, the player lost, so we can declare the winner
    #and move on to the next game
    if indicator == -1:
        print "Computer won!"
        total_computer_wins += 1
        time.sleep(4)
        continue

    print "\nPicking for " + pick_for
    #calculate the amount for 2 cards the computer has
    computer_sum = amount(computer_cards)
    if pick_for == 'computer':
        #computer wont risk it, if hs total is 18 or less, he will go for the card
        #else he will stand
        while amount(computer_cards) < 19:
            card = random.choice(cards)
            if number_of_picked_cards[card] >= 4:
                continue
            computer_cards.append(card)
            computer_cards = move_a_to_end(computer_cards)
            print "Current hand: ", computer_cards
            computer_sum = amount(computer_cards)
            print computer_sum
            number_of_picked_cards[card] += 1

            #indicator = -2 means that the computer lost
            if amount(computer_cards) > 21:
                indicator = -2

    #we know the computer lost, so we can move on to the next game
    if indicator == -2:
        print "Player won!"
        total_player_wins += 1
        time.sleep(4)
        continue

    #if neither player nor computer lost by going over 21, we check
    #final amounts, declare the winner and move on to the next game
    if player_sum > computer_sum:
        print "Player won!"
        total_player_wins += 1
    elif player_sum == computer_sum:
        print "Push!"
    else:
        print "Computer won!"
        total_computer_wins += 1
    time.sleep(4)

print "========================================"
print "\tPlayer won:", total_player_wins, "times"
print "\tDealer won:", total_computer_wins, "times"
print "========================================"
