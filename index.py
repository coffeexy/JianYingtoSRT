# step0 files
#  read/create
# step1 JSON -> SRT
import os
import json

# step0 files
def getDrafts():
    rootDir = os.path.expanduser('~') + '/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/'
    drafts = []
    if os.path.exists(rootDir):
        for file in os.listdir(rootDir):
            if os.path.exists(rootDir + file + '/draft_info.json'):
                drafts.append({
                    'name': file,
                    'draftDir': rootDir + file + '/draft_info.json'
                })
    return drafts

# step1 JSON -> SRT
def parseSRT(text):
    index = 0
    srt = ''
    for item in text:
        index += 1
        srt += f'{index}' + '\n'
        srt += item['time'] + '\n'
        srt += item['content'] + '\n'
        srt += '\n'

    return srt

def formatSubtitle(sdir):
    with open(sdir, 'r') as fd:
        obj = json.loads(fd.read())
    # parse json
    texts = {}
    subtitles = []

    # get subtitle texts
    for item in obj['materials']['texts']:
        if(item['type'] == 'subtitle'):
            texts[item['id']] = item['content']
    # get subtitle time range
    for segs in obj['tracks']:
        for item in segs['segments']:
            if(item['material_id'] in texts.keys()):
                subtitles.append({
                    'content': texts[item['material_id']],
                    'time': ms2Str(item['target_timerange']['start']) + ' --> ' + ms2Str(item['target_timerange']['start'] + item['target_timerange']['duration'])
                })
    return subtitles

def ms2Str(t=0):
    t //= 1000
    ms = t % 1000
    s = t // 1000 % 60
    m = t // 1000 // 60 % 60
    h = t // 1000 // 60 // 60
    return '%02d:%02d:%02d,%03d' % (h, m, s, ms)

if __name__ == '__main__':
    drafts = getDrafts()
    if len(drafts) > 0:
        print('We found subtitles below:')
        for index, item in enumerate(drafts):
            print(f'{index}:', item['name'])
        index_result = input('Which one do you want to export: ')

        if(index_result.isdigit() and int(index_result)>=0 and int(index_result)<len(drafts)):
            draft = formatSubtitle(drafts[int(index_result)]['draftDir'])
            exportFolder = os.path.expanduser('~') + '/Desktop/' + drafts[int(index_result)]['name'] + '.srt'
            with open(exportFolder, 'w') as fd:
                fd.write(parseSRT(draft))
            
        else:
            print('Error')
    else:
        print('No subtitles found!')