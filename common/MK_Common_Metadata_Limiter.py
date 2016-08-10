# Carlos A. Ibarra
# http://stackoverflow.com/questions/667508/whats-a-good-rate-limiting-algorithm/667706#667706

from __future__ import division
import time
import logging


# calls per second
API_Limit = {
'AniDB': (1, 4), # A Client MUST NOT send more than one packet every four seconds over an extended amount of time. (4-16-2016)
'Chart_Lyrics': (9999, 1), # no mention of limits 7/29/2016 just says don't abuse
'ComicVine': (1, 1), # (4-16-2016)
'GiantBomb': (1, 1), # (4-16-2016)
'IMDB': (9999, 1), # no mention of limits 7/29/2016
'IMVDb': (1000, 60), # 1000 per minute (6/30/2016)
'MusicBrainz': (9999, 1),
'NetflixRoulette': (9999, 1), # (6-27-2016)
'OMDb': (20, 1), # 7/29/2016 says 20 concurrent connections
'Pitchfork': (9999, 1), # no mention of limits 7/29/2016
'Rotten_Tomatoes': (9999, 1),
'televisiontunes': (1, 1), # since I'm scraping
'TheAudioDB': (9999, 1), # no mention of limits 7/29/2016
'TheGamesDB': (9999, 1), # no mention of limits 7/29/2016
'TheLogoDB': (9999, 1), # no mention of limits 7/29/2016
'theMovieDB': (30, 10), # We currently rate limit requests to 30 requests every 10 seconds. (4-16-2016)
'TheSportsDB': (9999, 1), # no mention of limits 7/29/2016
'theTVDB': (9999, 1), # no mention of limits besides play nice (4-16-2016)
'tv_intros': (1, 1), # since I'm scraping
'TVMaze': (9999, 1), # no mention of limits (4-16-2016)
'tvshowtime': (10, 60), # 10 requests per minute (4-16-2016)
'Z': (None, None), # catch all for limiter api program
}


# want a maximum of 5 messages per 8 seconds, 
# use @RateLimited(0.625) before your sendToQueue function.
def RateLimited(maxPerSecond):
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


'''
@RateLimited(2)  # 2 per second at most
def PrintNumber(num):
    print num

if __name__ == "__main__":
    print "This should print 1,2,3... at about 2 per second."
    for i in range(1,100):
        PrintNumber(i)
'''
