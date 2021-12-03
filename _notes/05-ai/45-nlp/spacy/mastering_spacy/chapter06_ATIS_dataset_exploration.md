```{.python .input  n=43}
import spacy 
import pandas as pd 
import utils

from collections import Counter 
from IPython.display import display
from spacy.matcher import Matcher

# auto load the changes of referenced codes
%load_ext autoreload
%autoreload 2

# ebablbe auto-completion
%config Completer.use_jedi = False
```

```{.json .output n=43}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "The autoreload extension is already loaded. To reload it, use:\n  %reload_ext autoreload\n"
 }
]
```

## Data

```{.python .input  n=7}
df_atis = pd.read_csv("./Chapter06/data/atis_intents.csv", header=None)
df_atis.columns = ['intent', 'text']
```

```{.python .input  n=35}
print('-'*50)
print(len(df_atis))

print('-'*50)
display(df_atis.head(5))

print('-'*50)
display(df_atis.describe().T)

print('-'*50)
df_atis.intent.unique()

print('-'*50)
df_atis.info()
```

```{.json .output n=35}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "--------------------------------------------------\n4978\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>intent</th>\n      <th>text</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>atis_flight</td>\n      <td>i want to fly from boston at 838 am and arriv...</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>atis_flight</td>\n      <td>what flights are available from pittsburgh to...</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>atis_flight_time</td>\n      <td>what is the arrival time in san francisco for...</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>atis_airfare</td>\n      <td>cheapest airfare from tacoma to orlando</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>atis_airfare</td>\n      <td>round trip fares from pittsburgh to philadelp...</td>\n    </tr>\n  </tbody>\n</table>\n</div>",
   "text/plain": "             intent                                               text\n0       atis_flight   i want to fly from boston at 838 am and arriv...\n1       atis_flight   what flights are available from pittsburgh to...\n2  atis_flight_time   what is the arrival time in san francisco for...\n3      atis_airfare            cheapest airfare from tacoma to orlando\n4      atis_airfare   round trip fares from pittsburgh to philadelp..."
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>count</th>\n      <th>unique</th>\n      <th>top</th>\n      <th>freq</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>intent</th>\n      <td>4978</td>\n      <td>22</td>\n      <td>atis_flight</td>\n      <td>3666</td>\n    </tr>\n    <tr>\n      <th>text</th>\n      <td>4978</td>\n      <td>4634</td>\n      <td>what is fare code h</td>\n      <td>8</td>\n    </tr>\n  </tbody>\n</table>\n</div>",
   "text/plain": "       count unique                   top  freq\nintent  4978     22           atis_flight  3666\ntext    4978   4634   what is fare code h     8"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "--------------------------------------------------\n--------------------------------------------------\n<class 'pandas.core.frame.DataFrame'>\nRangeIndex: 4978 entries, 0 to 4977\nData columns (total 2 columns):\n #   Column  Non-Null Count  Dtype \n---  ------  --------------  ----- \n 0   intent  4978 non-null   object\n 1   text    4978 non-null   object\ndtypes: object(2)\nmemory usage: 77.9+ KB\n"
 }
]
```

查看数据内容。可以看到：

- 第一个用户说想定某个时间，从某地到某地ide航班？
- 第二个用户同第一个用户
- 第三个用户想问航班的到达时间。
- 第三根用户想问从某地到某地最便宜的机票。
- 第五个用户问从某地到某地低于1000美元的航班。

```{.python .input  n=13}
print(*list(df_atis.head().text), sep='\n')
```

```{.json .output n=13}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": " i want to fly from boston at 838 am and arrive in denver at 1110 in the morning\n what flights are available from pittsburgh to baltimore on thursday morning\n what is the arrival time in san francisco for the 755 am flight leaving washington\n cheapest airfare from tacoma to orlando\n round trip fares from pittsburgh to philadelphia under 1000 dollars\n"
 }
]
```

查看意图的分布。

```{.python .input  n=36}
df_grouped = df_atis.groupby(['intent']).size()
df_grouped
```

