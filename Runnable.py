import pycurl
from io import BytesIO
import json


class ApiCalls:
    """

    """
    def __init__(self,region,api_key):

        self.region = region
        self.api_key = api_key

    def get_api_data(self, url):
        """
        Gets data from riotAPI based on params
        :param url: suburl for the actual api call
        :return: contents of the api call as UTF-8 string
        """

        full_url = "https://{0}.api.riotgames.com/{1}&api_key={2}"
        usable_url = full_url.format(self.region,url,self.api_key)
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, usable_url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        body = buffer.getvalue().decode("utf-8")
        return body
    def update_static_file( self, file_path, url ):
        """
        Reloads data in a single persisting file by picking up data from the api call
        :param file_path: local path of the file to be reloaded
        :param url: suburl for the actual api call
        """
        data = self.get_api_data( url=url)
        file = open(file_path, mode="w")
        file.write(data)

    def update_static_files(self, champions_file_path, items_file_path, runes_file_path, summoner_spells_file_path):
        """
        updates all local files so those can be read from rather than use cashe to store all data consistently
        :param champions_file_path: path to the persisting json file for champions api data
        :param items_file_path: path to the persisting json file for items api data
        :param runes_file_path: path to the persisting json file for runes api data
        :param summoner_spells_file_path: path to the persisting json file for summoner spells api data
        :return:
        """

        #Update champions data
        print("updating champion data")
        champions_url = "lol/static-data/v3/champions?locale=en_US&tags=all&dataById=false"
        self.update_static_file(file_path=champions_file_path,url=champions_url)

        #update items data
        print("updating items data")
        items_url = "lol/static-data/v3/items?locale=en_US&tags=all&dataById=false"
        self.update_static_file(file_path=items_file_path,url=items_url)

        # update summoner spells data
        print("updating summoner spells data")
        summoner_spells_url = "lol/static-data/v3/summoner-spells?locale=en_US&tags=all&dataById=false"
        self.update_static_file(file_path=summoner_spells_file_path,url=summoner_spells_url)

        #update runes data
        print("updating runes data")
        runes_url = "lol/static-data/v3/runes?locale=en_US&tags=all&dataById=false"
        self.update_static_file(file_path=runes_file_path,url=runes_url)

def main():
    print("Gotta get some api")
    champions_file_path = "C:\\Users\\FDM Consultant\\Desktop\\LolAPI\\champions.json"
    items_file_path = "C:\\Users\\FDM Consultant\\Desktop\\LolAPI\\items.json"
    runes_file_path = "C:\\Users\\FDM Consultant\\Desktop\\LolAPI\\runes.json"
    summoner_spells_file_path = "C:\\Users\\FDM Consultant\\Desktop\\LolAPI\\summoner_spells.json"
    api_key = "RGAPI-253da375-582f-46ae-9a14-770e7b061089"
    region = "na1"


    api_calls = ApiCalls(region=region, api_key=api_key)
    api_calls.update_static_files(champions_file_path=champions_file_path,
                        items_file_path=items_file_path,summoner_spells_file_path=summoner_spells_file_path,
                        runes_file_path=runes_file_path)
    print("done")
main()