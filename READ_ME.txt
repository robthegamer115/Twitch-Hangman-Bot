Twith Hangman Bot Version 3.2
Python Version 3.8
Last Updated August 9, 2020
by Robthegamer115

1. Setup:

	In order to run this bot, you must have Python 3.8 downloaded and working. Before 
	you run the twitch bot, you must open up Settings.txt and input your settings. Replace 
	"OAUTH CODE HERE" with an oauth code for the twitch account of the bot. Replace "BOT NAME HERE" 
	with the username of the bot, and finally replace "CHANNEL NAME HERE" with the channel you wish 
	to run the bot in. Once those changes are made, run "Run.py" to start up the hangman bot!

2. Global Commands:

	Global commands refer to commands which any user may use. The global commands programmed 
	by the twitch hangman bot include

	- "!hangmanrules": Gives a link to a pastebin of the rules of hangman for players
	- "!points": Gives the user the number of points they have earned
	- "!position": Gives the user the position they are in compared to all other players.
	- "!top10": Gives the names and points of the top 10 players in hangman. If there are less than
		ten players, it only gives as many players as there are.
	- "!hangman": Starts a game of hangman as long as enough time has passed (10 minutes since the last time
		hangman could have been played)
	- "!guess": Guesses a single character (if followed by a single character) or guesses the answer 
		(if followed by multiple characters)
	- "abouthangman": Gives information on myself and how to contact me if there is a problem

3. Channel Commands:

	Channel Commands refer to commands only the owner of the twitch channel can use. This includes
	
	- "!quit": Shuts down hangman bot
	- "!addpokes": Re-adds everything from the master list into the current hangman list.

4. Problems/Concerns/Future Updates

	If there are any issues at all, contact me either via Github, Discord, or Twitch. Future updates will likely
	add a command for any user to find out how many points another user has, as well as redesign so that the channel
	operator can add any category/otential answers they want. This was designed as a pokemon hangman game, but the
	framework for any hangman game to run exists.

5. Version History

	1.0 - ~May 2019: Had many issues including crashing around every 15 minutes
	2.0 - ~December 2019: Fixed major crashing issue, added Gen 8 Pokemon Things, added Location and Key Items as categories
	3.0 - ~May 2020: Added Top 10 as a command, made QoL improvements
	3.1 - June 2020: Added Side Locations and Notable Trainers as categories, retired Key Items as a category
	3.2 - August 2020: Uploaded to Github for first time, top 10 command revamped, code optimizations, READ_ME added.
