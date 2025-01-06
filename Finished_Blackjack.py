import pygame
import sys
import os
import random

#Initialize Pygame font module.
pygame.font.init()

#Constants for suits and ranks
Suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
Ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
#Function to combine the Ranks with Suits and create our deck of 52 cards.
def create_deck():
    return [{'Rank': rank, 'Suit': suit} for rank in Ranks for suit in Suits]

#Function to shuffle our deck with the random import.
def shuffle_deck(deck):
    random.shuffle(deck)

#Function to deal a card from the deck.
def deal_card(deck):
    return deck.pop()

#Function to calculate the value of a hand.  
def calculate_hand_value(hand):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
    hand_value = sum(values[card['Rank']] for card in hand)

    #Handle Aces because their value can be 1 or 11 depending on the player or dealer hand values.
    num_aces = sum(1 for card in hand if card['Rank'] == 'Ace')
    for _ in range(num_aces):
        if hand_value > 21:
            hand_value -= 10
    return hand_value


#Function to display cards on screen using the pygame scaling factor. 
def display_card(card_name, x, y, scale=1.0):
    scaled_card = pygame.transform.scale(card_images[card_name], (int(130 * scale), int(166 * scale)))
    screen.blit(scaled_card, (x, y))

#Function to display a box with the current hand value of the player and dealer.
#This updates ev0erytime the player or dealer "hit"
def display_hand_value_box(value, x, y):
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 30))  
    font = pygame.font.Font(None, 24)
    text = font.render(f"Value: {value}", True, (255, 255, 255))
    screen.blit(text, (x + 5, y + 5))

#Function that tells the program where to display the card images for the player and how to space them as new cards come in.
def display_player_hand(player_hand):
    for i, card in enumerate(player_hand):
        card_name = f"{card['Rank']}_{card['Suit']}"
        x = i * 70 + 50  
        y = screen_height - 150  
        display_card(card_name, x, y, scale=0.5)  
        display_hand_value_box(calculate_hand_value(player_hand), 50, 550)  

# Function to display dealer's hand using Pygame.
def display_dealer_hand(dealer_hand, show_all_cards):
    for i, card in enumerate(dealer_hand):
        card_name = f"{card['Rank']}_{card['Suit']}"
        x = i * 70 + 50  
        y = 50  
        if not show_all_cards and i == 1:  #Show card back for the second card, as in blackjack only one face card of the dealer is revealed to the player.
            display_card('card_back', x, y, scale=0.5)
        else:
            display_card(card_name, x, y, scale=0.5)
            display_hand_value_box(calculate_hand_value(dealer_hand) if show_all_cards else '?', 50, 20)  


#Function for the player's turn.  
def player_turn(player_hand, deck):
    while calculate_hand_value(player_hand) < 21:
        display_player_hand(player_hand)
        display_dealer_hand(dealer_hand, False)  #Display one of the dealer's cards facedown as talked about above.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Add a message to the window asking the player to hit or stand.
        #The screen.blit command is how we position this text. Trial and error worked until it was positioned where i wanted it.
        #The display.flip command updates the display surface with any changes. Essentially how cards and text are added to the screen live.
        font = pygame.font.Font(None, 36)
        text = font.render("Do you want to hit or stand? (Press H or S)", True, (255, 255, 255))
        screen.blit(text, (50, 400))
        pygame.display.flip()

        font = pygame.font.Font(None, 36)
        text = font.render("Dealer", True, (255, 255, 255))
        screen.blit(text, (400, 20))
        pygame.display.flip()

        font = pygame.font.Font(None, 36)
        text = font.render("Player", True, (255, 255, 255))
        screen.blit(text, (400, 550))
        pygame.display.flip()

#Tells the code to wait for the player to make a valid decision by pressing 'H' for hit or 'S' for stand.
        decision = ''
        while decision not in ['h', 's']:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        decision = 'h'
                    elif event.key == pygame.K_s:
                        decision = 's'

        #Based on their decision, this if/then statement determines whether or not the player is dealt another card.
        if decision == 'h':
            player_hand.append(deal_card(deck))
        elif decision == 's':
            break

    # Reveal the dealer's hidden card at the end of the player's turn.
    display_player_hand(player_hand)
    display_dealer_hand(dealer_hand, True)  


