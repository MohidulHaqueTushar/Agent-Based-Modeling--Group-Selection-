# -*- coding: utf-8 -*-
"""

Simulation of an agent-based model of multi-level selection.
This simulation shows two outcomes:
    1. without group selection pressures (without war/without groups conflict), 
       Non-Altruistic population will increase over time. 
    2. Under the pressures of group selection (with war/with groups conflict),
       Altruistic population will increase over time.

@author: Md Mohidul Haque
"""

"""import modules"""
import numpy as np
import matplotlib.pyplot as plt

"""Define classes"""

class GroupOfAgent():
    def __init__(self, number_of_groups, number_of_agents):
        """
        Set the initial variables
        
        Parameters
        ----------
        number_of_groups : int, total groups 
        number_of_agents : int, total agents
        
        """
        self.number_of_groups = number_of_groups
        self.number_of_agents = number_of_agents
        self.Groups = []
        
    def Setup(self):
        """
        Will create groups with agents where each agent has a trait Altruistic(A)
        or Non-Altruistic(N) (randomly choosen)
    
        Returns
        -------
        list of groups with agents, 0 means Non-Altruistic, 1 means Altruistic.
        """
        if self.number_of_agents % self.number_of_groups == 0:  #each group will have same population
            agent_each_group = self.number_of_agents // self.number_of_groups
            for i in range(self.number_of_groups):
                group = []
                for j in range(agent_each_group):
                    agent = np.random.choice([1,0])
                    group.append(agent)
                self.Groups.append(group)
            return self.Groups
        else: #odd
            agent_each_group = self.number_of_agents // self.number_of_groups
            for i in range(self.number_of_groups):
                group = []
                for j in range(agent_each_group):
                    agent = np.random.choice([1,0])
                    group.append(agent)
                self.Groups.append(group)
            extra_agent = np.random.choice([1,0])
            group_index = np.random.randint(0,self.number_of_groups)
            self.Groups[group_index].append(extra_agent)
            return self.Groups
        
