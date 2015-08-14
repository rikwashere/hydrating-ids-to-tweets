# hydrater-ids-to-tweets
Short script that hydrates tweet IDs - i.e. returns a full tweet.json object - from a list of tweet IDs gathered from Twiqs
(http://www.twiqs.nl): a Dutch Twitter archive. The script takes any number of files (specified in 'files') and 
outputs the tweet jsons in a seperate file based on your initial filename. 

Script deals with Twitter time-outs very naive -- it just waits and resumes when the ratelimit is removed. Progress is 
stored in pickled files. Twitter OAuth tokens are imported from a seperate file. 
