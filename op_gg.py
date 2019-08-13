import requests
import time
import datetime
from datetime import timedelta
import json
from fbchat import Client
from steam import SteamClient
from steam.enums.emsg import EMsg

KEY = "-----Riot developer API Key ------"
KAKAO_TOKEN = '------kakao api key token ------'

def get_ID(id):
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(id)
    headers= {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": KEY,
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Whale/1.5.73.16 Safari/537.36"
    }
    res = requests.get(url=url, headers=headers)
    return res.json()['id']


def search(id):
    url_ = "https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{}".format(id)
    headers_ = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": KEY,
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Whale/1.5.73.16 Safari/537.36"
    }

    cur_game = requests.get(url=url_, headers=headers_)
    return cur_game

def send_to_kakao(text):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    header = { "Authorization" : "Bearer " + KAKAO_TOKEN }
    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        }
    }
    data = {"template_object" : json.dumps(post)}
    return requests.post(url=url, headers=header, data=data)

def send_to_fb(fc, text):
    friends = fc.searchForUsers('------facebook id ------')
    friend = friends[0]
    sent = fc.sendMessage(text, thread_id = friend.uid)
    friends = fc.searchForUsers('---ex) 김철수 ----')
    friend = friends[0]
    sent = fc.sendMessage(text, thread_id = friend.uid)
    
def get_info(s_id, game_start_time):
    

    id = get_ID(s_id)
    
    cur_state = search(id)
    if( int(cur_state.status_code) == 200 ):
        tmp = cur_state.json()['gameStartTime']
        if( game_start_time[s_id] == tmp ):
            return
        f = open('playtime.txt', mode='a',encoding='utf-8')
        game_start_time[s_id] = tmp
        f.write('\n'+ s_id + (datetime.datetime.fromtimestamp(tmp/1000)).strftime('%Y-%m-%d %H:%M:%S.%f'))
        f.close()

        send_to_kakao("{}(이)가 롤을 시작하였습니다".format(s_id))
        send_to_fb(fc, "{}(이)가 롤을 시작하였습니다".format(s_id))
        
    #print(cur_state)


person = [('--lol summoner name --',0),('-- ex)skt t1 faker --',0)]  
game_start_time = dict(person)

fc = Client('-- facebook id--','-- facebook pw --')
i=0
while(True):
    get_info('-- lol summoner name --',game_start_time)
    
    # print(i)
    # i+=1
    # time.sleep(300)

# g_state = steam.client.user.SteamUser("PPinkK").state()
# print(g_state)   
    
# client = SteamClient()
# client.cli_login()
