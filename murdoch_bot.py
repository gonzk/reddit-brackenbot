import praw
import random
import time
import os
import brackenbot_config

config = brackenbot_config


def login():
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent=config.user_agent,
                         username=config.username,
                         password=config.password)
    return reddit


def run(reddit, replied_to):
    subreddit = reddit.subreddit("murdochmysteries")

    quotes = ["Bloody hell Murdoch",
              "Oi Bugalugs",
              "Me Ol' Mucker",
              "Follow the money"]

    characters = ["murdoch",
                  "george",
                  "gillies",
                  "julia",
                  "meyers"]

    for submission in subreddit.new(limit=10):

        for comment in submission.comments:
            if hasattr(comment, "body"):
                comment_lower = comment.body.lower()
                index = random.randint(0, len(characters) - 1)
                char = characters[index]

                if char in comment_lower and comment.id not in replied_to and comment.author != reddit.user.me():
                    print("-------")
                    print(char)
                    print(comment.body)
                    random_index = random.randint(0, len(quotes) - 1)
                    replied_to.append(comment.id)
                    comment_reply = "*beep. boop. 🤖 I'm the Brackenbot.* \n\n"
                    comment_reply += ">" + quotes[random_index]
                    comment_reply += "\n\n[Info](https://tinyurl.com/y68u5ggv)"

                    comment.reply(comment_reply)
                    print("Replied to comment " + comment.id)

                    with open("replied_to.txt", "a") as f:
                        f.write(comment.id + "\n")

                    time.sleep(900)
                    print("Sleep for 900 s")


def get_saved_comments():
    if not os.path.isfile("replied_to.txt"):
        replied_to = []
    else:
        with open("replied_to.txt", "r") as f:
            replied_to = f.read()
            replied_to = replied_to.split("\n")
    return replied_to


reddit = login()
replied_to = get_saved_comments()

while True:
    run(reddit, replied_to)
