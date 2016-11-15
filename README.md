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
#### Fresh install:
- install `git` : `sudo yum install git`
- clone repo : `git clone https://github.com/zamalchi/hoursapp.git <dirname>`
- `cd <dirname>`
- CentOS 6.8 :
    - run : `sudo yum install epel-release`
    - run : `wget https://ius.io/GettingStarted/ | rpm -i`
    - run : `sudo yum install python27-pip`
    - run : `sudo pip2.7 install --upgrade pip`
    - run : `sudo pip2.7 install markdown`
    - run : `sudo pip2.7 install pycrypto`
    - run : `chmod +x installers/centos6-8_install_python2-7.sh ; sudo ./installers/centos6-8_install_python2-7.sh`
        - original source : [Centos 6.8 install](https://gist.github.com/xuelangZF/570caf66cd1f204f98905e35336c9fc0)
    - run : `yum install -y python-pip`

- install and run with `python2.7`
    - Centos version : `cat /etc/redhat-release`
    - [Centos 6.3 install](https://github.com/h2oai/h2o-2/wiki/installing-python-2.7-on-centos-6.3.-follow-this-sequence-exactly-for-centos-machine-only)
    - [Centos 6.8 install](https://gist.github.com/xuelangZF/570caf66cd1f204f98905e35336c9fc0) or use `sudo ./installers/centos6-8_install_python2-7.sh`
    - [Centos 6/7 install](http://tecadmin.net/install-python-2-7-on-centos-rhel/)
- configure : `config/settings`
    - example : `config/settings_example`
- configure : `config/crypto` (optional)
- run with `./launcher.sh` or `python2.7 run.py -p <port>`

