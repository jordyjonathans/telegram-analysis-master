FROM python:3.9

ADD ChannelMessages.py .

RUN pip install telethon

CMD ["python", "./ChannelMessage.py"]