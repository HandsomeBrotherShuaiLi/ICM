import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import tqdm
match_path='2020_Problem_D_DATA/matches.csv'
passings='2020_Problem_D_DATA/passingevents.csv'
fullevents='2020_Problem_D_DATA/fullevents.csv'
def draw_graph():
    fp=pd.read_csv(passings)
    matchID=list(set(fp['MatchID']))
    for id in tqdm.tqdm(matchID,total=len(matchID)):
        match_passing=fp[fp.MatchID==id]
        all_team_id=set(match_passing['TeamID'])
        for team_id in all_team_id:
            graph=nx.DiGraph()
            sub_matching=match_passing[match_passing.TeamID==team_id]
            edges_label={}
            for index in sub_matching.index:
                team_id=match_passing.loc[index,'TeamID']
                original_coord=(match_passing.loc[index,'EventOrigin_x'],match_passing.loc[index,'EventOrigin_y'])
                dst_coord=(match_passing.loc[index,'EventDestination_x'],match_passing.loc[index,'EventDestination_y'])
                original_id=match_passing.loc[index,'OriginPlayerID']
                dst_id=match_passing.loc[index,'DestinationPlayerID']
                match_period=match_passing.loc[index,'MatchPeriod']
                match_time=match_passing.loc[index,'EventTime']
                type=match_passing.loc[index,'EventSubType']
                graph.add_nodes_from([
                    (original_id,{'id':original_id,'coord':original_coord,'team_id':team_id,'match_time':match_time,'match_period':match_period}),
                    (dst_id,{'id':dst_id,'coord':dst_coord,'team_id':team_id,'match_time:':match_time,'match_period':match_period})
                ])
                edges_label[(original_id,dst_id)]="{}".format(match_time)
                graph.add_edge(original_id,dst_id)
            nx.draw(graph,pos=nx.spring_layout(graph),with_labels=True,font_color='black',node_color='pink',
                    font_size=7)
            # nx.draw_networkx_edge_labels(graph,pos=nx.spring_layout(graph),edge_labels=edges_label,font_size=3,font_weight='bold',
            #                              font_color='green')
            plt.title('macthID_{}_teamID_{} passing graphs'.format(id,team_id))
            plt.savefig('passing_graphs/macthid_{}_teamid_{}_passing_graphs.png'.format(id,team_id),dpi=200)
            plt.close()
            graph.clear()

def draw_full_events_ball_count():
    fp=pd.read_csv(fullevents)
    match_ID=set(fp['MatchID'])
    for id in tqdm.tqdm(match_ID,total=len(match_ID)):
        match_ball_graph=fp[fp.MatchID==id]
        all_team_id=set(match_ball_graph['TeamID'])
        if len(list(all_team_id))!=2:
            raise ValueError('team error!')
        




if __name__=='__main__':
    draw_graph()