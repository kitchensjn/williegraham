import glob
from PIL import Image, IptcImagePlugin

dataFile = open("../../_data/gallery-metadata.tsv", "w")

dataFile.write("path\ttpath\ttwidth\ttheight\ttitle\tlocation\theadline\tdescription\tcreator\tcity\tstate\tcountry\tcopyright\tcategories\n")

images = glob.glob("../images/gallery/*")
for image in images:
    img = Image.open(image)
    iptc = IptcImagePlugin.getiptcinfo(img)

    empty = "".encode()

    #date = None
    #if iptc.get((2, 55), "") != "":
    #    date = iptc[(2, 55)].decode()
    #    date = "-".join([date[:4], date[4:6], date[6:]])

    path=image.replace("..", "assets")
    title=iptc.get((2, 5), empty).decode().replace('"', "")
    location=iptc.get((2, 92), empty).decode()
    if location == "Wye Greenhouse":
        continue
    headline=iptc.get((2, 105), empty).decode()
    description=iptc.get((2, 120), empty).decode().replace("\r\r", " ").replace('<"\\r">', "").replace('"', "")#.replace("f'", "'").replace("\r\n", " ").replace("\n", " ")
    if "Henry Lafayette Warren" in description:
        headline = headline[:-1]
    creator=iptc.get((2, 122), empty).decode()
    city=iptc.get((2, 90), empty).decode()
    state=iptc.get((2, 95), empty).decode()
    country=iptc.get((2, 101), empty).decode()
    copyright=iptc.get((2, 116), empty).decode()
    encoded_categories=iptc.get((2, 25), empty)
    categories = []
    for cat in encoded_categories:
        if type(cat) != int:
            categories.append(cat.decode().lower())
        else:
            categories.append(str(cat))
    
    img.thumbnail((300,img.size[1]*(300/img.size[0])))
    thumbnail_width = str(img.size[0])
    thumbnail_height = str(img.size[1])
    thumbnail_path = path.replace("gallery", "thumbnails")
    img.save(thumbnail_path.replace("assets", ".."))

    #if location == "Gripsholm Castle":
        #print("path", path)
        #print("tpath", thumbnail_path)
        #print("twidth", thumbnail_width)
        #print("theight", thumbnail_height)
        #print("loc", location)
        #print("headline", headline)
        #print("desc", description)
        #print("creator", creator)
        #print("city", city)
        #print("state", state)
        #print("country", country)
        #print("copy", copyright)
        #print()
    dataFile.write("\t".join([path,thumbnail_path,thumbnail_width,thumbnail_height,title,location,headline,description,creator,city,state,country,copyright,",".join(categories)]) + "\n")

dataFile.close()
    
