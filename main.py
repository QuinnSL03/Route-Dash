import discord
from discord.ext import commands
import random
import asyncio
import handeval

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="$",intents=intents)
top = "<:blankbacktop:714565166070759454>"
bot = "<:blankbackbot:714565093798576455>"
channel = client.get_channel("732386342402785418")
game = None
active_players = []
min_players = 1
messagestart = None
game_start = False
game = None


class Player: 
    def __init__(self, playerobj, hand, bal):
        self.bet = 0
        self.bal = bal
        self.hand = hand
        self.playerobj = playerobj

    def __str__(self):
        return self.hand

class Pot:
    def __init__(self, ammount, players):
        self.ammount = ammount
        self.players = players

    def findwinner(self):
        i = 1
        winner = self.players[0]
        wincondition = ""
        if len(self.players) == 1:
            return [winner, "N/A"]
        a = game.reformatcard(self.players[0].hand[0])
        b = game.reformatcard(self.players[0].hand[1])
        max = game.formatedtable + [a,b] 

        while i < len(self.players):
            a = game.reformatcard(self.players[i].hand[0])
            b = game.reformatcard(self.players[i].hand[1])
            next = game.formatedtable + [a,b] 
            result = handeval.compare_hands(max,next)
            print(i,a,b)
            if result[0] == "left":
                winner = max 
            else:
                winner = next
                max = next
            wincondition = result[1]
            i += 1
        return [winner, wincondition]
            