```{.json .output n=36}
[
 {
  "data": {
   "text/plain": "intent\natis_abbreviation                            147\natis_aircraft                                 81\natis_aircraft#atis_flight#atis_flight_no       1\natis_airfare                                 423\natis_airfare#atis_flight_time                  1\natis_airline                                 157\natis_airline#atis_flight_no                    2\natis_airport                                  20\natis_capacity                                 16\natis_cheapest                                  1\natis_city                                     19\natis_distance                                 20\natis_flight                                 3666\natis_flight#atis_airfare                      21\natis_flight_no                                12\natis_flight_time                              54\natis_ground_fare                              18\natis_ground_service                          255\natis_ground_service#atis_ground_fare           1\natis_meal                                      6\natis_quantity                                 51\natis_restriction                               6\ndtype: int64"
  },
  "execution_count": 36,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

在atis_abbreviation这种意图中，用户询问关于各种缩写的含义。

```{.python .input  n=24}
df_filter = df_atis.loc[(df_atis.intent=='atis_abbreviation')]
print(*list(df_filter.sample(10).text), sep='\n')
```

```{.json .output n=24}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": " what is the ap57 restriction\n what is ua\n what does nw stand for\n what are fare codes qw and qx\n what is sa\n what is the yn code\n what is fare code f\n what does ap57 mean\n what is fare code f\n what is fare code h\n"
 }
]
```

## Extracting named entities

需要注意的是，在书中使用如下代码获取文本（相当于df_atis的text列）

~~~shell
awk -F ',' '{print $2}' data/atis_intents.csv  > data/atis_utterances.txt
~~~

```{.python .input  n=27}
nlp  = spacy.load("en_core_web_md") 

corpus = open("Chapter06/data/atis_utterances.txt", "r").read().split("\n") 

all_ent_labels = [] 
for sentence in corpus: 
    doc = nlp(sentence.strip()) 
    ents = doc.ents 
    all_ent_labels += [ent.label_ for ent in ents] 

c = Counter(all_ent_labels) 
print(c) 
```

```{.json .output n=27}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "Counter({'GPE': 9219, 'DATE': 1454, 'TIME': 925, 'ORG': 425, 'CARDINAL': 275, 'ORDINAL': 201, 'FAC': 63, 'NORP': 60, 'MONEY': 52, 'PERSON': 17, 'PRODUCT': 14, 'LOC': 6, 'EVENT': 3})\n"
 }
]
```

上面的代码运行起来有些慢。采用如下代码快好几倍。

```{.python .input  n=39}
texts = list(df_atis.text)
texts = [text.strip() for text in texts]
docs = nlp.pipe(texts)

all_ent_labels = [] 
for doc in docs: 
    ents = doc.ents 
    all_ent_labels += [ent.label_ for ent in ents] 

c = Counter(all_ent_labels) 
print(c) 
```

```{.json .output n=39}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "Counter({'GPE': 9219, 'DATE': 1454, 'TIME': 925, 'ORG': 425, 'CARDINAL': 275, 'ORDINAL': 201, 'FAC': 63, 'NORP': 60, 'MONEY': 52, 'PERSON': 17, 'PRODUCT': 14, 'LOC': 6, 'EVENT': 3})\n"
 }
]
```

### Extracting named entities with Matcher
抽取的内容如下

```{.python .input  n=63}
def show_matches(nlp, doc, matches):
    for match_id, start, end in matches:
        pattern_name = nlp.vocab.strings[match_id]
        m_span = doc[start:end]  
        print(pattern_name, start, end, m_span.text)  
        
# 起始地址
matcher = Matcher(nlp.vocab)
pattern = [{"POS": "ADP"}, {"ENT_TYPE": "GPE"}]
matcher.add("prepositionLocation", [pattern])

# 航班信息
pattern = [{"ENT_TYPE": "ORG", "OP": "+"}]
matcher.add("AirlineName", [pattern])

# 日期和时间
pattern = [{"ENT_TYPE":  {"IN": ["DATE", "TIME"]}}]
matcher.add("Datetime", [pattern])

# 缩写abbreviation
pattern1 = [{"TEXT": {"REGEX": "\w{1,2}\d{1,2}"}}]
pattern2 = [{"SHAPE": { "IN": ["x", "xx"]}}, {"SHAPE": {"IN": ["d", "dd"]}}]
pattern3 = [{"TEXT": {"IN": ["class", "code", "abbrev", "abbreviation"]}}, {"SHAPE": { "IN": ["x", "xx"]}}]
pattern4 = [{"POS": "NOUN", "SHAPE": { "IN": ["x", "xx"]}}]
matcher.add("abbrevEntities", [pattern1, pattern2, pattern3, pattern4])

