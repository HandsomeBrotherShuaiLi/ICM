import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
def draw_graph():
    match_path='2020_Problem_D_DATA/matches.csv'
    passings='2020_Problem_D_DATA/passingevents.csv'
    fullevents='2020_Problem_D_DATA/fullevents.csv'
    fp=pd.read_csv(passings)
    matchID=list(set(fp['MatchID']))
    for id in matchID:
        match_passing=fp[fp.MatchID==id]
        all_team_id=set(match_passing['TeamID'])
        graph=nx.DiGraph()
        for team_id in all_team_id:
            sub_matching=match_passing[match_passing.TeamID==team_id]
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
                graph.add_edge(original_id,dst_id)
            fig = plt.figure()
            pos = nx.spring_layout(graph)
            nx.draw_networkx_nodes(graph, pos, node_color='black')
            nx.draw_networkx_edges(graph, pos, edge_color='red')
            plt.title('{}_{}_passing.png'.format(id,team_id))
            fig.show()
            break
        break
if __name__=='__main__':
    draw_graph()