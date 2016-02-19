# implement R Learn
import RLearnNP
# Naive
#albert = RLearnNP.NaiveAgent(11)
#conex = [[0,1],[1,2],[1,4],[2,3],[2,5],[3,6],[4,5],[4,7],[5,6],[5,8],[7,8],[8,9],[9,10]]
#albert.end_states = [10]
#albert.reward_states = [10]
#albert.punish_states = [6]
#print albert.multiTransition(conex, False)
#albert.startWeights()
#end_conds = albert.batchRun(1000)

# Greener
albert = RLearnNP.GreenerAgent(11)
conex = [[0,1],[1,2],[1,4],[2,3],[2,5],[3,6],[4,5],[4,7],[5,6],[5,8],[7,8],[8,9],[9,10]]
albert.end_states = [10]
albert.reward_states = {10:10, 6:-10}
print albert.multiTransition(conex, False)
albert.startWeights()
end_conds = albert.batchRun(1000)