texts = ["show me flights from denver to boston on tuesday",
         "i'm looking for a flight that goes from ontario to westchester and stops in chicago",
         "what flights arrive in chicago on sunday on continental",
         "yes i'd like a flight from long beach to st. louis by way of dallas",
         "what are the evening flights flying out of dalas",
         "what is the earliest united airlines flight flying from denver",
         'what does restriction ap 57 mean',
         'what does the abbreviation co mean',
         'what does fare code qo mean',
         'what is the abbreviation d10',
         'what does code y mean',
         'what does the fare code f and fn mean',
         'what is booking class c']
docs = nlp.pipe(texts)

for doc in docs:
    print('-'*50)
    spacy.displacy.render(doc, style='ent')
#     print([(ent.text, ent.label_) for ent in doc.ents])
    matches = matcher(doc)
    show_matches(nlp, doc, matches)
```

```{.json .output n=63}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">show me flights from \n<mark class=\"entity\" style=\"background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    denver\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">GPE</span>\n</mark>\n to \n<mark class=\"entity\" style=\"background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    boston\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">GPE</span>\n</mark>\n on \n<mark class=\"entity\" style=\"background: #bfe1d9; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    tuesday\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">DATE</span>\n</mark>\n</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "prepositionLocation 3 5 from denver\nprepositionLocation 5 7 to boston\nDatetime 8 9 tuesday\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">i'm looking for a flight that goes from \n<mark class=\"entity\" style=\"background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    ontario\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">GPE</span>\n</mark>\n to westchester and stops in \n<mark class=\"entity\" style=\"background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    chicago\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">GPE</span>\n</mark>\n</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "prepositionLocation 8 10 from ontario\nprepositionLocation 14 16 in chicago\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what flights arrive in \n<mark class=\"entity\" style=\"background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    chicago\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">GPE</span>\n</mark>\n on \n<mark class=\"entity\" style=\"background: #bfe1d9; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    sunday\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">DATE</span>\n</mark>\n on continental</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "prepositionLocation 3 5 in chicago\nDatetime 6 7 sunday\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">yes i'd like a flight from long beach to \n<mark class=\"entity\" style=\"background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    st. louis\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">GPE</span>\n</mark>\n by way of \n<mark class=\"entity\" style=\"background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    dallas\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">GPE</span>\n</mark>\n</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "prepositionLocation 9 11 to st\nprepositionLocation 15 17 of dallas\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what are the evening flights flying out of dalas</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what is the earliest \n<mark class=\"entity\" style=\"background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    united airlines\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">ORG</span>\n</mark>\n flight flying from \n<mark class=\"entity\" style=\"background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    denver\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">GPE</span>\n</mark>\n</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "AirlineName 4 5 united\nAirlineName 4 6 united airlines\nAirlineName 5 6 airlines\nprepositionLocation 8 10 from denver\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what does restriction ap \n<mark class=\"entity\" style=\"background: #e4e7d2; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;\">\n    57\n    <span style=\"font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem\">CARDINAL</span>\n</mark>\n mean</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "abbrevEntities 3 5 ap 57\nabbrevEntities 4 5 57\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what does the abbreviation co mean</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "abbrevEntities 3 5 abbreviation co\nabbrevEntities 4 5 co\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what does fare code qo mean</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "abbrevEntities 3 5 code qo\nabbrevEntities 4 5 qo\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what is the abbreviation d10</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "abbrevEntities 4 5 d10\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what does code y mean</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "abbrevEntities 2 4 code y\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what does the fare code f and fn mean</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "abbrevEntities 4 6 code f\nabbrevEntities 7 8 fn\n--------------------------------------------------\n"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><div class=\"entities\" style=\"line-height: 2.5; direction: ltr\">what is booking class c</div></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "abbrevEntities 3 5 class c\nabbrevEntities 4 5 c\n"
 }
]
```

### Using dependency trees for extracting entities

~~~
I want to fly to Munich tomorrow.
~~~

对于上面的语句，上节的抽取方法可以抽取到destination city，但是如果是下面的语句，就无能为了。

~~~
I'm going to a conference in Munich. I need an air ticket.
My sister's wedding will be held in Munich. I'd like to book a flight
I want to book a flight to my conference without stopping at Berlin.
~~~

本节将尝试使用dependency trees来解析他们之间的关系。

```{.python .input  n=67}
texts = ["I'm going to a conference in Munich. I need an air ticket.",
         "My sister's wedding will be held in Munich. I'd like to book a flight",
         "I want to book a flight to my conference without stopping at Berlin."]

