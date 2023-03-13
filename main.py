import pandas as pd
import json


def read_types(type_file='invTypes.csv', group_file='invGroups.csv'):
    return pd.merge(
        pd.read_csv(type_file),
        pd.read_csv(group_file),
        on='groupID',
        how='inner',
    )[['typeID', 'typeName', 'groupID', 'groupName']]


def read_kills(filename='kill_dump.json'):
    # Load JSON File
    with open('kill_dump.json', 'r') as file:
        data = json.load(file)
    kills_df = pd.json_normalize(data)

    # Rename victim and killer columns
    kills_df = kills_df.drop(columns=['victim'])
    kills_df = kills_df.rename(columns={
        'victim.character_id'   : 'victim_character_id',
        'victim.corporation_id' : 'victim_corporation_id',
        'victim.alliance_id'    : 'victim_alliance_id',
        'victim.ship_type_id'   : 'victim_ship_type_id',
        'killer.character_id'   : 'killer_character_id',
        'killer.corporation_id' : 'killer_corporation_id',
        'killer.alliance_id'    : 'killer_alliance_id',
        'killer.ship_type_id'   : 'killer_ship_type_id',
    })

    # Expload attacker columns
    attackers_df = []
    for row in kills_df[['kill_id', 'attackers']].itertuples():
        for attacker in row.attackers:
            attackers_df.append({
                'kill_id'                 : row.kill_id,
                'attacker_character_id'   : attacker['character_id'],
                'attacker_corporation_id' : attacker['corporation_id'],
                'attacker_alliance_id'    : attacker['alliance_id'],
                'attacker_ship_type_id'   : attacker['ship_type_id'],
            })
    attackers_df = pd.DataFrame(attackers_df)
    kills_df = kills_df.merge(
        attackers_df,
        on='kill_id',
        how='left',
    )

    return kills_df


def main():
    types_df = read_types()
    kills_df = read_kills()

    # Find characters & ships involved in each battle
    battle_chars_df = pd.concat([
        kills_df[['battle_id', 'victim_character_id', 'victim_ship_type_id']].rename(columns={'victim_character_id':'character_id', 'victim_ship_type_id':'ship_type_id'}),
        kills_df[['battle_id', 'killer_character_id', 'killer_ship_type_id']].rename(columns={'killer_character_id':'character_id', 'killer_ship_type_id':'ship_type_id'}),
        kills_df[['battle_id', 'attacker_character_id', 'attacker_ship_type_id']].rename(columns={'attacker_character_id':'character_id', 'attacker_ship_type_id':'ship_type_id'}),
    ]).dropna(subset=['character_id']).drop_duplicates().reset_index(drop=True)

    # Get some basic stats out of all the battles.
    battle_stats_df = battle_chars_df.groupby('battle_id').character_id.nunique().reset_index().rename(columns={'character_id':'unique_character_count'})
    battle_stats_df = battle_stats_df.merge(
        kills_df[['battle_id', 'solarsystem_id']].drop_duplicates(),
        on='battle_id',
        how='left'
    )

    # Look at battles over 100 big
    battle_stats_df = battle_stats_df[battle_stats_df.unique_character_count >= 100]

    ship_stats_df = battle_chars_df[battle_chars_df.battle_id.isin(battle_stats_df.battle_id.unique())]
    ship_stats_df = ship_stats_df.merge(
        types_df.rename(columns={'typeID':'ship_type_id', 'groupID':'group_id', 'groupName':'group_name'}),
        on='ship_type_id',
        how='inner'
    )
    ship_stats_df = ship_stats_df.groupby(['group_id', 'group_name']).size().to_frame('group_count').reset_index().sort_values('group_count', ascending=False).reset_index(drop=True)    
    ship_stats_df['group_percent'] = ship_stats_df.group_count / ship_stats_df.group_count.sum() * 100

    print(f'There where {battle_stats_df.battle_id.nunique():,} battles with over 100 characters involved.')
    print(f'A breakdown of ship group involvement in those battles is as follows:')
    print(ship_stats_df)


if __name__ == '__main__':
    main()