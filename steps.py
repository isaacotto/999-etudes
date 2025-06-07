import math
import random
from typing import List, Optional
import pandas as pd
from datetime import datetime
import yaml


PITCH_CLASSES = ['c', 'cis', 'd', 'ees', 'e', 'f', 'fis', 'g', 'gis', 'a', 'bes', 'b']


print("Loading parameters from YAML...")

def load_parameters_from_yaml(filename):
    with open(filename, 'r') as file:
        raw = yaml.safe_load(file)

    # Unpack pitch_sets (can be flat or nested)
    pitch_sets = {k: v for k, v in raw.items() if k.lower().startswith("pitches")}
    
    # Build params dict in same structure your script expects
    return {
        "pitch_sets": pitch_sets,
        "steps": [item['step'] for item in raw['steps']],
        "step_weights": [item['weight'] for item in raw['steps']],
        "rhythms": [item['rhythm'] for item in raw['rhythms']],
        "rhythm_weights": [item['weight'] for item in raw['rhythms']],
        "articulations": [item['articulation'] for item in raw['articulations']],
        "articulation_weights": [item['weight'] for item in raw['articulations']],
        "open": [item['directive'] for item in raw['open']],
        "open_weights": [item['weight'] for item in raw['open']],
        "expressions": raw.get("expressions", []),
        "rest_chance": raw.get("rest_chance", []),
        "output_notes": raw.get("output_notes", []),
        # "articulations": unpack_weighted_items(raw["articulations"])[0] if "articulations" in raw and isinstance(raw["articulations"][0], dict) else raw.get("articulations", []),
        # "articulation_weights": unpack_weighted_items(raw["articulations"])[1] if "articulations" in raw and isinstance(raw["articulations"][0], dict) else raw.get("articulation_weights", []),
        # "open": unpack_weighted_items(raw["open"])[0] if "open" in raw and isinstance(raw["open"][0], dict) else raw.get("open", []),
        # "open_weights": unpack_weighted_items(raw["open"])[1] if "open" in raw and isinstance(raw["open"][0], dict) else raw.get("open_weights", []),
        # "expressions": raw.get("expressions", []),
        # "rest_chance": raw.get("rest_chance", []),
        # "output_notes": raw.get("output_notes", []),
    }

def midi_to_lilypond(midi_num):
    pitch_class = PITCH_CLASSES[midi_num % 12]
    rel_octave = (midi_num - 60) // 12  # Middle C = 60
    if rel_octave >= 0:
        return pitch_class + ("'" * rel_octave)
    else:
        return pitch_class + ("," * abs(rel_octave))

def read_int_list(filename):
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file if line.strip()]

def read_float_list(filename):
    with open(filename, 'r') as file:
        return [float(line.strip()) for line in file if line.strip()]

# print("Generating pitch sequence...")
def generate_pitch_sequence(pitches, steps, step_weights, count):
    if not pitches:
        raise ValueError("Pitch list is empty.")
    if not steps:
        raise ValueError("Step list is empty.")
    if step_weights and len(step_weights) != len(steps):
        raise ValueError("Step weight count doesn't match step count.")

    # Initial index will be near the middle of the pitch range
    current_index = int(math.floor(random.randint(0, len(pitches) - 1))/2)
    sequence = [pitches[current_index]]

    for _ in range(count - 1):
        step = random.choices(steps, weights=step_weights if step_weights else None)[0]
        new_index = current_index + step

        if 0 <= new_index < len(pitches):
            current_index = new_index
        else:
            current_index = random.randint(0, len(pitches) - 1)

        sequence.append(pitches[current_index])

    return sequence

# print("Generating rhythm sequence...")
def generate_rhythm_sequence(rhythms, weights, count):
    if not rhythms:
        raise ValueError("Rhythm list is empty.")
    if weights and len(weights) != len(rhythms):
        raise ValueError("Rhythm weight count doesn't match rhythm count.")

    return random.choices(rhythms, weights=weights if weights else None, k=count)

# print("Generating articulations...")
def generate_articulations(artics: List[str], weights: Optional[List[float]], count: int) -> List[str]:
    if not artics:
        return ["" for _ in range(count)]
    if weights and len(weights) != len(artics):
        raise ValueError("Articulation weights don't match articulation count.")

    chosen = random.choices(artics, weights=weights if weights else None, k=count)
    return ["" if art == "none" else art for art in chosen]

# print("Generating in-between code...")
def generate_inbetween_code(open_directives: List[str], weights: Optional[List[float]], count: int) -> List[str]:
    if not open_directives:
        return ["" for _ in range(count)]
    if weights and len(weights) != len(open_directives):
        raise ValueError("Open directive weights don't match directive count.")

    chosen = random.choices(open_directives, weights=weights if weights else None, k=count)
    return ["" if directive.strip() == "none" else directive.strip() for directive in chosen]

# print("Inserting rests...")
def insert_rests(pitches, rhythms, rest_chance):
    """
    Randomly turn notes into rests based on rest_chance.
    """
    result = []
    for pitch, rhythm in zip(pitches, rhythms):
        if random.random() < rest_chance:
            result.append(('rest', rhythm))
        else:
            result.append((pitch, rhythm))
    return result

