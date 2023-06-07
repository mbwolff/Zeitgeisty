# Zeitgeisty

This is a bot that generates daily aphorisms from news headlines and Twitter commentary. It is based on an idea from the Oulipo for inventing aphorisms by using a computer to insert nouns and verbs into formulas. The bot finds words in a Word2Vec model constructed from the headlines and tweets. In this way it offers a *zeitgeist* that emerges from the Internet.

[Check it out!](https://zeitgeisty.hartwick.edu/)

## Setup

1. Install `Python 3.8` (as a virtual or Paas environment).
2. Install the Python modules in `requirements.txt`.
3. Create a `docs` subfolder. This is where content from headlines and Twitter will be archived.
4. Create an `aphorisms` subfolder. This is where lists of aphorisms  will be archived.
5. Create a `hate_speech` subfolder. This is where aphorisms [classified as hateful] (https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target) are archived. These aphorisms are not shared publicly.
5. Rename `twitter_credsTEMPLATE.py` as `twitter_creds.py` and supply your personal Twitter credentials.
6. Run `getDocs.py` to download content from news headlines and Twitter. I run this script twice a day (every twelve hours).
7. Run `pruneDocs.py` to eventually delete news and Twitter content that is over 90 days old.
8. Run `buildModel.py` to build the Word2Vec model from the archive in `docs/`.
9. Run `generateAphorisms.py` for a list of around 200 aphorisms. The code is parameterized to generate a total of at least 50,000 words in 30 days for [NaNoGenMo 2022](https://github.com/NaNoGenMo/2022).
10. Run `sendTweets.py` to share the aphorisms on Twitter, one every 30 minutes.
11. Here is a sample crontab file to automate things:
```
# IMPORTANT NOTE!
# Please make sure there is a blank line after the last cronjob entry.
0 2,14 * * * /your/path/to/Zeitgeisty/getDocs.py
30 2 * * * /your/path/to/Zeitgeisty/pruneDocs.py
0 3 * * * /your/path/to/Zeitgeisty/buildModel.py
0 4 * * * /your/path/to/Zeitgeisty/generateAphorisms.py
30 4 * * * /your/path/to/Zeitgeisty/sendTweets.py
```
