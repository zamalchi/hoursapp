### README
#### `hours` : bottle app for recording hours worked
- `run.py` uses:
    - -p : port (required)
- use `launcher.sh` to run with presets
- optional `config/crypto` for encrypting records
    - contains two 16-charater keys
    - separated by a newline
    - must match crypto file in the receiving server
    - [crypto app repo](https://github.com/zamalchi/crypto-app)
- optional `config/settings` for establishing SMTP and logging
    - newline-separated fields in the format: `name=value`
    - SMTP sender: `sender=foo`
    - SMTP reciever: `receivers=foo,bar`
    - server address: `loggingServerAddress=0.0.0.0`
    - server port: `loggingServerPort=1234`
- labels populated by `config/labels.txt`
- scss --> css transpiler script : `src/scss/transpiler.sh`
- hours stored under : `hours/`

