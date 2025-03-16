import TMGE
import Bejeweled
from time import sleep

GAME_SELECT_ART_1 = """.... .....-+**#*+-.....  .
.......:*%%######%%+:.....
 .+%%%%@%#*###%%%%%@#*+:..
.*@###%@###%#+=-.....:+%:.
.#%#%%@%##%%+=--:::::--%=.
 #@%%%@%##%%**+=-----=+@=.
.#@%%%@####%%##****##%%=..
.#@%%%@%#**##%%%%%%%%@=. .
.*@%%%@%##**********#@-...
.:@%%%@%%#**********#%-...
..-%@@@%%%##*******#%#:  .
....=%@@%%%%#######%@-....
  :%@%%@@%%%%%%%%%%%@*:...
..%%%%%%%@@@@@%%%%%%%%@=..
..*@%%%%%%%%#-+%%%%%%%%@#:
  .:+*%%@@%+:..-#%%%%%%%@:
.................-#%%%%@+.
.... .....  ..... .=++=:.."""

GAME_SELECT_ART_2 = """..........-#@@@@#=........
  .... :@@###**###@@: ....
..:===*@#******####%@+....
-@@#*#@#**##@@%#=-::::*@*.
%%*##%@#**%@=--:......-=@=
%%%%%@%#*#@#*=----------%+
%@%%%@%#*#@#***+=-----+#@-
%@%%%@%#**%@%##****##%@#: 
%@%%%@%##***####%#####@:..
%@%%%@%%#************#@...
+@%%%@%%%#***********%%.  
.%@%%@%%%%#**********@*.  
 .-#@@@%%%%%########%@:...
......@@%%%%%%%%%%%%@=....
... -@%%%@%%%%%@@@@#...   
....@@%%%%%%%%%%@%@.......
  ..@%%%%%%%%%%@@%@.  ....
....@@@%%%%%@@@%%%@:......
...  ...:-:#@%%%%%@....   
.............:---:........"""

GAME_SELECT_ART_3 = """........:*##%%%#+.........
.... ..#%########@=.. ....
..:-==@#**####%%%%@%+:..  
.+%##%@###%#=-:.....=#=...
.%%##@%##%%*=--------+*...
.%%%%@%##%%***+====+*%+...
.%%%%@%#*#%@%%%%%%%@%:....
.%%%%@%%#****####**%*.....
.#%%%@%%##********#@=.....
.=@%%@%%%%##******#@......
.-%@@@@%%%%%%%%%%%@@@*:...
-@%%%%@%%%%%%%%%@@%%%%%%-.
-@%%%%%%%%@===-+%%%%%%%@+.
.:#@@%%%@#:......+@%%%%%-.
  .................-#*-.  
"""

ANIMATION = [GAME_SELECT_ART_1, GAME_SELECT_ART_2, GAME_SELECT_ART_3]

class PlayerAccount:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.totalScore = 0

class MenuOption:
    def __init__(self, name, activation_function):
        self.name = name
        self.run = activation_function

class TMGEshell:
    def __init__(self):
        self._stillRunning = True
        self._next_player_id = 0
        self._players: dict[str, PlayerAccount] = dict()
        self._players_list: list[PlayerAccount] = list()

        def playBejeweled():
            game = Bejeweled.Bejeweled(self.playerAccountsToPlayerProfiles(self.selectPlayers(1)))
            self.storeResults(game.playGame())

        
        def playBejeweledVs():
            game = Bejeweled.Bejeweled(self.playerAccountsToPlayerProfiles(self.selectPlayers(2)))
            self.storeResults(game.playGame())
        
        def viewPlayerProfiles():
            self.clearScreen()
            print("PLAYERS LIST:")
            for player in self._players_list:
                print(f"{player.name}, {player.totalScore}")
            print("\n(press enter when finished viewing)")
            input()

        
        def quitTMGEshell():
            self._stillRunning = False

        self._options = [MenuOption("Quit", quitTMGEshell),
                         MenuOption("Play Bejeweled", playBejeweled),
                         MenuOption("Play BejeweledVs", playBejeweledVs),
                         MenuOption("Play Columns", None),
                         MenuOption("View Player Profiles", viewPlayerProfiles),
                         MenuOption("Add Player Profile", self.addPlayerProfile)]

    def register_player(self, name: str) -> bool:
        if name not in self._players_list:
            new_player = PlayerAccount(name, self._next_player_id)
            self._players[name] = new_player
            self._players_list.append(new_player)
            self._next_player_id += 1
            return True
        return False
    
    def storeResults(self, results: dict[int, int]):
        for player_id, player_score in results.items():
            self._players_list[player_id].totalScore += player_score

    def start(self):
        self.register_player("Guest")
        self.addPlayerProfile()
        self.gameSelectScreen()
        print('\nBye!')

    def addPlayerProfile(self):
        print("\nNAME YOUR ACCOUNT\n")
        account_name = input()
        self.register_player(account_name)

    def gameSelectScreen(self):
        self.playAnimation()
        self.REPL()

    def REPL(self):
        while (self._stillRunning):
            self.selectGameOptions()
            self.clearScreen()

    def showOptions(self, optstr: str, options: list):
        print(f"SELECT {optstr}:\n")
        option_on = 0
        for option in options:
            print(str(option_on) + ": " + option.name)
            option_on += 1

    def takeOptionInput(self, optstr: str, options: list):
        while self._stillRunning:
            try:
                instr = input()
                option_selected = int(instr.strip())
                if option_selected >= len(options) or option_selected < 0:
                    raise ValueError()
            except ValueError:
                self.clearScreen()
                print("Input " + instr + " was invalid. Please try again.")
                self.showOptions(optstr, options)
                continue
            return option_selected

    def clearScreen(self):
        print("\n" * 40)
    
    def playAnimation(self):
        for i in range(0, 3):
            for frame in ANIMATION:
                self.clearScreen()
                print(frame)
                sleep(0.1)
    
    def selectPlayerOptions(self) -> PlayerAccount:
        playerList = self._players_list
        self.showOptions("PLAYER", playerList)
        selected: int = self.takeOptionInput("PLAYER", playerList)
        return playerList[selected]
    
    def selectGameOptions(self):
        self.showOptions("OPTION", self._options)
        selected: int = self.takeOptionInput("OPTION", self._options)
        self._options[selected].run()

    def selectPlayers(self, playerCount: int) -> list[PlayerAccount]:
        players_selected = 0
        to_play = list()
        while players_selected < playerCount:
            print(f"\nCHOOSE PLAYER {players_selected + 1}")
            to_play.append(self.selectPlayerOptions())
            players_selected += 1
        return to_play

    def playerAccountsToPlayerProfiles(self, players: list[PlayerAccount]) -> list[TMGE.PlayerProfile]:
        pps = list()
        for player in players:
            pps.append(TMGE.PlayerProfile(player.id, [], 0, 0))
        return pps






def main():
    TMGEshell().start()


if __name__ == '__main__':
    main()