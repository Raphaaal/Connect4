from src.game.fight import fight
from src.common.constants import RED, YELLOW
from tqdm import tqdm

def contest(p1, p2, nb_fights, nb_playouts):
    p1_name = p1
    p2_name = p2
    if p1 == p2:
        p2_name = p2+"2"
    engines = {p1_name: p1, p2_name: p2}
    scores = {p1_name: 0, p2_name:0, "tie":0}
    players = {0: "tie"}
    for i in tqdm(range(nb_fights)):
        if i%2 == 0:
            players[RED] = p1_name
            players[YELLOW] = p2_name
        else:
            players[RED] = p2_name
            players[YELLOW] = p1_name
        winner = fight(engines[players[RED]], engines[players[YELLOW]], nb_playouts=nb_playouts, verbose=False)
        scores[players[winner]] +=1
    for player in scores:
        scores[player] /= nb_fights
    return scores
    
    