class Evolution():
    
    def __init__(self, list_of_groups, baseline_value = 10, b = 2, c = 1, e = 0.001, m = 0.2):
        """
        evaluate the evolution of agents over time
        
        Paramerers
        ----------
        list_of_groups: list of groups under evolution. Will be modified by mutation and migration
        baseline_value: default value 10
        b: benefit, default value 2
        c: cost, default value 1
        e: mutation rate, default value 0.001
        m: migration rate, default value 0.2
        
        """
        self.list_of_groups = list_of_groups #agent groups under evolution
        self.size = [] #each groups size
        self.agents_will_play = [] #those agents will play PD game
        self.agents_not_play = [] #those agents will not play PD game in one round
        self.paired_agents = [] #agents pair randomly to play PD game with
        self.Groups_payoff = [] #agent groups payoff
        self.Group_of_Agents = [] #agent groups after calculating payoff
        self.baseline_value = baseline_value #need to calculate payoff from PD game
        self.b = b #benefit of PD game
        self.c = c #cost of PD game
        self.parent_pool = [] #from this, will get new generation
        self.e = e #new generation will change trait with this probability, causes mutation
        self.after_mutation = [] #agent groups complete mutation, will under migration
        self.m = m #agents migrate to another group with this probability
    
    
    def GroupsLength(self):
        """
        Calculate the length of each groups
        
        Returns
        -------
        None
        """        
        for i in range(len(self.list_of_groups)):
            self.size.append(len(self.list_of_groups[i]))
    
    def Those_agents_play(self):
        """
        Determine which agent will play or not play in one round, by their size
        
        Returns
        -------
        None
        """
    
        for i in range(len(self.size)):
            if (self.size[i] % 2) == 0:
                #print("All agents will play from group {}".format(i))
                group = self.list_of_groups[i].copy()
                self.agents_will_play.append(group)
                self.agents_not_play.append([])
            
            else:
                #print("One agent will not play from group {}".format(i))
                group = self.list_of_groups[i].copy()
                index = np.random.randint(len(group))
                agent = [group.pop(index)]  #select a random agent, not to play in one round
                self.agents_will_play.append(group)
                self.agents_not_play.append(agent)
                
    def Getting_group_partner(self):
        """
        Agent pair randomly with another agents in own group
        
        Returns
        -------
        None
        """
        for group in range(len(self.agents_will_play)):
            pair_agents = []
            bb = self.agents_will_play[group].copy()
            r = len(bb)//2
            for j in range(r):
                for i in range(1): #get two random agent from group
                    pairing = []
                    a = np.random.choice(bb) 
                    pairing.append(a)
                    bb.remove(a)
                    b = np.random.choice(bb)
                    pairing.append(b)
                    bb.remove(b)
                    pair_agents.append(pairing)
            self.paired_agents.append(pair_agents)
            
    def Payoff(self): 
        """
        Calculate the payoff for each agent in groups.

        Row's payoff: [b-c,-c],[b,0]
        Column's Payoff: [b-c,b],[-c,0]
        
        Returns
        -------
        None
    
        """
    
        for i in range(len(self.paired_agents)):
            agents = []
            payoff = []
            group = self.paired_agents[i]
            for j in range(len(group)):
                sub_group = group[j] #paired agents
                agent_1 = sub_group[0]
                agent_2 = sub_group[1]
                agents.append(agent_1)
                agents.append(agent_2)
                if agent_1 == 1 and agent_2 == 1: #both agent Altruistic
                    agent_1_payoff = self.baseline_value + (self.b-self.c)
                    agent_2_payoff = self.baseline_value + (self.b-self.c)
                    payoff.append(agent_1_payoff)
                    payoff.append(agent_2_payoff)
                
    
                elif agent_1 == 1 and agent_2 == 0:  #agent_1 Altruistic but not agent_2
                    agent_1_payoff = self.baseline_value + (-self.c)
                    agent_2_payoff = self.baseline_value + (self.b)
                    payoff.append(agent_1_payoff)
                    payoff.append(agent_2_payoff)
            
                elif agent_1 == 0 and agent_2 == 1:  #agent_2 Altruistic but not agent_1
                    agent_1_payoff = self.baseline_value + (self.b)
                    agent_2_payoff = self.baseline_value + (-self.c)
                    payoff.append(agent_1_payoff)
                    payoff.append(agent_2_payoff)
            
                elif agent_1 == 0 and agent_2 == 0: #both agent Non-Altruistic
                    agent_1_payoff = self.baseline_value + (0)
                    agent_2_payoff = self.baseline_value + (0)
                    payoff.append(agent_1_payoff)
                    payoff.append(agent_2_payoff)
            
                else:
                    print("Something is wrong!")
            self.Groups_payoff.append(payoff)
            self.Group_of_Agents.append(agents)
            
    def NonPlayerPayoff(self):
        """
        Add non player agent's and payoff's to the respective groups
        
        Returns
        -------
        None
        """    
        for i in range(len(self.agents_not_play)):
            g = self.agents_not_play[i]
            for j in range(len(g)):
                self.Group_of_Agents[i].append(g[j]) #add non-player agent at the end of group
                self.Groups_payoff[i].append(self.baseline_value) #add non player payoff at the end of group
        return self.Groups_payoff
                
    def Fitness_determination(self):
        """
        Formulate a parent pool by spinning roulette wheel. The probability that 
        an agent is selected for the parent pool is  equal 
        to the agents relative payoff compared to the total payoff of the group
        
        Returns
        -------
        None
        """
        for i in range(len(self.Group_of_Agents)):
            group = self.Group_of_Agents[i]
            payoff = self.Groups_payoff[i]
            groups_total_payoff = sum(payoff)
            
            probability  = [] #to be in parent pool (agents)
    
            for j in range(len(group)):
                probability.append(payoff[j]/groups_total_payoff)
    
            pool = [] #agents select for parent pool
            for k in range(len(group)):
                pool.append(np.random.choice(group, p=probability))
            self.parent_pool.append(pool)
            
    def Mutation(self):
        """
        With probability e an agent randomly determines his trait. 
        Therefore the probability of one agent switching type is e /2.
        
        Returns
        -------
        None
        """

        d = 1-self.e #probability of one agent not switching type

        for i in range(len(self.parent_pool)):
            under_mutation = self.parent_pool[i]
            agents_done = []
            for j in range(len(under_mutation)):
                agent = under_mutation[j]
                choice = np.random.choice([True, False], p = [self.e, d])
                if choice == False:
                    agents_done.append(agent)
                else:
                    choose = np.random.choice([1,0], p=[0.5,0.5])
                    agents_done.append(choose)
                    
            self.after_mutation.append(agents_done)
            
    def Migration(self):
        """
        Every member of the population has equal probability, 
        to migrate to another group which is randomly selected among all the groups except its own
        
        Returns
        -------
        self.after_mutation: agent groups after migration, list
        """
        w = 1 - self.m
        
        groups_index = [i for i in range(len(self.after_mutation))]
        migrated_agent = []
        
        for j in range(len(self.after_mutation)):
            group = self.after_mutation[j]
            agent_migrating = []
            for agent in group:
                migration = np.random.choice([True, False], p = [self.m, w])
                if migration == True:
                    agent_migrating.append(agent)
                else:
                    pass
            migrated_agent.append(agent_migrating)
        
        for j in range(len(self.after_mutation)):
            remain_groups_index = groups_index.copy()
            remain_groups_index.remove(j)
        
            for agent in migrated_agent[j]:
                index = np.random.choice(remain_groups_index)
                self.after_mutation[index].append(agent)
                self.after_mutation[j].remove(agent)
        return self.after_mutation
    
    def Check(self):
        """
        Print values Just for check.
        For specific output, should use specific method.
        
        return
        ------
        None
        """
        print("group list is:", self.list_of_groups)
        print("groups size:", self.size)
        print("Agents will play:", self.agents_will_play)
        print("Agents will not play:", self.agents_not_play)
        print("Paired agents:", self.paired_agents)
        print("Baseline {}, benefit {}, cost {}".format(self.baseline_value, self.b, self.c))
        print("Groups of agents:", self.Group_of_Agents)
        print("Groups resrective payoff:", self.Groups_payoff)
        #print("Update agent Groups:", self.Group_of_Agents)
        #print("Update payoff's:", self.Groups_payoff)
        print("New generations:", self.parent_pool)
        #print("After mutation:", self.after_mutation)
        print("After migration:", self.after_mutation)
    
