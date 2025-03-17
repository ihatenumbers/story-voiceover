def get_name_dialogues(contents):
    contents = contents.split("<extracted_dialogues_with_name>")[-1].replace("</extracted_dialogues_with_name>", "").strip().split("\n")
    dialogues = []          # List to store grouped dialogues
    current_speaker = None  # Track the current speaker

    for line in contents:
        if line.startswith("("):
            # Extract name and dialogue
            name_part, dialogue = line.split(": ", 1)
            name = name_part[1:-1]  # Remove '(' and ')'
            dialogue = dialogue.strip()  # Remove extra spaces

            if name != current_speaker:
                # New speaker: start a new sublist
                current_speaker = name
                dialogues.append([name, dialogue])
            else:
                # Same speaker: append dialogue to current sublist
                dialogues[-1].append(dialogue)
        else:
            # Continuation of current speaker's dialogue
            dialogues[-1].append(line)

    return dialogues

if __name__ == "__main__":
    import json
    with open("dataset/main.jsonl", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            print(get_name_dialogues(data[-1]['content']))
            break