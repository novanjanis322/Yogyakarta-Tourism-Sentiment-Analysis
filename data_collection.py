import googleapiclient.discovery
import pandas as pd
import os
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = ""  # fill in with your API key
video_id = "I8hSL-t4G9s"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

next_page_token = None
comments = []
while True:
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100, 
        pageToken=next_page_token
    ).execute()
    comments.extend(response['items'])
    next_page_token = response.get('nextPageToken')
    if not next_page_token:
        break

comment_data = []

for item in comments:
    top_level_comment = item['snippet']['topLevelComment']['snippet']
    comment_data.append(top_level_comment)
    reply_response = youtube.comments().list(
        part='snippet',
        parentId=item['snippet']['topLevelComment']['id'],
        maxResults=100
    ).execute()
    for reply in reply_response['items']:
        comment_data.append(reply['snippet'])

df = pd.DataFrame(comment_data)

file_name = os.path.splitext(os.path.basename(__file__))[0]
df.to_csv(f'{file_name}.csv', index=False)

print(df)
