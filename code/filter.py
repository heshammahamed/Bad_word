import re
from abc import ABC, abstractmethod
from time import time
import logging
from chunks_processing_info import ChunkFilteringInfo, elapsed
from arguments import Args
import ahocorasick
from pandas import DataFrame


# interface (abstract class)
class TextFilter(ABC):
    @abstractmethod
    def __init__(self, bad_words: list[str],args:Args):
        pass

    @abstractmethod
    def prepare(self) -> None:
        """you must call once before you calling filter function"""
        pass

    @abstractmethod
    def filter(self, chunk: DataFrame ,chunk_number : int) :
        """Filters Healthy and UnHealthy Rows count"""
        pass


class AhoCorasickFilter(TextFilter):
    def __init__(self, bad_words: list[str] , args:Args):
        self.bad_words = bad_words
        self.args = args

    def prepare(self) -> None:
        # making the trie and aho search
        self.automaton = ahocorasick.Automaton()
        for word in map(lambda x: x.lower(), self.bad_words):
            self.automaton.add_word(word, word)
        self.automaton.make_automaton()

    def filter(self, chunk: DataFrame ,chunk_number:int):

        logging.info(
            "%s  Consumer: start filtering chunk number %s",
            elapsed(self.args.starting_time),
            chunk_number + 1,
        )
        start = time()

        health_filter = chunk.apply(
            lambda row: not any(
                map(
                    lambda field: len(list(self.automaton.iter(str(field).lower())))
                    != 0,
                    row,
                )
            ),
            axis=1,
        )
        end = time()
        logging.info(
            "%s  Consumer: finish filtering chunk number %s",
            elapsed(self.args.starting_time),
            chunk_number + 1,
        )
        dif = end - start
        healthy_rows_number = sum(health_filter)
        unhealthy_rows_number = len(health_filter) - healthy_rows_number
        return healthy_rows_number, unhealthy_rows_number , dif

    def __repr__(self) -> str:
        return "AhoCorasick"


class RegexFilter(TextFilter):
    def __init__(self, bad_words: list[str] , args:Args):
        self.bad_words = bad_words
        self.args = args

    def prepare(self) -> None:
        self.pattern = re.compile(
            "|".join(map(re.escape, self.bad_words)), flags=re.IGNORECASE
        )

    def filter(self, chunk: DataFrame , chunk_number : int):
        logging.info(
            "%s  Consumer: start filtering chunk number %s",
            elapsed(self.args.starting_time),
            chunk_number + 1,
        )
        start = time()

        health_filter = chunk.apply(
            lambda row: not any(
                map(lambda field: self.pattern.search(str(field)), row)
            ),
            axis=1,
        )

        end = time()
        logging.info(
            "%s  Consumer: finish filtering chunk number %s",
            elapsed(self.args.starting_time),
            chunk_number + 1,
        )

        dif = end - start
        healthy_rows_number = sum(health_filter)
        unhealthy_rows_number = len(health_filter) - healthy_rows_number
        return healthy_rows_number, unhealthy_rows_number , dif

    def __repr__(self) -> str:
        return "Regex"
