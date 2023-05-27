from riotwatcher import LolWatcher, ApiError
import riot_api_key 
import pandas as pd

# global variables
api_key = riot_api_key.api_key
watcher = LolWatcher(api_key)
my_region = 'na1'

# summoner_search = 'Doublelift'

def recent_matches(sum_name):
    me = watcher.summoner.by_name(my_region, sum_name)

    # check league's latest version
    latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']

    # static champions information
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

    # champ static list data to dict for looking up
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']

    champ_df = pd.DataFrame(champ_dict.items(), columns =['champion', 'champ_name'])

    champ_df['champion'] = champ_df['champion'].astype('int64')


    # Get last 20 Match ID's
    all_match_ids = watcher.match.matchlist_by_puuid(my_region, me['puuid'])

    participants = []
    match_counter = 0
    for id in all_match_ids:
        match_detail = watcher.match.by_id(my_region, id)
        for row in match_detail['info']['participants']:
            participants_row = {}
            participants_row['champion'] = row['championId']
            participants_row['spell1'] = row['spell1Casts']
            participants_row['spell2'] = row['spell2Casts']
            participants_row['win'] = row['win']
            participants_row['kills'] = row['kills']
            participants_row['deaths'] = row['deaths']
            participants_row['assists'] = row['assists']
            participants_row['totalDamageDealt'] = row['totalDamageDealt']
            participants_row['goldEarned'] = row['goldEarned']
            participants_row['champLevel'] = row['champLevel']
            participants_row['totalMinionsKilled'] = row['totalMinionsKilled']
            participants_row['item0'] = row['item0']
            participants_row['item1'] = row['item1']
            participants_row['summonerName'] = row['summonerName']
            participants_row['matchNumber'] = match_counter
            participants.append(participants_row)
        match_counter += 1

    all_matches = pd.DataFrame(participants)

    # bring in champion names
    all_matches = all_matches.merge(champ_df, on='champion',how="left")

    # last 20 matches for summoner search
    summoner_df = all_matches[all_matches['summonerName'] == sum_name]

    summoner_df = summoner_df.reset_index(drop=True)

    return summoner_df

def summoner_detail(sum_name):
    me = watcher.summoner.by_name(my_region, sum_name)
    ranked_stats = watcher.league.by_summoner(my_region, me['id'])
    sum_elo = ranked_stats[0]['tier'] + " " + str(ranked_stats[0]['leaguePoints']) + " LP"

    return sum_elo
