import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import tqdm,json,math
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
    mapping={}
    plt.rc('font',family='Times New Roman')
    ax=plt.gca()
    ax.spines['right'].set_color("none")
    ax.spines['top'].set_color("none")
    for id in tqdm.tqdm(match_ID,total=len(match_ID)):
        match_ball_graph=fp[fp.MatchID==id]
        all_team_id=set(match_ball_graph['TeamID'])
        if len(list(all_team_id))!=2:
            raise ValueError('team error!')
        ball_passing_coord=[]
        ball_control_player=[]
        for c,idx in enumerate(match_ball_graph.index):
            teamID=match_ball_graph.loc[idx,'TeamID']
            original_player_id=match_ball_graph.loc[idx,'OriginPlayerID']
            dstplayer_id=match_ball_graph.loc[idx,'DestinationPlayerID']
            original_x=match_ball_graph.loc[idx,'EventOrigin_x']
            original_y=match_ball_graph.loc[idx,'EventOrigin_y']
            dst_x=match_ball_graph.loc[idx,'EventDestination_x']
            dst_y=match_ball_graph.loc[idx,'EventDestination_y']
            if pd.isna(dst_x) or pd.isna(dst_y) or pd.isna(original_x) or pd.isna(original_y):
                continue
            if teamID.startswith('Opponent'):
                original_x=100-original_x
                original_y=100-original_y
                dst_x=100-dst_x
                dst_y=100-dst_y
            original_x,original_y,dst_x,dst_y=int(original_x),int(original_y),int(dst_x),int(dst_y)
            if c==0:
                ball_passing_coord.append((original_x,original_y,dst_x,dst_y))
                ball_control_player.append([original_player_id])
            else:
                if (original_x,original_y,dst_x,dst_y)==ball_passing_coord[-1]:
                    ball_control_player[-1].append(original_player_id)
                else:
                    if (original_x,original_y)==(ball_passing_coord[-1][2],ball_passing_coord[-1][3]):
                        ball_passing_coord.append((original_x,original_y,dst_x,dst_y))
                        ball_control_player.append([original_player_id])
                    else:
                        original_x,original_y=ball_passing_coord[-1][2],ball_passing_coord[-1][3]
                        if (original_x,original_y,dst_x,dst_y)==ball_passing_coord[-1]:
                            ball_control_player[-1].append(original_player_id)
                        else:
                            ball_passing_coord.append((original_x,original_y,dst_x,dst_y))
                            ball_control_player.append([original_player_id])
        assert len(ball_passing_coord)==len(ball_control_player)
        mapping[id]=[ball_control_player,ball_passing_coord]
        last_dst=None
        linesw=0.05
        for i in range(len(ball_control_player)):
            players=ball_control_player[i]
            coord=[j*10000 for j in ball_passing_coord[i]]
            teams=list(set([j.split('_')[0] for j in players]))
            if len(teams)==1 and teams[0]=='Huskies':
                if last_dst==None:
                    plt.scatter(x=[coord[0],coord[2]],y=[coord[1],coord[3]],
                                c='red',marker='^',linewidths=linesw)
                    plt.quiver(coord[0],coord[1],coord[2],coord[3],color='g', width=0.0005)
                else:
                    plt.scatter(x=[last_dst[0],coord[2]],y=[last_dst[1],coord[3]],c='red',
                                marker='^',linewidths=linesw)
                    plt.quiver(last_dst[0],last_dst[1],coord[2],coord[3],color='g', width=0.0005)
            elif len(teams)==1 and teams[0].startswith('Opponent'):
                if last_dst==None:
                    plt.scatter(x=[coord[0],coord[2]],y=[coord[1],coord[3]],
                                c='blue',marker='o',linewidths=linesw)
                    plt.quiver(coord[0],coord[1],coord[2],coord[3],color='g', width=0.0005)
                else:
                    plt.scatter(x=[last_dst[0],coord[2]],y=[last_dst[1],coord[3]],c='blue',
                                marker='o',linewidths=linesw)
                    plt.quiver(last_dst[0],last_dst[1],coord[2],coord[3],color='g', width=0.0005)
            else:
                if last_dst==None:
                    plt.scatter(x=[coord[0],coord[2]],y=[coord[1],coord[3]],
                                c='black',marker='o',linewidths=linesw)
                    plt.quiver(coord[0],coord[1],coord[2],coord[3],color='g', width=0.0005)
                else:
                    plt.scatter(x=[last_dst[0],coord[2]],y=[last_dst[1],coord[3]],c='black',
                            marker='o',linewidths=linesw)
                    plt.quiver(last_dst[0],last_dst[1],coord[2],coord[3],color='g', width=0.0005)

            last_dst=(coord[2],coord[3])
        plt.savefig('ball_graphs/{}_full_events.png'.format(id),dpi=300)
        plt.close()
    json.dump(mapping,open('all_match_mapping.json','w',encoding='utf-8'))

def conduct_new_passing_tables():
    fp=pd.read_csv(passings)
    match_id=list(set(fp['MatchID']))
    for id in tqdm.tqdm(match_id,total=len(match_id)):
        match_passing=fp[fp.MatchID==id]
        node=pd.DataFrame()
        edge=pd.DataFrame()
        for c,idx in enumerate(match_passing.index):
            original_x=match_passing.loc[idx,'EventOrigin_x']
            original_y=match_passing.loc[idx,'EventOrigin_y']
            dst_x=match_passing.loc[idx,'EventDestination_x']
            dst_y=match_passing.loc[idx,'EventDestination_y']
            if match_passing.loc[idx,'TeamID'].startswith('Opponent'):
                original_x=100-original_x
                original_y=100-original_y
                dst_x=100-dst_x
                dst_y=100-dst_y
            original_x,original_y,dst_x,dst_y=int(original_x),int(original_y),int(dst_x),int(dst_y)
            node=node.append({'Id':int(c),'Label':match_passing.loc[idx,'OriginPlayerID']},
                             ignore_index=True)
            edge=edge.append({
                'Source':match_passing.loc[idx,'OriginPlayerID'],
                'Target':match_passing.loc[idx,'DestinationPlayerID'],
                'EventTime':round(float(match_passing.loc[idx,'EventTime']),2),
                'EventSubType':match_passing.loc[idx,'EventSubType'],
                'MatchPeriod':match_passing.loc[idx,'MatchPeriod'].strip('H'),
                'EventOrigin_x':original_x,
                'EventOrigin_y':original_y,
                'EventDestination_x':dst_x,
                'EventDestination_y':dst_y,
                'Distance':round(math.sqrt((original_x-dst_x)**2+(original_y-dst_y)**2),2)
            },ignore_index=True)
        node.to_csv('new_passing_tables/passingevents_{}_node.csv'.format(id),index=False)
        edge.to_csv('new_passing_tables/passingevents_{}_edge.csv'.format(id),index=False)
if __name__=='__main__':
    conduct_new_passing_tables()