# hours app
### bottle app for recording hours worked
- `run.py` requires:
    - -p : port
    - -r : logging server address
- use `launcher.sh` to run with presets
- requires `config/crypto` for encrypting records
    - contains two 16-charater keys
    - separated by a newline
    - must match crypto file in the receiving server
- labels populated by `config/labels.txt`
- scss --> css transpiler script : `src/scss/transpiler.sh`
- hours stored under : `hours/`