class Poker:
    backcardtop = ":blankbacktop:714565166070759454" 
    backcardbottom = ":blankbackbot:714565093798576455"
    pots = []
    playersin = []
    currentbet = 0
    round = 1
    players = []
    currentplayer = None
    tablecards = []
    done = False
    bet = False
    turnsleft = []
    formatedtable = []
    mainpot = None
    i = 0
    deck = ["bAc", "bAs", "rAh", "rAd", 
    "b2c", "b2s", "r2h", "r2d", 
    "b3c", "b3s", "r3h", "r3d", 
    "b4c", "b4s", "r4h", "r4d",
    "b5c", "b5s", "r5h", "r5d",
    "b6c", "b6s", "r6h", "r6d",
    "b7c", "b7s", "r7h", "r7d",
    "b8c", "b8s", "r8h", "r8d",
    "b9c", "b9s", "r9h", "r9d",
    "b10c", "b10s", "r10h", "r10d",
    "bJc", "bJs", "rJh", "rJd",
    "bQc", "bQs", "rQh", "rQd",
    "bKc", "bKs", "rKh", "rKd"]
    active_deck = deck.copy()
    
    def __init__(self, players, blind, buyin, channel):
        for player in players:
            self.players.append(Player(player,[], buyin))
        self.currentplayer = self.players[0]
        self.channel = channel
        self.mainpot = Pot(0, self.players)
        
    def find_card_emoji(self, card):
        a = card[:2]
        b = card[2:]
        if card[2:3] == "0":
            a = card[:3]
            b = card[3:]
        print(card[:2], card[2:])
        suit = ""
        if b == "c":
            suit = "eclubs"
        elif b == "s":
            suit = "espades"
        elif b == "h":
            suit = "ehearts"
        else:
            suit = "ediamonds"
        return [str(discord.utils.get(client.emojis, name=a)), str(discord.utils.get(client.emojis, name=suit))]
         
    def deal(self): 
        card = str(random.choice(self.active_deck))
        self.active_deck.remove(card)
        print(card)
        return card

    def call(self):
        self.currentplayer.bal -= self.currentbet
        self.currentplayer.bet == self.currentbet
        self.done = True
        self.turnsleft.remove(self.currentplayer)
        return

    def raisecall(self, ammount):
        self.currentbet += ammount
        self.currentplayer.bal -= self.currentbet
        self.currentplayer.bet = self.currentbet
        self.turnsleft = self.playersin.copy()
        
        self.i = self.turnsleft.index(self.currentplayer)
        self.turnsleft.remove(self.currentplayer)
        if self.i == len(self.turnsleft) and len(self.turnsleft) > 0:
            self.i = 0
        self.done = True
        return
    
    def check(self):
        self.done = True
        self.turnsleft.remove(self.currentplayer)
        return

    def fold(self):
        print(type(self.playersin))
        self.playersin.remove(self.currentplayer)
        self.done = True
        self.turnsleft.remove(self.currentplayer)
        return

    def dealplayers(self):
        for player in self.players:
            print("dealt")
            player.hand = [self.deal(), self.deal()]
        self.playersin = self.players.copy()
        
    def reformatcard(self, card):
        card = card[1:]
        if card[:2] == "1":
            card = "T" + card[2:]
        print(type(card))
        return card

    async def startround(self, channel):
        round = self.round
        while True:
            if not(self.bet):
                break
        if round == 1:
            #pre-flop
            a = ['Qd', 'Kd', '9d', 'Jd', 'Td', '4h', '5c'] 
            b = ['Qd', 'Kd', '9d', 'Jd', 'Td', 'Ad', '5c'] 
            await channel.send(handeval.compare_hands(a,b))
            print("start 1")
            await channel.send("The Pre-Flop:")
            await channel.send(top + "\t" + top + "\t" + top + "\t" + top + "\t" + top + "\n"
            + bot + "\t" + bot + "\t" + bot + "\t" + bot + "\t" + bot)
            await asyncio.sleep(.1)
            await run_menu()
            await self.betting()
        elif round == 2:
            print("start 2")
            self.tablecards.append(self.deal())
            self.tablecards.append(self.deal())
            self.tablecards.append(self.deal())
            tablecard1 = self.find_card_emoji(self.tablecards[0])
            tablecard2 = self.find_card_emoji(self.tablecards[1])
            tablecard3 = self.find_card_emoji(self.tablecards[2])
            await channel.send("The Flop:")
            await channel.send(tablecard1[0] + "\t" + tablecard2[0] + "\t" + tablecard3[0] + "\t" + top + "\t" + top + "\n"
            + tablecard1[1] + "\t" + tablecard2[1] + "\t" + tablecard3[1] + "\t" + bot + "\t" + bot)
            await asyncio.sleep(.1)
            await run_menu()
            await self.betting()
            #flop
        elif round == 3:
            self.tablecards.append(self.deal())
            tablecard1 = self.find_card_emoji(self.tablecards[0])
            tablecard2 = self.find_card_emoji(self.tablecards[1])
            tablecard3 = self.find_card_emoji(self.tablecards[2])
            tablecard4 = self.find_card_emoji(self.tablecards[3])
            await channel.send("The Turn:")
            await channel.send(tablecard1[0] + "\t" + tablecard2[0] + "\t" + tablecard3[0] + "\t" + tablecard4[0] + "\t" + top + "\n"
            + tablecard1[1] + "\t" + tablecard2[1] + "\t" + tablecard3[1] + "\t" + tablecard4[1] + "\t" + bot)
            await asyncio.sleep(.1)
            await run_menu()
            await self.betting()
            #turn
        elif round == 4:
            self.tablecards.append(self.deal())
            tablecard1 = self.find_card_emoji(self.tablecards[0])
            tablecard2 = self.find_card_emoji(self.tablecards[1])
            tablecard3 = self.find_card_emoji(self.tablecards[2])
            tablecard4 = self.find_card_emoji(self.tablecards[3])
            tablecard5 = self.find_card_emoji(self.tablecards[4])
        
            await channel.send("The River:")
            await channel.send(tablecard1[0] + "\t" + tablecard2[0] + "\t" + tablecard3[0] + "\t" + tablecard4[0] + "\t" + tablecard5[0] + "\n"
            + tablecard1[1] + "\t" + tablecard2[1] + "\t" + tablecard3[1] + "\t" + tablecard4[1] + "\t" + tablecard5[1])
            await asyncio.sleep(.1)
            await run_menu()
            await self.betting()
            #river
        else:
            for card in self.tablecards:
                self.formatedtable.append(self.reformatcard(card))
            pot = Pot(10,[Player(None, [game.deal(),game.deal()], 30), Player(None, [game.deal(),game.deal()], 30), Player(None, [game.deal(),game.deal()], 30)])
            print(pot.findwinner())
            return
            #find winner

    async def betting(self):
        self.turnsleft = self.playersin.copy()
        self.bet = True
        self.currentplayer = self.turnsleft[0]
        self.currentbet = 0
        while True:
            print("loop")
            
            await channel.send(self.currentplayer.playerobj.display_name + "'s turn\nAuto fold/check in 10 seconds")
            await asyncio.sleep(5) 
            if not(self.done):
                if self.currentplayer.bet >= self.currentbet or self.currentplayer.bal == 0:
                    await channel.send(self.currentplayer.playerobj.display_name + " auto checked")
                    self.check()
                else:
                    await channel.send(self.currentplayer.playerobj.display_name + " auto folded")
                    self.fold()
            
            if len(self.turnsleft) > 0:
                self.i += 1
                self.currentplayer = self.turnsleft[(self.i)%len(self.turnsleft)]
                self.done = False
            else:
                break

        self.done = False
        self.bet = False                  
        self.round += 1
        
        await self.startround(channel)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def create_game(players):
    global game
    game = Poker(players, 1, 100, channel)
    print(game)
    await run_game(game)
    return

