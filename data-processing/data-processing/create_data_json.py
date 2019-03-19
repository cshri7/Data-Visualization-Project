import pandas as pd

df = pd.read_csv('combined.csv')

##
## number of questions answered by memberjob for a perticular topic
##

def numAnsweredByJobandTopic(memberjobId, topicId):
    return sum(df[df["memberJob"] == memberjobId]["topicId"] == topicId)
	
from collections import Counter
def numAnsweredByJobandTopic(memberjobId, topicId):
    return sum(df[df["memberJob"] == memberjobId]["topicId"] == topicId)

def topJobIdAnsweringQuesByTopic(topicId):
    d = {}
    for job in df["memberJob"].unique():
        if job != job:
            continue
        val = numAnsweredByJobandTopic(job, topicId)
        d[job] = val
        c = Counter(d)
        result = []
        for k,v in c.most_common(5):
            r = {}
            r["name"] = k
            r["size"] = str(v)
            result.append(r)
    return result
	
d = {}
for topic in df["topicId"].unique():
    d[topic] = topJobIdAnsweringQuesByTopic(topic)
	
import json
with open('topMemberJobAnsweringQuestionByTopic.txt', 'w') as outfile:
    json.dump(d, outfile)
	

##
## top job locations answering questions
##	

from collections import Counter
def numAnsweredByJobLocationandTopic(memberWorkplace, topicId):
    return sum(df[df["memberWorkplace"] == memberWorkplace]["topicId"] == topicId)

def topJobLocationAnsweringQuesByTopic(topicId):
    d = {}
    for location in df["memberWorkplace"].unique():
        if location != location:
            continue
        val = numAnsweredByJobLocationandTopic(location, topicId)
        d[location] = val
        c = Counter(d)
        result = []
        for k,v in c.most_common(10):
            r = {}
            r["name"] = k
            r["size"] = str(v)
            result.append(r)
    return result
	
d = {}
for topic in df["topicId"].unique():
    d[topic] = topJobLocationAnsweringQuesByTopic(topic)
	
import json
with open('topJobLocationAnsweringQuesByTopic.txt', 'w') as outfile:
    json.dump(d, outfile)
	
	
##
## top job locations answering questions
##	

def topUsersAnsweringQuestionByTopic(topicId):
    data = df[df["topicId"] == topicId][["memberName", "memberHelpfulVotes"]].groupby(["memberName"]).sum().reset_index().sort_values(by=['memberHelpfulVotes'], ascending=False)[:5]
    result = []
    for i in range(len(data)):
        d = {}
        name = data.iloc[i].memberName
        votes = data.iloc[i].memberHelpfulVotes
        d["name"] = name
        d["vote"] = str(votes)
        result.append(d)
    return result
	
d = {}
for topic in df["topicId"].unique():
    d[topic] = topUsersAnsweringQuestionByTopic(topic)
	
import json
with open('topUsersAnsweringQuestionByTopic.txt', 'w') as outfile:
    json.dump(d, outfile)
	
	
##
## questions by topic
##		
	
def questionsByTopic(topicId):
    data = df[df["topicId"] == topicId][["questionURL", "questionTitle"]].drop_duplicates(["questionURL", "questionTitle"])
    result = []
    for i in range(len(data[:20])):
        d = {}
        d["questionURL"] = data.iloc[i].questionURL
        d["questionTitle"] = data.iloc[i].questionTitle
        result.append(d)
    return result
	
	
d = {}
for topic in df["topicId"].unique():
    d[topic] = questionsByTopic(topic)
	
	
import json
with open('questionsByTopic.txt', 'w') as outfile:
    json.dump(d, outfile)
	
	
##
## calculate similarity
##			
	
df_test = df[["topicId","questionTopicId", "questionId"]].drop_duplicates(["topicId","questionTopicId", "questionId"]).dropna(how="any")

df_test.topicId = df_test.topicId.astype(str)
df_test.questionTopicId  = df_test.questionTopicId.astype(str)

df_test1 = pd.DataFrame(df_test.groupby('topicId')['questionTopicId'].apply(','.join).reset_index())


def func(x):
    return x.replace(",", "")
	
