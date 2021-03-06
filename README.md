E-research lab
==============

This tool is a prototype for exploring multimodal alignment between a
scientific article and the video recording of its presentation in a
conference.

Author
------

This is a work done by
[Matthieu Riou](https://github.com/Matthieu-Riou/) in the context of a
L3 Internship at LINA, Nantes, coached by
[Olivier Aubert](https://github.com/oaubert/), Colin de la Higuera and
Solen Quiniou.

Prototypes
----------

The `interfaces/` folder contains several prototypes:

- `interface/` − *PDF article* and  *talk video* joint navigation
- `visualisation/` − *PDF article* and  *talk video* alignment
- `evaluation/` and `evaluation_developpeur/` − evaluator for the alignment prototype
- `alignement_global/` − investigations on global alignment contraints
- `pdf/` − paragraph delimitation prototype

The website is live at http://alignement.comin-ocw.org/

Processing pipeline
-------------------

The `script/` folder contains python & bash scripts to extract text from PDFs and handle alignment with video transcripts.