class War():
    def __init__(self,after_migration,k = 0.25):
        """
        Determine winning and losing groups of agents after joining a war
        
        Parameters
        ----------
        after_migration: group of agents after migration
        k : probability of joing a war, default value 0.25
        """
        self.after_migration = after_migration.copy()
        self.k = k
        self.will_compete_index = []
        self.war_paired = []
        
    def Compete(self):
        """
        Will find interested groups index of war
        
        return 
        ------
        None
        """
        m = 1-self.k
        all_groups_index = [i for i in range(len(self.after_migration))]
        
        for i in all_groups_index:
            compete = np.random.choice([True, False], p = [self.k, m])
            if compete == False:
                pass
            else:
                self.will_compete_index.append(i)
                
        for j in self.will_compete_index:
            all_groups_index.remove(j)
            
        if (len(self.will_compete_index) % 2) != 0:
            index = np.random.choice(all_groups_index)
            self.will_compete_index.append(index)
            all_groups_index.remove(index)
        else:
            pass
        all_groups_index.clear()
        
    def CompetePartner(self):
        """
        pair group indexes for compete
        
        return
        ------
        None
        """
        r = len(self.will_compete_index) // 2
        for i in range(r):
            pairing  = []
            for j in range(1):
                choose = np.random.choice(self.will_compete_index)
                pairing.append(choose)
                self.will_compete_index.remove(choose)
                choose = np.random.choice(self.will_compete_index)
                pairing.append(choose)
                self.will_compete_index.remove(choose)

            self.war_paired.append(pairing)
        self.will_compete_index.clear()
        
    
    def GroupsConflicts(self):
        """
        Calculate the total payoff of the groups, and compare them. 
        In war, in between two groups, the group with highest relative payoff will be the winner.
        The loser groups agents will be replaced by winner groups agents.
        
        return
        ------
        groups of agents after war: list
        """
        for i in range(len(self.war_paired)):
            compete_groups_index = self.war_paired[i]
            group_1_index = compete_groups_index[0]
            group_2_index = compete_groups_index[1]
            group_1 = self.after_migration[group_1_index].copy()
            group_2 = self.after_migration[group_2_index].copy()
            compete_groups = [group_1, group_2]
            game = Evolution(compete_groups) #use evolution class to calculate payoff
            game.GroupsLength()
            game.Those_agents_play()
            game.Getting_group_partner()
            game.Payoff()
            update_compete_payoff = game.NonPlayerPayoff()
            
            group_1_total_payoff = sum(update_compete_payoff[0]) / len(group_1)
            group_2_total_payoff = sum(update_compete_payoff[1]) / len(group_2)
            
            merge_winner_agents = []
            if group_1_total_payoff > group_2_total_payoff:
                for i in range(2):
                    for j in range(len(group_1)):
                        merge_winner_agents.append(group_1[j])
            else:
                for i in range(2):
                    for j in range(len(group_2)):
                        merge_winner_agents.append(group_2[j])
            self.after_migration[group_1_index].clear()
            self.after_migration[group_2_index].clear()
            for i in range(len(merge_winner_agents)):
                agent = merge_winner_agents[i]
                random_selection = np.random.choice(compete_groups_index)
                self.after_migration[random_selection].append(agent)
        self.war_paired.clear()
        return self.after_migration
    
    def WCheck(self):
        """
        Print value to check
        
        return
        ------
        None
        """
        print("Grpups indexes join wars, end of time:", self.will_compete_index)
        print("War partner, before the end of time:", self.war_paired)
        print("After war:", self.after_migration)
        
