# 999 Etudes

## To do

- [ ] Add additional templates for different score classes:
    - [✓] Percussion scores
- [ ] Settle on additional parameter sets for different score classes:
    - [ ] Percussion scores
    - [ ] "Easy" scores
    - [ ] "Hard" scores
- [ ] Tweak visual appearance of scores
- [ ] Settle on title
- [ ] Settle on final text to be included at bottom of each score
    - Different for each set of scores
    - Bilingual

## Description

This is a utility used to procedurally generate scores for short etudes.

The intended use is in generating large batches of etudes for "999 etudes", an "improvisation simulator" centering one-time-use disposable etudes which will be conspicuously destroyed after performance.

## Dependencies
- python3
    - pandas>=1.0
    - pyyaml>=5.0
- lilypond
- pdfunite (for combining output .pdfs) 

## Use

Running ``./generate`` without any additional parameters will generate one score, prompting the user for a template file located in ``./templates`` and a parameters file located in ``./parameters``. Additional templates and sets of parameters may be added to these folders.

To generate multiple scores with the same set of parameters, provide the desired number, e.g. ``./generate 5``.

Details pertaining to score generation will be printed in the console. Each score will be generated separately in a time-stamped directory, then merged into a final pdf.

To clean the project directory, run ``./clean``.

### Parameters

Parameters for generation are given in the included ``parameters.yaml`` file.

| Parameter           | Description                                                |
| ---                 | ---                                                        |
| ``output_notes``    | total number of output notes                               |
| ``pitches01``, etc. | ordered lists of available pitches                         |
|                     | (more may be added following the pattern shown)            |
| ``rest_chance``     | list of available rest probabilities per note              |
| ``steps``           | list of available step intervals with weights              |
| ``rhythms``         | list of available durations with eights                    |
| ``articulations``   | list of available strings (appended to notes) with weights |
| ``open``            | list of available strings (between notes0 with weights     |
| ``expressions``     | list of available tempo/expression indications             |

## .gitignore
- Output files ignored:
    - ``*.txt``
    - ``*.midi``
    - ``*.pdf``
    - ``output-scores_*/``





