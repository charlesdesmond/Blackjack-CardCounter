# Blackjack-CardCounter
This is a command-line-based Python project that simulates a realistic casino Blackjack game. You can manage your bankroll and play as long a you'd like, or until you lose all your money. 

This project features a constantly updating card counter, displaying both the Running Count and True Count, helping players learn more complex strategies to maximize profits. It also features common casino rules like no doubling after splitting, dealer hits a soft 17, and more. It can handle multiple hands at the same time for splits, manage soft and hard aces, and process other small intricacies. It runs using a multideck shoe - 6 decks by default - that allows for card counting and automatically reshuffles when the deck gets low.

In the future, I plan to hard code basic strategy to allow a computer to play and simulate thousands of hands, utilizing betting deviation based on the True Count to track profits/losses over the long run.