# print("Combining ties...")
def combine_ties(note_rhythm_list, articulation_list, inter_note_code=None):
    output = []
    prev_note = None

    for i, current in enumerate(note_rhythm_list):
        articulation = articulation_list[i] if articulation_list else ""
        pitch = ""
        rhythm = ""
        note_string = ""

        if current[0] == 'rest':
            note_string = f"r{current[1]}"
            prev_note = None
        else:
            pitch = midi_to_lilypond(current[0])
            rhythm = str(current[1])
            note_head = f"{pitch}{rhythm}"

            if prev_note and prev_note[0] == current[0]:
                # Tie: insert "~" immediately after the rhythm
                # Modify the *previous* note instead of adding "~" here
                if output:
                    output[-1] = output[-1].replace(note_head, note_head + "~")
            else:
                note_string = f"{note_head}{articulation}"
                prev_note = current

                # Print melody to terminal with line break at the end.
                print(note_string, end=' ')

        if note_string:
            output.append(note_string)

        # Insert inter-note code *between* notes (but not after the last note)
        if inter_note_code and i < len(note_rhythm_list) - 1:
            code = inter_note_code[i]
            if code:
                output.append(code)

    return output

print("Writing LilyPond file...")
def write_lilypond_file(lilypond_notes, filename='score.ly', expression=''):
    note_string = " ".join(lilypond_notes)
    cnt = note_string.count('~')
    # print(f"There are {cnt} tildes")

    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3] # Current timestamp, microseconds truncated by three digits
    num_stamp = (format (int(time_stamp), ',d'))

    print("\n")
    print(f"Score number: {num_stamp}")

    # Import lilypond template from ./lilypond-template
    # This file should contain the basic structure of a LilyPond file
    # with placeholders for note_string, num_stamp, and expression
    # designated by {{note_string}}, {{num_stamp}}, and {{expression}}

    # # Prompt user to choose a template file from a list drawn from all files in the current directory with the prefix lilypond-template-
    # # If no such file exists, use the default template file lilypond-template-default
    # import os
    # template_files = [f for f in os.listdir('.') if f.startswith('lilypond-template-') and f.endswith('.ly')]
    # if template_files:
    #     print("Available LilyPond templates:")
    #     for i, file in enumerate(template_files):
    #         print(f"{i + 1}: {file}")
    #     choice = input("Choose a template by number (or press Enter to use default): ")
    #     if choice.isdigit() and 1 <= int(choice) <= len(template_files):
    #         lilypond_template_file = template_files[int(choice) - 1]
    #     else:
    #         lilypond_template_file = 'lilypond-template-default'
    # else:
    #     print("No custom templates found, using default template.")

    lilypond_template_file = 'template_temp'
    with open(lilypond_template_file, 'r', encoding='utf-8') as f:
        file_contents = f.read()

    lilypond_template = (
            file_contents # template
            .replace("{{note_string}}", note_string)
            .replace("{{num_stamp}}", num_stamp)
            .replace("{{expression}}", expression)
        )

    with open(filename, 'w') as f:
        f.write(lilypond_template)
    print(f"LilyPond score written to {filename}")

def main():
    parameter_file = 'parameters_temp.yaml'
    melody_file = 'melody.txt'
    lilypond_file = 'score.ly'

    try:
        params = load_parameters_from_yaml(parameter_file)

        pitch_sets = params["pitch_sets"]
        if not pitch_sets:
            raise ValueError("No pitch columns found in CSV.")

        # Randomly pick one pitch column
        chosen_column = random.choice(list(pitch_sets.keys()))
        print(f"Using pitch column: {chosen_column}")
        pitches = pitch_sets[chosen_column]

        steps = params["steps"]
        step_weights = params["step_weights"]
        rhythms = params["rhythms"]
        rhythm_weights = params["rhythm_weights"]
        articulations = params["articulations"]
        articulation_weights = params["articulation_weights"]
        open_directives = params["open"]
        open_weights = params["open_weights"]
        expressions = params["expressions"]

        chosen_expression = random.choice(expressions) if expressions else ""

        # Print chosen expression highlighted in red.
        print("\033[31m" + "Chosen expression: " + chosen_expression + "\033[0m")  # Red text

        # Selects number of output notes randomly from the list or defaults to 100
        # num_output = int(input("Enter number of output notes: "))
        num_output = random.choice(params["output_notes"]) if params["output_notes"] else 100
        print(f"Number of output notes set to: {num_output}")

        # Selects rest chance randomly from the list or defaults to 0.0
        # rest_chance = float(input("Enter probability of rest (0.0 to 1.0): "))
        rest_chance = random.choice(params["rest_chance"]) if params["rest_chance"] else 0.0
        print(f"Rest chance set to: {rest_chance}")

        pitch_sequence = generate_pitch_sequence(pitches, steps, step_weights, num_output)
        rhythm_sequence = generate_rhythm_sequence(rhythms, rhythm_weights, num_output)
        combined = insert_rests(pitch_sequence, rhythm_sequence, rest_chance)

        articulation_sequence = generate_articulations(articulations, articulation_weights, num_output)
        inter_note_code = generate_inbetween_code(open_directives, open_weights, num_output - 1)

        with open(melody_file, 'w') as f:
            for item in combined:
                if item[0] != 'rest':
                    f.write(f"{item[0]}\n")
        print(f"Melody written to {melody_file}\n")

        lilypond_notes = combine_ties(combined, articulation_sequence, inter_note_code)
        write_lilypond_file(lilypond_notes, filename=lilypond_file, expression=chosen_expression)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
