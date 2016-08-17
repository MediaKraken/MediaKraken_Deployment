# Carlos A. Ibarra
# http://stackoverflow.com/questions/667508/whats-a-good-rate-limiting-algorithm/667706#667706

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import time


# calls per second
API_Limit = {
    'anidb': (1, 4), # A Client MUST NOT send more than one packet every four seconds over an extended amount of time. (4-16-2016)
    'chart_lyrics': (9999, 1), # no mention of limits 7/29/2016 just says don't abuse
    'comicvine': (1, 1), # (4-16-2016)
    'giantbomb': (1, 1), # (4-16-2016)
    'imdb': (9999, 1), # no mention of limits 7/29/2016
    'imvdb': (1000, 60), # 1000 per minute (6/30/2016)
    'musicbrainz': (9999, 1),
    'netflixroulette': (9999, 1), # (6-27-2016)
    'omdb': (20, 1), # 7/29/2016 says 20 concurrent connections
    'pitchfork': (9999, 1), # no mention of limits 7/29/2016
    'rotten_tomatoes': (9999, 1),
    'televisiontunes': (1, 1), # since I'm scraping
    'theaudiodb': (9999, 1), # no mention of limits 7/29/2016
    'thegamesdb': (9999, 1), # no mention of limits 7/29/2016
    'thelogodb': (9999, 1), # no mention of limits 7/29/2016
    'themoviedb': (30, 10), # We currently rate limit requests to 30 requests every 10 seconds. (4-16-2016)
    'thesportsdb': (9999, 1), # no mention of limits 7/29/2016
    'thetvdb': (9999, 1), # no mention of limits besides play nice (4-16-2016)
    'tv_intros': (1, 1), # since I'm scraping
    'tvmaze': (9999, 1), # no mention of limits (4-16-2016)
    'tvshowtime': (10, 60), # 10 requests per minute (4-16-2016)
    'Z': (None, None), # catch all for limiter api program
}


# want a maximum of 5 messages per 8 seconds, 
# use @ratelimited(0.625) before your sendToQueue function.
def ratelimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args, **kargs):
            leftToWait = minInterval - time.time() - lastTimeCalled[0]
            if leftToWait > 0:
                time.sleep(leftToWait)
            lastTimeCalled[0] = time.time()
            return func(*args, **kargs)
        return rateLimitedFunction
    return decorate
