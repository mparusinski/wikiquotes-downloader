# wikiquotes-downloader

wikiquotes-downloader is a tool to download all quotes from a given philosopher using wikiquotes. 
To download all quotes from a given author (in this example Friedrich Nietzsche) do:

```
python DownloadQuotes.py --author "Friedrich Nietzsche"
```

The result will be a JSON object list all the quotes from Friedrich Nietzsche found on Friedrich Nietzsche's wikiquote page.
One can download from a list of authors using an external file. For instance

```
python DownloadQuotes.py --input authors.txt
```

the result will be one json object containing quotes from all the listed authors in the specified file.

Furthermore the content can be saved to a file using the syntax

```
python DownloadQuotes.py --input authors.txt --output output_file.json
```
