import pandas as pd

df_member = pd.read_json('webmd-member.json', orient='records')

df_topic = pd.read_json('webmd-topics.json', orient='records')

# In[4]:

df_related_topic = pd.read_json('webmd-related_topic.json', orient='records')

# In[5]:

df_questions = pd.read_json('webmd-question.json', orient='records')

# In[6]:

df_answer = pd.read_json('webmd-answer.json', orient='records')

df_topic_related_topic = df_related_topic.merge(df_topic, left_on='topicId', right_on='topicId', how='inner')

# In[62]:

df_question_topic_related_topic = df_topic_related_topic.merge(df_questions, left_on='questionId', right_on='questionId', how='right')

# In[76]:

df_member_question_topic_related_topic = df_question_topic_related_topic.merge(df_member, left_on='questionMemberId', right_on='memberId', how='left')

# In[ ]:

df_question_topic_related_topic.merge(df_member, left_on='questionMemberId', right_on='memberId', how='left')

df_answer_member = df_answer.merge(df_member, left_on='answerMemberId', right_on='memberId', how='left')

df_question_topic_related_topic_answer_member = df_question_topic_related_topic.merge(df_answer_member, left_on="questionId", right_on="questionId", how="left")

df_question_topic_related_topic_answer_member.to_csv('combined.csv')