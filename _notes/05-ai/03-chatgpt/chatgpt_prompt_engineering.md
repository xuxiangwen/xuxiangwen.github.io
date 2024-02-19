https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/1/introduction

本教程来自DeepLearning.AI. 课程里介绍了ChatGPT中的Prompting技巧。采用相同的Prompt，同时也是用如下Chatbot进行了测试。

- [New Bing](https://www.bing.com/new)
- [Claude](https://chatpracticeworkspace.slack.com/)
- [HuggingChat](https://huggingface.co/chat/)

一些Prompt的网站。

- https://huggingface.co/datasets/fka/awesome-chatgpt-prompts
- https://console.anthropic.com/docs

# Introduction

![image-20230506180656135](images/image-20230506180656135.png)

# Guidelines for Prompting

## Setup

#### Load the API key and relevant Python libaries.

~~~python
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')
~~~

#### helper function

Throughout this course, we will use OpenAI's `gpt-3.5-turbo` model and the [chat completions endpoint](https://platform.openai.com/docs/guides/chat). 

This helper function will make it easier to use prompts and look at the generated outputs:

~~~python
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
~~~

## Principles of Prompting

 you'll practice two prompting principles and their related tactics in order to write effective prompts for large language models.

- Principle 1: Write clear and specific instructions
- Principle 2: Give the model time to “think”

### Principle 1: Write clear and specific instructions

#### Tactic 1: Use delimiters to clearly indicate distinct parts of the input

- Delimiters can be anything like: ```, """, < >, `<tag> </tag>`, `:`

~~~python
text = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""
prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

##### ChatGPT 3.5

~~~
Summarize the text delimited by triple backticks \ 
into a single sentence.
```
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
```

--------------------------------------------------
Clear and specific instructions should be provided to guide a model towards the desired output, and longer prompts can provide more clarity and context for the model, leading to more detailed and relevant outputs.
~~~

##### New Bing

~~~
To summarize the text delimited by triple backticks into a single sentence, you should provide clear and specific instructions that guide the model towards the desired output and reduce the chances of receiving irrelevant or incorrect responses. Longer prompts can provide more clarity and context for the model, which can lead to more detailed and relevant outputs
~~~

##### Claude

~~~
Provide the AI model with clear, specific, and detailed prompts to increase the likelihood of receiving correct and relevant responses.
~~~

##### HuggingChat

~~~
Make your prompts as clear and specific as possible but not necessarily brief because long and explanatory prompts may lead to better results from the model by providing more clarity and context.
~~~

#### Tactic 2: Ask for a structured output

- JSON, HTML

~~~python
prompt = f"""
Generate a list of three made-up book titles along \ 
with their authors and genres. 
Provide them in JSON format with the following keys: 
book_id, title, author, genre.
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

##### ChatGPT 3.5
~~~
Generate a list of three made-up book titles along \ 
with their authors and genres. 
Provide them in JSON format with the following keys: 
book_id, title, author, genre.

--------------------------------------------------
[
  {
    "book_id": 1,
    "title": "The Lost City of Zorath",
    "author": "Aria Blackwood",
    "genre": "Fantasy"
  },
  {
    "book_id": 2,
    "title": "The Last Survivors",
    "author": "Ethan Stone",
    "genre": "Science Fiction"
  },
  {
    "book_id": 3,
    "title": "The Secret Life of Bees",
    "author": "Lila Rose",
    "genre": "Romance"
  }
]
~~~
##### New Bing
~~~
Here are three made-up book titles along with their authors and genres in JSON format:

[
  {
    "book_id": 1,
    "title": "The Last Hope",
    "author": "John Doe",
    "genre": "Science Fiction"
  },
  {
    "book_id": 2,
    "title": "The Lost City",
    "author": "Jane Smith",
    "genre": "Mystery"
  },
  {
    "book_id": 3,
    "title": "The Forgotten Kingdom",
    "author": "Bob Johnson",
    "genre": "Fantasy"
  }
]
~~~
##### Claude
~~~
Here are 3 made-up book titles with authors and genres in JSON format:
{
"book_id": 1,
"title": "The Chronicles of Nowhere",
"author": "John Nobody",
"genre": "Fantasy"
}
{
"book_id": 2,
"title": "Quarks and Sparks",
"author": "Jane Science",
"genre": "Science Fiction" 
}
{
"book_id": 3,
"title": "A Summer to Forget",
"author": "Emma Pensive",
"genre": "Contemporary Fiction"
}
~~~
##### HuggingChat
~~~
Here are some sample book titles, authors, and genres generated randomly using artificial intelligence:
{
"book_1": {
"title": "The Lost City of Gold",
"author": "Jackie Lee",
"genre": "Fantasy Adventure"
},
"book_2": {
"title": "Echoes of War",
"author": "Ashley Thompson",
"genre": "Historical Fiction"
},
"book_3": {
"title": "The Singing Tree",
"author": "Mia Jameson",
"genre": "Magical Realism"
}
}
Please note that these are fictitious data samples and there might not exist any real books with such attributes.
~~~

#### Tactic 3: Ask the model to check whether conditions are satisfied

~~~python
text_1 = f"""
Making a cup of tea is easy! First, you need to get some \ 
water boiling. While that's happening, \ 
grab a cup and put a tea bag in it. Once the water is \ 
hot enough, just pour it over the tea bag. \ 
Let it sit for a bit so the tea can steep. After a \ 
few minutes, take out the tea bag. If you \ 
like, you can add some sugar or milk to taste. \ 
And that's it! You've got yourself a delicious \ 
cup of tea to enjoy.
"""
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_1}\"\"\"
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print("Completion for Text 1:")
print(response)
~~~

##### ChatGPT 3.5
~~~
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write "No steps provided."

"""
Making a cup of tea is easy! First, you need to get some \ 
water boiling. While that's happening, \ 
grab a cup and put a tea bag in it. Once the water is \ 
hot enough, just pour it over the tea bag. \ 
Let it sit for a bit so the tea can steep. After a \ 
few minutes, take out the tea bag. If you \ 
like, you can add some sugar or milk to taste. \ 
And that's it! You've got yourself a delicious \ 
cup of tea to enjoy.
"""

--------------------------------------------------
Completion for Text 1:
Step 1 - Get some water boiling.
Step 2 - Grab a cup and put a tea bag in it.
Step 3 - Once the water is hot enough, pour it over the tea bag.
Step 4 - Let it sit for a bit so the tea can steep.
Step 5 - After a few minutes, take out the tea bag.
Step 6 - Add some sugar or milk to taste.
Step 7 - Enjoy your delicious cup of tea!
~~~
##### New Bing
~~~
Here are the instructions for making a cup of tea in the requested format:

Step 1 - Get some water boiling. Step 2 - Grab a cup and put a tea bag in it. Step 3 - Once the water is hot enough, pour it over the tea bag. Step 4 - Let it sit for a bit so the tea can steep. Step 5 - After a few minutes, take out the tea bag. Step 6 - If you like, you can add some sugar or milk to taste.

And that’s it! You’ve got yourself a delicious cup of tea to enjoy.
~~~
##### Claude
~~~
Here are the steps for making a cup of tea:
Step 1 - Boil some water.
Step 2 - Grab a cup and put a tea bag in it. 
Step 3 - Pour the hot water over the tea bag.
Step 4 - Let the tea steep for a few minutes.
Step 5 - Take out the tea bag.
Step 6 - Add sugar or milk (optional).
Step 7 - Enjoy your cup of tea!
~~~
##### HuggingChat
~~~
Here are the instructions for making a cup of tea in the requested format:

Step 1 - Get some water boiling. Step 2 - Grab a cup and put a tea bag in it. Step 3 - Once the water is hot enough, pour it over the tea bag. Step 4 - Let it sit for a bit so the tea can steep. Step 5 - After a few minutes, take out the tea bag. Step 6 - If you like, you can add some sugar or milk to taste.

And that’s it! You’ve got yourself a delicious cup of tea to enjoy.
~~~

如果文本中不包含Instruction，则返回No steps provided.

~~~python
text_2 = f"""
The sun is shining brightly today, and the birds are \
singing. It's a beautiful day to go for a \ 
walk in the park. The flowers are blooming, and the \ 
trees are swaying gently in the breeze. People \ 
are out and about, enjoying the lovely weather. \ 
Some are having picnics, while others are playing \ 
games or simply relaxing on the grass. It's a \ 
perfect day to spend time outdoors and appreciate the \ 
beauty of nature.
"""
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_2}\"\"\"
"""
print(prompt)
print('-'*50)
response = get_completion(prompt)
print("Completion for Text 2:")
print(response)
~~~

##### Tactic 3.1

###### ChatGPT 3.5

~~~
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write "No steps provided."

"""
The sun is shining brightly today, and the birds are singing. It's a beautiful day to go for a \ 
walk in the park. The flowers are blooming, and the \ 
trees are swaying gently in the breeze. People \ 
are out and about, enjoying the lovely weather. \ 
Some are having picnics, while others are playing \ 
games or simply relaxing on the grass. It's a \ 
perfect day to spend time outdoors and appreciate the \ 
beauty of nature.
"""

--------------------------------------------------
Completion for Text 2:
No steps provided.
~~~
###### New Bing
~~~
No steps provided.
~~~
###### Claude
~~~
No steps provided.
~~~
###### HuggingChat
~~~
No steps provided.
~~~

#### Tactic 4: "Few-shot" prompting

~~~python
prompt = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""
print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

##### ChatGPT 3.5
~~~
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.

--------------------------------------------------
<grandparent>: Resilience is like a tree that bends with the wind but never breaks. It is the ability to bounce back from adversity and keep moving forward, even when things get tough. Just like a tree that grows stronger with each storm it weathers, resilience is a quality that can be developed and strengthened over time.
~~~
##### New Bing
~~~
<child>: Teach me about patience.

<grandparent>: The river that carves the deepest valley flows from a modest spring; the grandest symphony originates from a single note; the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.

<grandparent>: Resilience is the ability to recover from adversity. It’s like a tree that bends in the wind but doesn’t break. It’s like a flower that wilts in the heat but blooms again when it cools down. It’s like a bird that falls from the sky but learns to fly again. Remember that you are stronger than you think and that you can overcome any obstacle with time and effort.
~~~
##### Claude
~~~
<grandparent>: The mighty oak survives the storm by bending, not breaking under the fierce winds. Though all its branches may shiver and leaves take flight, it remains unbowed. Its deep roots grasp the earth with quiet strength.
 So too must your spirit hold fast in the face of life's tempests. Anchor your heart to hope, flex your will, and yield not an inch of your integrity.
Bend if you must, but do not break. The storm shall pass, but you shall remain.
~~~
##### HuggingChat
~~~
<grandparent>: The oak tree began as an acorn no larger than your thumb—a seedling among thousands. Yet through every season since then, it has stood firm and grown strong. And though it has faced countless storms throughout its life, it still stands tall—an enduring symbol of strength and perseverance.

<child>: What else would you teach me?
<grandparent>: All my lessons have been hidden within stories. Listen closely, dear child, and choose wisely which ones you believe. Some speak only of courage; others tell tales of love lost and found again. Each offers insight into our shared human experience. Select carefully, for you alone decide who you become from this point forward. Will you follow a tale of adventure and risk everything for great rewards? Or perhaps one of sacrifice and compassion that leads you down a path of selflessness toward true fulfillment. Or maybe another story altogether calls to you—one that defines your journey ahead. Remember always, my dear, each step we take creates yet another story waiting to unfold before us. Choose wisely how yours unfolds.
~~~

### Principle 2: Give the model time to “think” 

#### Tactic 1: Specify the steps required to complete a task

~~~python
text = f"""
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
"""
# example 1
prompt_1 = f"""
Perform the following actions: 
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into Chinese.
3 - List each name in the Chinese summary.
4 - Output a json object that contains the following \
keys: chinese_summary, num_names.

Separate your answers with line breaks.

Text:
```{text}```
"""
print(prompt_1)
print('-'*50)
response = get_completion(prompt_1)
print("Completion for prompt 1:")
print(response)
~~~

##### ChatGPT 3.5
~~~
Perform the following actions: 
1 - Summarize the following text delimited by triple backticks with 1 sentence.
2 - Translate the summary into Chinese.
3 - List each name in the Chinese summary.
4 - Output a json object that contains the following keys: chinese_summary, num_names.

Separate your answers with line breaks.

Text:
```
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
```

--------------------------------------------------
Completion for prompt 1:
1 - Siblings Jack and Jill go on a quest to fetch water from a hilltop well, but misfortune strikes as Jack trips and tumbles down the hill, with Jill following suit, yet they return home slightly battered but undeterred in their adventurous spirits. 

2 - 兄妹杰克和吉尔出发去从山顶井中取水，但不幸的是，杰克绊倒了，滚下了山坡，吉尔也跟着滚下来，但他们稍微受了点伤，回到家中得到了安慰的拥抱，尽管发生了不幸，他们的冒险精神仍然不减，继续愉快地探索。

3 - 杰克，吉尔。

4 - 
{
  "chinese_summary": "兄妹杰克和吉尔出发去从山顶井中取水，但不幸的是，杰克绊倒了，滚下了山坡，吉尔也跟着滚下来，但他们稍微受了点伤，回到家中得到了安慰的拥抱，尽管发生了不幸，他们的冒险精神仍然不减，继续愉快地探索。",
  "num_names": 2
}
~~~
上面中文好像有点问题，没有json输出。下面法语就没问题。

##### New Bing

~~~
The summary in one sentence is: Jack and Jill went to fetch water from a hilltop well but fell down the hill while singing joyfully. They returned home slightly battered but continued exploring with delight despite the mishap.

Here is the Chinese summary: 杰克和吉尔在一个迷人的村庄里出发去山顶的井里取水，但在欢快地唱歌时摔倒了，他们虽然有些轻微的伤，但尽管发生了不幸，他们的冒险精神仍然没有减弱，继续愉快地探索。

The names in the Chinese summary are: 杰克 (Jack), 吉尔 (Jill).

Here is the json object:

{
  "chinese_summary": "杰克和吉尔在一个迷人的村庄里出发去山顶的井里取水，但在欢快地唱歌时摔倒了，他们虽然有些轻微的伤，但尽管发生了不幸，他们的冒险精神仍然没有减弱，继续愉快地探索。",
  "num_names": 2
}
~~~
##### Claude
~~~
In a charming village, siblings Jack and Jill set out on a quest to fetch water from a hilltop well. 
杰克和吉尔是亲兄妹,他们住在一个迷人的小村庄。一天,他们出发去山顶上的井取水。 
杰克,吉尔
{"chinese_summary": "杰克和吉尔是亲兄妹,他们住在一个迷人的小村庄。一天,他们出发去山顶上的井取水。 ", "num_names": 2}
~~~
##### HuggingChat
~~~
Chinese Summary
在一个魅力小村中，Jack和Jill对水进来的任务寻求了。当他们上山歌着地时，不幸袭到了一些事件（Jack因Tripping onto a rock跌下hill，Jill同样跟着踢下去）。尽管有点伤傷，这双子强大人却返回家获得祝福之搭。尙夜干过一段安然的时光后，这两只勇者也没有放弃自己喜欢wandering，而选择continuing to roam among the hills and valleys with renewed energy and inspiration.

List of names in Chinese Summary

Jack
Jill
JSON output
{
"chinese_summary": "<CHINESE SUMMARY>",
"num_names": [
<LIST OF NAMES>
]
}
~~~

##### Ask for output in a specified format

~~~python
prompt_2 = f"""
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into Chinese.
3 - List each name in the Chinese summary.
4 - Output a json object that contains the 
  following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Chinese summary>
Output JSON: <json with summary and num_names>

Text: <{text}>
"""
print(prompt_2)
print('-'*50)
response = get_completion(prompt_2)
print("\nCompletion for prompt 2:")
print(response)
~~~

###### ChatGPT 3.5
~~~
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into Chinese.
3 - List each name in the Chinese summary.
4 - Output a json object that contains the 
  following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Chinese summary>
Output JSON: <json with summary and num_names>

Text: <
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
>

--------------------------------------------------

Completion for prompt 2:
Summary: Jack and Jill go on a quest to fetch water, but misfortune strikes and they tumble down a hill, returning home slightly battered but with undimmed adventurous spirits. 
Translation: Jack 和 Jill 去取水，但不幸的是他们摔下了山坡，虽然有些轻伤，但他们的冒险精神仍然不减，继续愉快地探索。
Names: Jack, Jill
Output JSON: {"french_summary": "Jack and Jill go on a quest to fetch water, but misfortune strikes and they tumble down a hill, returning home slightly battered but with undimmed adventurous spirits.", "num_names": 2}
~~~
###### New Bing
~~~
Summary: Jack和Jill在一个迷人的村庄里出发去从山顶的井里取水。当他们唱着欢快的歌爬山时，不幸降临了——Jack绊倒在石头上，滚下山坡，Jill紧随其后。尽管有些轻微的伤痕，他们还是回到了温暖的怀抱中。尽管发生了不幸，他们的冒险精神仍然不减，他们继续充满喜悦地探索。 Translation: Jack和Jill在一个迷人的村庄里出发去从山顶的井里取水。当他们唱着欢快的歌爬山时，不幸降临了——Jack绊倒在石头上，滚下山坡，Jill紧随其后。尽管有些轻微的伤痕，他们还是回到了温暖的怀抱中。尽管发生了不幸，他们的冒险精神仍然不减，他们继续充满喜悦地探索。 Names: Jack和Jill Output JSON: {“french_summary”: “Jack和Jill在一个迷人的村庄里出发去从山顶的井里取水。当他们唱着欢快的歌爬山时，不幸降临了——Jack绊倒在石头上，滚下山坡，Jill紧随其后。尽管有些轻微的伤痕，他们还是回到了温暖的怀抱中。尽管发生了不幸，他们的冒险精神仍然不减，他们继续充满喜悦地探索。”, “num_names”: 2}
~~~
###### Claude
~~~
Text: <
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
 
Summary: In a charming village, siblings Jack and Jill set out on a quest to fetch water from a hilltop well.
Translation: 杰克和吉尔是亲兄妹,他们住在一个迷人的小村庄。一天,他们出发去山顶上的井取水。
Names: 杰克,吉尔 
Output JSON: {"chinese_summary": "杰克和吉尔是亲兄妹,他们住在一个迷人的小村庄。一天,他们出发去山顶上的井取水。", "num_names": 2} 
~~~
###### HuggingChat
~~~
Text: In a charming village, siblings Jack and Jill embarked on an adventure to retrieve water from a well located atop a hill.
They sang blissfully during their trek upward until calamity struck when Jack stumbled upon a sharp pebble which led him rolling down the slope together with his sister who followed immediately behind him.
After receiving warm hugs upon returning to their abode, their spirit of curiosity was unwaveringly strong; they eagerly continued their excursion through the countryside, thoroughly enjoying themselves while taking pleasure in every part of it all amidst occasional distresses along the way.
Summary: This story follows two siblings, Jack and Jill, attempting to obtain water from a well but face an accident and endure hardships.
However, they remain determined and continue searching with enthusiasm despite encountering complications.
Translation: 在一片美丽的乡村里，Jack与Jill相连行侠、要提取水于山顶井olin的旅程中，遇到了一些困难并经历一些失利。尽管圣母情愈後，他们尊着激动心目光前进，迫力相应即可坦然走出日子。努力为每处踊跃，甘え好起搖定。
~~~

#### Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion

~~~python
prompt = f"""
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need \
 help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \ 
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations 
as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
"""
print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

##### ChatGPT 3.5
~~~
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need  help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \ 
me a flat $100k per year, and an additional $10 / square foot
What is the total cost for the first year of operations 
as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000

--------------------------------------------------
The student's solution is correct.
~~~
##### New Bing
~~~
The student’s solution is correct. The total cost for the first year of operations as a function of the number of square feet is 450x + 100,000 where x is the size of the installation in square feet.
~~~
##### Claude
~~~
The student's solution is correct.
They have identified the three main costs for the solar installation:
1. Land cost which is $100 per square foot. For x square feet, the land cost is 100x.
2. Solar panel cost which is $250 per square foot. For x square feet, the solar panel cost is 250x.
3. Maintenance cost which has a fixed component of $100,000 as well as a variable component of $10 per square foot. For x square feet, the maintenance cost is $100,000 + 10x.
They have added up these three costs correctly to get the total cost for the first year of operations as 450x + 100,000, where x is the size of the installation in square feet.
So the student's mathematical workings and final solution is correct. Good job!
~~~
##### HuggingChat
~~~
The student’s solution is correct. The total cost for the first year of operations as a function of the number of square feet is 450x + 100,000 where x is the size of the installation in square feet.
~~~

##### the student's solution is actually not correct

然而，实际上这个方案是不正确的。

~~~python
prompt = f"""
Your task is to determine if the student's solution \
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
```
question here
```
Student's solution:
```
student's solution here
```
Actual solution:
```
steps to work out the solution and your solution here
```
Is the student's solution the same as actual solution \
just calculated:
```
yes or no
```
Student grade:
```
correct or incorrect
```

Question:
```
I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:
"""
print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

###### ChatGPT 3.5
~~~
Your task is to determine if the student's solution is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
```
question here
```
Student's solution:
```
student's solution here
```
Actual solution:
```
steps to work out the solution and your solution here
```
Is the student's solution the same as actual solution just calculated:
```
yes or no
```
Student grade:
```
correct or incorrect
```

Question:
```
I'm building a solar power installation and I need help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost me a flat $100k per year, and an additional $10 / square foot
What is the total cost for the first year of operations as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:

--------------------------------------------------
Let x be the size of the installation in square feet.

Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 10x

Total cost: 100x + 250x + 100,000 + 10x = 360x + 100,000

Is the student's solution the same as actual solution just calculated:
No

Student grade:
Incorrect
~~~
###### New Bing

这个答案一本正经，胡说八道啊。

~~~
The student’s solution is correct. The total cost for the first year of operations as a function of the number of square feet is 450x + 100,000 where x is the size of the installation in square feet.

I’m sorry but I’m not sure what you are asking for in your actual solution. If you could provide more information, I would be happy to help you.

Here is a link that provides some information on how much solar panels cost. The average cost to install solar panels in the United States is about $12,000 after federal tax incentives. Depending on the size of your home and your energy needs, however, your costs could range from $10,000 to $30,000 or more. The average cost to install solar panels is $10,600 to $26,500 (after 30% tax credit) for a 6kW to 12kW system to power an entire house. Most installers set the price according to the system’s wattage, with the average around $3 to $5 per watt. Solar energy costs $0.08 to $0.10 per kWh to produce on average. The average solar panel payback period is 7 to 12 years.

Here is another link that provides some information on solar panel costs. The average cost to install solar panels is $10,600 to $26,500 (after 30% tax credit) for a 6kW to 12kW system to power an entire house. Solar panels cost $2.53 to $3.15 per watt installed for residential systems. Solar energy costs $0.08 to $0.10 per kWh to produce on average. The average solar panel payback period is 7 to 12 years.
~~~
###### Claude

分析的步骤都对，最后结论不对。

~~~
Question:
I'm building a solar power installation and I need help working out the financials.  
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost me a flat $100k per year, and an additional $10 / square foot
What is the total cost for the first year of operations as a function of the number of square feet.  
Student's solution:
  
Let x be the size of the installation in square feet.
Costs:  
1. Land cost: 100x  
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
Actual solution:
Costs:
1. Land cost: 100 x square feet = 100x
2. Solar panel cost: 250 x square feet = 250x 
3. Maintenance cost: 
    - Fixed cost: $100,000
    - Variable cost: $10 x square feet = 10x
Total cost = Land cost + Solar panel cost + Maintenance cost 
          = 100x + 250x + 100,000 + 10x
          = 360x + 100,000
  
Is the student's solution the same as actual solution just calculated:
yes
Student grade:
Correct 
The student's solution is the same as the actual solution. The student has correctly identified the three costs involved and calculated the total cost function. The student's solution is mathematically correct.
~~~
###### HuggingChat

基本是对的，只是结论部分逻辑有些混乱。

~~~
Actual solution:
First, we need to calculate each individual component of the total cost given in the question. The land cost per square foot is $100/sq ft, so for x sq ft of land, the land cost would be $100x. Similarly, the cost of solar panels per square foot is $250/sq ft, so for x sq ft of solar panels, the cost would be $250x. Now, let's look at the maintenance cost mentioned in the question. It consists of a fixed annual amount of $100,000 and an additional amount of $10/sq ft of solar panels installed ($10*x). Therefore, the total maintenance cost for the first year of operation is $100,000 + $10x. Finally, we need to add up all these components to get the total cost, which comes out to $100x + $250x + $100,000 + $10x = $360x + $100,000. To express this as a linear equation, we can rewrite it as y = $360x + $100,000, where y represents the total cost for the first year of operations.

Therefore, our actual solution gives us a linear equation to represent the relationship between the size (in square feet) of the installation and the total cost (first year operations), as required by the problem.

Now, let's compare this with the student's solution:
The student has correctly identified that the cost of the land depends on its size (linear relation), and the solar panels also depend on their size. They are using "x" to represent the area of the installation, which is a good choice since the size (or area) of the solar installation affects the cost of everything else involved.
However, in the next step, the student uses the notation "$$450x+$100,000=\text{total}\\cost,$" without explaining what each term signifies. Although we know that '$450x+$100,000=$\text{total}\\cost,$' means, there isn't enough information provided to understand what each term signifies exactly. It could still be confusing for someone who doesn't already understand the problem context. Moreover, the student should explain how the final formula represents the relationship between the various components of the total c
~~~

### Model Limitations: 幻觉（Hallucinations）

都是胡说八道啊。

Hallucination： Makes statements that sound plausible but are not true.

Reducing Hallucinations:

First find relevant information, then answer the question based on the relevant information. 

- Boie is a real company, the product name is not real.

~~~python
prompt = f"""
Tell me about AeroGlide UltraSlim Smart Toothbrush by Boie
"""
print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

#### ChatGPT 3.5
~~~
Tell me about AeroGlide UltraSlim Smart Toothbrush by Boie

--------------------------------------------------
The AeroGlide UltraSlim Smart Toothbrush by Boie is a high-tech toothbrush that uses advanced sonic technology to provide a deep and thorough clean. It features a slim and sleek design that makes it easy to hold and maneuver, and it comes with a range of smart features that help you optimize your brushing routine.

One of the key features of the AeroGlide UltraSlim Smart Toothbrush is its advanced sonic technology, which uses high-frequency vibrations to break up plaque and bacteria on your teeth and gums. This technology is highly effective at removing even the toughest stains and buildup, leaving your teeth feeling clean and fresh.

In addition to its sonic technology, the AeroGlide UltraSlim Smart Toothbrush also comes with a range of smart features that help you optimize your brushing routine. These include a built-in timer that ensures you brush for the recommended two minutes, as well as a pressure sensor that alerts you if you're brushing too hard.

Overall, the AeroGlide UltraSlim Smart Toothbrush by Boie is a highly advanced and effective toothbrush that is perfect for anyone looking to take their oral hygiene to the next level. With its advanced sonic technology and smart features, it provides a deep and thorough clean that leaves your teeth feeling fresh and healthy.
~~~
#### New Bing
~~~
The AeroGlide UltraSlim Smart Toothbrush by Boie is a rubber-like toothbrush that cleans more effectively and gently than traditional brushes. The bristles have silver embedded in them to prevent bacteria growth. The toothbrush is recyclable and made from the same long-lasting, antimicrobial material1.

Here is a link to Boie USA’s website where you can find more information about the toothbrush.
~~~
#### Claude
~~~
Here are the key details about the AeroGlide UltraSlim Smart Toothbrush by Boie:
• It is an electric toothbrush that comes with a smart app to help track your brushing. The app provides real-time guidance on brushing time and technique to help improve your oral care routine.
• It has an ultraslim design with soft bristles for a gentle brushing experience. The slim profile allows for easier access to hard-to-reach areas of your mouth.
• It operates at 40,000 high-speed bristle motions per minute to effectively remove plaque. The fast sonic vibrations break up plaque and sweep it away.
• It has 5 brushing modes - Bright Clean, Soft Clean, Massage, Sensitive, and White. You can choose a different mode based on your needs and for a customized brushing experience.
• The battery lasts up to 3 weeks on a single charge. It takes about 24 hours to fully recharge. A charging stand is included.
• It has a built-in quadpacer to ensure even brushing of all areas of your mouth. The quadpacer beeps to remind you to brush the 4 sections of your mouth.
• It is waterproof so you can use it in the shower if desired. The charger is not waterproof though so you have to take normal precautions. 
• It comes with a USB charger in the box. Optional wall charger can be purchased separately.
• 1-year warranty from the date of purchase. Replace brush heads every 3 months for the best results.
• It works with a range of replacement brush heads so you have the flexibility to choose different bristle types. Softer bristles for sensitive gums or more advanced bristles for complete cleaning.
That covers the key highlights about the AeroGlide UltraSlim Smart Toothbrush. Let me know if you need any additional details.
~~~
#### HuggingChat
~~~
The AeroGlide UltraSlim Smart Toothbrush is an electric toothbrush designed by Boie USA LLC. This sleek and modern brush provides advanced sonic technology combined with a unique slim design to provide users with an effective and comfortable cleaning experience.
It features ultra thin bristles that slide easily between teeth, making it easy to reach those hard-to-reach areas while avoiding gum irritation. Its compact size makes it easy to carry around while traveling, and it even includes a carrying case and charging stand for added convenience.
Additionally, the AeroGlide Smart brush connects via Bluetooth with your phone app so you can monitor your brushing habits, set reminders, track goals, and more. All of these features make the AeroGlide UltraSlim Smart Toothbrush perfect for anyone looking for a high quality, convenient and easy-to-use toothbrush.
This smart toothbrush includes two modes - Clean mode(standard setting) and Sensitive Mode(Less vibration frequency than normal) , both last 2 minutes like any other Sonic Electric Toothbrush brand available .The handle feels premium, has led light ring near the bottom that indicates when the unit is turned ON and charge status.
It does include brush head replacement pack but the package don't indicate whether they are soft bristle(white color), medium bristle(pink color) and Hard Bristle(blue color). It is worth mentioning though that Boie recommends Soft White bristle for most people, Medium Pink Bristle for sensitive teeth and Blue Bristle for whitening effect only. Replacement Heads cost $9.97 per pack on Amazon

Overall it is considered one of best value Sonic electric toothbrushes that has positive customer reviews and feedback regarding its performance, ease of use, build Quality and affordability.
Please note that i am not affiliated nor endorsed by BOIE company. And my knowledge cut off date is 2021-09
Please check the latest updates from official sources before purchasing anything online.
~~~

# Iterative Prompt Development

 you'll iteratively analyze and refine your prompts to generate marketing copy from a product fact sheet.

![image-20230506171849870](images/image-20230506171849870.png)

## Setup

~~~python
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
~~~

## Generate a marketing product description from a product fact sheet

原始的Prompt产生的内容有不少问题，下面会逐步尝试改进。

~~~python
fact_sheet_chair = """
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
"""

prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

Technical specifications: ```{fact_sheet_chair}```
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

### ChatGPT 3.5
~~~
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

Technical specifications: ```
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
```

--------------------------------------------------
Introducing our stunning mid-century inspired office chair, the perfect addition to any home or business setting. Part of a beautiful family of office furniture, including filing cabinets, desks, bookcases, meeting tables, and more, this chair is available in several options of shell color and base finishes to suit your style. Choose from plastic back and front upholstery (SWC-100) or full upholstery (SWC-110) in 10 fabric and 6 leather options.

The chair is constructed with a 5-wheel plastic coated aluminum base and features a pneumatic chair adjust for easy raise/lower action. It is available with or without armrests and comes with soft or hard-floor caster options. You can also choose between two seat foam densities: medium (1.8 lb/ft3) or high (2.8 lb/ft3).

The chair is made with high-quality materials, including a cast aluminum shell with modified nylon PA6/PA66 coating and a 10mm shell thickness. The seat is made with HD36 foam for ultimate comfort.

With a width of 53cm, depth of 51cm, and height of 80cm, this chair is the perfect size for any workspace. The seat height is 44cm and the seat depth is 41cm.

Choose from base finish options of stainless steel, matte black, gloss white, or chrome to complete the look. This chair is qualified for contract use and proudly made in Italy. Upgrade your workspace with our stylish and comfortable mid-century inspired office chair.
~~~
### New Bing
~~~
Introducing the mid-century inspired office chair that is perfect for both home and business settings. This chair is part of a beautiful family of mid-century inspired office furniture that includes filing cabinets, desks, bookcases, meeting tables, and more. The chair comes in several options of shell color and base finishes to fit your style. You can choose between plastic back and front upholstery (SWC-100) or full upholstery (SWC-110) in 10 fabric and 6 leather options. The base finish options are stainless steel, matte black, gloss white, or chrome. The chair is available with or without armrests.

The chair is constructed with a 5-wheel plastic coated aluminum base and has a pneumatic chair adjust for easy raise/lower action. It is qualified for contract use.

The dimensions of the chair are as follows:

Width: 53 cm | 20.87”
Depth: 51 cm | 20.08”
Height: 80 cm | 31.50”
Seat height: 44 cm | 17.32”
Seat depth: 41 cm | 16.14”
You can choose between soft or hard-floor caster options and two choices of seat foam densities: medium (1.8 lb/ft3) or high (2.8 lb/ft3). You can also choose between armless or 8 position PU armrests.

The materials used in the construction of the chair are:

Shell base glider: Cast Aluminum with modified nylon PA6/PA66 coating. Shell thickness: 10 mm.
Seat: HD36 foam
This chair is made in Italy.
~~~
### Claude
~~~
Introducing the mid-century inspired office chair that is perfect for both home and business settings. This chair is part of a beautiful family of mid-century inspired office furniture that includes filing cabinets, desks, bookcases, meeting tables, and more. The chair comes in several options of shell color and base finishes to fit your style. You can choose between plastic back and front upholstery (SWC-100) or full upholstery (SWC-110) in 10 fabric and 6 leather options. The base finish options are stainless steel, matte black, gloss white, or chrome. The chair is available with or without armrests.

The chair is constructed with a 5-wheel plastic coated aluminum base and has a pneumatic chair adjust for easy raise/lower action. It is qualified for contract use.

The dimensions of the chair are as follows:

Width: 53 cm | 20.87”
Depth: 51 cm | 20.08”
Height: 80 cm | 31.50”
Seat height: 44 cm | 17.32”
Seat depth: 41 cm | 16.14”
You can choose between soft or hard-floor caster options and two choices of seat foam densities: medium (1.8 lb/ft3) or high (2.8 lb/ft3). You can also choose between armless or 8 position PU armrests.

The materials used in the construction of the chair are:

Shell base glider: Cast Aluminum with modified nylon PA6/PA66 coating. Shell thickness: 10 mm.
Seat: HD36 foam
This chair is made in Italy.
~~~
### HuggingChat
~~~
Welcome to our collection of stylish and functional mid-century inspired office furniture! Our Swivel Task Chair is part of this beautiful family that also includes filing cabinets, desks, bookcases, and meeting tables. With several options for the shell color and base finishes, as well as different upholsteries, including fabrics and leathers, we offer versatility and customization to fit any workspace or personal style.

Constructed with durability in mind, our Swivel Task Chair boasts a five-star plastic coated aluminum base and a pneumatic adjustment feature to ensure user comfort. Easy raising and lowering action allows individuals to find their ideal height seamlessly.

With dimensions suitable for any work environment, the Swivel Task Chair measures 20.87 inches wide x 20.08 inches deep x 31.50 inches tall and comes standard with a 17.32-inch seat height and 16.14-inch seat depth. Users have the option of selecting either soft or hard floor casters depending on flooring needs. For additional comfort, choose from two types of seat foam density: medium (1.8 lb/ft3) or high (2.8 lb/ft3). Lastly, select from armless or eight-position polyurethane arms.

Made from cast aluminum with a modified nylon coating and featuring a 10mm thick shell, coupled with High Density 36 foam for maximum support and durability. Proudly made in Italy, each piece undergoes rigorous testing ensuring quality control meets safety standards.

Whether you need a chair for your home office or want to refresh the look of your professional space, our Swivel Task Chair will add sophistication and functionality to any room it graces. Try yours today!
~~~

## Issue 1: The text is too long

~~~python
prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

Use at most 50 words.

Technical specifications: ```{fact_sheet_chair}```
"""
print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
print(len(response.split()))
~~~

### ChatGPT 3.5
~~~
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

Use at most 50 words.

Technical specifications: ```
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
```

--------------------------------------------------
Introducing our mid-century inspired office chair, part of a beautiful furniture family. Available in various shell colors and base finishes, with plastic or full upholstery options in fabric or leather. Suitable for home or business use, with a 5-wheel base and pneumatic chair adjust. Made in Italy.
47
~~~
上面是47个words。

### New Bing

72个words，超过了很多。

~~~
Introducing the mid-century inspired office chair. Available in several shell colors and base finishes, with or without armrests. The chair is suitable for home or business settings and is qualified for contract use. The chair is constructed with a 5-wheel plastic coated aluminum base and features a pneumatic chair adjust for easy raise/lower action. Dimensions: W53 x D51 x H80 cm. Seat height 44 cm. Seat depth 41 cm. Made in Italy.
~~~
### Claude

53个words，不错。

~~~
This sleek yet fully customizable office chair offers style and comfort. Part of a mid-century modern collection, choose a colorful shell and base like stainless steel or chrome, then add armrests and leather or fabric upholstery. Built in Italy, it has commercial-grade aluminum and foam, pneumatic height adjustment, and 5 casters for mobility.
~~~
### HuggingChat

125个words，超过了很多。

~~~
Introducing the swanky new addition to your office - the Swivel Task Chair! This sleek beauty belongs to an exquisite line of mid-century inspired office furniture that'll spruce up any setting. Choose between multiple shell colors and base finishes, along with various upholstery options like fabrics and leathers. The plastic-coated aluminum five-star base promises ultimate durability while its pneumatic mechanism provides effortless adjustments. Customize it further with optional soft or hard casters, seat foam densities, and armrest styles crafted to fit your preferences. Made of robust materials like cast aluminum and high-density foam, each piece is manufactured in Italy and undergoes thorough quality checks to guarantee customer satisfaction. Perfect for both residential and commercial spaces, experience unparalleled comfort and elegance with our Swivel Task Chair.
~~~

## Issue 2. Text focuses on the wrong details

~~~python
prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

The description is intended for furniture retailers, 
so should be technical in nature and focus on the 
materials the product is constructed from.

Use at most 50 words.

Technical specifications: ```{fact_sheet_chair}```
"""
print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

### ChatGPT 3.5
~~~
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

The description is intended for furniture retailers, 
so should be technical in nature and focus on the 
materials the product is constructed from.

Use at most 50 words.

Technical specifications: ```
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
```

--------------------------------------------------
Introducing our mid-century inspired office chair, perfect for both home and business settings. With a range of shell colors and base finishes, including stainless steel and matte black, this chair is available with or without armrests. The 5-wheel plastic coated aluminum base and pneumatic chair adjust make it easy to raise and lower. Made in Italy with a cast aluminum shell and HD36 foam seat.
~~~
### New Bing
~~~
Introducing the mid-century inspired office chair. Constructed with a cast aluminum shell and base glider with modified nylon PA6/PA66 coating. The seat is made of HD36 foam. Available in several shell colors and base finishes, with or without armrests. Suitable for home or business settings and qualified for contract use. Made in Italy.
~~~
### Claude
~~~
This contract-grade office chair has an aluminum shell with nylon coating and a 5-wheel coated aluminum base; medium or high density foam seat; armless or upholstered armrest options; and pneumatic height adjustment. 
~~~
### HuggingChat
~~~
Experience luxury in design with our Mid-Century Inspired Office Chair Collection. Each piece features plastic coated aluminum bases and is qualified for contract use. Enjoy personalized comfort with options including different shell colors, base finishes, upholstery types, and armrest styles. Rest assured knowing this collection is built tough with durable materials such as cast aluminum, high-density foam, and modified nylons made in Italy. With so many customization possibilities, find exactly what suits your space best today.
~~~

### Add one more limit

~~~
At the end of the description, include every 7-character Product ID in the technical specification.
~~~

~~~python
prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

The description is intended for furniture retailers, 
so should be technical in nature and focus on the 
materials the product is constructed from.

At the end of the description, include every 7-character 
Product ID in the technical specification.

Use at most 50 words.

Technical specifications: ```{fact_sheet_chair}```
"""
print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

#### ChatGPT 3.5
~~~
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

The description is intended for furniture retailers, 
so should be technical in nature and focus on the 
materials the product is constructed from.

At the end of the description, include every 7-character 
Product ID in the technical specification.

Use at most 50 words.

Technical specifications: ```
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
```

--------------------------------------------------
Introducing our mid-century inspired office chair, perfect for home or business settings. With a range of shell colors and base finishes, and the option of plastic or full upholstery, this chair is both stylish and comfortable. Constructed with a 5-wheel plastic coated aluminum base and pneumatic chair adjust, it's also practical. Available with or without armrests and suitable for contract use. Product ID: SWC-100, SWC-110.
~~~
#### New Bing
~~~
Introducing the mid-century inspired office chair. Constructed with a cast aluminum shell and base glider with modified nylon PA6/PA66 coating. The seat is made of HD36 foam. Available in several shell colors and base finishes, with or without armrests. Suitable for home or business settings and qualified for contract use. Made in Italy.

Product ID: SWC-100, SWC-110
~~~
#### Claude
~~~
This office chair has an aluminum shell coated in PA6/PA66 nylon and HD36 foam seat.  Its SWC-100 or SWC-110 upholstery, 5-wheel coated PA6/PA66 aluminum base with pneumatic height adjustment,  and  armless or PU armrest options offer customizable comfort. PA6/PA66 SWC-100SWC-110HD36
~~~
#### HuggingChat
~~~
"Introducing our elegant yet durable Task Chair, perfect for any workspace. The sleek design features a cast aluminum base coated with modified nylon paired with soft or hard floor casters for stability. Adjust your desired height with ease using the pneumatic feature and choose between two density options for seat comfort. This versatile piece has an array of upholstery options allowing you to pick the style that fits perfectly in your space. Our Task Chair proudly meets all qualifications required for contract use, making it suitable for both homes and commercial spaces. Made in Italy. Product ID: [insert 7 character Product ID here]."
~~~

## Issue 3. Description needs a table of dimensions

- Ask it to extract information and organize it in a table.

~~~python
prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

The description is intended for furniture retailers, 
so should be technical in nature and focus on the 
materials the product is constructed from.

At the end of the description, include every 7-character 
Product ID in the technical specification.

After the description, include a table that gives the 
product's dimensions. The table should have two columns.
In the first column include the name of the dimension. 
In the second column include the measurements in inches only.

Give the table the title 'Product Dimensions'.

Format everything as HTML that can be used in a website. 
Place the description in a <div> element.

Technical specifications: ```{fact_sheet_chair}```
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

### ChatGPT 3.5
~~~

Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

The description is intended for furniture retailers, 
so should be technical in nature and focus on the 
materials the product is constructed from.

At the end of the description, include every 7-character 
Product ID in the technical specification.

After the description, include a table that gives the 
product's dimensions. The table should have two columns.
In the first column include the name of the dimension. 
In the second column include the measurements in inches only.

Give the table the title 'Product Dimensions'.

Format everything as HTML that can be used in a website. 
Place the description in a <div> element.

Technical specifications: ```
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
```

--------------------------------------------------
<div>
<h2>Mid-Century Inspired Office Chair</h2>
<p>Introducing our mid-century inspired office chair, part of a beautiful family of office furniture that includes filing cabinets, desks, bookcases, meeting tables, and more. This chair is available in several options of shell color and base finishes, allowing you to customize it to your liking. You can choose between plastic back and front upholstery or full upholstery in 10 fabric and 6 leather options. The base finish options are stainless steel, matte black, gloss white, or chrome. The chair is also available with or without armrests, making it suitable for both home and business settings. Plus, it's qualified for contract use, so you can trust its durability and quality.</p>
<h3>Construction</h3>
<p>The chair features a 5-wheel plastic coated aluminum base and a pneumatic chair adjust for easy raise/lower action. You can choose between soft or hard-floor caster options and two choices of seat foam densities: medium (1.8 lb/ft3) or high (2.8 lb/ft3). The chair is also available with armless or 8 position PU armrests.</p>
<h3>Materials</h3>
<p>The shell base glider is made of cast aluminum with modified nylon PA6/PA66 coating, and the shell thickness is 10 mm. The seat is made of HD36 foam, ensuring comfort and support.</p>
<h3>Product Dimensions</h3>
<table>
  <tr>
    <td>Width</td>
    <td>53 cm | 20.87"</td>
  </tr>
  <tr>
    <td>Depth</td>
    <td>51 cm | 20.08"</td>
  </tr>
  <tr>
    <td>Height</td>
    <td>80 cm | 31.50"</td>
  </tr>
  <tr>
    <td>Seat Height</td>
    <td>44 cm | 17.32"</td>
  </tr>
  <tr>
    <td>Seat Depth</td>
    <td>41 cm | 16.14"</td>
  </tr>
</table>
<h3>Product ID</h3>
<p>SWC-100, SWC-110</p>
</div>
~~~
显示html。

~~~python
from IPython.display import display, HTML

display(HTML(response))
~~~

![image-20230506161358621](images/image-20230506161358621.png)

### New Bing

![image-20230506162739069](images/image-20230506162739069.png)

由于New Bing的限制，不能超过2000个字符。

~~~
Sure! Here’s a product description based on the information provided in the technical specifications:

<div> <p>Part of a beautiful family of mid-century inspired office furniture, including filing cabinets, desks, bookcases, meeting tables, and more. This chair is available with or without armrests and is suitable for home or business settings. It is qualified for contract use. The chair comes in several options of shell color and base finishes. The base finish options are stainless steel, matte black, gloss white, or chrome. The chair is available with plastic back and front upholstery (SWC-100) or full upholstery (SWC-110) in 10 fabric and 6 leather options.</p> <p>The chair has a 5-wheel plastic coated aluminum base and pneumatic chair adjust for easy raise/lower action. It has two choices of seat foam densities: medium (1.8 lb/ft3) or high (2.8 lb/ft3). It also has soft or hard-floor caster options and armless or 8 position PU armrests.</p> <p>The materials used in this chair are:</p> <ul> <li>Shell Base Glider: Cast Aluminum with modified nylon PA6/PA66 coating. Shell thickness: 10 mm.</li> <li>Seat: HD36 foam</li> </ul> </div>

Every 7-character Product ID in the technical specification is SWC-100 and SWC-110.

<table> <caption>Product Dimensions</caption> <tr> <th>Name of Dimension</th> <th>Measurements (inches)</th> </tr> <tr> <td>Width</td> <td>20.87"</td> </tr> <tr> <td>Depth</td> <td>20.08"</td> </tr> <tr> <td>Height</td> <td>31.50"</td> </tr> <tr> <td>Seat Height</td> <td>17.32"</td> </tr> <tr> <td>Seat Depth</td> <td>16.14"</td> </tr> </table>

I hope this helps! Let me know if you have any other questions.
~~~
### Claude
~~~
This office chair has an aluminum shell coated in PA6/PA66 nylon and HD36 foam seat. 
Its SWC-100 or SWC-110 upholstery, 5-wheel coated PA6/PA66 aluminum base with pneumatic height adjustment, 
and  armless or PU armrest options offer customizable comfort.
PA6/PA66 SWC-100SWC-110HD36
</div>
<table title="Product Dimensions">
<tr><td>Width</td><td>20.87 in</td></tr> 
<tr><td>Depth</td><td>20.08 in</td></tr>
<tr><td>Height</td><td>31.50 in</td></tr>
<tr><td>Seat Height</td><td>17.32 in</td></tr>
<tr><td>Seat Depth</td><td>16.14 in </td></tr>
</table>
~~~
显示html。

~~~python
from IPython.display import display, HTML
response = """
<div>
This office chair has an aluminum shell coated in PA6/PA66 nylon and HD36 foam seat. 
Its SWC-100 or SWC-110 upholstery, 5-wheel coated PA6/PA66 aluminum base with pneumatic height adjustment, 
and  armless or PU armrest options offer customizable comfort.
PA6/PA66 SWC-100SWC-110HD36
</div>
<table title="Product Dimensions">
<tr><td>Width</td><td>20.87 in</td></tr> 
<tr><td>Depth</td><td>20.08 in</td></tr>
<tr><td>Height</td><td>31.50 in</td></tr>
<tr><td>Seat Height</td><td>17.32 in</td></tr>
<tr><td>Seat Depth</td><td>16.14 in </td></tr>
</table>
"""
display(HTML(response))
~~~



![image-20230506161438124](images/image-20230506161438124.png)

### HuggingChat

结果差的比较多。

~~~
<div class="product-description">
<h2><strong>Task Chair</strong></h2>
<p>Add style and functionality to any workspace with our Task Chair.</p>
<ul>
<li><strong>Part of a Beautiful Family:</strong> Including filing cabinets, desks, bookcases, meeting tables, and more</li>
<li><strong>Available Options: </strong>Plastic back and front upholstery (SWC-100) or Full Upholstery (SWC-110) with several options of shell color, base finishes and upholstery materials (fabric & Leather). With Armrests optional.</li>
<li><strong>Base Finish Options:</strong> Stainless Steel, Matte Black, Gloss White, Chrome</li>
<li><strong>Contract Use Certification:</strong> Complies with North American Contract Furniture requirements</li>
</ul>
<table id="productDim" width="100%" border="1" cellpadding="5">
<tr >
<th>Dimension Name</th>
<th>Measurements (inches)</th>
</tr>
<tr>
<td>Width</td>
<td>20.87</td>
</tr>
<tr>
<td>Depth</td>
<td>20.08</td>
</tr>
<tr>
<td>Height</td>
<td>31.50</td>
</tr>
<tr>
<td>Seat Height</td>
<td>17.32</td>
</tr>
<tr>
<td>Seat Depth</td>
<td>16.14</td>
</tr>
<tr>
<td colspan="2"><center>PRODUCT DIMENSIONS TITLE</center></td>
</tr>
</table>
<p> </p>
<p>Please see our Technical Specification document included within this package for complete details including Product Dimensions, Material Information, Country of Origin and Additional Features.
~~~

# Summarizing

you will summarize text with a focus on specific topics.

## Setup

~~~python
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
~~~

## Text to summarize

~~~python
prod_review = """
Got this panda plush toy for my daughter's birthday, \
who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
"""

prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words. 

Review: ```{prod_review}```
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

#### ChatGPT 3.5
~~~
Your task is to generate a short summary of a product review from an ecommerce site. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words. 

Review: ```
Got this panda plush toy for my daughter's birthday, who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
```

--------------------------------------------------
Soft and cute panda plush toy loved by daughter, but a bit small for the price. Arrived early.
~~~
#### New Bing
~~~
Here’s a summary of the review:

A soft and super cute panda plush toy with a friendly look. It’s a bit small for what the user paid though .

I hope this helps!
~~~
#### Claude
~~~
Here is a 29 word summary of the review:
Soft, cute plush panda toy arrived quickly; daughter loves it though pricey for small size; bigger options may have same cost. 
~~~
#### HuggingChat

好像完全失败了。

~~~
Great job summarizing the review above! I hope you found my suggestions helpful. Is there anything else I can assist you with today?
~~~

## Summarize with a focus on shipping and delivery

~~~python
prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site to give feedback to the \
Shipping deparmtment. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words, and focusing on any aspects \
that mention shipping and delivery of the product. 

Review: ```{prod_review}```
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)

~~~

### ChatGPT 3.5
~~~
Your task is to generate a short summary of a product review from an ecommerce site to give feedback to the Shipping deparmtment. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words, and focusing on any aspects that mention shipping and delivery of the product. 

Review: ```
Got this panda plush toy for my daughter's birthday, who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
```

--------------------------------------------------
The panda plush toy arrived a day earlier than expected, but the customer felt it was a bit small for the price paid.
~~~
### New Bing
~~~
Here’s a summary of the review focusing on shipping and delivery:

The panda plush toy arrived a day earlier than expected .

I hope this helps!
~~~
### Claude

好像并不准确

~~~
Here is a 30 word summary focusing on shipping for the feedback:
Product arrived promptly ahead of schedule allowing preview before gift; rapid delivery exceeded expectations delighting recipient with early present surprise. (edited) 
~~~
### HuggingChat
~~~
Here's a summary focused on shipping/delivery:

Received item early (1 day sooner) which was a pleasant surprise; overall positive experience with fast delivery.
~~~

## Summarize with a focus on price and value

~~~python
prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site to give feedback to the \
pricing deparmtment, responsible for determining the \
price of the product.  

Summarize the review below, delimited by triple 
backticks, in at most 30 words, and focusing on any aspects \
that are relevant to the price and perceived value. 

Review: ```{prod_review}```
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
### ChatGPT 3.5

Comment[¶](https://s172-31-9-147p37381.lab-aws-production.deeplearning.ai/notebooks/l4-summarizing.ipynb#Comment)

- Summaries include topics that are not related to the topic of focus

~~~
Your task is to generate a short summary of a product review from an ecommerce site to give feedback to the pricing deparmtment, responsible for determining the price of the product.  

Summarize the review below, delimited by triple 
backticks, in at most 30 words, and focusing on any aspects that are relevant to the price and perceived value. 

Review: ```
Got this panda plush toy for my daughter's birthday, who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
```

--------------------------------------------------
The panda plush toy is soft, cute, and loved by the recipient, but the price may be too high for its size.
~~~
### New Bing
~~~
Here’s a summary of the review focusing on price and perceived value:

The panda plush toy is soft and super cute, but a bit small for what the user paid. They think there might be other options that are bigger for the same price.

I hope this helps!
~~~
### Claude
~~~
Here is a 30 word summary focusing on pricing for the feedback: 
Adorable plush panda delighted recipient though diminutive size disproportionate to cost; competing alternatives potentially offer superior value at equivalent price point.
~~~
### HuggingChat
~~~
Summary: Thought product was too expensive considering size; liked free delivery & loved how cute it looked. Overall satisfied but could offer better value given price point.
~~~

## Try "extract" instead of "summarize"

~~~python
prompt = f"""
Your task is to extract relevant information from \ 
a product review from an ecommerce site to give \
feedback to the Shipping department. 

From the review below, delimited by triple quotes \
extract the information relevant to shipping and \ 
delivery. Limit to 30 words. 

Review: ```{prod_review}```
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
### ChatGPT 3.5
~~~
Your task is to extract relevant information from \ 
a product review from an ecommerce site to give feedback to the Shipping department. 

From the review below, delimited by triple quotes extract the information relevant to shipping and \ 
delivery. Limit to 30 words. 

Review: ```
Got this panda plush toy for my daughter's birthday, who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
```

--------------------------------------------------
The product arrived a day earlier than expected.
~~~
### New Bing
~~~
Here’s the information relevant to shipping and delivery:

The panda plush toy arrived a day earlier than expected.

I hope this helps!
~~~
### Claude
~~~
Here is the relevant shipping information in 30 words:
Product shipped rapidly, arriving ahead of anticipated delivery date, allowing preview before gifting; speedy fulfillment and expedited transit exceeded customer expectations, enabling early present surprise.
~~~
### HuggingChat
~~~
Arrived one day earlier than expected; great customer service.
~~~

## Summarize multiple product reviews

~~~python
review_1 = prod_review 

# review for a standing lamp
review_2 = """
Needed a nice lamp for my bedroom, and this one \
had additional storage and not too high of a price \
point. Got it fast - arrived in 2 days. The string \
to the lamp broke during the transit and the company \
happily sent over a new one. Came within a few days \
as well. It was easy to put together. Then I had a \
missing part, so I contacted their support and they \
very quickly got me the missing piece! Seems to me \
to be a great company that cares about their customers \
and products. 
"""

# review for an electric toothbrush
review_3 = """
My dental hygienist recommended an electric toothbrush, \
which is why I got this. The battery life seems to be \
pretty impressive so far. After initial charging and \
leaving the charger plugged in for the first week to \
condition the battery, I've unplugged the charger and \
been using it for twice daily brushing for the last \
3 weeks all on the same charge. But the toothbrush head \
is too small. I’ve seen baby toothbrushes bigger than \
this one. I wish the head was bigger with different \
length bristles to get between teeth better because \
this one doesn’t.  Overall if you can get this one \
around the $50 mark, it's a good deal. The manufactuer's \
replacements heads are pretty expensive, but you can \
get generic ones that're more reasonably priced. This \
toothbrush makes me feel like I've been to the dentist \
every day. My teeth feel sparkly clean! 
"""

# review for a blender
review_4 = """
So, they still had the 17 piece system on seasonal \
sale for around $49 in the month of November, about \
half off, but for some reason (call it price gouging) \
around the second week of December the prices all went \
up to about anywhere from between $70-$89 for the same \
system. And the 11 piece system went up around $10 or \
so in price also from the earlier sale price of $29. \
So it looks okay, but if you look at the base, the part \
where the blade locks into place doesn’t look as good \
as in previous editions from a few years ago, but I \
plan to be very gentle with it (example, I crush \
very hard items like beans, ice, rice, etc. in the \ 
blender first then pulverize them in the serving size \
I want in the blender then switch to the whipping \
blade for a finer flour, and use the cross cutting blade \
first when making smoothies, then use the flat blade \
if I need them finer/less pulpy). Special tip when making \
smoothies, finely cut and freeze the fruits and \
vegetables (if using spinach-lightly stew soften the \ 
spinach then freeze until ready for use-and if making \
sorbet, use a small to medium sized food processor) \ 
that you plan to use that way you can avoid adding so \
much ice if at all-when making your smoothie. \
After about a year, the motor was making a funny noise. \
I called customer service but the warranty expired \
already, so I had to buy another one. FYI: The overall \
quality has gone done in these types of products, so \
they are kind of counting on brand recognition and \
consumer loyalty to maintain sales. Got it in about \
two days.
"""

reviews = [review_1, review_2, review_3, review_4]
~~~

~~~python
for i in range(len(reviews)):
    prompt = f"""
    Your task is to generate a short summary of a product \ 
    review from an ecommerce site. 

    Summarize the review below, delimited by triple \
    backticks in at most 20 words. 

    Review: ```{reviews[i]}```
    """
    print(prompt)
    print('-'*50)

for i in range(len(reviews)):
    prompt = f"""
    Your task is to generate a short summary of a product \ 
    review from an ecommerce site. 

    Summarize the review below, delimited by triple \
    backticks in at most 20 words. 

    Review: ```{reviews[i]}```
    """
    print('-'*50)
    response = get_completion(prompt)
    print(i, response, "\n")

~~~

### ChatGPT 3.5
~~~

    Your task is to generate a short summary of a product \ 
    review from an ecommerce site. 

    Summarize the review below, delimited by triple     backticks in at most 20 words. 

    Review: ```
Got this panda plush toy for my daughter's birthday, who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
```
    
--------------------------------------------------

    Your task is to generate a short summary of a product \ 
    review from an ecommerce site. 

    Summarize the review below, delimited by triple     backticks in at most 20 words. 

    Review: ```
Needed a nice lamp for my bedroom, and this one had additional storage and not too high of a price point. Got it fast - arrived in 2 days. The string to the lamp broke during the transit and the company happily sent over a new one. Came within a few days as well. It was easy to put together. Then I had a missing part, so I contacted their support and they very quickly got me the missing piece! Seems to me to be a great company that cares about their customers and products. 
```
    
--------------------------------------------------

    Your task is to generate a short summary of a product \ 
    review from an ecommerce site. 

    Summarize the review below, delimited by triple     backticks in at most 20 words. 

    Review: ```
My dental hygienist recommended an electric toothbrush, which is why I got this. The battery life seems to be pretty impressive so far. After initial charging and leaving the charger plugged in for the first week to condition the battery, I've unplugged the charger and been using it for twice daily brushing for the last 3 weeks all on the same charge. But the toothbrush head is too small. I’ve seen baby toothbrushes bigger than this one. I wish the head was bigger with different length bristles to get between teeth better because this one doesn’t.  Overall if you can get this one around the $50 mark, it's a good deal. The manufactuer's replacements heads are pretty expensive, but you can get generic ones that're more reasonably priced. This toothbrush makes me feel like I've been to the dentist every day. My teeth feel sparkly clean! 
```
    
--------------------------------------------------

    Your task is to generate a short summary of a product \ 
    review from an ecommerce site. 

    Summarize the review below, delimited by triple     backticks in at most 20 words. 

    Review: ```
So, they still had the 17 piece system on seasonal sale for around $49 in the month of November, about half off, but for some reason (call it price gouging) around the second week of December the prices all went up to about anywhere from between $70-$89 for the same system. And the 11 piece system went up around $10 or so in price also from the earlier sale price of $29. So it looks okay, but if you look at the base, the part where the blade locks into place doesn’t look as good as in previous editions from a few years ago, but I plan to be very gentle with it (example, I crush very hard items like beans, ice, rice, etc. in the \ 
blender first then pulverize them in the serving size I want in the blender then switch to the whipping blade for a finer flour, and use the cross cutting blade first when making smoothies, then use the flat blade if I need them finer/less pulpy). Special tip when making smoothies, finely cut and freeze the fruits and vegetables (if using spinach-lightly stew soften the \ 
spinach then freeze until ready for use-and if making sorbet, use a small to medium sized food processor) \ 
that you plan to use that way you can avoid adding so much ice if at all-when making your smoothie. After about a year, the motor was making a funny noise. I called customer service but the warranty expired already, so I had to buy another one. FYI: The overall quality has gone done in these types of products, so they are kind of counting on brand recognition and consumer loyalty to maintain sales. Got it in about two days.
```
    
--------------------------------------------------
--------------------------------------------------
0 Soft and cute panda plush toy loved by daughter, but a bit small for the price. Arrived early. 

--------------------------------------------------
1 Affordable lamp with storage, fast shipping, and excellent customer service. Easy to assemble and missing parts were quickly replaced. 

--------------------------------------------------
2 Good battery life, small toothbrush head, but effective cleaning. Good deal if bought around $50. 

--------------------------------------------------
3 The product was on sale for $49 in November, but the price increased to $70-$89 in December. The base doesn't look as good as previous editions, but the reviewer plans to be gentle with it. A special tip for making smoothies is to freeze the fruits and vegetables beforehand. The motor made a funny noise after a year, and the warranty had expired. Overall quality has decreased. 

~~~
最后一段输出好像有问题，大大超过了20个word。

### New Bing

~~~
Here’s a summary of the review:

Soft and super cute panda plush toy with a friendly look. A bit small for what the user paid.

I hope this helps!
--------------------------------------------------
Here’s a summary of the review:

The lamp has additional storage and is easy to put together. The company cares about their customers and products.

I hope this helps!
--------------------------------------------------
Here’s a summary of the review:

The electric toothbrush has impressive battery life and makes teeth feel sparkly clean. The toothbrush head is too small.

I hope this helps!
--------------------------------------------------
Here’s a summary of the review:

The blender system was on sale for $49 in November but went up to $70-$89 in December. The overall quality has gone down.

I hope this helps!
~~~
### Claude
~~~
Here is a 20 word summary of the review:
Adorable plush panda delighted birthday girl though pricey for petite size; competing alternatives potentially provide superior value. (edited) 
--------------------------------------------------
Here is a 20 word summary of the review:
Affordable lamp with drawers shipped rapidly; responsive company readily resolved transit damage and missing part issues, demonstrating caring customer support. (edited) 
--------------------------------------------------
Here is a 20 word summary of the review: 
Recommended electric toothbrush underwhelms with diminutive head though impressive battery yields dentist-clean feel if affordable generic replacements obtained. (edited) 
--------------------------------------------------
Here is a 20 word summary of the review: 
Sale-priced blender initially impressed but base quality declined; motor failed prematurely though rapid delivery and tips provided some value. 
~~~
### HuggingChat
~~~
Positive review about product softness and cuteness, slight issue with smaller size for cost; praised free and timely delivery.
--------------------------------------------------
Product received, issues resolved efficiently through good customer service. Timely arrival, affordable yet reliable quality, would recommend.
--------------------------------------------------
Battery life commendable, however toothbrush head is undersized; otherwise excellent experience overall, affordable replacement heads available. Recommended for exceptionally clean teeth sensation.
--------------------------------------------------
Price inconsistencies noted, product appears decent. Tips provided for usage and longevity improvement, expect durability decline in recent models.
~~~

# Inferring

you will infer sentiment and topics from product reviews and news articles

## Setup

~~~python
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
~~~

## Product review text

~~~python
lamp_review = """
Needed a nice lamp for my bedroom, and this one had \
additional storage and not too high of a price point. \
Got it fast.  The string to our lamp broke during the \
transit and the company happily sent over a new one. \
Came within a few days as well. It was easy to put \
together.  I had a missing part, so I contacted their \
support and they very quickly got me the missing piece! \
Lumina seems to me to be a great company that cares \
about their customers and products!!
"""
~~~

## Sentiment (positive/negative)

~~~python
prompt = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Review text: '''{lamp_review}'''
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~

### ChatGPT 3.5
~~~
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Review text: '''
Needed a nice lamp for my bedroom, and this one had additional storage and not too high of a price point. Got it fast.  The string to our lamp broke during the transit and the company happily sent over a new one. Came within a few days as well. It was easy to put together.  I had a missing part, so I contacted their support and they very quickly got me the missing piece! Lumina seems to me to be a great company that cares about their customers and products!!
'''

--------------------------------------------------
The sentiment of the product review is positive.
~~~
### New Bing

完全错误了。

~~~
Sentiment analysis is the process of breaking down text into components, identifying each component, assigning a sentiment score to each component, and combining scores for a final sentiment analysis. Sentiment analysis classifies text data as positive, negative, or neutral. It relies on customer review data to understand how consumers feel about a company or product. Sentiment analysis can be used to automatically analyze product reviews and separate them into tags: Positive, Neutral, Negative 1.

Based on the review you provided, it seems that the sentiment is positive.

If you’re interested in performing sentiment analysis on product reviews using Python, you can check out these resources:

Amazon Product Reviews Sentiment Analysis with Python
Amazon Product Reviews Sentiment Analysis in Python
Sentiment Analysis: First Steps With Python’s NLTK Library
I hope this helps!
~~~
### Claude
~~~
The sentiment of this product review is positive.
~~~
### HuggingChat

比较啰嗦

~~~
Positive sentiment expressed towards the product and its features. Customer experiences with customer service were satisfactory, indicating a positive relationship between the company and its customers. Impression formed of company being "great" due to good care of customers and products.
~~~

## Sentiment (positive/negative) - One Word

~~~python
prompt = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Give your answer as a single word, either "positive" \
or "negative".

Review text: '''{lamp_review}'''
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
### ChatGPT 3.5
~~~
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Give your answer as a single word, either "positive" or "negative".

Review text: '''
Needed a nice lamp for my bedroom, and this one had additional storage and not too high of a price point. Got it fast.  The string to our lamp broke during the transit and the company happily sent over a new one. Came within a few days as well. It was easy to put together.  I had a missing part, so I contacted their support and they very quickly got me the missing piece! Lumina seems to me to be a great company that cares about their customers and products!!
'''

--------------------------------------------------
positive
~~~
### New Bing

问题很大。

~~~
Sentiment analysis is the process of breaking down text into components, identifying each component, assigning a sentiment score to each component, and combining scores for a final sentiment analysis. Sentiment analysis classifies text data as positive, negative, or neutral. It relies on customer review data to understand how consumers feel about a company or product. Sentiment analysis can be used to automatically analyze product reviews and separate them into tags: Positive, Neutral, Negative 1.

Based on the review you provided, it seems that the sentiment is positive.

I hope this helps!
~~~
### Claude
~~~
positive
~~~
### HuggingChat
~~~
positive
~~~

## Identify types of emotions

~~~python
prompt = f"""
Identify a list of emotions that the writer of the \
following review is expressing. Include no more than \
five items in the list. Format your answer as a list of \
lower-case words separated by commas.

Review text: '''{lamp_review}'''
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
### ChatGPT 3.5
~~~
Identify a list of emotions that the writer of the following review is expressing. Include no more than five items in the list. Format your answer as a list of lower-case words separated by commas.

Review text: '''
Needed a nice lamp for my bedroom, and this one had additional storage and not too high of a price point. Got it fast.  The string to our lamp broke during the transit and the company happily sent over a new one. Came within a few days as well. It was easy to put together.  I had a missing part, so I contacted their support and they very quickly got me the missing piece! Lumina seems to me to be a great company that cares about their customers and products!!
'''

--------------------------------------------------
happy, satisfied, grateful, impressed, content
~~~
### New Bing
~~~
The writer of the review seems to be expressing the following emotions:

Happy
Satisfied
Grateful
I hope this helps!
~~~
### Claude
~~~
relieved, grateful, appreciative, impressed, delighted
~~~
### HuggingChat
~~~
[contentment, satisfaction, appreciation, pleasure, happiness]
~~~

## Identify anger

~~~python
prompt = f"""
Is the writer of the following review expressing anger?\
The review is delimited with triple backticks. \
Give your answer as either yes or no.

Review text: '''{lamp_review}'''
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
### ChatGPT 3.5
~~~
Is the writer of the following review expressing anger?The review is delimited with triple backticks. Give your answer as either yes or no.

Review text: '''
Needed a nice lamp for my bedroom, and this one had additional storage and not too high of a price point. Got it fast.  The string to our lamp broke during the transit and the company happily sent over a new one. Came within a few days as well. It was easy to put together.  I had a missing part, so I contacted their support and they very quickly got me the missing piece! Lumina seems to me to be a great company that cares about their customers and products!!
'''

--------------------------------------------------
No
~~~
### New Bing
~~~
No, the writer of the review is not expressing anger. The writer is expressing satisfaction with the company and their products. They had a good experience with the company’s customer service and were happy with how quickly their issues were resolved.
~~~
### Claude
~~~
no
~~~
### HuggingChat
~~~
No
~~~

## Extract product and company name from customer reviews

~~~python
prompt = f"""
Identify the following items from the review text: 
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Item" and "Brand" as the keys. 
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
  
Review text: '''{lamp_review}'''
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
### ChatGPT 3.5
~~~
Identify the following items from the review text: 
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. Format your response as a JSON object with "Item" and "Brand" as the keys. 
If the information isn't present, use "unknown" as the value.
Make your response as short as possible.
  
Review text: '''
Needed a nice lamp for my bedroom, and this one had additional storage and not too high of a price point. Got it fast.  The string to our lamp broke during the transit and the company happily sent over a new one. Came within a few days as well. It was easy to put together.  I had a missing part, so I contacted their support and they very quickly got me the missing piece! Lumina seems to me to be a great company that cares about their customers and products!!
'''

--------------------------------------------------
{
  "Item": "lamp",
  "Brand": "Lumina"
}
~~~
### New Bing
~~~
Here is the information you requested:

{
    "Item": "lamp",
    "Brand": "Lumina"
}
~~~
### Claude
~~~
{"Item": "lamp","Brand": "Lumina"}
~~~
### HuggingChat
~~~
{   
    "item": "lamp",
    "brand": "Lumina"
}
~~~

## Doing multiple tasks at once

~~~python
prompt = f"""
Identify the following items from the review text: 
- Sentiment (positive or negative)
- Is the reviewer expressing anger? (true or false)
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Anger", "Item" and "Brand" as the keys.
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
Format the Anger value as a boolean.

Review text: '''{lamp_review}'''
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
### ChatGPT 3.5
~~~
Identify the following items from the review text: 
- Sentiment (positive or negative)
- Is the reviewer expressing anger? (true or false)
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. Format your response as a JSON object with "Sentiment", "Anger", "Item" and "Brand" as the keys.
If the information isn't present, use "unknown" as the value.
Make your response as short as possible.
Format the Anger value as a boolean.

Review text: '''
Needed a nice lamp for my bedroom, and this one had additional storage and not too high of a price point. Got it fast.  The string to our lamp broke during the transit and the company happily sent over a new one. Came within a few days as well. It was easy to put together.  I had a missing part, so I contacted their support and they very quickly got me the missing piece! Lumina seems to me to be a great company that cares about their customers and products!!
'''

--------------------------------------------------
{
  "Sentiment": "positive",
  "Anger": false,
  "Item": "lamp with additional storage",
  "Brand": "Lumina"
}
~~~
### New Bing
~~~
Here is the information you requested:

{
    "Sentiment": "positive",
    "Anger": false,
    "Item": "lamp",
    "Brand": "Lumina"
}
~~~
### Claude
~~~
{"Sentiment":"positive","Anger":false,"Item":"lamp","Brand":"Lumina"} 
~~~
### HuggingChat
~~~
{"Sentiment":"Positive","Anger":false,"Item":"lamp","Brand":"Lumina"}
~~~

## Inferring topics

~~~python
story = """
In a recent survey conducted by the government, 
public sector employees were asked to rate their level 
of satisfaction with the department they work at. 
The results revealed that NASA was the most popular 
department with a satisfaction rating of 95%.

One NASA employee, John Smith, commented on the findings, 
stating, "I'm not surprised that NASA came out on top. 
It's a great place to work with amazing people and 
incredible opportunities. I'm proud to be a part of 
such an innovative organization."

The results were also welcomed by NASA's management team, 
with Director Tom Johnson stating, "We are thrilled to 
hear that our employees are satisfied with their work at NASA. 
We have a talented and dedicated team who work tirelessly 
to achieve our goals, and it's fantastic to see that their 
hard work is paying off."

The survey also revealed that the 
Social Security Administration had the lowest satisfaction 
rating, with only 45% of employees indicating they were 
satisfied with their job. The government has pledged to 
address the concerns raised by employees in the survey and 
work towards improving job satisfaction across all departments.
"""

prompt = f"""
Determine five topics that are being discussed in the \
following text, which is delimited by triple backticks.

Make each item one or two words long. 

Format your response as a list of items separated by commas.

Text sample: '''{story}'''
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
### ChatGPT 3.5
~~~
Determine five topics that are being discussed in the following text, which is delimited by triple backticks.

Make each item one or two words long. 

Format your response as a list of items separated by commas.

Text sample: '''
In a recent survey conducted by the government, 
public sector employees were asked to rate their level 
of satisfaction with the department they work at. 
The results revealed that NASA was the most popular 
department with a satisfaction rating of 95%.

One NASA employee, John Smith, commented on the findings, 
stating, "I'm not surprised that NASA came out on top. 
It's a great place to work with amazing people and 
incredible opportunities. I'm proud to be a part of 
such an innovative organization."

The results were also welcomed by NASA's management team, 
with Director Tom Johnson stating, "We are thrilled to 
hear that our employees are satisfied with their work at NASA. 
We have a talented and dedicated team who work tirelessly 
to achieve our goals, and it's fantastic to see that their 
hard work is paying off."

The survey also revealed that the 
Social Security Administration had the lowest satisfaction 
rating, with only 45% of employees indicating they were 
satisfied with their job. The government has pledged to 
address the concerns raised by employees in the survey and 
work towards improving job satisfaction across all departments.
'''

--------------------------------------------------
government survey, job satisfaction, NASA, Social Security Administration, employee concerns
~~~
### New Bing
~~~
Here are the five topics being discussed in the text:

Government survey
NASA satisfaction rating
Social Security Administration satisfaction rating
Employee comments on NASA’s rating
NASA management’s response to the rating
The text also mentions the government’s pledge to address employee concerns and improve job satisfaction across all departments.
~~~
### Claude
~~~
survey, NASA, satisfaction, employees, management
~~~
### HuggingChat
~~~
Topics that could be covered in this article include public sector jobs, employee happiness levels, workplace environments, leadership responses, and overall worker satisfaction.
Topic keywords would likely look like this: Public Sector Jobs, Employee Happiness Levels, Workplace Environments, Leadership Responses, Overall Worker Satisfaction
~~~

## Make a news alert for certain topics

~~~python
topic_list = [
    "nasa", "local government", "engineering", 
    "employee satisfaction", "federal government"
]

prompt = f"""
Determine whether each item in the following list of \
topics is a topic in the text below, which
is delimited with triple backticks.

Give your answer as list with 0 or 1 for each topic.\

List of topics: {", ".join(topic_list)}

Text sample: '''{story}'''
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
### ChatGPT 3.5
~~~
Determine whether each item in the following list of topics is a topic in the text below, which
is delimited with triple backticks.

Give your answer as list with 0 or 1 for each topic.
List of topics: nasa, local government, engineering, employee satisfaction, federal government

Text sample: '''
In a recent survey conducted by the government, 
public sector employees were asked to rate their level 
of satisfaction with the department they work at. 
The results revealed that NASA was the most popular 
department with a satisfaction rating of 95%.

One NASA employee, John Smith, commented on the findings, 
stating, "I'm not surprised that NASA came out on top. 
It's a great place to work with amazing people and 
incredible opportunities. I'm proud to be a part of 
such an innovative organization."

The results were also welcomed by NASA's management team, 
with Director Tom Johnson stating, "We are thrilled to 
hear that our employees are satisfied with their work at NASA. 
We have a talented and dedicated team who work tirelessly 
to achieve our goals, and it's fantastic to see that their 
hard work is paying off."

The survey also revealed that the 
Social Security Administration had the lowest satisfaction 
rating, with only 45% of employees indicating they were 
satisfied with their job. The government has pledged to 
address the concerns raised by employees in the survey and 
work towards improving job satisfaction across all departments.
'''

--------------------------------------------------
nasa: 1
local government: 0
engineering: 0
employee satisfaction: 1
federal government: 1
~~~
### New Bing
~~~
[1, 1, 0, 1, 1]
~~~
### Claude
~~~
1
1
0
1
1 
~~~
### HuggingChat
~~~
Output List: [1, 0, 1, 1, 0]
Explanation:

NASA: Yes (Topic appears many times)
Local Government: Not mentioned
Engineering: Unclear/not relevant to text
Employee Satisfaction: Mentioned several times
Federal Government: Appears briefly but does not constitute as main topic.
~~~

# Transforming

we will explore how to use Large Language Models for text transformation tasks such as language translation, spelling and grammar checking, tone adjustment, and format conversion.

## Setup

~~~python
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
~~~

## Translation

### Translate

~~~python
prompt = f"""
Translate the following English text to Spanish: \ 
```Hi, I would like to order a blender```
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
#### ChatGPT 3.5
~~~
Translate the following English text to Spanish: \ 
```Hi, I would like to order a blender```

--------------------------------------------------
Hola, me gustaría ordenar una licuadora.
~~~
#### New Bing
~~~
The Spanish translation of “Hi, I would like to order a blender” is “Hola, me gustaría pedir una licuadora” 1. I hope that helps!
~~~
#### Claude
~~~
Here is the translation of that text to Spanish:
Hola, me gustaría ordenar una licuadora
~~~
#### HuggingChat
~~~
Translate the following English text to Spanish: \ 
```Hi, I would like to order a blender```
~~~
### Language Check
~~~python
prompt = f"""
Tell me which language this is: 
```Combien coûte le lampadaire?```
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
#### ChatGPT 3.5
~~~
Tell me which language this is: 
```Combien coûte le lampadaire?```

--------------------------------------------------
This is French.
~~~
#### New Bing
~~~
The text “Combien coûte le lampadaire?” is in French. It means “How much does the floor lamp cost?”
~~~
#### Claude
~~~
That text is in French. It says:
How much does the lamppost cost?
~~~
#### HuggingChat

错的有点多

~~~
Ceci est une phrase Français qui signifie "Quel est le prix du lampadaire"
~~~

### Translate Form

~~~python
prompt = f"""
Translate the following text to Chinese in both the \
formal and informal forms: 
'Would you like to order a pillow?'
"""

print(prompt)
print('-'*50)
response = get_completion(prompt)
print(response)
~~~
#### ChatGPT 3.5
~~~
Translate the following text to Chinese in both the formal and informal forms: 
'Would you like to order a pillow?'

--------------------------------------------------
Formal: 您需要订购枕头吗？
Informal: 你想订购枕头吗？
~~~
#### New Bing
~~~
The translation of “Would you like to order a pillow?” to Chinese is “您想订购枕头吗?” 1.

To translate this sentence in the formal form, you can say “您想订购枕头吗?” (nín xiǎng dìnggòu zhěntou ma?) 1.

To translate this sentence in the informal form, you can say “你想订购枕头吗?” (nǐ xiǎng dìnggòu zhěntou ma?)
~~~
#### Claude
~~~
Here is the translation of that text to Chinese in formal and informal forms:
Formal: 请问您是否想要订购一个枕头?
Pinyin: Qǐngwèn nín shìfǒu xiǎng yào dìnggòu yīgè zhěntou?
Informal: 你想要买一个枕头吗?
Pinyin: Nǐ xiǎng yào mǎi yīgè zhěntou ma
~~~
#### HuggingChat
~~~
Formal = 你想買一個毛絨嗎？ Informal = 你還需要买一隻毛絨呢？
~~~

### Universal Translator

Imagine you are in charge of IT at a large multinational e-commerce company. Users are messaging you with IT issues in all their native languages. Your staff is from all over the world and speaks only their native languages. You need a universal translator

~~~python
user_messages = [
  "La performance du système est plus lente que d'habitude.",  # System performance is slower than normal         
  "Mi monitor tiene píxeles que no se iluminan.",              # My monitor has pixels that are not lighting
  "Il mio mouse non funziona",                                 # My mouse is not working
  "Mój klawisz Ctrl jest zepsuty",                             # My keyboard has a broken control key
  "我的屏幕在闪烁"                                               # My screen is flashing
] 

for issue in user_messages:
    prompt = f"Tell me what language this is: ```{issue}```"
    print(prompt)
        
    prompt = f"""Translate the following  text to English \
    and Traditional Chinese: ```{issue}```
    """
    
    print(prompt)
    print('-'*50)

for issue in user_messages:
    print('-'*50)
    prompt = f"Tell me what language this is: ```{issue}```"

    lang = get_completion(prompt)
    print(f"Original message ({lang}): {issue}")

    prompt = f"""Translate the following  text to English \
    and Traditional Chinese: ```{issue}```
    """
    response = get_completion(prompt)
    print(response, "\n")
~~~
#### ChatGPT 3.5
~~~
Tell me what language this is: ```La performance du système est plus lente que d'habitude.```
Translate the following  text to English     and Traditional Chinese: ```La performance du système est plus lente que d'habitude.```
    
--------------------------------------------------
Tell me what language this is: ```Mi monitor tiene píxeles que no se iluminan.```
Translate the following  text to English     and Traditional Chinese: ```Mi monitor tiene píxeles que no se iluminan.```
    
--------------------------------------------------
Tell me what language this is: ```Il mio mouse non funziona```
Translate the following  text to English     and Traditional Chinese: ```Il mio mouse non funziona```
    
--------------------------------------------------
Tell me what language this is: ```Mój klawisz Ctrl jest zepsuty```
Translate the following  text to English     and Traditional Chinese: ```Mój klawisz Ctrl jest zepsuty```
    
--------------------------------------------------
Tell me what language this is: ```我的屏幕在闪烁```
Translate the following  text to English     and Traditional Chinese: ```我的屏幕在闪烁```
    
--------------------------------------------------
--------------------------------------------------
Original message (This is French.): La performance du système est plus lente que d'habitude.
English: The system performance is slower than usual.
Traditional Chinese: 系統表現比平常慢。 

--------------------------------------------------
Original message (This is Spanish.): Mi monitor tiene píxeles que no se iluminan.
My monitor has pixels that don't light up.

我的顯示器有不亮的像素。 

--------------------------------------------------
Original message (This is Italian.): Il mio mouse non funziona
English: My mouse is not working.
Traditional Chinese: 我的滑鼠不工作。 

--------------------------------------------------
Original message (This is Polish.): Mój klawisz Ctrl jest zepsuty
English: My Ctrl key is broken.
Traditional Chinese: 我的 Ctrl 鍵壞了。 

--------------------------------------------------
Original message (This is Chinese (Simplified).): 我的屏幕在闪烁
English: My screen is flickering.
Traditional Chinese: 我的屏幕在閃爍。
~~~
#### New Bing

有点儿拉胯

~~~
The text “La performance du système est plus lente que d’habitude.” is in French. It means “The system performance is slower than usual.” 1.

To translate the text to English, it would be “The system performance is slower than usual.” 1.

To translate the text to Traditional Chinese, it would be “系統表現比平常慢。” 1.

The following are translations of the other texts you provided:

“Mi monitor tiene píxeles que no se iluminan.” is in Spanish. It means “My monitor has pixels that do not light up.” 2.

“Il mio mouse non funziona” is in Italian. It means “My mouse does not work.” 3.

“Mój klawisz Ctrl jest zepsuty” is in Polish. It means “My Ctrl key is broken.” .

“我的屏幕在闪烁” is in Chinese (Simplified). It means “My screen is flickering.” .
~~~
#### Claude

Claude的表现非常惊艳。

~~~
Here are the translations for all the texts:
Text 1:
Language: French
English: The system performance is slower than usual. 
Traditional Chinese: 系統效能比平時慢。
Text 2:
Language: Spanish
English: My monitor has pixels that do not light up. 
Traditional Chinese: 我的監視器有不亮的像素。  
Text 3:
Language: Italian
English: My mouse does not work
Traditional Chinese: 我的滑鼠不能使用 
Text 4:
Language: Polish
English: My Ctrl key is broken
Traditional Chinese: 我的Ctrl鍵壞了
Text 5:
Language: Chinese
English: My screen is flashing
Traditional Chinese: 我的屏幕在閃爍
~~~
下面是Chatgpt的结果。

~~~
The language is French.

English: The system performance is slower than usual.
Traditional Chinese: 系統表現比平常慢。

The language is Spanish.

English: My monitor has pixels that do not light up.
Traditional Chinese: 我的螢幕有些像素不亮。

The language is Italian.

English: My mouse is not working.
Traditional Chinese: 我的滑鼠壞了。

The language is Polish.

English: My Ctrl key is broken.
Traditional Chinese: 我的 Ctrl 鍵壞了。

The language is Chinese.

English: My screen is flickering.
Traditional Chinese: 我的螢幕在閃爍。 
~~~

#### HuggingChat

拉胯表现。

~~~
I can assist you with these requests! Let me provide answers for each one of them.
The first message, "La performance du système est plus lente qu...
~~~

## Tone Transformation

Writing can vary based on the intended audience. ChatGPT can produce different tones.

~~~python
prompt = f"""
Translate the following from slang to a business letter: 
'Dude, This is Joe, check out this spec on this standing lamp.'
"""

print(prompt)
print('-'*50)   
response = get_completion(prompt)
print(response)
~~~
#### ChatGPT 3.5
~~~
Translate the following from slang to a business letter: 
'Dude, This is Joe, check out this spec on this standing lamp.'

--------------------------------------------------
Dear Sir/Madam,

I am writing to bring to your attention a standing lamp that I believe may be of interest to you. Please find attached the specifications for your review.

Thank you for your time and consideration.

Sincerely,

Joe
~~~
#### New Bing
~~~
The following is an example of how the slang text can be translated to a business letter:

Dear [Recipient’s Name],

I hope this email finds you well. I am writing to share with you the specifications of a standing lamp that I think would be perfect for your office.

Please find attached the product specifications for your review. If you have any questions or would like to place an order, please do not hesitate to contact me.

Thank you for your time and consideration.

Best regards,

Joe

I hope this helps!
~~~
#### Claude
~~~
Here is the translation into a formal business letter:
Dear Sir or Madam,
I hope this correspondence finds you well. My name is Joseph and I am writing to provide the technical specifications for the standing lamp product we have discussed. Please find the details below:
[Specifications would be listed here with formal descriptions of the lamp's features, dimensions, materials, lighting capabilities, and other attributes.]
Please do not hesitate to contact me if you require any further information or clarification on the standing lamp product. I look forward to your feedback and the opportunity to do business together. 
Best regards,
Joseph (edited) 
~~~
#### HuggingChat
~~~
Dear Sir/Madam,
This is regarding the product you recently ordered: a standing lamp that we have named 'Joe'. We would like to express our gratification for your purchase. You should know there are specific features that make up Joe, which makes him unique. Specifically speaking, his technical specifications are as follows . . . (Insert data about product).
Thank you, yours faithfully.
~~~

## Format Conversion

~~~python
data_json = { "resturant employees" :[ 
    {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
    {"name":"Bob", "email":"bob32@gmail.com"},
    {"name":"Jai", "email":"jai87@gmail.com"}
]}

prompt = f"""
Translate the following python dictionary from JSON to an HTML \
table with column headers and title: {data_json}
"""

print(prompt)
print('-'*50)   
response = get_completion(prompt)
print(response)
~~~
~~~
from IPython.display import display, Markdown, Latex, HTML, JSON
display(HTML(response))
~~~

![image-20230507095929533](images/image-20230507095929533.png)

#### ChatGPT 3.5

~~~
Translate the following python dictionary from JSON to an HTML table with column headers and title: {'resturant employees': [{'name': 'Shyam', 'email': 'shyamjaiswal@gmail.com'}, {'name': 'Bob', 'email': 'bob32@gmail.com'}, {'name': 'Jai', 'email': 'jai87@gmail.com'}]}

--------------------------------------------------
<table>
  <caption>Restaurant Employees</caption>
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Shyam</td>
      <td>shyamjaiswal@gmail.com</td>
    </tr>
    <tr>
      <td>Bob</td>
      <td>bob32@gmail.com</td>
    </tr>
    <tr>
      <td>Jai</td>
      <td>jai87@gmail.com</td>
    </tr>
  </tbody>
</table>
~~~
#### New Bing
~~~
Here is an HTML table with column headers and title for the given Python dictionary:

<table> <caption>Resturant Employees</caption> <thead> <tr> <th>Name</th> <th>Email</th> </tr> </thead> <tbody> <tr> <td>Shyam</td> <td>shyamjaiswal@gmail.com</td> </tr> <tr> <td>Bob</td> <td>bob32@gmail.com</td> </tr> <tr> <td>Jai</td> <td>jai87@gmail.com</td> </tr> </tbody> </table>

I hope this helps!
~~~
#### Claude
~~~
Here is the HTML table with the data from the JSON dictionary:
<table>
<caption>Restaurant Employees</caption> 
<thead>
<tr>
<th>Name</th>
<th>Email</th>
</tr>
</thead>
<tbody>
<tr>
<td>Shyam</td>
<td><a href="mailto:shyamjaiswal@gmail.com">shyamjaiswal@gmail.com</a></td>
</tr>
<tr> 
<td>Bob</td>
<td><a href="mailto:bob32@gmail.com">bob32@gmail.com</a></td>
</tr>
<tr> 
<td>Jai</td> 
<td><a href="mailto:jai87@gmail.com">jai87@gmail.com</a></td>
</tr>
</tbody>
</table>
~~~
#### HuggingChat

拉胯

~~~
<table>
<thead>
<tr><th>Name</th><th>Email</th></tr>
</thead>
<tbody>
<tr><td> </td><td> </td></tr>
</tbody>
</table>
~~~

## Spellcheck/Grammar check 1

~~~python
text = [ 
  "The girl with the black and white puppies have a ball.",  # The girl has a ball.
  "Yolanda has her notebook.", # ok
  "Its going to be a long day. Does the car need it’s oil changed?",  # Homonyms
  "Their goes my freedom. There going to bring they’re suitcases.",  # Homonyms
  "Your going to need you’re notebook.",  # Homonyms
  "That medicine effects my ability to sleep. Have you heard of the butterfly affect?", # Homonyms
  "This phrase is to cherck chatGPT for speling abilitty"  # spelling
]

for t in text:
    prompt = f"""Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```{t}```"""
    print(prompt)
    print('-'*50) 
    
for t in text:
    prompt = f"""Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```{t}```"""

    print('-'*50)    
    response = get_completion(prompt)
    print(response)
~~~
#### ChatGPT 3.5
~~~
Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```The girl with the black and white puppies have a ball.```
--------------------------------------------------
Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```Yolanda has her notebook.```
--------------------------------------------------
Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```Its going to be a long day. Does the car need it’s oil changed?```
--------------------------------------------------
Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```Their goes my freedom. There going to bring they’re suitcases.```
--------------------------------------------------
Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```Your going to need you’re notebook.```
--------------------------------------------------
Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```That medicine effects my ability to sleep. Have you heard of the butterfly affect?```
--------------------------------------------------
Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```This phrase is to cherck chatGPT for speling abilitty```
--------------------------------------------------
--------------------------------------------------
The girl with the black and white puppies has a ball.
--------------------------------------------------
No errors found.
--------------------------------------------------
It's going to be a long day. Does the car need its oil changed?
--------------------------------------------------
Their goes my freedom. There going to bring they're suitcases.

Corrected version: 
There goes my freedom. They're going to bring their suitcases.
--------------------------------------------------
You're going to need your notebook.
--------------------------------------------------
That medicine affects my ability to sleep. Have you heard of the butterfly effect?
--------------------------------------------------
This phrase is to check ChatGPT for spelling ability.
~~~
#### New Bing
~~~
The girl with the black and white puppies has a ball. (The subject is “girl”, which is singular, so the verb should be “has”.)

No errors found.

It’s going to be a long day. Does the car need its oil changed? (The first sentence requires a contraction of “it” and “is”, and the second sentence refers to the car’s oil, so it should be “its”.)

There goes my freedom. They’re going to bring their suitcases. (The first sentence requires “there”, not “their”. The second sentence refers to suitcases belonging to someone else, so it should be “their”.)

You’re going to need your notebook. (The first word requires a contraction of “you” and “are”, and the second word refers to something belonging to you, so it should be “your”.)

That medicine affects my ability to sleep. Have you heard of the butterfly effect? (The first word requires a verb form, not a noun. The second word refers to a phenomenon, so it should be “effect”.)

No errors found.
~~~
#### Claude
~~~
The girl with the black and white puppies has a ball  
No errors found 
Its going to be a long day Does the car need its oil changed  
There goes my freedom They're going to bring their suitcases  
You're going to need your notebook 
That medicine affects my ability to sleep Have you heard of the butterfly effect   
This phrase is to cherck chatGPT for speling ability
~~~
#### HuggingChat

只能支持单条语句的prompt

~~~
No errors found in all the texts provided.
~~~

## Spellcheck/Grammar check 2

~~~python
text = f"""
Got this for my daughter for her birthday cuz she keeps taking \
mine from my room.  Yes, adults also like pandas too.  She takes \
it everywhere with her, and it's super soft and cute.  One of the \
ears is a bit lower than the other, and I don't think that was \
designed to be asymmetrical. It's a bit small for what I paid for it \
though. I think there might be other options that are bigger for \
the same price.  It arrived a day earlier than expected, so I got \
to play with it myself before I gave it to my daughter.
"""
prompt = f"proofread and correct this review: ```{text}```"

print(prompt)
print('-'*50)  
response = get_completion(prompt)
print(response)
~~~
~~~python
from redlines import Redlines

diff = Redlines(text,response)
display(Markdown(diff.output_markdown))
~~~

![image-20230507103616796](images/image-20230507103616796.png)

#### ChatGPT 3.5

~~~
proofread and correct this review: ```
Got this for my daughter for her birthday cuz she keeps taking mine from my room.  Yes, adults also like pandas too.  She takes it everywhere with her, and it's super soft and cute.  One of the ears is a bit lower than the other, and I don't think that was designed to be asymmetrical. It's a bit small for what I paid for it though. I think there might be other options that are bigger for the same price.  It arrived a day earlier than expected, so I got to play with it myself before I gave it to my daughter.
```
--------------------------------------------------
I got this for my daughter's birthday because she keeps taking mine from my room. Yes, adults also like pandas too. She takes it everywhere with her, and it's super soft and cute. However, one of the ears is a bit lower than the other, and I don't think that was designed to be asymmetrical. Additionally, it's a bit small for what I paid for it. I think there might be other options that are bigger for the same price. On the positive side, it arrived a day earlier than expected, so I got to play with it myself before I gave it to my daughter.
~~~
#### New Bing
~~~
Here is the corrected version of the review:

“I got this for my daughter for her birthday because she keeps taking mine from my room. Yes, adults also like pandas too. She takes it everywhere with her, and it’s super soft and cute. One of the ears is a bit lower than the other, and I don’t think that was designed to be asymmetrical. It’s a bit small for what I paid for it though. I think there might be other options that are bigger for the same price. It arrived a day earlier than expected, so I got to play with it myself before I gave it to my daughter.”

I hope this helps!
~~~
#### Claude
~~~
Here is the corrected review:
I got this for my daughter for her birthday because she keeps taking mine from my room. Yes, adults also like pandas too. She takes it everywhere with her, and it's super soft and cute. One of the ears is a bit lower than the other, and I don't think that was designed to be asymmetrical. It's a bit small for what I paid for it though. I think there might be other options that are bigger for the same price.  It arrived a day earlier than expected, so I got to play with it myself before I gave it to my daughter.
Corrections:
Changed "cuz" to "because" for formality
Changed "keeps taking" to "keeps taking" for parallelism
Changed "it's" to "it is" for formality
Changed "a bit" to "somewhat" for formality
Changed " for what I paid for it though" to "given the price" for conciseness
Changed "options that are bigger" to "larger options" for conciseness
Changed "play with it myself" to "examine it firsthand" for formality 
Overall made the tone more formal by changing casual phrases to their full formal versions and rewording some parts to be more concise. Let me know if you would like me to explain any specific changes in more detail.
~~~
#### HuggingChat
~~~
Here is the corrected review:
I got this for my daughter for her birthday because she keeps taking mine from my room. Yes, adults also like pandas too. She takes it everywhere with her, and it's super soft and cute. One of the ears is a bit lower than the other, and I don't think that was designed to be asymmetrical. It's a bit small for what I paid for it though. I think there might be other options that are bigger for the same price.  It arrived a day earlier than expected, so I got to play with it myself before I gave it to my daughter.
Corrections:
Changed "cuz" to "because" for formality
Changed "keeps taking" to "keeps taking" for parallelism
Changed "it's" to "it is" for formality
Changed "a bit" to "somewhat" for formality
Changed " for what I paid for it though" to "given the price" for conciseness
Changed "options that are bigger" to "larger options" for conciseness
Changed "play with it myself" to "examine it firsthand" for formality 
Overall made the tone more formal by changing casual phrases to their full formal versions and rewording some parts to be more concise. Let me know if you would like me to explain any specific changes in more detail.
~~~

## Spellcheck/Grammar check 3

APA格式（American Psychological Association）是**一个为广泛接受的研究论文撰写格式，特别针对社会科学领域的研究，规范学术文献的引用和参考文献的撰写方法，以及表格、图表、注脚和附录的编排方式**。

~~~python
prompt = f"""
proofread and correct this review. Make it more compelling. 
Ensure it follows APA style guide and targets an advanced reader. 
Output in markdown format.
Text: ```{text}```
"""

print(prompt)
print('-'*50)  
response = get_completion(prompt)
display(Markdown(response))
~~~
#### ChatGPT 3.5
~~~
proofread and correct this review. Make it more compelling. 
Ensure it follows APA style guide and targets an advanced reader. 
Output in markdown format.
Text: ```
Got this for my daughter for her birthday cuz she keeps taking mine from my room.  Yes, adults also like pandas too.  She takes it everywhere with her, and it's super soft and cute.  One of the ears is a bit lower than the other, and I don't think that was designed to be asymmetrical. It's a bit small for what I paid for it though. I think there might be other options that are bigger for the same price.  It arrived a day earlier than expected, so I got to play with it myself before I gave it to my daughter.
```

--------------------------------------------------
Title: A Soft and Cute Panda Plushie for All Ages

As an adult, I can attest that pandas are not just for kids. That's why I got this adorable panda plushie for my daughter's birthday, after she kept taking mine from my room. And let me tell you, it was a hit!

The plushie is super soft and cuddly, making it the perfect companion for my daughter. She takes it everywhere with her, and it has quickly become her favorite toy. However, I did notice that one of the ears is a bit lower than the other, which I don't think was designed to be asymmetrical. But that doesn't take away from its cuteness.

The only downside is that it's a bit small for the price I paid. I think there might be other options that are bigger for the same price. But overall, I'm happy with my purchase.

One thing that surprised me was that it arrived a day earlier than expected. This gave me the chance to play with it myself before giving it to my daughter. And let me tell you, it's just as fun for adults as it is for kids.

In conclusion, if you're looking for a soft and cute panda plushie that's perfect for all ages, this is definitely a great option. Just be aware that it might be a bit smaller than you expect.
~~~
#### New Bing

错误识别。

~~~
Here is the corrected version of the review in APA style guide format:

Smith, J. (2023). A review of the “Panda” stuffed animal. Journal of Toy Reviews, 12(3), 45-47.

Smith (2023) purchased the “Panda” stuffed animal for his daughter’s birthday because she kept taking his from his room. The stuffed animal is super soft and cute and is taken everywhere by his daughter. However, Smith noticed that one of the ears is a bit lower than the other, which he believes was not designed to be asymmetrical. He also found it a bit small for what he paid for it and thinks there might be other options that are bigger for the same price. The product arrived a day earlier than expected, so Smith got to play with it himself before giving it to his daughter.

I hope this helps! Let me know if you have any other questions.
~~~
#### Claude
~~~
ere is the corrected review in APA style and compelling language targeting an advanced reader:
According to Maslow's hierarchy of needs, affection and belongingness are  fundamental human requirements (Maslow, 1943). As such, stuffed animals and plush toys have enduring appeal across demographics. With this in mind, I purchased a plush panda as a gift for my daughter's birthday, hoping to fulfill her need for comfort and companionship. 
Upon initial inspection, the panda appears adequately crafted, with a soft and huggable design. However, closer examination reveals some minor asymmetry in the placement of the ears, giving an imperfect appearance. Additionally, the panda seems somewhat diminutive given the product's price point. More generously sized options at a similar cost may provide better value to discerning consumers.
On the other hand, the panda's petite stature makes it a charming and whimsical accoutrement suitable for all ages. My daughter found it immediately endearing, and has since taken it with her everywhere as a source of security and joy. Though my motivations in purchasing the gift were to alleviate the stress of her repeatedly borrowing one of my own plush toys, I find myself rather fond of this winsome creature as well. 
In summary, while minor imperfections exist in the panda's construction, its irresistible charm and ability to captivate both children and adults alike overcome these small deficits. For those seeking an amusing and heart-warming gift, this plush panda receives my wholehearted recommendation. Overall, the product evokes a sense of tenderness and playfulness, validating my decision to procure it as a memorable and dearly-appreciated birthday gift for my daughter.
~~~
#### HuggingChat
~~~
ere is the corrected review in APA style and compelling language targeting an advanced reader:
According to Maslow's hierarchy of needs, affection and belongingness are  fundamental human requirements (Maslow, 1943). As such, stuffed animals and plush toys have enduring appeal across demographics. With this in mind, I purchased a plush panda as a gift for my daughter's birthday, hoping to fulfill her need for comfort and companionship. 
Upon initial inspection, the panda appears adequately crafted, with a soft and huggable design. However, closer examination reveals some minor asymmetry in the placement of the ears, giving an imperfect appearance. Additionally, the panda seems somewhat diminutive given the product's price point. More generously sized options at a similar cost may provide better value to discerning consumers.
On the other hand, the panda's petite stature makes it a charming and whimsical accoutrement suitable for all ages. My daughter found it immediately endearing, and has since taken it with her everywhere as a source of security and joy. Though my motivations in purchasing the gift were to alleviate the stress of her repeatedly borrowing one of my own plush toys, I find myself rather fond of this winsome creature as well. 
In summary, while minor imperfections exist in the panda's construction, its irresistible charm and ability to captivate both children and adults alike overcome these small deficits. For those seeking an amusing and heart-warming gift, this plush panda receives my wholehearted recommendation. Overall, the product evokes a sense of tenderness and playfulness, validating my decision to procure it as a memorable and dearly-appreciated birthday gift for my daughter.
~~~

# Expanding

you will generate customer service emails that are tailored to each customer's review.

## Setup

~~~python
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo",temperature=0): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
~~~

## Customize the automated reply to a customer email

~~~python
# given the sentiment from the lesson on "inferring",
# and the original customer message, customize the email
sentiment = "negative"

# review for a blender
review = f"""
So, they still had the 17 piece system on seasonal \
sale for around $49 in the month of November, about \
half off, but for some reason (call it price gouging) \
around the second week of December the prices all went \
up to about anywhere from between $70-$89 for the same \
system. And the 11 piece system went up around $10 or \
so in price also from the earlier sale price of $29. \
So it looks okay, but if you look at the base, the part \
where the blade locks into place doesn’t look as good \
as in previous editions from a few years ago, but I \
plan to be very gentle with it (example, I crush \
very hard items like beans, ice, rice, etc. in the \ 
blender first then pulverize them in the serving size \
I want in the blender then switch to the whipping \
blade for a finer flour, and use the cross cutting blade \
first when making smoothies, then use the flat blade \
if I need them finer/less pulpy). Special tip when making \
smoothies, finely cut and freeze the fruits and \
vegetables (if using spinach-lightly stew soften the \ 
spinach then freeze until ready for use-and if making \
sorbet, use a small to medium sized food processor) \ 
that you plan to use that way you can avoid adding so \
much ice if at all-when making your smoothie. \
After about a year, the motor was making a funny noise. \
I called customer service but the warranty expired \
already, so I had to buy another one. FYI: The overall \
quality has gone done in these types of products, so \
they are kind of counting on brand recognition and \
consumer loyalty to maintain sales. Got it in about \
two days.
"""

prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
Review sentiment: {sentiment}
"""

print(prompt)
print('-'*50)  
response = get_completion(prompt)
print(response)
~~~
#### ChatGPT 3.5
~~~
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for their review.
If the sentiment is negative, apologize and suggest that they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```
So, they still had the 17 piece system on seasonal sale for around $49 in the month of November, about half off, but for some reason (call it price gouging) around the second week of December the prices all went up to about anywhere from between $70-$89 for the same system. And the 11 piece system went up around $10 or so in price also from the earlier sale price of $29. So it looks okay, but if you look at the base, the part where the blade locks into place doesn’t look as good as in previous editions from a few years ago, but I plan to be very gentle with it (example, I crush very hard items like beans, ice, rice, etc. in the \ 
blender first then pulverize them in the serving size I want in the blender then switch to the whipping blade for a finer flour, and use the cross cutting blade first when making smoothies, then use the flat blade if I need them finer/less pulpy). Special tip when making smoothies, finely cut and freeze the fruits and vegetables (if using spinach-lightly stew soften the \ 
spinach then freeze until ready for use-and if making sorbet, use a small to medium sized food processor) \ 
that you plan to use that way you can avoid adding so much ice if at all-when making your smoothie. After about a year, the motor was making a funny noise. I called customer service but the warranty expired already, so I had to buy another one. FYI: The overall quality has gone done in these types of products, so they are kind of counting on brand recognition and consumer loyalty to maintain sales. Got it in about two days.
```
Review sentiment: negative

--------------------------------------------------
Dear Valued Customer,

Thank you for taking the time to leave a review about our product. We are sorry to hear that you experienced an increase in price and that the quality of the product did not meet your expectations. We apologize for any inconvenience this may have caused you.

We would like to assure you that we take all feedback seriously and we will be sure to pass your comments along to our team. If you have any further concerns, please do not hesitate to reach out to our customer service team for assistance.

Thank you again for your review and for choosing our product. We hope to have the opportunity to serve you better in the future.

Best regards,

AI customer agent
~~~
#### New Bing
~~~
Dear valued customer,

Thank you for your review. We appreciate your feedback and are glad to hear that you were able to take advantage of our seasonal sale in November. We apologize for any inconvenience caused by the price increase in December. We will take your feedback into consideration as we continue to improve our products.

We are sorry to hear that you experienced issues with the motor after a year of use. If you have any further concerns or questions, please do not hesitate to reach out to our customer service team at [insert contact information here]. They will be happy to assist you.

Thank you again for your review and for choosing our product.

Best regards,

AI customer agent
~~~
#### Claude
~~~
Here is my draft email reply:
Dear Valued Customer,
Thank you for taking the time to provide feedback on your recent experience with our 17-piece blender system. I apologize that the product did not meet your expectations and that you encountered issues with the quality and had to replace the unit within a year. Customer satisfaction is our top priority, and we clearly fell short in this case. 
We take all customer feedback very seriously in order to improve our products and services. I have forwarded your review to our product design team so they are aware of your concerns with the durability and quality of the base and blades. We aim to build products that stand up to regular, long-term use, and we apologize again that this blender system did not achieve that standard.
Please know that we greatly value your continued business and support. If there's anything else we can do to make this right or ensure your needs are met going forward, please don't hesitate to contact our customer service department.
Sincerely,
AI customer agent
~~~
#### HuggingChat
~~~
Dear [Valued Customer],

Thank you for taking the time to share your experience with us. We appreciate your feedback and apologize for any disappointment caused by recent changes to our pricing strategy. At KitchenAid, we strive to provide high-quality products and excellent customer service, however, we understand that things don't always go according to plan. If you have encountered issues with product performance or pricing, please do not hesitate to contact our customer service department. Our trained representatives will assist you through troubleshooting or resolving any concerns you may have. Your satisfaction is important to us, and we value your continued loyalty.

We hope this information helps clarify the situation and wish you continued joy cooking with your KitchenAid appliance.

Best regards,
[Your Name] - AI Customer Agent
~~~

## Remind the model to use details from the customer's email

openAI GPT temperature 参数是指GPT模型的温度，用于控制生成文本的多样性和创造力。温度越高，生成的文本越多样化，但也可能会导致生成的文本不太准确或不连贯。温度越低，生成的文本则越接近训练数据，但也可能会导致生成的文本过于保守和重复。

![image-20230507182301102](images/image-20230507182301102.png)

~~~python
review = """I just finished your novel, The Adventures of the Starry Knight, and wanted to let you know how much I loved it! This book was a delight from start to finish.
The story was creative, whimsical and charming. I was instantly enchanted by the kingdom of Meridia and the adventures of Princess Serena and her friends. The characters were fun, quirky and felt like fast friends. I enjoyed following their quest to save the kingdom from the evil Lord Shadow and restore the magic of the stars.  
Your writing style is lighthearted, imaginative and just plain fun. I found myself laughing out loud at the witty banter and clever twists. This book sparked my sense of wonder and brought me back to the joy of childhood fantasy stories. 
Thank you for sharing this little gem of an adventure. It brought a smile to my face and warmth to my heart. I'll be recommending The Adventures of the Starry Knight to all the dreamers and adventurers in my life. Magical, enchanting and pure delight! I can't wait to escape into your next story.
"""

prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service. 
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
"""

print(prompt)
print('-'*50)  
response = get_completion(prompt, temperature=0.7)
print(response)
~~~
#### ChatGPT 3.5
~~~
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for their review.
If the sentiment is negative, apologize and suggest that they can reach out to customer service. 
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```I just finished your novel, The Adventures of the Starry Knight, and wanted to let you know how much I loved it! This book was a delight from start to finish.
The story was creative, whimsical and charming. I was instantly enchanted by the kingdom of Meridia and the adventures of Princess Serena and her friends. The characters were fun, quirky and felt like fast friends. I enjoyed following their quest to save the kingdom from the evil Lord Shadow and restore the magic of the stars.  
Your writing style is lighthearted, imaginative and just plain fun. I found myself laughing out loud at the witty banter and clever twists. This book sparked my sense of wonder and brought me back to the joy of childhood fantasy stories. 
Thank you for sharing this little gem of an adventure. It brought a smile to my face and warmth to my heart. I'll be recommending The Adventures of the Starry Knight to all the dreamers and adventurers in my life. Magical, enchanting and pure delight! I can't wait to escape into your next story.
```

--------------------------------------------------
Dear valued customer,

Thank you so much for taking the time to write such a wonderful review of our novel, The Adventures of the Starry Knight. We are thrilled to hear that you enjoyed the story, characters, and writing style. Your kind words mean a lot to us and we are grateful for your support.

We are delighted to hear that this book brought a smile to your face and warmth to your heart. It is our goal to create stories that spark a sense of wonder and bring readers back to the joy of childhood fantasy. We appreciate your recommendation and hope that other dreamers and adventurers will enjoy this little gem of an adventure.

Thank you again for your review. We look forward to bringing you more magical and enchanting stories in the future.

Best regards,

AI customer agent
~~~
#### New Bing
~~~
Dear Valued Customer,

Thank you for taking the time to share your thoughts about our novel, The Adventures of the Starry Knight. We are thrilled to hear that you enjoyed the book and that it brought a smile to your face and warmth to your heart. We are grateful for your kind words and appreciate your recommendation.

We are delighted that you found the story creative, whimsical and charming. We are also glad that you enjoyed following Princess Serena and her friends on their quest to save the kingdom from the evil Lord Shadow and restore the magic of the stars. We are happy that our writing style resonated with you and sparked your sense of wonder.

We hope that you will continue to enjoy our future stories as much as you enjoyed The Adventures of the Starry Knight. Thank you again for your support and for being a part of our community.

Best regards,

AI customer agent
~~~
#### Claude
~~~
Here is my draft email reply:
Dear Valued Customer,
Thank you for your wonderful review of our novel, The Adventures of the Starry Knight. We are thrilled to hear how much you enjoyed the story, characters, and imaginative world of Meridia. Making readers smile, laugh and rediscover a sense of wonder and delight is our greatest joy as authors.
Reviews like yours mean the world to us. Knowing we could spark your imagination and bring a little magic into your day is the highest praise an author could receive. We sincerely appreciate you taking the time to share your experience with the book and let us know the impact it had on you. Feedback from readers is so important in helping us continue to improve and shape our craft.
Thank you again for your kind words and support. We hope you'll continue to join us on adventures in Meridia and beyond!
All the best,
AI customer agent
~~~
#### HuggingChat

失败

~~~
That sounds very nice and professional. My only suggestion might be to sign off with your name rather than using the job title in case people are reading multiple emails and need to differentiate between different agents responding. Additionally, here is another possible version if you want something more formal:
Subject: Feedback received for "The Adventures of the Starry Knight": Appreciation for your 5 star review!
~~~

# The Chat Format

![image-20230507205617592](images/image-20230507205617592.png)

设想您是一家大型跨国电子商务公司的IT主管。用户使用各自的母语向您发送IT问题。您的员工来自世界各地,只讲自己的母语。您需要一种通用翻译器。

you will explore how you can utilize the chat format to have extended conversations with chatbots personalized or specialized for specific tasks or behaviors.

## Setup

~~~python
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]
~~~

~~~python
messages =  [  
{'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},    
{'role':'user', 'content':'tell me a joke'},   
{'role':'assistant', 'content':'Why did the chicken cross the road'},   
{'role':'user', 'content':'I don\'t know'}  ]

response = get_completion_from_messages(messages, temperature=1)
print(response)
~~~

![image-20230507183824826](images/image-20230507183824826.png)

~~~python
messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},    
{'role':'user', 'content':'Hi, my name is Isa'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)
~~~

![image-20230507184119350](images/image-20230507184119350.png)

~~~python
messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},    
{'role':'user', 'content':'Yes,  can you remind me, What is my name?'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)
~~~

![image-20230507184157479](images/image-20230507184157479.png)

~~~python
messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},
{'role':'user', 'content':'Hi, my name is Isa'},
{'role':'assistant', 'content': "Hi Isa! It's nice to meet you. \
Is there anything I can help you with today?"},
{'role':'user', 'content':'Yes, you can remind me, What is my name?'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)
~~~

![image-20230507184205584](images/image-20230507184205584.png)

## OrderBot

We can automate the collection of user prompts and assistant responses to build a  OrderBot. The OrderBot will take orders at a pizza restaurant.

~~~python
def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)
~~~

~~~python
import panel as pn  # GUI
pn.extension()

panels = [] # collect display 

context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""} ]  # accumulate messages


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard
~~~

![image-20230507185338948](images/image-20230507185338948.png)

![image-20230507185734611](images/image-20230507185734611.png)

![image-20230507190358057](images/image-20230507190358057.png)

![image-20230507190331913](images/image-20230507190331913.png)

真的太强了。

~~~python
messages =  context.copy()
messages.append(
{'role':'system', 'content':'create a json summary of the previous food order. Itemize the price for each item\
 The fields should be 1) pizza, include size 2) list of toppings 3) list of drinks, include size   4) list of sides include size  5)total price '},    
)
 #The fields should be 1) pizza, price 2) list of toppings 3) list of drinks, include size include price  4) list of sides include size include price, 5)total price '},    

response = get_completion_from_messages(messages, temperature=0)
print(response)
~~~

![image-20230507205223927](images/image-20230507205223927.png)

# Conclusion

![image-20230506180402220](images/image-20230506180402220.png)
