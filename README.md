# Facebook Log Extractor

This program finds and opens all HTML files in the same directory. It then creates a folder with the same name as the file and places text files in it. The one named `_onefile` will output only one text file with the user's first names before the respective message. `_messenger` works on HTML files requested from Facebook specifically from Messenger (I'm not sure exactly how you get either of these formats). In more concrete terms:
* `_all` works for HTML files where the user's name is between `<span class="user">` and `</span>`
* `_messenger` is for files where they are seperated by `<div class="_3-96 _2pio _2lek _2lel">` and `</div><div class="_3-96 _2let">`

# Usage:

* Place HTML file(s) in the same folder as the program
* Run it