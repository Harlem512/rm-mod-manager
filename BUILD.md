# Building RMM(L/M)

The distributed zip file is built using the following tools.

- Python
- [Katsaii's Python-based Catspeak tokenizer](https://raw.githubusercontent.com/katsaii/catspeak-lang/refs/heads/main/docs-gen/catlog/highlight.py), dropped into the root directory of the repo.
- Any python dependencies required to run `build.py`

Once everything is set up, execute `build.py` with Python. Artifacts will be created in the `build` directory and the final ZIP distributable will be in the `dist` folder, marked with the version numbers from RMML and RMMM.

# Other stuff

`transpiler.py` is a Python command line utility to convert between the `.md` and `.csv` mod formats.
