import os
import csv
def summary_to_csv(sec_uid='MS4wLjABAAAANDIHLwHtMrXJ5vukUYqhujOLhdBBkJg5qg__R9pb_Q4'):
    video_dir = f'data/{sec_uid}/'
    files = [i for i in os.listdir(video_dir) if i.endswith('.mp4')][:20]

    with open(f"{video_dir}{sec_uid}.csv","w") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["视频标题","视频主题","文字","主要内容","质量缺陷","品质口碑","汽车服务相关","汽车需求相关"])
        for video_file in files:
            video_prefix = video_file[0:-4]
            text_content = video_dir+video_prefix+'.txt'
            gpt_content = video_dir+'gpt-'+video_prefix+'.txt'
            with open(gpt_content,'r') as f:
                lines = f.readlines()
            lines = [i.strip() for i in lines if i.strip()]

            with open(text_content,'r') as f:
                text = f.readlines()
            text = ''.join(text)

            writer.writerow([video_prefix,
                             lines[0][5:],
                             text,
                             lines[1][7:],
                             lines[2][5:], 
                             lines[3][5:],
                             lines[4][7:],
                             lines[5][7:]
                            ])

if __name__ == '__main__':
    summary_to_csv('MS4wLjABAAAANDIHLwHtMrXJ5vukUYqhujOLhdBBkJg5qg__R9pb_Q4')