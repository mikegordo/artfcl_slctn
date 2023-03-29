import random
import os
import json
import bottle
import socket


class SentenceGenerator:

    def get_sentence(self, file_path: str, max_length: int, min_length: int):
        """
        This function returns a random sentence from the given file path, with a length between min_length and max_length.
        :param file_path: The path to the file containing the sentences.
        :param max_length: The maximum length of the sentence to pick.
        :param min_length: The minimum length of the sentence to pick.
        :return: The randomly selected sentence.
        """
        sentence = self.pick_random_sentence(file_path, max_length, min_length)
        return self.remove_non_latin(sentence).upper().strip(' ')

    @staticmethod
    def pick_random_sentence(file_path: str, max_length: int, min_length: int):
        """
        Picks a random sentence from the given file path, with a length between min_length and max_length.
        :param file_path: The path to the file containing the sentences.
        :param max_length: The maximum length of the sentence to pick.
        :param min_length: The minimum length of the sentence to pick.
        :return: The randomly selected sentence.
        """
        with open(file_path, 'r', encoding="utf-8") as file:
            sentence = ""
            for line in file:
                sentence += line.strip('\n ') + ' '
            sentences = sentence.split('.')
            sentence = ""
            while len(sentence) > max_length or len(sentence) < min_length:
                sentence = random.choice(sentences)

        return sentence

    @staticmethod
    def remove_non_latin(sentence: str):
        """
        Removes all non-Latin characters from the given sentence.
        :param sentence: The sentence to remove non-Latin characters from.
        :return: The sentence with only Latin characters.
        """
        latin_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
        new_sentence = ""
        for char in sentence:
            if char in latin_alphabet:
                new_sentence += char
        return new_sentence

    @staticmethod
    def get_hostname():
        """
        This function returns the hostname of the machine.
        :return: The hostname of the machine.
        """
        return socket.gethostname()


sg = SentenceGenerator()
app = bottle.default_app()


@app.route(path="/get-sentence", method="GET")
def main_route():
    max_length = bottle.request.query.max_length
    max_length = int(max_length) if max_length else 1000
    max_length = min(max_length, 1000)

    min_length = bottle.request.query.min_length
    min_length = int(min_length) if min_length else 10
    min_length = max(10, min_length)

    dir_path = os.path.dirname(os.path.realpath(__file__)) + '\pg1228.txt'
    data = sg.get_sentence(dir_path, max_length, min_length)

    bottle.response.content_type = 'application/json'
    return json.dumps({'sentence': data, 'max_length': max_length, 'min_length': min_length, 'host': sg.get_hostname()})


app.run(host='localhost', port=8080)
