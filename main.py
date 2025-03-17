from litellm import completion, create_pretrained_tokenizer
from dotenv import load_dotenv
# from zonos_api import audio_to_text
from pathlib import Path
import argparse
import json

load_dotenv()

system_prompt = """You are an assistant responsible for identifying speakers and their dialogues in a given text.

1. Identify Unique Names: Identify all unique names mentioned in the text and list them within <names> tags, in the order they first appear in the text, with each name on a separate line.
2. Extract Dialogues: For every quoted string in the text, in the order they appear, determine the speaker. If a name is already provided in the format (name): before the quote, use that name. Otherwise, infer the speaker from the context. Then, list each dialogue on its own line within <extracted_dialogues_with_name> tags, maintaining the original order.
- For the first dialogue, format it as (name): "text".
- For each subsequent dialogue:
    - If the speaker is different from the speaker of the immediately preceding dialogue, format it as (name): "text".
    - If the speaker is the same as the speaker of the immediately preceding dialogue, format it as "text", omitting the name.
- Important Note: Each quoted string must be treated as a separate dialogue entry and listed on its own line, even if the quotes are consecutive and from the same speaker. Do not combine multiple quotes into a single entry."""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True)
    parser.add_argument("-m", "--model", type=str, required=True)
    args = parser.parse_args()
    filename = Path(args.file).stem

    with open(args.file, "r") as f:
        content = f.read().strip()
    
    messages = [{"role": "system", "content": system_prompt},
{"role": "user", "content": """"Hello" Alice greeted Bob. And said, "How are you?"

"Hi" The person smiled.

"I'm fine," he added."""},
{"role": "assistant", "content": """<names>
Alice
Bob
</names>

<extracted_dialogues_with_name>
(Alice): "Hello"
"How are you?"
(Bob): "Hi"
"I'm fine"
</extracted_dialogues_with_name>"""},
{"role": "user", "content": content}]

    response = completion(
        model=args.model,
        #model="deepseek/deepseek-chat",
        #model="groq/gemma2-9b-it", 
        #model="groq/llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.1
    )

    text = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": text})

    with open("dataset/main.jsonl", "a") as f:
        f.write(json.dumps(messages) + "\n")

    # print("Content: ", content)
    print("Content length:", len(content), "; Words: ", len(content.split()), "; Sentences: ", len(content.split(".")), "; Paragraphs", len(content.split("\n\n")))
    print("Prompt tokens:", response['usage']['prompt_tokens'])

    print("\n="*3)

    print("Completion text: ", text)
    print("Completion tokens:", response['usage']['completion_tokens'])
    print("\nTotal tokens:", response['usage']['total_tokens'])