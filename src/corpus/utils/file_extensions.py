import urllib.request
import re

urls = ["https://www.file-extensions.org/filetype/extension/name/source-code-and-script-files",
        "https://www.file-extensions.org/filetype/extension/name/source-code-and-script-files/"
        "sortBy/visits/order/desc/page/2",
        "https://www.file-extensions.org/filetype/extension/name/source-code-and-script-files/"
        "sortBy/visits/order/desc/page/3",
        "https://www.file-extensions.org/filetype/extension/name/source-code-and-script-files/"
        "sortBy/visits/order/desc/page/4"]

for url in urls:
    f = urllib.request.FancyURLopener({}).open(url)
    content = f.read()

    with open("../../out/extensions.txt", "a") as output:
        content_str = str(content)
        extensions = re.findall(r'"\w{5}3">([a-zA-Z0-9]*)<\/\w{6}>', content_str)
        output.writelines(extension + ";" for extension in extensions)
