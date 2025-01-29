import itertools
import collections

from clldutils.misc import nfilter
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from clldutils.misc import slug
from nameparser import HumanName

from pycldf import Sources


import cmzz
from cmzz import models


def main(args):
    data = Data()
    ds = data.add(
        common.Dataset,
        cmzz.__name__,
        id=cmzz.__name__,
        name="Cáo Mó Zhī Zhèn 曹沫之陳",
        domain='cmzz.digling.org',

        publisher_name = "University of Passau",
        publisher_place = "Passau",
        publisher_url = "https://uni-passau.de",
        license = "http://creativecommons.org/licenses/by/4.0/",
        jsondata = {
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'},

    )

    for i, name in enumerate(['Michele Pulini', 'Johann-Mattis List']):
        common.Editor(
            dataset=ds,
            ord=i,
            contributor=common.Contributor(id=slug(HumanName(name).last), name=name)
        )


    contrib = data.add(
        common.Contribution,
        "Cáo Mó Zhī Zhèn 曹沫之陳",
        id='cldf',
        name=args.cldf.properties.get('dc:title'),
        description=args.cldf.properties.get('dc:bibliographicCitation'),
    )

    svg_snippet = """
<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="{0}">
  <image x="0" y="0" width="{2}" height="{3}" href="http://127.0.0.1:6543/static/media/{1}.jpg" />
</svg>
"""


    for lang in args.cldf.iter_rows('LanguageTable', 'id', 'glottocode', 'name', 'latitude', 'longitude'):
        data.add(
            models.Variety,
            lang['id'],
            id=lang['id'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            glottocode=lang['glottocode'],
        )

    chinese = data.add(
        common.Language, 'zhn',
        id='chin',
        name='Chinese')
    
    examples = {}
    values = collections.defaultdict(list)
    for entry in args.cldf.iter_rows(
            "ExampleTable", "id", "Analyzed_Word", "gloss", "Translated_Text", "Text_Unit", "Word_IDS",
            "Middle_Chinese_Reading", "Old_Chinese_Reading", "Character_IDS",
            "IDS_in_Source"
            ):
        examples[entry["id"]] = entry 
        idx = 0
        images = []
        for i, wordid in enumerate(entry["Word_IDS"]):
            try:
                if len(entry["Analyzed_Word"][i]) == 1:
                    images += [entry["Character_IDS"][idx]]
                    idx += 1
                else:
                    new_image = []
                    for j in range(len(entry["Analyzed_Word"][i])):
                        new_image += [entry["Character_IDS"][idx]]
                        idx += 1
                    images += ["//".join(new_image)]
            except:
                print(entry["Analyzed_Word"])
                print(entry["Character_IDS"])

        if len(images) != len(entry["Analyzed_Word"]):
            print(images)
            images = images + ["?" for x in entry["Analyzed_Word"]]
        for i in range(len(entry["Analyzed_Word"])):
            if entry["Word_IDS"][i] and entry["Middle_Chinese_Reading"][i]:
                values[entry["Word_IDS"][i]] += [{
                        "word": entry["Analyzed_Word"][i],
                        "gloss": entry["gloss"][i],
                        "middle_chinese": entry["Middle_Chinese_Reading"][i].replace("_", " "),
                        "old_chinese": entry["Old_Chinese_Reading"][i],
                        "phrase": entry["id"],
                        "image": images[i],
                        }]
    
    # get image data
    characters = {}
    images = {}
    for entry in args.cldf.iter_rows(
            "characters.csv", "ID", "Name", "Rectangle", "Image"):
        characters[entry["ID"]] = entry
    for entry in args.cldf.iter_rows(
            "images.csv", "ID", "Path", "Height", "Width"):
        images[entry["ID"]] = entry

    for key, data_ in characters.items():
        viewbox = []
        for itm in data_["Rectangle"].split(","):
            viewbox += [itm.split("=")[1]]
    
        data_["svg"] = svg_snippet.format(
                " ".join(viewbox),
                data_["Image"],
                images[data_["Image"]]["Width"],
                images[data_["Image"]]["Height"]).replace("\n", "")

    for entry in args.cldf.iter_rows(
            "EntryTable", "id", "headword",
            "Middle_Chinese", "Old_Chinese", "Glosses", "Example_IDS"):
        #try:
        idx = entry["id"].split("-")[1]
        param = data.add(
                models.Words,
                idx,
                id=idx,
                name=entry["headword"],
                middle_chinese=entry["Middle_Chinese"],
                old_chinese=entry["Old_Chinese"],
                gloss=entry["Glosses"][0],
                occurrences=len(entry["Example_IDS"]),
                sentences=" ".join(entry["Example_IDS"]),
                #images=" ".join(images)
                )
        #except:
        #    print(entry["id"])
        #    param = False
        if param:
            for i, value in enumerate(values[entry["id"]]):
                vid = entry["id"] + "-" + str(i + 1)
                vs = common.ValueSet(
                        id=vid,
                        description="nada",
                        language=chinese,
                        parameter=param
                        )
                img = []
                if value["image"]:
                    for imgid in value["image"].split("//"):
                        if imgid in characters:
                            img += [characters[imgid]["svg"]]
                img = " ".join(img)
                data.add(
                        models.Examples,
                        vid,
                        id=vid,
                        word=value["word"],
                        gloss=value["gloss"],
                        valueset=vs,
                        middle_chinese=value["middle_chinese"],
                        old_chinese=value["old_chinese"],
                        phrase=value["phrase"],
                        image=img
                        )
    for k, entry in examples.items():
        images = []
        for idx in entry["Character_IDS"]:
            if idx in characters:
                images += [characters[idx]["svg"]]
            else:
                images += ["?"]

        example = data.add(
                models.Phrase,
                entry["id"],
                id=entry["id"],
                language=chinese,
                name=" ".join(entry["Analyzed_Word"]),
                description=" ".join(entry["gloss"]),
                middle_chinese=" ".join([itm if itm else "?" for itm in
                                         entry["Middle_Chinese_Reading"]]),
                old_chinese=" ".join([itm if itm else "?" for itm in entry["Old_Chinese_Reading"]]),
                images=" ".join(images)
                )





    #for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
    #    data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    #refs = collections.defaultdict(list)


    #for (vsid, sid), pages in refs.items():
    #    DBSession.add(common.ValueSetReference(
    #        valueset=data['ValueSet'][vsid],
    #        source=data['Source'][sid],
    #        description='; '.join(nfilter(pages))
    #    ))



def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
