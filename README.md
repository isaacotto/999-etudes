# 999 Etudes

## To do

- [ ] Add additional templates for different score classes:
    - [✓] Percussion scores
- [ ] Settle on additional parameter sets for different score classes:
    - [ ] Percussion scores
    - [ ] "Easy" scores
    - [ ] "Hard" scores
- [ ] Tweak visual appearance of scores
- [ ] Settle on final text to be included at bottom of each score


## Description

This is a utility used to procedurally generate scores for short etudes.

The intended use is in generating large batches of etudes for "999 etudes", an "improvisation simulator" centering one-time-use disposable etudes which will be conspicuously destroyed after performance.

## Use

Running ``make.sh`` without any additional parameters will generate one score based on the parameters given in ``parameters.yaml``.

To generate multiple scores with the same set of parameters, provide the desired number, e.g. ``make.sh 5``.

Details pertaining to score generation will be printed in the console. Each score will be generated separately in a time-stamped directory, then merged into a final pdf.

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