class Simulation():
    
    def __init__(self,total_group,total_agent,t,conflict = False):
        """
        Set values
        
        Parameters
        ----------
        total_group: total groups under evolution, int
        total_agent: total agent under evolution, int
        t: time, how much time the simulation will run
        conflict: war exist or not, default value False
        
        """
        self.t = t #time
        self.conflict = conflict #groups war
        self.total_group = total_group
        self.total_agent = total_agent
        self.agent_groups = GroupOfAgent(self.total_group,self.total_agent).Setup() #modefied over time
        self.Number_of_Altruists = []
        self.Number_of_NonAltruists = []
    
    def Run(self):
        if self.conflict == False: #without war
            for time in range(self.t):
                count_a = []
                count_n = []
                process = Evolution(self.agent_groups) #use Evolution class
                process.GroupsLength()
                process.Those_agents_play()
                process.Getting_group_partner()
                process.Payoff()
                process.NonPlayerPayoff()
                process.Fitness_determination()
                process.Mutation()
                after_mig = process.Migration() #agents after migration
                
                self.agent_groups.clear()
                
                for i in range(len(after_mig)):
                    count_a.append(after_mig[i].count(1))
                    count_n.append(after_mig[i].count(0))
                    self.agent_groups.append(after_mig[i])
                self.Number_of_Altruists.append(sum(count_a))
                self.Number_of_NonAltruists.append(sum(count_n))
        else:
            for time in range(self.t):
                count_a = []
                count_n = []
                process = Evolution(self.agent_groups) #use evolution class
                process.GroupsLength()
                process.Those_agents_play()
                process.Getting_group_partner()
                process.Payoff()
                process.NonPlayerPayoff()
                process.Fitness_determination()
                process.Mutation()
                after_mig = process.Migration()
                    
                after_war = War(after_mig) #use war class
                after_war.Compete()
                after_war.CompetePartner()
                after_war_agents = after_war.GroupsConflicts()
                    
                self.agent_groups.clear()
                
                for i in range(len(after_war_agents)):
                    count_a.append(after_war_agents[i].count(1))
                    count_n.append(after_war_agents[i].count(0))
                    self.agent_groups.append(after_war_agents[i])
                self.Number_of_Altruists.append(sum(count_a))
                self.Number_of_NonAltruists.append(sum(count_n))
        
    def Plot(self):
        """
        fig-1: plot Number of Altruistic and Number of Non-Altruistic over time, seperately
        fig-2: plot Number of Altruistic and Non-Altruistic over time, together
        fig-3: plot Number of Altruistic against Number of Non-Altruistic
        Both figure saves as image
        """
        fig1, ax = plt.subplots(nrows=2, ncols=1, squeeze=False)
        ax[0][0].plot(np.arange(self.t),self.Number_of_NonAltruists,c="b", label = "Non-Altruists")
        ax[1][0].plot(np.arange(self.t),self.Number_of_Altruists, c="g", label = "Altruists" )
        ax[0][0].set_xlabel("Time")
        ax[1][0].set_xlabel("Time")
        ax[0][0].set_ylabel("Number of Non-Altruistic")
        ax[1][0].set_ylabel("Number of Altruistic")
        ax[0][0].set_title("Altruistic and Non-Altruistic population over time")
        ax[0][0].legend()
        ax[1][0].legend()
        plt.tight_layout()
        plt.savefig("Altruistic and Non-Altruistic population over time.png", dpi=300)
        
        fig2, ax = plt.subplots(nrows=1, ncols=1, squeeze=False)
        ax[0][0].plot(np.arange(self.t),self.Number_of_NonAltruists,c="b", label = "Non-Altruists")
        ax[0][0].plot(np.arange(self.t),self.Number_of_Altruists, c="g", label = "Altruists" )
        ax[0][0].set_xlabel("Time")
        ax[0][0].set_ylabel("Altruistic and Non-Altruistic population")
        ax[0][0].set_title("Altruistic and Non-Altruistic population over time")
        ax[0][0].legend()
        plt.tight_layout()
        plt.savefig("Altruistic and Non-Altruistic population over time (together).png", dpi=300)
        
        fig3, ax = plt.subplots(nrows=1, ncols=1, squeeze=False)
        ax[0][0].plot(self.Number_of_NonAltruists,self.Number_of_Altruists)
        ax[0][0].set_xlabel("Number of Non-Altruistic")
        ax[0][0].set_ylabel("Number of Altruistic")
        ax[0][0].set_title("Altruistic population against  Non-Altruistic population")
        plt.tight_layout()
        plt.savefig("Change of Altruistic against Non-Altruistic.png", dpi=300)        
        plt.show()


"""Main script"""
"""set, group = 20, total agent = 400, time = 100, war = False """
if __name__ == '__main__':
    test_case_1 = Simulation(20,400,100) #without war
    test_case_1.Run()
    test_case_1.Plot()
    
    """set, group = 20, total agent = 400, time = 100, war = True """
    
    test_case_2 = Simulation(20,400,100,True) #with war
    test_case_2.Run()
    test_case_2.Plot()
