# TODO: Make a leaderboard class and integrate it with the game file.

import pygame
import datetime
import os
import json

# This class handles the leaderboard and holds some pretty good snippets (IMO, remember - this is my first game).


class Leaderboard(pygame.font.Font):
    FILE_NAME = "leaderboard.json"
    score = None
    font = None
    new_score = None
    new_name = None
    scores = None

    def __init__(self, new_name, new_score):
        self.score = 0
        self.font = pygame.font.SysFont("freesansbold.ttf", 17)
        self.new_score = int(new_score)
        self.new_name = new_name
        self.topScore = 0

        if not os.path.isfile(self.FILE_NAME):
            self.on_empty_file()

    # So here's a check if the highscore file exists or not, and if
    # it doesn't it creates a file with an empty list in it (so the JSON-parser doesn't go bananans).
    def on_empty_file(self):
        empty_score_file = open(self.FILE_NAME, "w")
        empty_score_file.write("[]")
        empty_score_file.close()

    # Here we save the score as JSON.
    # At this point we should have loaded the previous scores already (but if we haven't, it will do it "again").
    # Then we append *this* score to the list of previous scores, then we sort it in a separate method by highest score,
    # and finally we write it to the leaderboard.json-file. Tada!
    def save_score(self):
        if not self.scores == None:  # Make sure the prev. scores are loaded.
            new_json_score = {  # Create a JSON-object with the score, name and a timestamp.
                "name": self.new_name,
                "score": self.new_score,
                "date": str(datetime.datetime.now().date())
            }

            self.scores.append(new_json_score)  # Add the score to the list of scores.

            self.scores = self.sort_scores(self.scores)  # Sort the scores.

            highscore_file = open(self.FILE_NAME, "r+")
            highscore_file.write(json.dumps(self.scores))  # Save the list of scores to highscore.json
        else:
            self.load_previous_scores()  # This is reeeally bad practice...
            self.save_score()  # ...and lets hope loading works!

    def sort_scores(self, json):
        # A somewhat dirty method for sorting the JSON entries... It works though!
        scores_dict = dict()  # Create a dictionary object.
        sorted_list = list()  # Create a list object.

        for obj in json:
            scores_dict[
                obj["score"]] = obj  # Add every score to a dictionary with its score as key. Key collisions ensue...

        for key in sorted(scores_dict.keys(),
                          reverse=True):  # Read the sorted dictionary in reverse order (highest score first)...
            sorted_list.append(scores_dict[key])  # ...and add it to a list.
        self.topScore = sorted_list[0]

        return sorted_list  # Tada! Returns a sorted list.

    # Reads the previous scores from the highscores.json-file
    # and adds it to a list (a python list object, that is).
    def load_previous_scores(self):
        with open(self.FILE_NAME) as highscore_file:
            self.scores = json.load(highscore_file)
            self.scores = self.scores

    # Just like every other draw method, this
    # paints the list. But this paints every score
    # in the list with a 20px padding to the next one.
    def draw(self, screen):
        padding_y = 0
        max_scores = 10  # We *could* paint every score, but it's not any good if you can't see them (because we run out of the screen).
        nbr_scores = 1
        for score in self.scores:
            if nbr_scores <= max_scores:
                screen.blit(
                    self.font.render(str(nbr_scores) + ". " + str(score["name"]) + ": " + str(score["score"]), 1,
                                     (0, 0, 0)), (220, 200 + padding_y))
                padding_y += 20
                nbr_scores += 1
