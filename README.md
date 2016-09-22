# hours app
### bottle app for recording hours worked
- `run.py` requires:
    - -p : port
- use `launcher.sh` to run with presets
- requires `config/crypto` for encrypting records
    - contains two 16-charater keys
    - separated by a newline
    - must match crypto file in the receiving server
- optional `config/settings` for establishing SMTP and logging
    - separated by newlines
    - `sender=foo`
    - `receivers=foo,bar`
    - `loggingServerAddress=0.0.0.0`
    - `loggingServerPort=1234`
- labels populated by `config/labels.txt`
- scss --> css transpiler script : `src/scss/transpiler.sh`
- hours stored under : `hours/`

