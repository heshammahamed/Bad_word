
from time import time
from Enums import FilterMode, ProcessingMode
from concurrent_model import *
from producer import Producer
from consumer import Consumer
from queue import Queue
import pandas as pd
import multiprocessing
import logging
from arguments import Args, parse_args
from filter import *
from statistics_writer import StatisticsWriter
from chunks_processing_info import ChunkFilteringInfo

# this is the vonfigration 'creation of the logging file'

logging.basicConfig(
    filename="logfile.log",
    format=" %(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    force=True,
)


def main(args: Args):
    # first initilze producer consumer are objects
    producer, consumer = setup_producer_consumer(args)

    # make inistance from the StatisticsWriter class whcih we will use to write the csv file content
    writer = StatisticsWriter(args)

    logging.info("Main: run in pool of processes")
    concurrent_model : ConcurrentModel = ProcessesPoolModel()
    try:
        # this methode return list
        chunks_info = concurrent_model.start(producer, consumer) 
        #writer.start(chunks_info)
    except Exception as e:
        logging.exception("Exception occurred while running program: {}".format(str(e)))

# we will delet this cause we will have one process_mode 



# arguments -> tuple[producer , consumer]
#tuple is like a list but we can not mutate 'change its content' it after initilize it 

def setup_producer_consumer(args: Args) -> tuple[Producer, Consumer]:

    # here we make a list which will contain all the bad words
    # we read the badwords file which is passed by arguments 
    # using pandas
    bad_words: list[str] = (
        pd.read_csv(args.bad_words_file, header=None).iloc[:, 0].tolist()
    )


    # here we choose which filter mode we will use 
    # and then create variable which will contain the instance of choosen filter mode 
    if args.filter_mode == FilterMode.AhoCorasick:
        text_filter: TextFilter = AhoCorasickFilter(bad_words)
    else:
        text_filter: TextFilter = RegexFilter(bad_words)

    # here we will delte this part of the code 
    # and we will make the code automaticlly choose the the processmode depent on the 
    # system he run on.

    # i dont know actually for what these queues are used for
    chunks_queue = multiprocessing.Queue(maxsize=1000)
    # allow multiple process to share python objects like 'list,dic,queues'
    manager = multiprocessing.Manager()
    reading_info_queue = manager.Queue()
    filtering_info_queue = manager.Queue()

    # see the filter.py to see more details
    #not calculate in the filtering time
    # for aho it create the trie datastructure
    text_filter.prepare()

    # here initilize inistance of the producer class and consumer class
    producer = Producer(chunks_queue, reading_info_queue, args)
    consumer = Consumer(chunks_queue, filtering_info_queue, text_filter, args)

    return producer, consumer


if __name__ == "__main__":

    args = parse_args()
    print('from main',args)
    # region for normal usage
    main(args)
    # endregion

    # region for benchmark usage
    # while args.chunk_size <= 100_000:
    #      main(args)
    #      args.chunk_size += 10_000
    #      args.starting_time = time()
    # endregion
