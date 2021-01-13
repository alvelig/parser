import re
import json
from json import JSONEncoder
import string
from collections import Counter

def flatsplit(arr, separator):
    newarr = []
    for item in arr:
        splitted = item.split(separator)
        for s in splitted:
            newarr.append(s.strip())
    return newarr

def feature_comparator(a, b):
    equal = a.lower() == b.lower()
    stripped = a.replace(" ", "") == b.replace(" ", "")
    # starts = a.startswith(b) or b.startswith(a)
    # ends = a.endswith(b) or b.endswith(a)
    return equal or stripped # or starts or ends

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__  

class Chunk:
    def __init__(self, text, id, by, type = 'text'):
        self.text = text
        self.id = id
        self.by = by
        self.type = type

    def __str__(self):
        return "%s, %s, %s, %s" % (self.text, self.id, self.by, self.type)
    
    def __repr__(self):
        return "%s, %s, %s, %s" % (self.text, self.id, self.by, self.type)

class Feature:
    def __init__(self, chunk):
        self.name = chunk.text
        # self.names = set()
        self.chunks = []
        self.add(chunk)

    def add(self, chunk):
        # self.names.add(chunk.text)
        self.chunks.append(chunk)

    # TODO: make chunks a hash (optimize)
    def compare(self, chunk):
        matched = False
        for c in self.chunks:
            if feature_comparator(chunk.text, c.text):
                self.add(chunk)
                matched = True
                break
            # remove all puntuation .,-/ and compare again
            if feature_comparator(chunk.text.translate(str.maketrans('', '', string.punctuation)), c.text.translate(str.maketrans('', '', string.punctuation))):
                self.chunks.append(chunk)
                matched = True
                break
        self.recalc_name()
        return matched

    def recalc_name(self):
        names = []
        for c in self.chunks:
            names.append(c.text)
        name, _ = Counter(names).most_common(1)[0]
        self.name = name
    
    def instance(self):
        return "(%s, %s)" % (self.name, self.count)

    def __str__(self):
        return self.instance()
    
    def __repr__(self):
        return self.instance()


def parse(df, cache, id):
    features = []
    chunks = []
    for index, row in df.iterrows():
        # if index > 10:
        #     break
        # TODO: extract mentions and try to parse them as text
        text = row['Text']
        results = re.findall("@([a-zA-Z0-9]{1,15})", text)
        
        # Extract mentions
        for r in results:
            chunks.append(Chunk(text = "@%s" % r, id = row['Tweet Id'], by = row['Username'], type = 'mention'))
            text = text.replace("@%s" % r, '')

        results = re.findall('https?://[^\s]+', text)        
        
        # extract links
        # TODO: extract properly images and videos
        for r in results:
            chunks.append(Chunk(text = "%s" % r, id = row['Tweet Id'], by = row['Username'], type = 'mention'))
            text = text.replace("%s" % r, '')

        # TODO: check if it's a common speech phrase or a set of independent nouns (just without any separators like this: "Slack Vs code Sublime" or this "Slack.Vs code.Sublime.")
        # spacy.io has a decent set of tools for that
        # NO TIME FOR MACHINE LEARNING, JUST SEPARATE IT
        text = text.lower()
        textchunks = text.split('\n')
        textchunks = flatsplit(textchunks, '. ')
        textchunks = flatsplit(textchunks, ';')
        textchunks = flatsplit(textchunks, '!')
        textchunks = flatsplit(textchunks, '?')
        textchunks = flatsplit(textchunks, ': ')
        textchunks = flatsplit(textchunks, ' and ')
        textchunks = flatsplit(textchunks, ' with ')
        textchunks = flatsplit(textchunks, ',')
        # textchunks = flatsplit(textchunks, '+')
        # textchunks = flatsplit(textchunks, '/')
        # textchunks = flatsplit(textchunks, '(')
        # textchunks = flatsplit(textchunks, ')')

        for chunk in textchunks:
            if chunk:
                chunks.append(Chunk(text = chunk, id = row['Tweet Id'], by = row['Username']))
        
    total_chunks = len(chunks)
    print("%d chunks formed" % total_chunks)

    ii = 0
    for chunk in chunks:
        ii += 1
        if ii % 1000 == 0:
            cache[id] = "Tweet thread %s: %d of %d chunks processed." % (id, ii, total_chunks)
            print(cache[id])

        matched = False
        for feature in features:
            if feature.compare(chunk):
                matched = True
        if not matched:
            features.append(Feature(chunk))
    
    # TODO: here we could compare popular features if they are contained in other features
    print("%d features formed" % len(features))

    return features