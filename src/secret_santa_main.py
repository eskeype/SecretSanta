import csv
import json
import smtplib
import ssl
import sys

from secret_santa_participant import Participant
from secret_santa_participant import get_matching

SSL_PORT = 465

SANTA_CREDENTIALS_FILE_NAME = "santa_credentials.json"
PARTICIPANTS_FILE_NAME = "squad.csv"

MESSAGE_SKELETON = """\
Subject: Secret Santa

Hi {0},

For this year's secret santa, you will be paired with {1}

Their email is: {2}
Their address is: {3}

Merry Christmas,

Santa Bot"""

TEST_MESSAGE_SKELETON = """\
Subject: Test Secret Santa Message

Hi All,

This is a message to confirm whether you were able to receive messages from my secret santa email address.

Hopefully this doesn't end up in your spam.

TEST CODE: {0}

- Santa Bot"""


def get_santa_credentials(file_name=SANTA_CREDENTIALS_FILE_NAME):
    credentials = json.loads(open(file_name, 'r').read())
    return (credentials['sender_address'], credentials['sender_password'])


def get_message(gift_giver, gift_receiver):
    return MESSAGE_SKELETON.format(
        gift_giver.get_name(),
        gift_receiver.get_name(),
        gift_receiver.get_email(),
        gift_receiver.get_address())


def get_participants(file_name=PARTICIPANTS_FILE_NAME):
    participants = []

    with open(file_name, 'r') as participants_file:
        reader = csv.reader(participants_file)

        # discard field names - columns will be hard coded
        next(reader)

        for row in reader:
            participants.append(Participant(row[0], row[1], row[2]))
    return participants


def get_participant_messages(participants):

    matching = get_matching(participants)
    participant_messages = {}
    for gift_giver, gift_receiver in matching.items():
        participant_messages[gift_giver] = get_message(
            gift_giver, gift_receiver)

    return participant_messages


def get_test_participant_messages(participants, test_message):
    return {participant: test_message for participant in participants}


def main():
    participants = get_participants()

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        participant_messages = get_test_participant_messages(
            participants, TEST_MESSAGE_SKELETON.format(1))
    else:
        participant_messages = get_participant_messages(participants)

    ssl_context = ssl.create_default_context()
    santa_email, santa_password = get_santa_credentials()

    with smtplib.SMTP_SSL('smtp.gmail.com', SSL_PORT, context=ssl_context) as server:
        server.login(santa_email, santa_password)
        for participant, message in participant_messages.items():
            server.sendmail(santa_email, participant.get_email(), message)


if __name__ == '__main__':
    main()
