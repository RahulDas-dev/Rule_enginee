from xml_transformer import Loader
from jsonata import jsonata

data_path = "./data/sample/1af3f6c9-9010-4aa2-9488-7f54165f2dee.html"

loder = Loader.from_path(data_path)

loder.save_as_json("test.json")

expr = jsonata.Jsonata("$sch:InquiryResponseHeader.sch:CustomerCode")

result = expr.evaluate(loder.document)

print(result)
