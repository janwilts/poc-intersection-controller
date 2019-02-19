import sys
import os
from dotenv import load_dotenv
from mq.publisher import Publisher
from mq.subscriber import Subscriber
from intersection.intersection import Intersection
from intersection.user_type import UserType

GROUP_IDS = {
    UserType.FOOT: [],
    UserType.CYCLE: [1, 2],
    UserType.MOTOR_VEHICLE: [1, 2, 3, 4, 5, 6, 7],
    UserType.PUBLIC_SERVICE_VEHICLE: [],
    UserType.VESSEL: [1],
}


def main(argv):
    # Load environment variables from .env file
    load_dotenv()

    intersection = Intersection(GROUP_IDS)
    print(intersection.light_topics)

    # Set up subscriber
    subscriber = Subscriber(os.getenv('SUBSCRIBER_ID'), os.getenv('SUBSCRIBER_HOST'), int(os.getenv('SUBSCRIBER_PORT')))

    # Set up publisher
    publisher = Publisher(os.getenv('PUBLISHER_ID'), os.getenv('PUBLISHER_HOST'), int(os.getenv('PUBLISHER_PORT')))

    # Connecting
    subscriber.connect()
    publisher.connect()

    publisher.publish('test', 'test')


if __name__ == '__main__':
    main(sys.argv)
