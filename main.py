#
#  _                                _                __          __ _  _    _        _____      _ 
# | |                              (_)               \ \        / /(_)| |  | |      / ____|    | |
# | |      ___   __ _  _ __  _ __   _  _ __    __ _   \ \  /\  / /  _ | |_ | |__   | |         | |
# | |     / _ \ / _` || '__|| '_ \ | || '_ \  / _` |   \ \/  \/ /  | || __|| '_ \  | |     _   | |
# | |____|  __/| (_| || |   | | | || || | | || (_| |    \  /\  /   | || |_ | | | | | |____| |__| |
# |______|\___| \__,_||_|   |_| |_||_||_| |_| \__, |     \/  \/    |_| \__||_| |_|  \_____|\____/ 
#                                              __/ |                                              
#                                             |___/                         -  By CJ
#
# YouTube : www.youtube.com/@LearningWithCJ
# GitHub  : www.github.com/LearningWithCJ
# Telegram: t.me/LearningWithCJ
#

import pygame
import sys, os, random, math, copy



# Sound
class Sound:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        # pygame.mixer.init()
    
    def load(self):
        # self.shot = self._Sound("sound/shot.mp3")
        # self.reload = self._Sound("sound/reload.mp3")

        self.music = self._Music("sound/music.mp3")

    class _Sound():
        def __init__(self, sound):
            self.sound = pygame.mixer.Sound(sound)

        def play(self):
            self.sound.play()
        
    class _Music():
        def __init__(self, music):
            self.music = pygame.mixer.music.load(music)

        def play(self):
            pygame.mixer.music.play(-1)