def reach_parent(source_token, dest_token):
    source_token = source_token.head
    while source_token != dest_token:
        if source_token.head == source_token:
            return None
        source_token = source_token.head
    return source_token

doc = nlp("I'm going to a conference in Munich.")
source_token = reach_parent(doc[-2], doc[3])
print(doc[-2], doc[3], source_token)
```

```{.json .output n=67}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "Munich to to\n"
 }
]
```

## Using dependency relations for intent recognition
### Linguistic primer

ATIS数据中包含了多个意图（intent），比如：

- book a flight
- purchase a meal on their already booked flight
- cancel their flight

可以发现这些意图可以表示为：动词（verb） + 对象（object）。在本节中将使用这个规则，将抽取：
- 及物动词/非及物动词（transitive/intransitive verbs）
- 直接宾语/间接宾语（direct/indirect objects）

下面是首先来理解及物动词/非及物动词。

- 及物动词
    ~~~
    I bought flowers.
    He loved his cat.
    He borrowed my book.
    ~~~

- 非及物动词
    ~~~
    Yesterday I slept for 8 hours.
    The cat ran towards me.
    When I went out, the sun was shining.
    Her cat died 3 days ago.
    ~~~

再来看直接宾语/间接宾语。

- 直接宾语
    ~~~
    I bought flowers.  I bought what? - flowers
    He loved his cat.  He loved who?  - his cat
    He borrowed my book. He borrowed what? - my book
    ~~~

- 间接宾语
    ~~~
    He gave me his book.  He gave his book to whom?  - me
    He gave his book to me. He gave his book to whom? -me
    ~~~

下面代码将展示直接宾语和间接宾语。更多相关知识，可以参见这本书[Linguistic Fundamentals for Natural Language
Processing: 100 Essentials from Morphology and
Syntax](https://dl.acm.org/doi/book/10.5555/2534456)。

- 直接宾语： 用dobj表示。
- 间接宾语： 用dative表示。

```{.python .input  n=69}
doc = nlp("He gave me his book.")
spacy.displacy.render(doc, style='dep')

doc = nlp("He gave his book to me. ")
spacy.displacy.render(doc, style='dep')
```

```{.json .output n=69}
[
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:lang=\"en\" id=\"1024557b37d640038e8157e1e05a4f6a-0\" class=\"displacy\" width=\"925\" height=\"312.0\" direction=\"ltr\" style=\"max-width: none; height: 312.0px; color: #000000; background: #ffffff; font-family: Arial; direction: ltr\">\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"222.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"50\">He</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"50\">PRON</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"222.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"225\">gave</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"225\">VERB</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"222.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"400\">me</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"400\">PRON</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"222.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"575\">his</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"575\">PRON</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"222.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"750\">book.</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"750\">NOUN</tspan>\n</text>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-1024557b37d640038e8157e1e05a4f6a-0-0\" stroke-width=\"2px\" d=\"M70,177.0 C70,89.5 220.0,89.5 220.0,177.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-1024557b37d640038e8157e1e05a4f6a-0-0\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">nsubj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M70,179.0 L62,167.0 78,167.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-1024557b37d640038e8157e1e05a4f6a-0-1\" stroke-width=\"2px\" d=\"M245,177.0 C245,89.5 395.0,89.5 395.0,177.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-1024557b37d640038e8157e1e05a4f6a-0-1\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">dative</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M395.0,179.0 L403.0,167.0 387.0,167.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-1024557b37d640038e8157e1e05a4f6a-0-2\" stroke-width=\"2px\" d=\"M595,177.0 C595,89.5 745.0,89.5 745.0,177.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-1024557b37d640038e8157e1e05a4f6a-0-2\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">poss</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M595,179.0 L587,167.0 603,167.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-1024557b37d640038e8157e1e05a4f6a-0-3\" stroke-width=\"2px\" d=\"M245,177.0 C245,2.0 750.0,2.0 750.0,177.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-1024557b37d640038e8157e1e05a4f6a-0-3\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">dobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M750.0,179.0 L758.0,167.0 742.0,167.0\" fill=\"currentColor\"/>\n</g>\n</svg></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:lang=\"en\" id=\"420c01e6569d4971a3d9f57d92542e3d-0\" class=\"displacy\" width=\"1100\" height=\"399.5\" direction=\"ltr\" style=\"max-width: none; height: 399.5px; color: #000000; background: #ffffff; font-family: Arial; direction: ltr\">\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"50\">He</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"50\">PRON</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"225\">gave</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"225\">VERB</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"400\">his</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"400\">PRON</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"575\">book</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"575\">NOUN</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"750\">to</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"750\">ADP</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"925\">me.</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"925\">PRON</tspan>\n</text>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-420c01e6569d4971a3d9f57d92542e3d-0-0\" stroke-width=\"2px\" d=\"M70,264.5 C70,177.0 215.0,177.0 215.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-420c01e6569d4971a3d9f57d92542e3d-0-0\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">nsubj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M70,266.5 L62,254.5 78,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-420c01e6569d4971a3d9f57d92542e3d-0-1\" stroke-width=\"2px\" d=\"M420,264.5 C420,177.0 565.0,177.0 565.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-420c01e6569d4971a3d9f57d92542e3d-0-1\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">poss</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M420,266.5 L412,254.5 428,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-420c01e6569d4971a3d9f57d92542e3d-0-2\" stroke-width=\"2px\" d=\"M245,264.5 C245,89.5 570.0,89.5 570.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-420c01e6569d4971a3d9f57d92542e3d-0-2\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">dobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M570.0,266.5 L578.0,254.5 562.0,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-420c01e6569d4971a3d9f57d92542e3d-0-3\" stroke-width=\"2px\" d=\"M245,264.5 C245,2.0 750.0,2.0 750.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-420c01e6569d4971a3d9f57d92542e3d-0-3\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">dative</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M750.0,266.5 L758.0,254.5 742.0,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-420c01e6569d4971a3d9f57d92542e3d-0-4\" stroke-width=\"2px\" d=\"M770,264.5 C770,177.0 915.0,177.0 915.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-420c01e6569d4971a3d9f57d92542e3d-0-4\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">pobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M915.0,266.5 L923.0,254.5 907.0,254.5\" fill=\"currentColor\"/>\n</g>\n</svg></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 }
]
```

### Extracting transitive verbs and their direct objects

通过抽取transitive verbs和direct objects，我们可以识别用户意图（intent）。比如:

```{.python .input  n=72}
doc = nlp("find a flight from washington to sf")
spacy.displacy.render(doc, style='dep')
for token in doc:
    if token.dep_ == "dobj":
        print(token.head.text + token.text.capitalize())
