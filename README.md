# hydrater-ids-to-tweets
Short script that hydrates tweet IDs - i.e. returns a full tweet.json object - from a list of tweet IDs gathered from Twiqs (http://www.twiqs.nl): a Dutch Twitter archive. The script takes any number of files (specified in 'files', under 'main') and saves the tweet jsons in a seperate .json based on your initial filename. 

The script currently deals with Twitter API time-outs very naively -- it just waits and resumes when the ratelimit is removed. Progress is stored in pickled files. Twitter OAuth tokens are imported from a seperate file ('config.py'). 

TO DO:
- Remove pickled files when source files are fully hydrated.
- Build better rate limit handler.
- Build better progress storage/monitor.
- Handle user input -- allow user to specifiy file on command line.
