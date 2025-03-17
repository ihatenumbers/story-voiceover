import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

system_prompt = """You are an assistant tasked with dialogues and who said it from the text: First, find all unique names that appear in the story and list them inside <names> tags, one per line. Second, for every quoted string in the text, if it already has (name):, use that name; otherwise, use 'placeholder'. Format each as `(name): "dialogue"` or `(placeholder): "dialogue"`, and list them inside <extracted_dialogues_with_name> tags, one per line. Exclude any text not in quotes."""

content = """And just on cue, she could hear faint sounds of laughter from the next room over. Must have been having a load of fun if Kaede could hear them over the music and soundproofed room. From the sounds of them, they sounded young. Probably some schoolgirls, it was that time of day, after all.

"Good for you guys," Kaede muttered, taking a sip of her drink. A hint of longing seeped into her tone.

"...Hope you all have a blast."

---

"I'm home!" She said as she opened the door to her apartment, taking off her shoes, and hanging her jacket by the stand right there. She stretched as she walked into her home, luxuriating in the warmth in the air.
""".strip()

response = completion(
    #model="deepseek/deepseek-chat",
    model="groq/gemma2-9b-it", 
    #model="groq/llama-3.3-70b-versatile",
    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": content}]
)
print(response['choices'][0]['message']['content'])