#Function for the dealer's turn.
def dealer_turn(dealer_hand, deck):
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
        display_dealer_hand(dealer_hand, True)  #Display the second card of the dealer's hand.
        

   
#Function to determine the winner by calculating hand values for the player and dealer.
def determine_winner(player_hand, dealer_hand):
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    # Determines the winner based on player and dealer hand values.
    # Also determines busts, ties, and standard winning conditions.
    if player_value > 21:
        return "Player busts! Dealer wins."
    elif dealer_value > 21:
        return "Dealer busts! Player wins."
    elif player_value == dealer_value:
        return "It's a push!"   
    elif player_value == 21 or (dealer_value < 21 and player_value > dealer_value):
        return "Player wins!"
    else:
        return "Dealer wins."


#Function to display start screen with random card images.
def display_start_screen():
    screen.fill((0, 0, 0))

    #Display instructions near the top of the screen.
    font = pygame.font.Font(None, 28)
    instructions = [
        "Welcome to Blackjack!",
        "",
        "How to play:",
        "",
        "- Press H to hit and draw a single card",
        "- Aces can be worth 1 or 11 points.",
        "- Face cards are worth 10 points",
        "- Cards 2-10 are worth their face value",
        "- Get as close to 21 as possible without going over.",
        "- Press S to stand and end your turn",
        "",
        "- Press 'S' to start a game",
        "- Press 'Q' to exit",
    ]

    for i, line in enumerate(instructions):
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, 50 + i * 30))  
        screen.blit(text, text_rect)

    #Display random card images below the last line of text.  This is my poor attempt at designing detail for my start screen.
    for _ in range(8):
        random_suit = random.choice(Suits)
        random_rank = random.choice(Ranks)
        random_card_name = f'{random_rank}_{random_suit}'

        #Display below the last line of text (Was overlapping my instructions).
        random_x = random.randint(100, screen_width - 100)
        random_y = text_rect.bottom + random.randint(20, 100)
        display_card(random_card_name, random_x, random_y, scale=0.5)  

    pygame.display.flip()


#Initialize the deck outside of any functions.
deck = create_deck()
shuffle_deck(deck)

#Load card images.  
#To do this we have a folder with 52 card PNG's that correspond to the name of each card so they display correctly.
card_images = {}
for suit in Suits:
    for rank in Ranks:
        card_name = f'{rank}_{suit}'
        file_path = os.path.join('/Users/Tyler/Desktop/PlayingCards', f'{card_name}.png')
        card_images[card_name] = pygame.image.load(file_path)

#Load card back image.
card_images['card_back'] = pygame.image.load('/Users/Tyler/Desktop/PlayingCards/card_back.png')

#Define screen dimensions.
screen_width, screen_height = 800, 600

#Initialize the Pygame screen and set the window caption.
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BlackJack")

#Initialize dealer_hand globally.
dealer_hand = []

#Set up clock to control the frame rate.
clock = pygame.time.Clock()

#Display start screen.
display_start_screen()

def clear_screen():
    screen.fill((0, 0, 0))

# Function to display messages on the screen.
def display_message(message, y_offset=0):
    font = pygame.font.Font(None, 36)
    text = font.render(str(message), True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, (screen_height // 2 + y_offset))) 
    screen.blit(text, text_rect)
    pygame.display.flip()


#Run the game.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                clear_screen()

                #Reset hands for a new round.
                player_hand = [deal_card(deck), deal_card(deck)]
                dealer_hand = [deal_card(deck), deal_card(deck)]

                #Player's turn.
                player_turn(player_hand, deck)

                #Dealer's turn.
                dealer_turn(dealer_hand, deck)

                #Determine the winner and display the result.
                winner_message = determine_winner(player_hand, dealer_hand)

                #Display winner message.
                display_message(winner_message)

                #Add a message to press 'S' for the next round, slightly below the winner message.
                display_message("Press 'S' twice to start the next round.", y_offset=50)

                
                pygame.display.flip()

                #Wait for the player to press 'S' for the next round.
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_s:
                                waiting_for_input = False

                #Control the frame rate of the screen.
                clock.tick(30)
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

