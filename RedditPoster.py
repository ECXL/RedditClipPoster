import praw

import time

reddit = praw.Reddit(
    client_id="c_id_here",
    client_secret="c_secret_here",
    username="uname",
    password="pword",
    user_agent="user_agent_here",
)

#Valildate correct authorization
#should print reddit username:
print(reddit.user.me())

#check if in read only mode:
#print(reddit.read_only)
#should return false

#list of subreddits to post to
subreddits = ["ExampleSub", "AnotherSub", "ThirdSub"]

#title of post
title = "Title goes here"

#video for posting
videoPath = "path/to/video.mp4"

#thumbnail for video as otherwise it defaults to the PRAW logo
thumbnail = "path/to/thumbnail.png"

#comment to automatically reply to post
comment = "Let me know if you enjoyed!"

#post to subreddits
for sub in subreddits:
    print("Attempting to post to ", sub)
    try:
        my_post = reddit.subreddit(sub).submit_video(title, videoPath, thumbnail_path=thumbnail)
        my_post.reply(comment)
        print("Successfully posted to", sub)
    except praw.exceptions.RedditAPIException as exception:
        for subexception in exception.items:
            #print(subexception)
            if subexception.error_type == "RATELIMIT":
                #you may have to wait between posts
                print("Waiting then reposting...")
                wait = str(subexception.replace("RATELIMIT: 'you are doing that too much. try again in ", ""))
                if 'minute' in wait:
                    wait = wait[:2]
                    wait = int[wait] + 1
                    #waits the rate limit plus one more minute for safe measures
                else:
                    wait = 1
                    #if the wait is in seconds wait only a full minute

                #wait for that many minutes
                time.sleep(wait*60)
                my_post = reddit.subreddit(sub).submit_video(title, videoPath, thumbnail_path=thumbnail)
                my_post.reply(comment)
                print("Successfully posted to", sub)
            if subexception.error_type == "SUBMIT_VALIDATION_FLAIR_REQUIRED":
                #you sometimes have to add a flair to a post beforehand
                print("Adding Flair then reposting...")
                #unfotunately each subreddit has its own flair template id so you will have to input them individually for each sub
                def flair(subName):
                    switch={
                        'ExampleSub':'flair_template_id',
                        'AnotherSub':'another_flair_template_id',
                        'ThirdSub':'third_flair_template_id'
                    }
                    return switch.get(subName)
                
                #if you need to fetch the flair ids uncomment the next 2 lines and comment out the rest of the if innards:
                #flairs = list(reddit.subreddit(sub).flair.link_templates.user_selectable())
                #print(flairs)

                my_post = reddit.subreddit(sub).submit_video(title, videoPath, thumbnail_path=thumbnail, flair_id=flair(sub))
                my_post.reply(comment)
                print("Successfully posted to", sub)