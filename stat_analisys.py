import cProfile
import pstats
from main import main


def stat():

    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='stats.prof')


if __name__ == '__main__':
    stat()