```

```{.json .output n=72}
[
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:lang=\"en\" id=\"767e4cc7645c4c8e9b1b2f449c18b618-0\" class=\"displacy\" width=\"1275\" height=\"399.5\" direction=\"ltr\" style=\"max-width: none; height: 399.5px; color: #000000; background: #ffffff; font-family: Arial; direction: ltr\">\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"50\">find</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"50\">VERB</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"225\">a</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"225\">DET</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"400\">flight</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"400\">NOUN</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"575\">from</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"575\">ADP</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"750\">washington</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"750\">PROPN</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"925\">to</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"925\">ADP</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"1100\">sf</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"1100\">PROPN</tspan>\n</text>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-0\" stroke-width=\"2px\" d=\"M245,264.5 C245,177.0 390.0,177.0 390.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-0\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">det</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M245,266.5 L237,254.5 253,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-1\" stroke-width=\"2px\" d=\"M70,264.5 C70,89.5 395.0,89.5 395.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-1\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">dobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M395.0,266.5 L403.0,254.5 387.0,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-2\" stroke-width=\"2px\" d=\"M420,264.5 C420,177.0 565.0,177.0 565.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-2\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">prep</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M565.0,266.5 L573.0,254.5 557.0,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-3\" stroke-width=\"2px\" d=\"M595,264.5 C595,177.0 740.0,177.0 740.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-3\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">pobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M740.0,266.5 L748.0,254.5 732.0,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-4\" stroke-width=\"2px\" d=\"M70,264.5 C70,2.0 925.0,2.0 925.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-4\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">prep</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M925.0,266.5 L933.0,254.5 917.0,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-5\" stroke-width=\"2px\" d=\"M945,264.5 C945,177.0 1090.0,177.0 1090.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-767e4cc7645c4c8e9b1b2f449c18b618-0-5\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">pobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M1090.0,266.5 L1098.0,254.5 1082.0,254.5\" fill=\"currentColor\"/>\n</g>\n</svg></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "findFlight\n"
 }
]
```

### Extracting multiple intents with conjunction relation

有些用户场景，覆盖了多个用户意图。比如：

~~~
show all flights and fares from denver to san francisco
~~~

使用token.conjuncts可以返回coordinated tokens。这样我们不难发现用户的意图是showFlights和showFares.

```{.python .input  n=75}
doc = nlp("show all flights and fares from denver to san francisco")
spacy.displacy.render(doc, style='dep')
for token in doc:
    if token.dep_ == "dobj":
        dobj = token.text
        conj = [t.text for t in token.conjuncts]
        verb = token.head
