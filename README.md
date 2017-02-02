----

<a name="running"></a>
####Running :
- the server will run continuously in a terminal
- use `run.sh` to start the server (runs command: `/usr/bin/env python app.py -p 8080`)
    - to specify an alternate port: `./run.py PORT=<port>`
- `Makefile` contains useful commands for running the server and manipulating server files
    - `make run` is an alternate way to start the server (also accepts `PORT=<port>`)
    - `make debug` will run the server in debug mode and display additional console messages
- full list of arguments available for `app.py`:
    - `-p <port>`
    - `-d` : debug mode
    - `-r` : automatic reloading on-change to `app.py`
- configuration file `config/settings` : establishes SMTP emailing and remote-host logging
    - should contain newline-separated fields in the format: `name=value`
    - email (necessary for being able to send records via SMTP):
        - SMTP sender: `sender=foo`
        - SMTP reciever: `receivers=foo,bar`
    - remote logging (optional here, see section "Remote Host Logging") :
        - server address: `loggingServerAddress=0.0.0.0`
        - server port: `loggingServerPort=1234`

----

<a name="installation"></a>
####Installation :
- CentOS version : `cat /etc/redhat-release`
- **CentOS 7** :
    - make sure wget is installed : `rpm -qa wget` ? : `sudo yum install wget`
    - get the installer file : `wget https://raw.githubusercontent.com/zamalchi/installers/master/hoursapp/centos7-hoursapp-installer.sh ; chmod +x centos7-hoursapp-installer.sh`
    - run : `./centos7-hoursapp-installer.sh ~/path/to/install` (example path: `~/apps/hours`)
- **CentOS 6.8** (wip) :
    - run : `sudo yum install epel-release`
    - run : `wget https://ius.io/GettingStarted/ | rpm -i`
    - run : `sudo yum install python27-pip`
    - run : `sudo pip2.7 install --upgrade pip`
    - run : `sudo pip2.7 install markdown`
    - run : `sudo pip2.7 install pycrypto`
    - run : `chmod +x installers/centos6-8_install_python2-7.sh ; sudo ./installers/centos6-8_install_python2-7.sh`
        - original source : [Centos 6.8 install](https://gist.github.com/xuelangZF/570caf66cd1f204f98905e35336c9fc0)
    - run : `yum install -y python-pip`
- [Centos 6.3 install](https://github.com/h2oai/h2o-2/wiki/installing-python-2.7-on-centos-6.3.-follow-this-sequence-exactly-for-centos-machine-only)
- [Centos 6/7 install](http://tecadmin.net/install-python-2-7-on-centos-rhel/)

----

<a name="usage"></a>
####Usage:
- run the server
- go to : `localhost:<port>/hours` in the browser (`<port>` preset is 8080)
- top controls :
    - subtotals : pay period ends on the 25th of the month (and running subtotal is reset)
        - running subtotal saved under `hours/` in the format `YY-MM-subtotal-name`
    - pull records :
        - sets the date used for recording the hours (defaults to the current date)
        - if a file with the name and date exists, it will pull it up from `hours/`
    - raw : displays formatted plaintext of the current records (in chronological order)
    - delete : deletes all records for the current date
    - email : emails records for the current date
        - uses sender/receivers information pulled from `config/settings`
        - sends subject line in format : `Hours MM-DD (Subtotal: XX.XX)`
    - send : sends the records for the current date to a remote host
        - address and host are pulled from `config/settings` if present
        - address and port can be manually changed
        - requires that the crypto app is running on the remote host (see section "Remote Host Logging")
- new record form :
    - name : username
    - start/end time :
        - 24-hour time
        - round to nearest quarter-hour mark
        - if the start/end time overlaps with an adjacent record, the adjacent record will be adjusted
    - end time :
        - if not supplied, the result will be an incomplete record
    - label : select one of the dropdown options (manually-typed label must match an option)
    - notes : a description of the work done
    - duration : optional field for manually setting the duration of a record
    - billable/emergency : automatically set when choosing a label
    - add record : enter key will also submit the form
- record list :
    - down-arrow : open a form for inserting another record **before**
    - x : double-click to delete the record
    - to finish an incomplete record :
        - manually enter the end time
        - click enter in the end-time field (will auto-complete with the current rounded time)
        - add a new record (the new record's start time will be used)
    - billable/emergency : toggles
    - notes : change text by hitting enter within the field

----

<a name="remote-host-logging"></a>
#### Remote Host Logging :
- secondary method of storing hours
- not necessary in order to use the app
- requires : `sshuttle` to be connecting to the remote host
- requires : an instance of the companion [crypto app](https://github.com/zamalchi/crypto-app) on the remote host
- sources file : `config/crypto` for keys to use in encrypting and decrypting records
    - the file must contains two lines ; each of which must have a 16-character key
    - the keys must match the ones you use in the crypto app on the remote host

----

<a name="misc"></a>
#### Misc :
- hours stored under : `hours/`
    - file name format : `YY-MM-DD-name`
- labels populated by `config/labels.txt`
- scss --> css transpiler script : `src/scss/transpiler.sh`
    - `make scss` and `make scss-watch` will also transpile scss code

<a href="#top">
    <div style="background-color: lightgrey; position: fixed; right: 0; top: 0; border: 2px solid black; border-radius: 3px;">
        <span class="glyphicon glyphicon-arrow-up" style="padding: 15px"></span>
    </div>
</a>
