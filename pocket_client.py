from pocket import Pocket, PocketException
import json


class PythonPocketAPI:
    POCKET = None

    def __init__(self, pocketJsonFile):
        with open(pocketJsonFile) as data_file:
            data = json.load(data_file)
            self.init_pocket(data['consumer_key'], data['access_token'])

    def init_pocket(self, consumer_key, access_token):
        self.POCKET = Pocket(
            consumer_key=consumer_key,
            access_token=access_token
        )

    def favourite(self, articles):
        for article in articles:
            self.POCKET.add(article)

        self.POCKET.commit()

    def favourite(self, articles, tags):
        for article in articles:
            for attempt in range(5):
                try:
                    self.POCKET.add(article, tags=tags)
                except Exception as e:
                    print(e)
                    print("Attempt: " + str(attempt) + "-----" + article)
                else:
                    break

        self.POCKET.commit()


def main():
    # Fetch a list of articles
    p = Pocket(
        consumer_key='<Your consumer key>',
        access_token='<Your access token>'
    )
    try:
        print(p.retrieve(offset=0, count=10))
    except PocketException as e:
        print(e.message)

    # Add an article
    p.add('https://pymotw.com/3/asyncio/')

    # Start a bulk operation and commit
    p.archive(1186408060).favorite(1188103217).tags_add(
        1168820736, 'Python'
    ).tags_add(
        1168820736, 'Web Development'
    ).commit()


if __name__ == '__main__':
    main()