df_test1["questionTopicId"] = df_test1["questionTopicId"].apply(func)

from sklearn.feature_extraction.text import TfidfVectorizer
v = TfidfVectorizer()
df_test1['questionTopicId'] = list(v.fit_transform(df_test1['questionTopicId']).toarray())

from sklearn.neighbors import KNeighborsClassifier
neigh = KNeighborsClassifier(n_neighbors=41, metric='cosine')
neigh.fit(list(df_test1['questionTopicId']), list(df_test1['topicId'])) 

d = {}
for topic in list(df_test1['topicId']):
    distances, neighbors = neigh.kneighbors(list(df_test1[df_test1['topicId'] == topic]['questionTopicId']))
    arr = []
    for i in range(1,21):
        n_d = {}
        n_d["axis"] = lst[neighbors[0][i]]
        n_d["value"] = 1 - distances[0][i]
        if n_d["value"] > 0.25:
            arr.append(n_d)
    d[topic] = arr
	
	
import json
with open('similarity.txt', 'w') as outfile:
    json.dump(d, outfile)
	
##
## Find top users answering question.
##	

d = {}
for topic in list(df_test1['topicId']):
    n_d = topUsersAnsweringQuestionByTopic(topic)
    d[topic] = n_d
	
import json
with open('topUsersAnsweringQuestionByTopic.txt', 'w') as outfile:
    json.dump(d, outfile)
	
def questionsByTopic(topicId):
    data = df[df["topicId"] == topicId][["questionURL", "questionTitle"]].drop_duplicates(["questionURL", "questionTitle"])
    return len(data)
	
	
##
## Find topics and count
##	
	
df_test = df[["questionURL", "questionTitle","topicId","topicName"]]

df_test = df_test.drop_duplicates(["questionURL", "questionTitle"])

df_test = df_test.groupby(["topicId","topicName"]).count().reset_index()

result = []
for i in range(len(df_test)):
    data = {}
    data['topicId'] = df_test.iloc[i].topicId
    data['topicName'] = df_test.iloc[i].topicName
    data['questionCount'] = int(df_test.iloc[i].questionURL)
    result.append(data)
	
import json
with open('topicAndCount.txt', 'w') as outfile:
    json.dump(d, outfile)
	

	
##
## create data for filter topics by date.
##	
	
	
df.set_index(keys='questionId', inplace=True)

df_test = pd.DataFrame(df['questionPostDate'].dropna(axis='index'))

df_t = df.join(df_test, how='inner', lsuffix='_left', rsuffix='_right')

df_t['questionPostDate'] = pd.to_datetime(df_t['questionPostDate_left'])

df_t1 = df_t[['topicId', 'topicName', 'questionPostDate']]

df_t1.to_csv('datesFiltered.csv')

df_date = pd.read_csv('datesFiltered.csv', parse_dates=['questionPostDate'])

mask = (df_date['questionPostDate'] > '2011-12-10') & (df_date['questionPostDate'] <= '2017-12-10')

df_result = pd.DataFrame(df_date[mask].groupby(['topicId']).size().reset_index())

df_result = df_result.sort_values(by=[0], ascending=False)[:8]

df_date = pd.read_csv('datesFiltered.csv', parse_dates=['questionPostDate'])

df_result = pd.DataFrame(df_date.groupby(['topicName', 'questionPostDate']).size().reset_index())

df_result = pd.read_csv('dateFiltered.csv', parse_dates=['questionPostDate'])

df_result = pd.read_csv('dateFiltered.csv', parse_dates=['questionPostDate'])

def filterTopicsByDate(start_date, end_date):
    mask = (df_result['questionPostDate'] > start_date) & (df_result['questionPostDate'] <= end_date)
    df_r = pd.DataFrame(df_result[mask].groupby(['topicId']).sum().reset_index())
    df_r = df_r[['topicId','0']]
    df_r = df_r.sort_values(by=['0'], ascending=False)[:10]
    result = []
    for i in range(len(df_r)):
        d = {}
        obj = df_r.iloc[i]
        d["topicId"] = obj.topicId
        d["size"] = obj['0']
        result.append(d)
    return result
	