print(verb, dobj, conj)
```

```{.json .output n=75}
[
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:lang=\"en\" id=\"69ac43a0e12f46f2b7266b84e25b959d-0\" class=\"displacy\" width=\"1800\" height=\"487.0\" direction=\"ltr\" style=\"max-width: none; height: 487.0px; color: #000000; background: #ffffff; font-family: Arial; direction: ltr\">\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"50\">show</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"50\">VERB</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"225\">all</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"225\">DET</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"400\">flights</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"400\">NOUN</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"575\">and</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"575\">CCONJ</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"750\">fares</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"750\">NOUN</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"925\">from</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"925\">ADP</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"1100\">denver</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"1100\">PROPN</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"1275\">to</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"1275\">ADP</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"1450\">san</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"1450\">PROPN</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"397.0\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"1625\">francisco</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"1625\">PROPN</tspan>\n</text>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-69ac43a0e12f46f2b7266b84e25b959d-0-0\" stroke-width=\"2px\" d=\"M245,352.0 C245,264.5 385.0,264.5 385.0,352.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-69ac43a0e12f46f2b7266b84e25b959d-0-0\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">det</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M245,354.0 L237,342.0 253,342.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-69ac43a0e12f46f2b7266b84e25b959d-0-1\" stroke-width=\"2px\" d=\"M70,352.0 C70,177.0 390.0,177.0 390.0,352.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-69ac43a0e12f46f2b7266b84e25b959d-0-1\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">dobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M390.0,354.0 L398.0,342.0 382.0,342.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-69ac43a0e12f46f2b7266b84e25b959d-0-2\" stroke-width=\"2px\" d=\"M420,352.0 C420,264.5 560.0,264.5 560.0,352.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-69ac43a0e12f46f2b7266b84e25b959d-0-2\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">cc</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M560.0,354.0 L568.0,342.0 552.0,342.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-69ac43a0e12f46f2b7266b84e25b959d-0-3\" stroke-width=\"2px\" d=\"M420,352.0 C420,177.0 740.0,177.0 740.0,352.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-69ac43a0e12f46f2b7266b84e25b959d-0-3\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">conj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M740.0,354.0 L748.0,342.0 732.0,342.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-69ac43a0e12f46f2b7266b84e25b959d-0-4\" stroke-width=\"2px\" d=\"M420,352.0 C420,89.5 920.0,89.5 920.0,352.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-69ac43a0e12f46f2b7266b84e25b959d-0-4\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">prep</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M920.0,354.0 L928.0,342.0 912.0,342.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-69ac43a0e12f46f2b7266b84e25b959d-0-5\" stroke-width=\"2px\" d=\"M945,352.0 C945,264.5 1085.0,264.5 1085.0,352.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-69ac43a0e12f46f2b7266b84e25b959d-0-5\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">pobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M1085.0,354.0 L1093.0,342.0 1077.0,342.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-69ac43a0e12f46f2b7266b84e25b959d-0-6\" stroke-width=\"2px\" d=\"M420,352.0 C420,2.0 1275.0,2.0 1275.0,352.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-69ac43a0e12f46f2b7266b84e25b959d-0-6\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">prep</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M1275.0,354.0 L1283.0,342.0 1267.0,342.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-69ac43a0e12f46f2b7266b84e25b959d-0-7\" stroke-width=\"2px\" d=\"M1470,352.0 C1470,264.5 1610.0,264.5 1610.0,352.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-69ac43a0e12f46f2b7266b84e25b959d-0-7\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">compound</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M1470,354.0 L1462,342.0 1478,342.0\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-69ac43a0e12f46f2b7266b84e25b959d-0-8\" stroke-width=\"2px\" d=\"M1295,352.0 C1295,177.0 1615.0,177.0 1615.0,352.0\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-69ac43a0e12f46f2b7266b84e25b959d-0-8\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">pobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M1615.0,354.0 L1623.0,342.0 1607.0,342.0\" fill=\"currentColor\"/>\n</g>\n</svg></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "show flights ['fares']\n"
 }
]
```

### Recognizing the intent using wordlists

```{.python .input  n=91}
doc = nlp("i want to make a reservation for a flight")
spacy.displacy.render(doc, style='dep')

