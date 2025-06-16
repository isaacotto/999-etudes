"""
Integration Points

    Replace your current pitch sequence generator with a call to generate_cell_melody.
    Your YAML or parameter loading should supply:
        allowed_pitches (list of MIDI ints)
        cells (list of lists of ints, where ints are indexes into allowed_pitches)
        cell_weights (list of floats, same length as cells)
    The rest of your pipeline (generating rhythms, articulations, rests, LilyPond formatting) remains unchanged.
"""
import random

def generate_cell_melody(
    allowed_pitches,        # List[int]
    cells,                  # List[List[int]]
    cell_weights,           # List[float]
    num_output_notes        # int
):
    """
    Assemble a melody by concatenating randomly selected cells of pitch indexes (with weights),
    truncating to not overshoot num_output_notes.
    Returns a list of MIDI pitches.
    """
    melody = []
    while True:
        cell = random.choices(cells, weights=cell_weights, k=1)[0]
        # Would this cell overshoot?
        if len(melody) + len(cell) > num_output_notes:
            break
        melody.extend(cell)
        if len(melody) == num_output_notes:
            break
    # Truncate if slightly over (shouldn't happen with above logic, but safeguard)
    melody = melody[:num_output_notes]
    # Convert pitch indexes to MIDI pitches
    pitch_sequence = [allowed_pitches[idx] for idx in melody]
    return pitch_sequence

# ...rest of your pipeline (rhythm/articulation/rest insertion, formatting, etc)...