class Game():
    def __init__(self):

        # General
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)

        self.sound = Sound()
        pygame.init()
        self.sound.load()

        # Screen
        self.screen_name = "Zombie Game"
        self.screen = pygame.display.set_mode()
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption(self.screen_name)

        self.fps = 120
        self.colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "black": (0, 0, 0),
            "white": (255, 255, 255)
        }

        self.game_logo_font = pygame.font.SysFont("fonts/HomeVideo-Regular.ttf", 100)
        self.text_font = pygame.font.SysFont("fonts/HomeVideo-Regular.ttf", 100)
        self.alert_font = pygame.font.SysFont("fonts/HomeVideo-Regular.ttf", 200)
        
        # Game Setting
        self.objects = {}
        self.spawned_objects = []
        self.player = {}
        self.enemies = {}
        self.spawned_enemies = []

        self.producer_logo = False
        self.game_logo = False
        self.game_delay = 1000

        self.game_setting = {
            "status": "play", "level": -1,
            "stages": [
                {
                    "name": "city1", "level": 1, "score": 20,
                    "pos_x_start": 10, "pos_y_start": 100, "size": 8,
                    "img": pygame.transform.scale(pygame.image.load("images/background/city1.png"), (self.screen_width, self.screen_height)),
                    "enemies": {
                        "spawned": 0, "chance": 1000,
                        "zombie_man": {
                            "health": 2, "damage": 2
                        },
                        "zombie_woman": {
                            "health": 1, "damage": 1
                        }
                    }
                },
                {
                    "name": "city2", "level": 2, "score": 40,
                    "pos_x_start": 10, "pos_y_start": 100, "size": 6,
                    "img": pygame.transform.scale(pygame.image.load("images/background/city2.png"), (self.screen_width, self.screen_height)),
                    "enemies": {
                        "spawned": 0, "chance": 800,
                        "zombie_man": {
                            "health": 3, "damage": 4
                        },
                        "zombie_woman": {
                            "health": 2, "damage": 2
                        }
                    }
                },
                {
                    "name": "city3", "level": 3, "score": 60,
                    "pos_x_start": 10, "pos_y_start": 100, "size": 3,
                    "img": pygame.transform.scale(pygame.image.load("images/background/city3.png"), (self.screen_width, self.screen_height)),
                    "enemies": {
                        "spawned": 0, "chance": 600,
                        "zombie_man": {
                            "health": 4, "damage": 6
                        },
                        "zombie_woman": {
                            "health": 3, "damage": 4
                        }
                    }
                },
                {
                    "name": "city4", "level": 4, "score": 80,
                    "pos_x_start": 10, "pos_y_start": 100, "size": 5,
                    "img": pygame.transform.scale(pygame.image.load("images/background/city4.png"), (self.screen_width, self.screen_height)),
                    "enemies": {
                        "spawned": 0, "chance": 400,
                        "zombie_man": {
                            "health": 5, "damage": 8
                        },
                        "zombie_woman": {
                            "health": 4, "damage": 6
                        }
                    }
                }
            ]
        }

    # load
    def load(self):

        self.spawned_enemies = []
        self.spawned_objects = []
        self.game_setting["stages"][self.game_setting["level"]]["enemies"]["spawned"] = 0

        # Objects
        objects_dir = "images/objects/"
        objects_indexes = {}
        objects = {"props": {"bullet": 5, "ammo": 3, "grenade": 2, "medkit": 3, "heart": 1, "empty_heart": 1}, "events": {"explosion": 1}}
        for i in objects:
            if i == "props":
                for ii in os.listdir(f"{objects_dir}{i}"):
                    png = ii.rsplit(".", 1)[0]
                    if png in objects[i]:
                        img = pygame.image.load(f"{objects_dir}{i}/{ii}").convert_alpha()
                        w, h = img.get_width() * (self.game_setting["stages"][self.game_setting["level"]]["size"] / objects[i][png]), img.get_height() * (self.game_setting["stages"][self.game_setting["level"]]["size"] / objects[i][png])
                        img = pygame.transform.scale(img, (w, h))
                        if png == "bullet": img = pygame.transform.rotate(img, -90)
                        objects_indexes[png] = {"img": img, "size_x": w, "size_y": h}
            else:
                for ii in zip(objects[i], os.listdir(f"{objects_dir}{i}")):
                    objects_indexes[ii[0]] = []
                    for iii in os.listdir(f"{objects_dir}{i}/{ii[1]}"):
                        img = pygame.image.load(f"{objects_dir}{i}/{ii[1]}/{iii}").convert_alpha()
                        w, h = img.get_width() * (self.game_setting["stages"][self.game_setting["level"]]["size"] / objects[i][ii[0]]), img.get_height() * (self.game_setting["stages"][self.game_setting["level"]]["size"] / objects[i][ii[0]])
                        img = pygame.transform.scale(img, (w, h))
                        objects_indexes[ii[0]].append({"img": img, "size_x": w, "size_y": h})

        self.objects = {
            "props": {
                "heart": objects_indexes["heart"],
                "emptyHeart": objects_indexes["empty_heart"],
                "ammo": {
                    "name": "ammo",
                    "pos_x": 0, "pos_y": -objects_indexes["ammo"]["size_y"],
                    "index": objects_indexes["ammo"],
                    "speed": 5,
                    "magazine": 30, "grenade": 1
                },
                "medkit": {
                    "name": "medkit",
                    "pos_x": 0, "pos_y": -objects_indexes["medkit"]["size_y"],
                    "index": objects_indexes["medkit"],
                    "speed": 5,
                    "heal": 20
                },
                "bullet": {
                    "name": "bullet",
                    "magazine": [30, 120],
                    "index": objects_indexes["bullet"],
                    "speed": 10, "damage": 1,
                    "pos_x": 17 * self.game_setting["stages"][self.game_setting["level"]]["size"],
                    "pos_y": 38 * self.game_setting["stages"][self.game_setting["level"]]["size"],
                    "dir": ""
                },
                "grenade": {
                    "name": "grenade",
                    "index": objects_indexes["grenade"],
                    "speed": 10, "radius": 300, "damage": 10,
                    "pos_x": 0,
                    "pos_y": 46 * self.game_setting["stages"][self.game_setting["level"]]["size"],
                    "dir": ""
                },

            },
            "events": {
                "explosion": {
                    "index": 0,
                    "indexes": objects_indexes["explosion"]
                }
            }
        }

        # Player
        player_dir = "images/player/"

        self.player_total_health = 100
        self.player_each_health = self.player_total_health / 5

        player_indexes = {}
        statuses = ["stand", "walk", "run", "shot", "grenade", "reload", "death"]
        for i in statuses:
            player_indexes[i] = []
            for ii in os.listdir(f"{player_dir}{i}"):
                img = pygame.image.load(f"{player_dir}{i}/{ii}").convert_alpha()
                w, h = img.get_width() * self.game_setting["stages"][self.game_setting["level"]]["size"], img.get_height() * self.game_setting["stages"][self.game_setting["level"]]["size"]
                img = pygame.transform.scale(img, (w, h))
                player_indexes[i].append({"img": img, "size_x": w, "size_y": h})

        self.player = {
            "size_x": player_indexes["stand"][0]["size_x"], "size_y": player_indexes["stand"][0]["size_y"],
            "pos_x": self.game_setting["stages"][self.game_setting["level"]]["pos_x_start"], "pos_y": self.screen_height - self.game_setting["stages"][self.game_setting["level"]]["pos_y_start"] - player_indexes["stand"][0]["size_y"],
            "totalHealth": self.player_total_health, "eachHealthAmount": self.player_each_health, "health": self.player_total_health,
            "dir": "right", "gravity": 0, "status": "stand", "score": 0, "magazine": [self.objects["props"]["bullet"]["magazine"][0], self.objects["props"]["bullet"]["magazine"][1]], "grenade": 5,
            "statuses": {
                "stand": {"index": 0, "indexes": player_indexes["stand"]},
                "walk": {"speed": 5, "index": 0, "indexes": player_indexes["walk"]},
                "run": {"speed": 10, "index": 0, "indexes": player_indexes["run"]},
                # "jump": {"speed": 20, "length": 200, "index": 0, "indexes": []},
                "shot": {"index": 0, "indexes": player_indexes["shot"]},
                "grenade": {"index": 0, "indexes": player_indexes["grenade"]},
                "reload": {"index": 0, "indexes": player_indexes["reload"]},
                "death": {"index": 0, "indexes": player_indexes["death"]}
            }
        }

        # Enemiy
        enemies_dir = "images/enemies/"

        enemies_indexes = {}
        enemies = {
            "zombie_man": ["stand", "walk", "run", "attack", "death"],
            "zombie_woman": ["stand", "walk", "run", "attack", "death"]
        }
        for i in enemies:
           enemies_indexes[i] = {}
           for ii in enemies[i]:
                enemies_indexes[i][ii] = []
                for iii in os.listdir(f"{enemies_dir}{i}/{ii}"):
                    img = pygame.image.load(f"{enemies_dir}{i}/{ii}/{iii}").convert_alpha()
                    w, h = img.get_width() * self.game_setting["stages"][self.game_setting["level"]]["size"], img.get_height() * self.game_setting["stages"][self.game_setting["level"]]["size"]
                    img = pygame.transform.scale(img, (w, h))
                    enemies_indexes[i][ii].append({"img": img, "size_x": w, "size_y": h})

        # Zombie Man
        self.enemies = {
            "zombie_man": {
                "indexes": {
                    "stand": enemies_indexes["zombie_man"]["stand"],
                    "walk": enemies_indexes["zombie_man"]["walk"],
                    "run": enemies_indexes["zombie_man"]["run"],
                    "attack": enemies_indexes["zombie_man"]["attack"],
                    "death": enemies_indexes["zombie_man"]["death"]
                },
                "data": {
                    "name": "zombie_man",
                    "pos_x": self.screen_width + 50, "pos_y": 0,
                    "dir": "left", "health": 0, "status": "stand", "score": 1, "opacity": 400,
                    "moveType": "",
                    "statuses": {
                        "stand": {"index": 0, "indexes": []},
                        "walk": {"speed": (1, 3), "index": 0, "indexes": []},
                        "run": {"speed": (4, 6), "index": 0, "indexes": []},
                        "attack": {"range": (50, 100), "damage": 0, "index": 0, "indexes": []},
                        "death": {"index": 0, "indexes": []}
                    }
                }
            },
            "zombie_woman": {
                "indexes": {
                    "stand": enemies_indexes["zombie_woman"]["stand"],
                    "walk": enemies_indexes["zombie_woman"]["walk"],
                    "run": enemies_indexes["zombie_woman"]["run"],
                    "attack": enemies_indexes["zombie_woman"]["attack"],
                    "death": enemies_indexes["zombie_woman"]["death"]
                },
                "data": {
                    "name": "zombie_woman",
                    "pos_x": self.screen_width + 50, "pos_y": 0,
                    "dir": "left", "health": 0, "status": "stand", "score": 1, "opacity": 400,
                    "moveType": "",
                    "statuses": {
                        "stand": {"index": 0, "indexes": []},
                        "walk": {"speed": (1, 2), "index": 0, "indexes": []},
                        "run": {"speed": (3, 5), "index": 0, "indexes": []},
                        "attack": {"range": (50, 80), "damage": 0, "index": 0, "indexes": []},
                        "death": {"index": 0, "indexes": []}
                    }
                }
            }
        }

    # ui
    def ui(self, type=""):
        # Private Logo
        if not self.producer_logo or type == "producer_logo":
            self.producer_logo = True
            img = pygame.image.load("images/producer_logo/producer_logo.png").convert_alpha()

            alpha = -400
            done = False
            while True:
                self.screen.fill(self.colors["black"])
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                imgRect = img.get_rect(center=self.screen.get_rect().center)
                img.set_alpha(alpha)
                self.screen.blit(img, imgRect)

                if alpha >= 255 and not done:
                    done = True
                    alpha = 800
                if done:
                    alpha -= 0.8
                    if alpha <= 0:
                        break
                else:
                    alpha += 0.8

                pygame.display.update()

        # Game Logo
        if not self.game_logo or type == "game_logo":
            self.game_logo = True

            alpha = -400
            done = False
            while True:
                self.screen.fill(self.colors["black"])
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                text = self.game_logo_font.render(self.screen_name, True, self.colors["white"])
                text.set_alpha(alpha)
                textRect = text.get_rect(center=self.screen.get_rect().center)
                self.screen.blit(text, textRect)

                if alpha >= 255 and not done:
                    done = True
                    alpha = 800
                if done:
                    alpha -= 0.8
                    if alpha <= 0:
                        break
                else:
                    alpha += 0.8

                pygame.display.update()

            self.sound.music.play()

        if type == "owner_logo":
            alpha = -300
            done = False
            while True:
                self.screen.fill(self.colors["black"])
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                text = self.game_logo_font.render("LearningWithCJ", True, self.colors["white"])
                text.set_alpha(alpha)
                textRect = text.get_rect(center=self.screen.get_rect().center)
                self.screen.blit(text, textRect)

                if alpha >= 255 and not done:
                    done = True
                    alpha = 800
                if done:
                    alpha -= 0.8
                    if alpha <= 0:
                        break
                else:
                    alpha += 0.8

                pygame.display.update()
            pygame.quit()
            sys.exit()

        # Texts
        if type == "score":
            text = self.text_font.render(f"Score: {self.player["score"]}", True, self.colors["white"])
            self.screen.blit(text, (20, 20))
        elif type == "ammo":
            text = self.text_font.render(f"{self.player["grenade"]} - {self.player["magazine"][0]}/{self.player["magazine"][1]}", True, self.colors["white"])
            self.screen.blit(text, (self.screen_width - text.get_width() - 20, 20))
        elif type == "gameover":
            text = self.alert_font.render("Game Over", True, self.colors['red'])
            self.screen.blit(text, text.get_rect(center=self.screen.get_rect().center))
        elif type == "gamewin":
            text = self.alert_font.render("You Won", True, self.colors["white"])
            self.screen.blit(text, text.get_rect(center=self.screen.get_rect().center))

    # Game Setting
    def game(self):
        # Level
        if self.game_setting["level"] == -1 or self.player["score"] >= self.game_setting["stages"][self.game_setting["level"]]["score"]:
            if self.game_setting["level"] == len(self.game_setting["stages"]) - 1:
                self.game_setting["status"] = "gamewin"    
            else:
                self.game_setting["level"] += 1

                self.load()

                self.game_setting["status"] = "play"

        self.screen.blit(self.game_setting["stages"][self.game_setting["level"]]["img"], (0, 0))
        self.ui("score")
        self.ui("ammo")

        # Game Win
        if self.game_setting["status"] == "gamewin":
            self.player["health"], self.player["status"] = self.player_total_health, "stand"

            self.ui("gamewin")

            self.game_delay -= 1
            if self.game_delay <= 0:
                self.ui("owner_logo")

        # Game Over
        if self.game_setting["status"] == "gameover":
            self.ui("gameover")

            self.game_delay -= 1
            if self.game_delay <= 0:
                self.game_delay = 400

                self.load()

                self.game_setting["status"] = "play"

    # Player
    def player_func(self):
        # General
        index = self.player["statuses"][self.player["status"]]["indexes"][int(self.player["statuses"][self.player["status"]]["index"])]
        self.player["size_x"], self.player["size_y"] = index["size_x"], index["size_y"]
        self.player["pos_y"] = self.screen_height - self.game_setting["stages"][self.game_setting["level"]]["pos_y_start"] - index["size_y"]

        # Health
        if self.player["health"] % self.player_each_health == 0:
            heart = int(self.player["health"] / self.player_each_health)
        else:
            heart = int(self.player["health"] / self.player_each_health + 1)
        emptyHeart = int(self.player_total_health / self.player_each_health - heart)
        coord = self.screen_width / 2 - ((heart + emptyHeart) * self.objects["props"]["heart"]["size_x"]) / 2
        for h in range(1, heart + emptyHeart + 1):
            if h <= heart:
                self.screen.blit(self.objects["props"]["heart"]["img"], (coord, 20))
            else:
                self.screen.blit(self.objects["props"]["emptyHeart"]["img"], (coord, 20))
            coord += self.objects["props"]["heart"]["size_x"] + 10
        if self.player["health"] <= 0:
            self.player["health"] = 0
            self.player["status"] = "death"

        # Stand, Walk & Run
        if self.player["status"] in ("stand", "walk", "run"):
            img = self.player["statuses"][self.player["status"]]["indexes"][int(self.player["statuses"][self.player["status"]]["index"])]["img"]
            self.player["statuses"][self.player["status"]]["index"] += 0.1
            if round(self.player["statuses"][self.player["status"]]["index"], 1) > len(self.player["statuses"][self.player["status"]]["indexes"]) - 1: self.player["statuses"][self.player["status"]]["index"] = 0
            if self.player["dir"] == "left": img = pygame.transform.flip(img, True, False)
            self.screen.blit(img, (self.player["pos_x"], self.player["pos_y"]))
        
        # Jump
        # elif self.player["status"] == "jump":
        #     pass

        # Shot
        elif self.player["status"] == "shot":
            img = self.player["statuses"]["shot"]["indexes"][int(self.player["statuses"]["shot"]["index"])]["img"]
            self.player["statuses"]["shot"]["index"] += 0.1
            if round(self.player["statuses"]["shot"]["index"], 1) == 2.0:
                self.spawned_objects.append(
                    {
                        "name": self.objects["props"]["bullet"]["name"],
                        "img": self.objects["props"]["bullet"]["index"]["img"],
                        "size_x": self.objects["props"]["bullet"]["index"]["size_x"], "size_y": self.objects["props"]["bullet"]["index"]["size_y"],
                        "damage": self.objects["props"]["bullet"]["damage"],
                        "speed": self.objects["props"]["bullet"]["speed"],
                        "pos_x": self.player["pos_x"] + self.player["size_x"] - self.objects["props"]["bullet"]["pos_x"] if self.player["dir"] == "right" else self.player["pos_x"] + self.objects["props"]["bullet"]["pos_x"],
                        "pos_y": self.player["pos_y"] + self.player["size_y"] - self.objects["props"]["bullet"]["pos_y"],
                        "dir": self.player["dir"]
                    }
                )
                self.player["magazine"][0] -= 1
                # self.sound.shot.play()
            if round(self.player["statuses"]["shot"]["index"], 1) > len(self.player["statuses"]["shot"]["indexes"]) - 1:
                self.player["statuses"]["shot"]["index"] = 0
                self.player["status"] = "stand"
            if self.player["dir"] == "left": img = pygame.transform.flip(img, True, False)
            self.screen.blit(img, (self.player["pos_x"], self.player["pos_y"]))

        # Grenade
        elif self.player["status"] == "grenade":
            img = self.player["statuses"][self.player["status"]]["indexes"][int(self.player["statuses"][self.player["status"]]["index"])]["img"]
            self.player["statuses"][self.player["status"]]["index"] += 0.1
            if round(self.player["statuses"][self.player["status"]]["index"], 1) > len(self.player["statuses"][self.player["status"]]["indexes"]) - 1:
                self.player["statuses"][self.player["status"]]["index"] = 0
                self.spawned_objects.append(
                    {
                        "name": self.objects["props"]["grenade"]["name"],
                        "img": self.objects["props"]["grenade"]["index"]["img"],
                        "size_x": self.objects["props"]["grenade"]["index"]["size_x"], "size_y": self.objects["props"]["grenade"]["index"]["size_y"],
                        "speed": self.objects["props"]["grenade"]["speed"],
                        "damage": self.objects["props"]["grenade"]["damage"],
                        "radius": self.objects["props"]["grenade"]["radius"],
                        "pos_x": self.player["pos_x"] + self.player["size_x"] if self.player["dir"] == "right" else self.player["pos_x"],
                        "pos_y": self.player["pos_y"] + self.player["size_y"] - self.objects["props"]["grenade"]["pos_y"],
                        "dir": self.player["dir"]
                    }
                )
                self.player["grenade"] -= 1
            if self.player["dir"] == "left": img = pygame.transform.flip(img, True, False)
            self.screen.blit(img, (self.player["pos_x"], self.player["pos_y"]))
        
        # Reload
        elif self.player["status"] == "reload":
            # if self.player["statuses"][self.player["status"]]["index"] == 0: self.sound.reload.play()
            img = self.player["statuses"][self.player["status"]]["indexes"][int(self.player["statuses"][self.player["status"]]["index"])]["img"]
            self.player["statuses"][self.player["status"]]["index"] += 0.1
            if round(self.player["statuses"][self.player["status"]]["index"], 1) > len(self.player["statuses"][self.player["status"]]["indexes"]) - 1:
                self.player["statuses"][self.player["status"]]["index"] = 0
                free = 30 - self.player["magazine"][0]
                if self.player["magazine"][1] >= free:
                    self.player["magazine"][0] += free
                    self.player["magazine"][1] -= free
                else:
                    self.player["magazine"][0] += self.player["magazine"][1]
                    self.player["magazine"][1] -= self.player["magazine"][1]
                self.player["status"] = "stand"
            if self.player["dir"] == "left": img = pygame.transform.flip(img, True, False)
            self.screen.blit(img, (self.player["pos_x"], self.player["pos_y"]))

        # Death
        elif self.player["status"] == "death":
            img = self.player["statuses"]["death"]["indexes"][int(self.player["statuses"]["death"]["index"])]["img"]
            self.player["statuses"]["death"]["index"] += 0.1
            if round(self.player["statuses"]["death"]["index"], 1) > len(self.player["statuses"]["death"]["indexes"]) - 1:
                self.player["statuses"]["death"]["index"] = len(self.player["statuses"]["death"]["indexes"]) - 1
                self.game_setting["status"] = "gameover"
            if self.player["dir"] == "left": img = pygame.transform.flip(img, True, False)
            self.player["pos_y"] = self.screen_height - self.game_setting["stages"][self.game_setting["level"]]["pos_y_start"] - img.get_height()
            self.screen.blit(img, (self.player["pos_x"], self.player["pos_y"]))

        # Jump
        # if self.player["statuses"]["jump"]["index"] > 0:
        #     if self.player["gravity"] < self.player["statuses"]["jump"]["index"]:
        #         self.player["gravity"] += self.player["statuses"]["jump"]["speed"]
        #         self.player["pos_y"] -= self.player["statuses"]["jump"]["speed"]
        #     elif self.player["gravity"] == self.player["statuses"]["jump"]["index"]:
        #         self.player["gravity"] -= self.player["statuses"]["jump"]["speed"]
        #         self.player["pos_y"] += self.player["statuses"]["jump"]["speed"]
        #         self.player["statuses"]["jump"]["index"] -= self.player["statuses"]["jump"]["speed"]

    # Objects
    def object(self):
        props = ["ammo", "medkit"]
        if random.randint(1, 1000000) % random.randint(1, 5000) == 0:
            prop = random.choice(props)
            self.spawned_objects.append(self.objects["props"][prop].copy())
            self.spawned_objects[-1]["pos_x"] = random.randint(50, self.screen_width - 50)
            self.spawned_objects[-1]["size_x"] = self.spawned_objects[-1]["index"]["size_x"]
            self.spawned_objects[-1]["size_y"] = self.spawned_objects[-1]["index"]["size_y"]

        for o in self.spawned_objects:
            if o["name"] == "bullet" and (o["pos_x"] > self.screen_width or o["pos_x"] < 0):
                self.spawned_objects.remove(o); continue

            if o["name"] in props:
                if o["pos_y"] < self.screen_height - self.game_setting["stages"][self.game_setting["level"]]["pos_y_start"] - o["size_y"]:
                    free = self.screen_height - self.game_setting["stages"][self.game_setting["level"]]["pos_y_start"] - o["size_y"] - o["pos_y"]
                    if free < o["speed"]: o["pos_y"] += free
                    else: o["pos_y"] += o["speed"]
                if len(list(filter(lambda x: x in list(range(int(self.player["pos_x"]), int(self.player["pos_x"]) + int(self.player["size_x"]))), list(range(int(o["pos_x"]), int(o["pos_x"]) + int(o["size_x"])))))) > 0 and \
                    len(list(filter(lambda x: x in list(range(int(self.player["pos_y"]), int(self.player["pos_y"]) + int(self.player["size_y"]))), list(range(int(o["pos_y"]), int(o["pos_y"]) + int(o["size_y"])))))) > 0:
                    if o["name"] == "ammo":
                        self.player["magazine"][1] += o["magazine"]
                        self.player["grenade"] += o["grenade"]
                        self.spawned_objects.remove(o)
                    elif o["name"] == "medkit":
                        if self.player["health"] < self.player_total_health:
                            self.player["health"] += o["heal"]
                            if self.player["health"] > self.player_total_health: self.player["health"] = self.player_total_health
                            self.spawned_objects.remove(o)
                self.screen.blit(o["index"]["img"], (o["pos_x"], o["pos_y"]))

            # Player Bullet
            if o["name"] == "bullet":
                img = o["img"]
                if o["dir"] == "left": o["pos_x"] -= o["speed"]; img = pygame.transform.flip(img, True, False)
                else: o["pos_x"] += o["speed"]
                self.screen.blit(img, (o["pos_x"], o["pos_y"]))

                for e in self.spawned_enemies:
                    if e["status"] != "death":
                        if o["pos_x"] in list(range(int(e["pos_x"]), int(e["pos_x"]) + int(e["size_x"]))):
                            e["health"] -= o["damage"]
                            self.spawned_objects.remove(o)
                            break

            # Player Grenade
            elif o["name"] == "grenade":
                if o["pos_y"] < (self.screen_height - self.game_setting["stages"][self.game_setting["level"]]["pos_y_start"] - o["size_y"]):
                    img = o["img"]
                    free = self.screen_height - self.game_setting["stages"][self.game_setting["level"]]["pos_y_start"] - o["size_y"] - o["pos_y"]
                    if free < o["speed"] / 3: o["pos_y"] += free
                    else: o["pos_y"] += o["speed"] / 3
                    if o["dir"] == "left":
                        o["pos_x"] -= o["speed"]
                        img = pygame.transform.flip(img, True, False)
                    else: o["pos_x"] += o["speed"]
                    self.screen.blit(img, (o["pos_x"], o["pos_y"]))
                else:
                    index = self.objects["events"]["explosion"]["indexes"][int(self.objects["events"]["explosion"]["index"])]
                    img = index["img"]
                    self.objects["events"]["explosion"]["index"] += 0.1
                    if round(self.objects["events"]["explosion"]["index"], 1) == 2.0:
                        for e in self.spawned_enemies:
                            if math.dist([e["pos_x"]], [o["pos_x"]]) < o["radius"] or math.dist([e["pos_x"] + e["size_x"]], [o["pos_x"]]) < o["radius"]:
                                e["health"] -= o["damage"]
                    if round(self.objects["events"]["explosion"]["index"], 1) > len(self.objects["events"]["explosion"]["indexes"]) - 1:
                        self.objects["events"]["explosion"]["index"] = 0
                        self.spawned_objects.remove(o)
                    if o["dir"] == "left": img = pygame.transform.flip(img, True, False)
                    self.screen.blit(img, (o["pos_x"] - index["size_x"] / 2, o["pos_y"] - index["size_y"]))

    # Enemy Spawner
    def enemy_spawner(self):
        if self.game_setting["status"] == "play" and self.game_setting["stages"][self.game_setting["level"]]["enemies"]["spawned"] < self.game_setting["stages"][self.game_setting["level"]]["score"]:
            if random.randint(1, 1000000) % random.randint(1, self.game_setting["stages"][self.game_setting["level"]]["enemies"]["chance"]) == 1:
                c = random.choice(tuple(self.enemies.keys()))
                s = copy.deepcopy(self.enemies[c]["data"])
                for i in self.enemies[c]["indexes"]:
                    s["statuses"][i]["indexes"] = self.enemies[c]["indexes"][i]
                s["health"] = self.game_setting["stages"][self.game_setting["level"]]["enemies"][c]["health"]
                if random.randint(1, 10) % random.randint(1, 10) == 0: s["moveType"] = "run"
                else: s["moveType"] = "walk"

                s["statuses"]["attack"]["damage"] = self.game_setting["stages"][self.game_setting["level"]]["enemies"][c]["damage"]
                s["statuses"]["walk"]["speed"] = random.randint(s["statuses"]["walk"]["speed"][0], s["statuses"]["walk"]["speed"][1])
                s["statuses"]["run"]["speed"] = random.randint(s["statuses"]["run"]["speed"][0], s["statuses"]["run"]["speed"][1])
                s["statuses"]["attack"]["range"] = random.randint(s["statuses"]["attack"]["range"][0], s["statuses"]["attack"]["range"][1])

                self.spawned_enemies.append(s)
                self.game_setting["stages"][self.game_setting["level"]]["enemies"]["spawned"] += s["score"]

    # Enemy AI
    def enemy_ai(self):
        for e in self.spawned_enemies:
            # General
            index = e["statuses"][e["status"]]["indexes"][int(e["statuses"][e["status"]]["index"])]
            e["size_x"], e["size_y"] = index["size_x"], index["size_y"]
            e["pos_y"] = self.screen_height - self.game_setting["stages"][self.game_setting["level"]]["pos_y_start"] - index["size_y"]
            
            if self.game_setting["status"] == "play" or e["status"] == "death":
                if e["status"] != "death":
                    if self.player["pos_x"] > e["pos_x"]:
                        e["dir"] = "right"
                        if int(math.dist([self.player["pos_x"]], [e["pos_x"]])) > e["statuses"]["attack"]["range"]:
                            e["pos_x"] += e["statuses"][e["moveType"]]["speed"]
                            e["status"] = e["moveType"]
                        else:
                            e["status"] = "attack"
                    else:
                        e["dir"] = "left"
                        if int(math.dist([self.player["pos_x"]], [e["pos_x"]])) > e["statuses"]["attack"]["range"]:
                            e["pos_x"] -= e["statuses"][e["moveType"]]["speed"]
                            e["status"] = e["moveType"]
                        else:
                            e["status"] = "attack"
                else:
                    if int(e["statuses"]["death"]["index"]) == len(e["statuses"]["death"]["indexes"]) - 1:
                        e["opacity"] -= 1
                        if e["opacity"] <= 0:
                            self.spawned_enemies.remove(e)
            else:
                if e["status"] in ("walk", "run", "attack"):
                    e["status"] = "stand"

    # Enemy
    def enemy(self):
        for e in self.spawned_enemies:
            if e["status"] != "death" and (e["health"] == 0 or e["health"] < 0):
                e["status"] = "death"
                self.player["score"] += e["score"]

            if e["status"] in ("stand", "walk", "run"):
                img = e["statuses"][e["status"]]["indexes"][int(e["statuses"][e["status"]]["index"])]["img"]
                if e["statuses"][e["status"]]["index"] < len(e["statuses"][e["status"]]["indexes"]) - 1: e["statuses"][e["status"]]["index"] += 0.1
                else: e["statuses"][e["status"]]["index"] = 0
                if e["dir"] == "left": img = pygame.transform.flip(img, True, False)
                self.screen.blit(img, (e["pos_x"], e["pos_y"]))
            elif e["status"] == "attack":
                img = e["statuses"]["attack"]["indexes"][int(e["statuses"]["attack"]["index"])]["img"]
                if round(e["statuses"]["attack"]["index"], 1) == 3.0:
                    if e["dir"] == "right":
                        if e["pos_x"] > self.player["pos_x"] and e["pos_x"] < (self.player["pos_x"] + self.player["size_x"] + e["statuses"]["attack"]["range"]):
                            self.player["health"] -= e["statuses"]["attack"]["damage"]
                    else:
                        if e["pos_x"] < (self.player["pos_x"] + self.player["size_x"]) and e["pos_x"] > (self.player["pos_x"] - e["statuses"]["attack"]["range"]):
                            self.player["health"] -= e["statuses"]["attack"]["damage"]
                if e["statuses"]["attack"]["index"] < len(e["statuses"]["attack"]["indexes"]) - 1: e["statuses"]["attack"]["index"] += 0.1
                else: e["statuses"]["attack"]["index"] = 0
                if e["dir"] == "left": img = pygame.transform.flip(img, True, False)
                self.screen.blit(img, (e["pos_x"], e["pos_y"]))
            elif e["status"] == "death":
                img = e["statuses"]["death"]["indexes"][int(e["statuses"]["death"]["index"])]["img"]
                if e["statuses"]["death"]["index"] < len(e["statuses"]["death"]["indexes"]) - 1: e["statuses"]["death"]["index"] += 0.05
                if e["dir"] == "left": img = pygame.transform.flip(img, True, False)
                e["pos_y"] = self.screen_height - self.game_setting["stages"][self.game_setting["level"]]["pos_y_start"] - img.get_height()
                img.set_alpha(e["opacity"])
                self.screen.blit(img, (e["pos_x"], e["pos_y"]))

    # Main Loop
    def main(self):
        clock = pygame.time.Clock()
        while True:
            # ui
            self.ui()

            # Game Setting
            self.game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.game_setting["status"] == "play":
                if self.player["status"] != "death" and self.player["statuses"]["shot"]["index"] == 0 and self.player["statuses"]["reload"]["index"] == 0 and self.player["statuses"]["grenade"]["index"] == 0:
                    keys = pygame.key.get_pressed()
                    mouse = pygame.mouse.get_pressed()
                    if keys[pygame.K_d]:
                        if keys[pygame.K_LSHIFT]:
                            if self.player["pos_x"] + self.player["size_x"] + self.player["statuses"]["run"]["speed"] < self.screen_width - 10:
                                self.player["pos_x"] += self.player["statuses"]["run"]["speed"]
                                self.player["status"] = "run"
                                self.player["dir"] = "right"
                        else:
                            if self.player["pos_x"] + self.player["size_x"] + self.player["statuses"]["walk"]["speed"] < self.screen_width - 10:
                                self.player["pos_x"] += self.player["statuses"]["walk"]["speed"]
                                self.player["status"] = "walk"
                                self.player["dir"] = "right"
                    elif keys[pygame.K_a]:
                        if keys[pygame.K_LSHIFT]:
                            if self.player["pos_x"] - self.player["statuses"]["run"]["speed"] > 10:
                                self.player["pos_x"] -= self.player["statuses"]["run"]["speed"]
                                self.player["status"] = "run"
                                self.player["dir"] = "left"
                        else:
                            if self.player["pos_x"] - self.player["statuses"]["walk"]["speed"] > 10:
                                self.player["pos_x"] -= self.player["statuses"]["walk"]["speed"]
                                self.player["status"] = "walk"
                                self.player["dir"] = "left"
                    elif keys[pygame.K_r]:
                        if self.player["magazine"][0] < self.objects["props"]["bullet"]["magazine"][0] and self.player["magazine"][1] != 0:
                            self.player["status"] = "reload"
                    elif keys[pygame.K_g]:
                        if self.player["grenade"] > 0:
                            self.player["status"] = "grenade"
                    elif mouse[0]:
                        if self.player["magazine"][0] > 0:
                            self.player["status"] = "shot"
                    elif not keys[pygame.K_d] and not keys[pygame.K_a] and not keys[pygame.K_SPACE] and not pygame.mouse.get_pressed()[0]:
                        self.player["status"] = "stand"
                    # if keys[pygame.K_SPACE] and self.player["statuses"]["jump"]["index"] == 0:
                    #     self.player["statuses"]["jump"]["index"] += self.player["statuses"]["jump"]["length"]
                        # self.player["status"] = "jump"
            else:
                if self.player["status"] != "death" and self.player["statuses"]["shot"]["index"] == 0 and self.player["statuses"]["reload"]["index"] == 0 and self.player["statuses"]["grenade"]["index"] == 0:
                    self.player["status"] = "stand"

            # Player
            self.player_func()

            # Enemy
            self.enemy_spawner()
            self.enemy_ai()
            self.enemy()

            # Object
            self.object()

            # Update the Display
            pygame.display.update()
            clock.tick(self.fps)



if __name__ == "__main__":
    game = Game()
    game.main()