dObj =None
tVerb = None

# Extract the direct object and its transitive verb
for token in doc:
    if token.dep_ == "dobj":
        dObj = token
        tVerb = token.head 

print(f'dObj: {dObj}')
print(f'tVerb: {tVerb}')
        
# Extract the helper verb
intentVerb = None
verbList = ["want", "like", "need", "order"]
if tVerb.text in verbList:
    intentVerb = tVerb
else:
    if tVerb.head.dep_ == "ROOT":
        intentVerb = tVerb.head
        
# Extract the object of the intent
intentObj = None
objList = ["flight", "meal", "booking"]
if dObj.text in objList:
    intentObj = dObj
else:
    for child in tVerb.children:
        if child.dep_ == "prep":
            intentObj = list(child.children)[0]
            break
        elif child.dep_ == "compound":
            intentObj = child
            break
            
print(intentVerb.text + intentObj.text.capitalize())            
```

```{.json .output n=91}
[
 {
  "data": {
   "text/html": "<span class=\"tex2jax_ignore\"><svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:lang=\"en\" id=\"74fa13ba25d7482ab43b9770f91ef04c-0\" class=\"displacy\" width=\"1625\" height=\"399.5\" direction=\"ltr\" style=\"max-width: none; height: 399.5px; color: #000000; background: #ffffff; font-family: Arial; direction: ltr\">\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"50\">i</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"50\">PRON</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"225\">want</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"225\">VERB</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"400\">to</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"400\">PART</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"575\">make</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"575\">VERB</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"750\">a</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"750\">DET</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"925\">reservation</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"925\">NOUN</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"1100\">for</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"1100\">ADP</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"1275\">a</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"1275\">DET</tspan>\n</text>\n\n<text class=\"displacy-token\" fill=\"currentColor\" text-anchor=\"middle\" y=\"309.5\">\n    <tspan class=\"displacy-word\" fill=\"currentColor\" x=\"1450\">flight</tspan>\n    <tspan class=\"displacy-tag\" dy=\"2em\" fill=\"currentColor\" x=\"1450\">NOUN</tspan>\n</text>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-74fa13ba25d7482ab43b9770f91ef04c-0-0\" stroke-width=\"2px\" d=\"M70,264.5 C70,177.0 215.0,177.0 215.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-74fa13ba25d7482ab43b9770f91ef04c-0-0\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">nsubj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M70,266.5 L62,254.5 78,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-74fa13ba25d7482ab43b9770f91ef04c-0-1\" stroke-width=\"2px\" d=\"M420,264.5 C420,177.0 565.0,177.0 565.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-74fa13ba25d7482ab43b9770f91ef04c-0-1\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">aux</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M420,266.5 L412,254.5 428,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-74fa13ba25d7482ab43b9770f91ef04c-0-2\" stroke-width=\"2px\" d=\"M245,264.5 C245,89.5 570.0,89.5 570.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-74fa13ba25d7482ab43b9770f91ef04c-0-2\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">xcomp</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M570.0,266.5 L578.0,254.5 562.0,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-74fa13ba25d7482ab43b9770f91ef04c-0-3\" stroke-width=\"2px\" d=\"M770,264.5 C770,177.0 915.0,177.0 915.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-74fa13ba25d7482ab43b9770f91ef04c-0-3\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">det</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M770,266.5 L762,254.5 778,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-74fa13ba25d7482ab43b9770f91ef04c-0-4\" stroke-width=\"2px\" d=\"M595,264.5 C595,89.5 920.0,89.5 920.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-74fa13ba25d7482ab43b9770f91ef04c-0-4\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">dobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M920.0,266.5 L928.0,254.5 912.0,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-74fa13ba25d7482ab43b9770f91ef04c-0-5\" stroke-width=\"2px\" d=\"M595,264.5 C595,2.0 1100.0,2.0 1100.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-74fa13ba25d7482ab43b9770f91ef04c-0-5\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">prep</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M1100.0,266.5 L1108.0,254.5 1092.0,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-74fa13ba25d7482ab43b9770f91ef04c-0-6\" stroke-width=\"2px\" d=\"M1295,264.5 C1295,177.0 1440.0,177.0 1440.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-74fa13ba25d7482ab43b9770f91ef04c-0-6\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">det</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M1295,266.5 L1287,254.5 1303,254.5\" fill=\"currentColor\"/>\n</g>\n\n<g class=\"displacy-arrow\">\n    <path class=\"displacy-arc\" id=\"arrow-74fa13ba25d7482ab43b9770f91ef04c-0-7\" stroke-width=\"2px\" d=\"M1120,264.5 C1120,89.5 1445.0,89.5 1445.0,264.5\" fill=\"none\" stroke=\"currentColor\"/>\n    <text dy=\"1.25em\" style=\"font-size: 0.8em; letter-spacing: 1px\">\n        <textPath xlink:href=\"#arrow-74fa13ba25d7482ab43b9770f91ef04c-0-7\" class=\"displacy-label\" startOffset=\"50%\" side=\"left\" fill=\"currentColor\" text-anchor=\"middle\">pobj</textPath>\n    </text>\n    <path class=\"displacy-arrowhead\" d=\"M1445.0,266.5 L1453.0,254.5 1437.0,254.5\" fill=\"currentColor\"/>\n</g>\n</svg></span>",
   "text/plain": "<IPython.core.display.HTML object>"
  },
  "metadata": {},
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "dObj: reservation\ntVerb: make\nwantFlight\n"
 }
]
```

## Semantic similarity methods for semantic parsing

一般来说，有两种方式来识别语法的相似性。

- 使用同义词字典（synonyms dictionary）
- 使用基于词向量的语义相似度

本节将尝试这两种方法。

### Using synonyms lists for semantic similarity

```{.python .input  n=102}

