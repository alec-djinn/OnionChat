from configparser import SafeConfigParser
import sys
import uuid

if len(sys.argv) > 3:
    print("""
Nodotjs may be invoked with a single argument, telling it
which mode from `config.ini` to use:

python nodotjs/server.py <MODE>

You may additionally specify the config path by supplying a config.ini path:

python nodotjs/server.py <MODE> <CONFIG_PATH>

Look at `config.ini` for defined modes. Defaults are `production`,
`staging`, and `test`.""")
    exit(1)

MODE = sys.argv[1]

if len(sys.argv) > 2:
    CONFIG_PATH = sys.argv[2]
else:
    CONFIG_PATH = 'config.ini'

print(CONFIG_PATH)

PARSER = SafeConfigParser()

if not len(PARSER.read(CONFIG_PATH)):
    print("No config.ini file found in this directory.  Writing a config...")

    modes = ['production', 'staging', 'test']
    for i in range(0, len(modes)): # ew redis dbs made me loop like this
        mode = modes[i]
        PARSER.add_section(mode)
        PARSER.set(mode, 'db', str(i))
        PARSER.set(mode, 'cookie_secret', str(uuid.uuid4()))
        PARSER.set(mode, 'timeout', '30')
        PARSER.set(mode, 'port', '7000')
        PARSER.set(mode, 'templates_dir', './templates')

    try:
        conf = open(CONFIG_PATH, 'w')
        PARSER.write(conf)
        conf.close()
    except IOError:
        print("Could not write config file to `config.ini`, exiting...")
        exit(1)

DB = int(PARSER.get(MODE, 'db'))
COOKIE_SECRET = PARSER.get(MODE, 'cookie_secret')
TIMEOUT = int(PARSER.get(MODE, 'timeout'))
PORT = int(PARSER.get(MODE, 'port'))
TEMPLATES_DIR = PARSER.get(MODE, 'templates_dir')