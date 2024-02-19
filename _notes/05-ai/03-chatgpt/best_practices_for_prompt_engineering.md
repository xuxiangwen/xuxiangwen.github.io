# [Best practices for prompt engineering with OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)

## 经验法则（Rules of Thumb）and Examples

1. 在 prompt 的开头放置 instruction，并使用 ### 或 """ 分隔 instruction 和 context。

   Put instructions at the beginning of the prompt and use ### or """ to separate the instruction and context 

   Less effective ❌:

   ```
   Summarize the text below as a bullet point list of the most important points.
   
   {text input here}
   ```

   Better ✅:

   ```
   Summarize the text below as a bullet point list of the most important points.
   
   Text: """
   {text input here}
   """
   ```

2. 在 prompt 中，请尽可能详细具体地描述：所期望的 context、outcome、length、format、style 等。

   Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style, etc 

   Less effective ❌:

   ```
   Write a poem about OpenAI. 
   ```

   Better ✅:

   ```
   Write a short inspiring poem about OpenAI, focusing on the recent DALL-E product launch (DALL-E is a text to image ML model) in the style of a {famous poet}
   ```

3. **通过示例详细说明所期望的输出格式（[示例1](https://beta.openai.com/playground/p/DoMbgEMmkXJ5xOyunwFZDHdg)，[示例2](https://beta.openai.com/playground/p/3U5Wx7RTIdNNC9Fg8fc44omi)）。**

   Articulate the desired output format through examples ([example 1](https://beta.openai.com/playground/p/DoMbgEMmkXJ5xOyunwFZDHdg), [example 2](https://beta.openai.com/playground/p/3U5Wx7RTIdNNC9Fg8fc44omi)). 

   Less effective ❌:

   ```
   Extract the entities mentioned in the text below. Extract the following 4 entity types: company names, people names, specific topics and themes.
   
   Text: {text}
   ```

   Show, and tell - the models respond better when shown specific format requirements. This also makes it easier to programmatically parse out multiple outputs reliably.

   Better ✅:

   ```
   Extract the important entities mentioned in the text below. First extract all company names, then extract all people names, then extract specific topics which fit the content and finally extract general overarching themes
   
   Desired format:
   Company names: <comma_separated_list_of_company_names>
   People names: -||-
   Specific topics: -||-
   General themes: -||-
   
   Text: {text}
   ```

4. 从zero-shot开始，然后进行few-shot（[示例](https://beta.openai.com/playground/p/Ts5kvNWlp7wtdgWEkIAbP1hJ)），两者都没有奏效，然后进行微调。

   Start with zero-shot, then few-shot ([example](https://beta.openai.com/playground/p/Ts5kvNWlp7wtdgWEkIAbP1hJ)), neither of them worked, then fine-tune

   ✅ Zero-shot 

   ```
   Extract keywords from the below text.
   
   Text: {text}
   
   Keywords:
   ```

   ✅ Few-shot - provide a couple of examples

   ```
   Extract keywords from the corresponding texts below.
   
   Text 1: Stripe provides APIs that web developers can use to integrate payment processing into their websites and mobile applications.
   Keywords 1: Stripe, payment processing, APIs, web developers, websites, mobile applications
   ##
   Text 2: OpenAI has trained cutting-edge language models that are very good at understanding and generating text. Our API provides access to these models and can be used to solve virtually any task that involves processing language.
   Keywords 2: OpenAI, language models, text processing, API.
   ##
   Text 3: {text}
   Keywords 3:
   ```

   ✅Fine-tune: see fine-tune best practices [here](https://docs.google.com/document/d/1h-GTjNDDKPKU_Rsd0t1lXCAnHltaXTAzQ8K2HRhQf9U/edit#).

5. 减少“空洞”和不精确的描述

   Reduce “fluffy” and imprecise descriptions

   Less effective ❌:

   ```
   The description for this product should be fairly short, a few sentences only, and not too much more.
   ```

   Better ✅:

   ```
   Use a 3 to 5 sentence paragraph to describe this product.
   ```

6. 不仅要说不要做什么，还要说明应该做什么。

   Instead of just saying what not to do, say what to do instead

   Less effective ❌:

   ```
   The following is a conversation between an Agent and a Customer. DO NOT ASK USERNAME OR PASSWORD. DO NOT REPEAT.
   
   Customer: I can’t log in to my account.
   Agent:
   ```

   Better ✅:

   ```
   The following is a conversation between an Agent and a Customer. The agent will attempt to diagnose the problem and suggest a solution, whilst refraining from asking any questions related to PII. Instead of asking for PII, such as username or password, refer the user to the help article www.samplewebsite.com/help/faq
   
   Customer: I can’t log in to my account.
   Agent:
   ```

7. 代码生成特定 - 使用“leading words”来引导模型朝特定模式发展。

   Code Generation Specific - Use “leading words” to nudge the model toward a particular pattern

   Less effective ❌:

   ```
   # Write a simple python function that
   # 1. Ask me for a number in mile
   # 2. It converts miles to kilometers
   ```

   In this code example below, adding “*import*” hints to the model that it should start writing in Python. (Similarly “SELECT” is a good hint for the start of a SQL statement.) 

   Better ✅:

   ```
   # Write a simple python function that
   # 1. Ask me for a number in mile
   # 2. It converts miles to kilometers
    
   import 
   ```

## **Parameters** 

通常，我们发现**`model`** 和 **`temperature`** 是最常用的参数来改变模型的输出。

1. **`model` -** 性能更高的[模型](https://beta.openai.com/docs/models)更昂贵，且延迟更高。

2. **`temperature` -** 一个衡量模型输出不太可能 token 的频率的指标。`temperature`越高，输出的随机性（通常也是创造性）越大。然而，这并不等同于“真实性”。对于大多数事实性的用例，如数据提取，和真实的问答，0 的`temperature` 是最好的。

3. **`max_tokens`** (**maximum length)** - 并不控制输出的长度，而是 token 生成的硬截止限制。理想情况下，你不会经常达到这个限制，因为你的模型会在认为完成的时候停止，或者在达到你定义的停止序列时停止。

4. **`stop` (stop sequences)** - 一组字符（tokens），在生成时，会导致文本生成停止。

   关于其他参数的描述，请参阅[API参考](https://beta.openai.com/docs/api-reference/completions/create)。

## **Additional Resources**

- Guides
  - [Text completion](https://beta.openai.com/docs/guides/completion/text-completion) - learn how to generate or edit text using our models
  - [Code completion](https://beta.openai.com/docs/guides/code/code-completion-private-beta) - explore prompt engineering for Codex
  - [Fine-tuning](https://beta.openai.com/docs/guides/fine-tuning/fine-tuning) - Learn how to train a custom model for your use case
  - [Embeddings](https://beta.openai.com/docs/guides/embeddings/embeddings) - learn how to search, classify, and compare text
  - [Moderation](https://beta.openai.com/docs/guides/moderation/moderation)
- [OpenAI cookbook repo](https://github.com/openai/openai-cookbook/tree/main/examples) - contains example code and prompts for accomplishing common tasks with the API, including Question-answering with Embeddings
- [Community Forum](https://community.openai.com/)