verbSynsets = {
    "show": ["list"],
    "book": ["make a reservation", "buy", "reserve"]
} 

objSynsets = {
    "meal": ["food"],
    "plane": ["aircraft", "airplane"]
}    


def get_vert_object(doc):
    for token in doc:
        if token.dep_ == "dobj":
            obj = token.lemma_
            verb = token.head.lemma_
            break    
    return verb, obj

def synonym_replace(verb, obj, 
                    verbSynsets=verbSynsets, 
                    objSynsets=objSynsets):
    for key, synonyms in verbSynsets.items():
        if verb in synonyms:
            verb = key
            break
                
    for key, synonyms in objSynsets.items():
        if obj in synonyms:
            obj = key
            break                
        
    return verb, obj
    


doc1 = nlp("show me all aircrafts that cp uses")
doc2 = nlp("list all meals on my flight")

verb1, obj1 = get_vert_object(doc1)
verb2, obj2 = get_vert_object(doc2)

print(verb1+obj1.capitalize())
print(verb2+obj2.capitalize())

synonym_verb1, synonym_obj1 = synonym_replace(verb1, obj1)
synonym_verb2, synonym_obj2 = synonym_replace(verb2, obj2)

print('-'*50)
print(verb1+obj1.capitalize())
print(verb2+obj2.capitalize())
```

```{.json .output n=102}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "showAircraft\nlistMeal\n--------------------------------------------------\nshowAircraft\nlistMeal\n"
 }
]
```

### Using word vectors to recognize semantic similarity

从下面的相似度，结果可以认定，这两个语句是统一场景的可能性非常低。

```{.python .input  n=108}
def get_vert_object(doc):
    for token in doc:
        if token.dep_ == "dobj":
            obj = token
            verb = token.head
            break    
    return verb, obj

verb1, obj1 = get_vert_object(doc1)
verb2, obj2 = get_vert_object(doc2)

print(obj1.similarity(obj2))
print(verb1.similarity(verb2))
```

```{.json .output n=108}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "0.15025872\n0.33161193\n"
 }
]
```

## Putting it all together

```{.python .input  n=117}
matcher = Matcher(nlp.vocab)

doc = nlp("show me flights from denver to philadelphia on tuesday")
ents = doc.ents
print(f'ents = {ents}')

# 介词 + 地点
print('-'*50)
pattern = [{"POS": "ADP"}, {"ENT_TYPE": "GPE"}]
matcher.add("prepositionLocation", [pattern])
matches = matcher(doc)
show_matches(nlp, doc, matches)

# 直接宾语
print('-'*50)
for token in doc:
    if token.dep_ == "dobj":
        print(token.head.lemma_ + token.lemma_.capitalize())
```

```{.json .output n=117}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "ents = (denver, philadelphia, tuesday)\n--------------------------------------------------\nprepositionLocation 3 5 from denver\nprepositionLocation 5 7 to philadelphia\n--------------------------------------------------\nshowFlight\n"
 }
]
```

```{.python .input}

```
