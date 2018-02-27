import csv, traceback, json 
from hypothesis import Hypothesis
from collections import defaultdict 

h = Hypothesis(username='{USERNAME}', token='{TOKEN}')

def orderByFields(names):
    fields = 'project_id,report_id,report_title,report_url,report_date,media_content,media_url,report_status,report_author,time_delta_to_first_status,time_delta_to_last_status,time_original_media_publishing,type,contributing_users,tags,notes_count,notes_ugc_count,tasks_count,tasks_resolved_count,task_question_1,task_user_1,task_date_1,task_answer_1,task_note_1,task_question_2,task_user_2,task_date_2,task_answer_2,task_note_2,task_question_3,task_user_3,task_date_3,task_answer_3,task_note_3,task_question_4,task_user_4,task_date_4,task_answer_4,task_note_4,task_question_5,task_user_5,task_date_5,task_answer_5,task_note_5,task_question_6,task_user_6,task_date_6,task_answer_6,task_note_6,task_question_7,task_user_7,task_date_7,task_answer_7,task_note_7,task_question_8,task_user_8,task_date_8,task_answer_8,task_note_8,task_question_9,task_user_9,task_date_9,task_answer_9,task_note_9,task_question_10,task_user_10,task_date_10,task_answer_10,task_note_10,task_question_11,task_user_11,task_date_11,task_answer_11,task_note_11,task_question_12,task_user_12,task_date_12,task_answer_12,task_note_12,task_question_13,task_user_13,task_date_13,task_answer_13,task_note_13,task_question_14,task_user_14,task_date_14,task_answer_14,task_note_14,task_question_15,task_user_15,task_date_15,task_answer_15,task_note_15,task_question_16,task_user_16,task_date_16,task_answer_16,task_note_16,task_question_17,task_user_17,task_date_17,task_answer_17,task_note_17,task_question_18,task_user_18,task_date_18,task_answer_18,task_note_18,task_question_19,task_user_19,task_date_19,task_answer_19,task_note_19,task_question_20,task_user_20,task_date_20,task_answer_20,task_note_20,task_question_21,task_user_21,task_date_21,task_answer_21,task_note_21,task_question_22,task_user_22,task_date_22,task_answer_22,task_note_22,task_question_23,task_user_23,task_date_23,task_answer_23,task_note_23,task_question_24,task_user_24,task_date_24,task_answer_24,task_note_24,note_date_1,note_user_1,note_content_1,task_question_25,task_user_25,task_date_25,task_answer_25,task_note_25'.split(',')
    orderedList = []
    for fieldName in fields:
        if fieldName in names:
            orderedList.append(fieldName)
    return orderedList

headerTemplate = """<p>
<i>Checked at {report_url}</i>
</p>
<hr>
"""

questionTemplate = """<p>{question}</p>"""

multiAnswerTemplate = """<p><ul>{answers}</ul></p>"""

singleAnswerTemplate = """<li>{answer}</li>"""

targets = [
    'https://www.usatoday.com/story/news/nation-now/2017/06/16/coconut-oil-isnt-healthy-its-never-been-healthy/402719001/',
    'https://www.independent.co.uk/news/world/asia/india-floods-bangladesh-nepal-deaths-millions-homeless-latest-news-updates-a7919006.html',
    'https://ewao.com/2017/08/16/johns-hopkins-researcher-releases-shocking-report-on-flu-vaccines/'
    ]

def createPayload(h, url, text):
    payload = {
        "uri": url,
        "group": h.group,
        "user": 'acct:' + h.username + '@hypothes.is',
        "permissions": h.permissions,
        "text": text,
        "document": {
           "title": [url]
        },
        "tags": ["CredcoTest"],
    }
    return payload

# check data in check.csv
def postCheckPagenotes():

    targetUrlResultsCheck = defaultdict(list)

    with open('check.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
 
        for record in reader:
            media_url = record['media_url']
            if media_url in targets:
                targetUrlResultsCheck[media_url].append(record)
            else:
             continue

        for media_url in targetUrlResultsCheck:

            print 'media_url %s' % media_url
       
            report_url = record['report_url']
            report_url = '<a href="{report_url}">{report_url}</a>'.format(report_url=report_url)
            report_date = record['report_date'][0:10]
            header = headerTemplate.format(report_url=report_url, report_date=report_date)

            results = targetUrlResultsCheck[media_url]

            questions = {}
            collatedAnswers = defaultdict(list)

            for result in results:
                keys = result.keys()
                keys = [key for key in keys if key is not None]
                _questions = [name for name in keys if 'question' in name]
                questionNames = orderByFields(_questions)
                _answers = [name for name in keys if 'answer' in name]
                answerNames = orderByFields(_answers)
                _users = [name for name in keys if 'user' in name]
                userNames = orderByFields(_users)

            for i in range(len(questionNames)):
                qname = questionNames[i]
                questions[qname] = result[qname]
                aname = answerNames[i]
                if result[aname]:
                    collatedAnswers[aname].append(result[aname])

            body = header

            for i in range(len(questionNames)):
                qname = questionNames[i]
                question = questions[qname]
                body += questionTemplate.format(question=question)
                aname = answerNames[i]
                answers = ''
                for collatedAnswer in collatedAnswers[aname]:
                    answers += singleAnswerTemplate.format(answer=collatedAnswer)

            body += multiAnswerTemplate.format(answers=answers)
            payload = createPayload(h, media_url, body)
            r = h.post_annotation(payload)
            print 'check %s' % r.status_code


# public editor data in publiceditor.json  
def postPublicEditorAnnotations():

    targetUrlResultsPublicEditor = defaultdict(list)

    with open('publiceditor.json', 'rb') as jsonfile:
        allAnnos = json.load(jsonfile)
        filteredAnnos = [anno for anno in allAnnos if anno['uri'] in targets]
        for anno in filteredAnnos:
            uri = anno['uri']
            targetUrlResultsPublicEditor[uri].append(anno)
        
    for targetUrl in targetUrlResultsPublicEditor.keys():
        annos = targetUrlResultsPublicEditor[targetUrl]
        for anno in annos:
            payload = createPayload(h, targetUrl, anno['text'])
            if 'selector' in anno['target'].keys():
                payload['target'] = [ anno['target'] ]
                r = h.post_annotation(payload)
                print 'pe %s' % r.status_code

def cleanup():
    annos = h.search_all({"user":"{USERNAME","tags":"CredcoTest"});
    for anno in annos:
        r = h.delete_annotation(anno['id'])
        print r.status_code

cleanup()

postCheckPagenotes()

postPublicEditorAnnotations()


                     


