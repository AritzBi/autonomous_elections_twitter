import json, gzip, glob
for filename in glob.iglob('./corpus_new/*.txt.gz'):
    with gzip.open(filename, 'rb') as f:
        file_content = f.read()
        file_content = file_content.split('\n')
        print(len(file_content))
        print filename
        if len(file_content) > 1:
            del file_content[-1]
            print len(file_content)
            tuit = json.loads(file_content[100])
            print tuit
