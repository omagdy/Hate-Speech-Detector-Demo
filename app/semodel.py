
from app.keras_import import *

seed = 42
np.random.seed(seed)
max_sentence_length = 150
pad = '<pad>'
unk = '<unk>'


andPattern = re.compile('&amp;')
gtPattern = re.compile('&gt;')
ltPattern = re.compile('&lt;')
stemmer = PorterStemmer()

with open('app/semeval/tokenizer.pickle', 'rb') as handle:
   tkz = pickle.load(handle)

def tokenize(text):
    text = re.sub(andPattern, "and", text)
    text = re.sub(gtPattern, ">", text)
    text = re.sub(ltPattern, "<", text)
    output = []
    tokens = tkz.tokenize(text)
    for token in tokens:
        if len(token) > 1:
            if token[0] == '#':
                output.append('#')
                token = token[1:]
            subtoken = token.split('-')
            if len(subtoken) > 1:
                for t in subtoken:
                    output.append(t)
            else:
                output.append(token)
    return output

with open('app/semeval/i2t.pkl', 'rb') as handle:
  i2t = pickle.load(handle)

with open('app/semeval/t2i.pkl', 'rb') as handle:
  t2i = pickle.load(handle)

model = keras.models.load_model('app/semeval/semevalcnn.model')
graph = tf.get_default_graph()

def analyze_eng_text(text):
    te = np.array([text], dtype=object)
    Xt = [[t2i[t] if t in t2i else t2i[unk] for t in tokenize(tweet)]
                    for tweet in te]
    Xt = sequence.pad_sequences(Xt, maxlen=max_sentence_length)
    global graph
    with graph.as_default():
        predictions_final = model.predict(Xt)
    if predictions_final[0][0] > 0.5:
        f = open("Hateful_Tweets.txt", "a")
        f.write(text+"\n")
        f.close()
        return "Tweet is offensive", True
    else:
        return "Tweet is not offensive", False


