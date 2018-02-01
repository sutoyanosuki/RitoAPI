import pycurl
from io import BytesIO
import json

class DynamicChampion:

    def __init__(self):
        print("hi")


class StaticData:
    """
    Contains static data from the staticData api calls
    """

    def __init__(self, config, region):
        """
        will attemp to load the files into memory if present, otherwise will force api loads
        """
        api_key = config["connectivity"]["api_key"]
        apicall = ApiCalls(region, api_key)
        try:
            champions_file_path = config["file_paths"]["champions_file_path"]
            champions_file = open(champions_file_path)
            self.champions_json = json.load(champions_file)
        except:
            # if failed to load, rerun the api
            apicall.update_champions(champions_file_path)
        finally:
            champions_file.close()

        try:
            items_file_path = config["file_paths"]["items_file_path"]
            items_file = open(items_file_path, mode="r")
            self.items_json = json.load(items_file)
        except:
            # if failed to load, rerun the api
            apicall.update_items(items_file)
        finally:
            items_file.close()

        try:
            summoner_spells_file_path = config["file_paths"]["summoner_spells_file_path"]
            summoner_spells_file = open(summoner_spells_file_path, mode="r")
            self.summoner_spells_json = json.load(summoner_spells_file)
        except:
            # if failed to load, rerun the api
            apicall.update_champions(summoner_spells_file)
        finally:
            summoner_spells_file.close()

        try:
            runes_file_path = config["file_paths"]["runes_file_path"]
            runes_file = open(runes_file_path, mode="r")
            self.runes_json = json.load(runes_file)
        except:
            # if failed to load, rerun the api
            apicall.update_champions(runes_file_path)
        finally:
            runes_file.close()



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

    def update_champions(self,champions_file_path):
        # Update champions data
        print("updating champion data")
        champions_url = "lol/static-data/v3/champions?locale=en_US&tags=all&dataById=false"
        self.update_static_file(file_path=champions_file_path, url=champions_url)

    def update_items(self,items_file_path):
        # update items data
        print("updating items data")
        items_url = "lol/static-data/v3/items?locale=en_US&tags=all&dataById=false"
        self.update_static_file(file_path=items_file_path, url=items_url)

    def update_summoner_spells(self, summoner_spells_file_path):
        # update summoner spells data
        print("updating summoner spells data")
        summoner_spells_url = "lol/static-data/v3/summoner-spells?locale=en_US&tags=all&dataById=false"
        self.update_static_file(file_path=summoner_spells_file_path, url=summoner_spells_url)

    def update_runes(self,runes_file_path):
        # update runes data
        print("updating runes data")
        runes_url = "lol/static-data/v3/runes?locale=en_US&tags=all&dataById=false"
        self.update_static_file(file_path=runes_file_path, url=runes_url)

def main():
    print("Gotta get some api")

    # load the config
    config_file = open("C:\\Users\\FDM Consultant\\Desktop\\LolAPI\\config.json")
    config = json.load(config_file)
    config_file.close()

    region = "na1"

    last_selected_region = config["profile"]["last_selected_region"]
    if last_selected_region is None:

        user_input = input("select a region")
        if user_input not in config["region_list"]:
            #default to NA if no valid region given
            region = "na1"
        else:
            region = user_input
    else:
        region = last_selected_region

    print(region)

    #load the static data
    static_data = StaticData(config,region)
    # print(static_data.items_json)
    #
    #
    #
    # api_calls = ApiCalls(region=region, api_key=api_key)
    # api_calls.update_static_files(champions_file_path=champions_file_path,
    #                     items_file_path=items_file_path,summoner_spells_file_path=summoner_spells_file_path,
    #                     runes_file_path=runes_file_path)
    print("done")
main()