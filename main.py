#--*-- conding: utf-8 --*--
import json
import zwave

settings = json.loads(open("data/settings.json").read())
texts = json.loads(open("data/languages/%s.json" % settings["language"]).read())

zwave.init(texts, settings["scale"], settings["width"], settings["height"], settings["fullscreen"])
