import praw
import time
import config

TEMPLATE = 'u/{} score'.format(config.USERNAME)
done = []
reddit = ''

def main():
    reddit = praw.Reddit(user_agent=config.USERAGENT, client_id=config.CLIENTID, client_secret=config.CLIENTSECRET, username=config.USERNAME, password=config.PASSWORD)
    
    print('\nLogged in!\n')
    subredditname = config.SUBREDDIT

    try:
        print('Catching stream of comments in subreddit {}\n'.format(subredditname))
        check_comments(reddit.subreddit(subredditname))
    except KeyboardInterrupt:
        exit()
    except ConnectionAbortedError:
        print('Session timed up, starting new session...')
        time.sleep(2)
        main()

def check_comments(subreddit):
    comments = subreddit.stream.comments()
    for comment in comments:
        body = comment.body.lower()
        id = comment.id
        if id not in done and TEMPLATE in body:
            print('Found match {}\n'.format(id))
            comment_score(comment)
            
def comment_score(comment):
    id = comment.id
    splitbody = comment.body.strip().split(' ')
    if len(splitbody) == 3:
        user = reddit.redditor(splitbody[2])
        who = splitbody[2] + "'s"
    else:
        user = comment.author
        who = 'Your'
            
    try:
        link_score = get_score(user.link_karma)
        comment_score = get_score(user.comment_karma)
        total_score = get_score(user.link_karma + user.comment_karma, 3)
                
        reply = '{0} link karma score: {1}\n\n{0} comment karma score: {2}\n\n{0} elite karma score: {3}'.format(who, link_score, comment_score, total_score)
            
    except praw.exceptions.APIException:
        reply = "User {} was not found. Please don't blame me :(".format(who)
            
    comment.reply(reply + '\n\n' + config.BOTMESSAGE)
    done.append(id)
        
    print('Replied to comment {} successfully\n'.format(id))
    
def get_score(karma, multiplier = 1):
    m = multiplier
    
    if karma < 200 * m:
        rank = 'Fresh Meat'
    elif karma < 500 * m:
        rank = 'Noob'
    elif karma < 1000 * m:
        rank = 'Lazy'
    elif karma < 1750 * m:
        rank = 'Boring'
    elif karma < 3000 * m:
        rank = 'Meh'
    elif karma < 4500 * m:
        rank = 'Average Joe'
    elif karma < 6000 * m:
        rank = 'Wew lad'
    elif karma < 8500 * m:
        rank = 'Good shit'
    elif karma < 9000 * m:
        rank = 'Very good shit'
    elif karma < 15000 * m:
        rank = 'Over 9000!!!'
    elif karma < 20000 * m:
        rank = 'Impressive shit'
    elif karma < 50000 * m:
        rank = 'Awesome!'
    elif karma < 100000 * m:
        rank = 'Banned from /r/outside'
    elif karma < 200000 * m:
        rank = 'Shitposter'
    elif karma < 450000 * m:
        rank = 'Karmahole'
    elif karma < 700000 * m:
        rank = 'Winner'
    elif karma < 1000000 * m:
        rank = 'Karmamine'
    elif karma > 1000000 * m:
        rank = 'Gallowboob'
        
    return rank

if __name__ == '__main__':
    main()