async def run_menu():
    view = Menu()
    await channel.send("",view=view)

class JoinMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Join Table", style = discord.ButtonStyle.green)
    async def call(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in active_players:
            active_players.append(interaction.user)
            await interaction.response.send_message(str(interaction.user.display_name) + " joined the table! \n" + str(len(active_players)) + "/" + str(min_players))
        else:
            await interaction.response.send_message(str(interaction.user.display_name) + " already joined")

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="View Hand", style = discord.ButtonStyle.blurple)
    async def gethand(self, interaction: discord.Interaction, button: discord.ui.Button):
        i = 0
        while i < len(game.players):
            if game.players[i].playerobj.id == interaction.user.id:
                card1 = game.find_card_emoji(game.players[i].hand[0])
                card2 = game.find_card_emoji(game.players[i].hand[1])
                await interaction.response.send_message("\n" + card1[0] + "\t" + card2[0] + "\n" + card1[1] + "\t" + card2[1], ephemeral=True)
            i += 1

    @discord.ui.button(label="Call", style = discord.ButtonStyle.green)
    async def call(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("called")
        if interaction.user == game.currentplayer.playerobj and game.bet and not(game.done):
            game.call()
            await interaction.response.send_message(interaction.user.display_name +" called for " + str(game.currentbet))
        else:
            await interaction.response.send_message("Not your turn" + str(game.bet) + str(game.done), ephemeral=True)
        
    @discord.ui.button(label="Raise", style = discord.ButtonStyle.red)
    async def raisecall(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == game.currentplayer.playerobj and game.bet and not(game.done):
            game.raisecall(1)
            await interaction.response.send_message("Raised for " + str(game.currentbet))
        else:
            await interaction.response.send_message("Not your turn", ephemeral=True)

    @discord.ui.button(label="Check", style = discord.ButtonStyle.gray)
    async def check(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == game.currentplayer.playerobj and game.bet and not(game.done):
            game.check()
            await interaction.response.send_message("Checked")
        else:
            await interaction.response.send_message("Not your turn", ephemeral=True)
    @discord.ui.button(label="Fold", style = discord.ButtonStyle.grey)
    async def fold(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == game.currentplayer.playerobj and game.bet and not(game.done):
            game.fold()
            await interaction.response.send_message("Folded")
        else:
            await interaction.response.send_message("Not your turn", ephemeral=True)

@client.event
async def on_message(message):
    if message.channel.id == 732386342402785418:
        if message.author == client.user:
            return
        if message.content.startswith('$p'):
            global channel
            channel = message.channel
            
            await lobby(message)
            
async def lobby(messagestart):
    ##ex = discord.utils.get(client.emojis, name='rQ')
    view = JoinMenu()
    await messagestart.channel.send(view=view)
  
    await asyncio.sleep(2)

    if len(active_players) >= min_players:
        await messagestart.channel.send("Starting game in 5 seconds")
        await asyncio.sleep(5)

        await create_game(active_players)
        
    else:
        await messagestart.channel.send("Game Expired")

async def run_game(game):
    print("dealing")
    game.dealplayers()
    await game.startround(channel)

token = ''
client.run(token)



