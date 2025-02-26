import random

class BlackJackGame:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.deck = self.create_deck()
        self.bankroll = 1000  # Starting bankroll
        self.card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                           '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}  # Ace can be 1 or 11
        self.running_count = 0  # Tracks the Hi-Lo running count
        self.hi_lo_values = {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, 
                             '7': 0, '8': 0, '9': 0, 
                             '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}  # Hi-Lo card values

    def create_deck(self):
        """Create and shuffle a multi-deck shoe."""
        base_deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
        deck = base_deck * self.num_decks
        random.shuffle(deck)
        return deck

    def draw_card(self):
        """Draw a card from the deck and reshuffle if necessary."""
        if len(self.deck) < 15:  # Reshuffle when fewer than 15 cards remain
            print("\n--- Reshuffling deck ---")
            self.deck = self.create_deck()
            self.running_count = 0  # Reset count after reshuffle
        card = self.deck.pop()
        self.update_count(card)  # Update Hi-Lo count
        return card

    def update_count(self, card):
        """Update the running count based on the Hi-Lo system."""
        self.running_count += self.hi_lo_values[card]

    def calculate_true_count(self):
        """Calculate the true count by dividing the running count by remaining decks."""
        remaining_decks = len(self.deck) / 52  # Estimate remaining decks
        return self.running_count / remaining_decks if remaining_decks > 0 else 0

    def calculate_hand(self, hand):
        """Calculate the value of a hand, adjusting for Aces."""
        value = sum(self.card_values[card] for card in hand)
        aces = hand.count('A')
        
        # Adjust for Aces if the hand is bust
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value

    def dealer_turn(self, dealer_hand):
        """Dealer logic: hits on soft 17 and stands otherwise."""
        while self.calculate_hand(dealer_hand) < 17:
            dealer_hand.append(self.draw_card())
        return dealer_hand

    def play_round(self):
        """Play a single round of Blackjack."""
        # Get player's bet
        while True:
            try:
                bet = int(input(f"\nBankroll: ${self.bankroll} | Enter bet (10-{self.bankroll}): "))
                if 10 <= bet <= self.bankroll:
                    self.bankroll -= bet
                    break
                print(f"Invalid bet! Enter between 10-{self.bankroll}")
            except ValueError:
                print("Numbers only!")

        # Deal initial hands
        player_hands = [[self.draw_card(), self.draw_card()]]  # List of hands (for splits)
        dealer_hand = [self.draw_card(), self.draw_card()]
        print(f"\nDealer shows: {dealer_hand[0]}")

        # Display running count and true count
        print(f"Running Count: {self.running_count}")
        print(f"True Count: {self.calculate_true_count():.2f}")

        # Process each player hand (accounting for splits)
        final_hands = []
        for hand in player_hands:
            while True:
                print(f"\nYour hand: {hand} ({self.calculate_hand(hand)})")
                
                # Check for blackjack
                if self.calculate_hand(hand) == 21:
                    print("Blackjack!")
                    final_hands.append(hand)
                    break
                    
                # Check split eligibility
                if len(hand) == 2 and hand[0] == hand[1] and self.bankroll >= bet:
                    split = input("Split? (y/n): ").lower()
                    if split == 'y':
                        self.bankroll -= bet
                        new_hand1 = [hand[0], self.draw_card()]
                        new_hand2 = [hand[1], self.draw_card()]
                        player_hands.extend([new_hand1, new_hand2])
                        print(f"Split into: {new_hand1} and {new_hand2}")
                        continue
                
                # Player action loop
                while True:
                    action = input("[H]it, [S]tand, [D]ouble: ").lower()
                    
                    if action == 'd' and len(hand) == 2 and self.bankroll >= bet:
                        self.bankroll -= bet
                        bet *= 2
                        hand.append(self.draw_card())
                        print(f"Doubled: {hand} ({self.calculate_hand(hand)})")
                        final_hands.append(hand)
                        break
                    elif action == 'h':
                        hand.append(self.draw_card())
                        print(f"Hit: {hand} ({self.calculate_hand(hand)})")
                        if self.calculate_hand(hand) > 21:
                            print("Bust!")
                            final_hands.append(hand)
                            break
                    elif action == 's':
                        final_hands.append(hand)
                        break
                    else:
                        print("Invalid action!")
                break

        # Dealer plays
        dealer_hand = self.dealer_turn(dealer_hand)
        dealer_total = self.calculate_hand(dealer_hand)
        print(f"\nDealer's hand: {dealer_hand} ({dealer_total})")

        # Calculate outcomes
        for hand in final_hands:
            player_total = self.calculate_hand(hand)
            original_bet = bet // (len(final_hands))  # Split bets
            
            if player_total > 21:
                print(f"Hand {hand} BUST - Lost ${original_bet}")
                continue
                
            # Blackjack payout (3:2)
            if len(hand) == 2 and player_total == 21:
                if dealer_total != 21:
                    win = int(original_bet * 1.5)
                    self.bankroll += win + original_bet
                    print(f"BLACKJACK! Won ${win}")
                    continue

            # Normal outcomes
            if dealer_total > 21 or player_total > dealer_total:
                self.bankroll += original_bet * 2
                print(f"Hand {hand} WON ${original_bet}")
            elif player_total == dealer_total:
                self.bankroll += original_bet
                print(f"Hand {hand} PUSH")
            else:
                print(f"Hand {hand} LOST ${original_bet}")

    def play_game(self):
        """Main game loop."""
        print("--- Welcome to Blackjack! ---")
        while self.bankroll >= 10:
            self.play_round()
            if self.bankroll < 10:
                print("\n⚠️ You're broke! Game over.")
                break
            if input("\nPlay again? (y/n): ").lower() != 'y':
                print(f"\nThanks for playing! Final bankroll: ${self.bankroll}")
                break

# Start the game
if __name__ == "__main__":
    game = BlackJackGame()
    game.play_game()