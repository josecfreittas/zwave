#--*-- conding: utf-8 --*--
import json
import zwave

config = json.loads(open("data/settings.json").read())
texts = json.loads(open("data/languages/%s.json" % config["language"]).read())

zwave.init(texts)
