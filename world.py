import random
from collections import defaultdict

class Node:
    def __init__(self, index):
        self.index = index
        self.soldiers = 0
        self.owner = "N"
        self.left = None
        self.right = None

    def __str__(self):
        return f"(Loc:{self.index}, Own:{self.owner}, Sols:{self.soldiers})"

    def add_soldiers(self, agent_name, additional_soldiers, name_to_anon):
        agent_name = name_to_anon.get(agent_name, agent_name)
        if self.owner == "N" or self.owner == agent_name:
            self.owner = agent_name
            self.soldiers += additional_soldiers
        else:
            if self.soldiers >= additional_soldiers:
                self.soldiers -= additional_soldiers
            else:
                self.owner = agent_name
                self.soldiers = additional_soldiers - self.soldiers

    def split_right(self, max_soldiers):
        if self.soldiers <= max_soldiers:
            return
        to_right = self.soldiers - max_soldiers
        self.soldiers = max_soldiers
        self.right.soldiers += to_right
        self.right.owner = self.owner

    def split_left(self, max_soldiers):
        if self.soldiers <= max_soldiers:
            return
        to_left = self.soldiers - max_soldiers
        self.soldiers = max_soldiers
        self.left.soldiers += to_left
        self.left.owner = self.owner

class World:
    def __init__(self, num_nodes, agents, max_soldiers, starting_soldiers, visibility_range):
        self.num_nodes = num_nodes
        self.max_soldiers = max_soldiers
        self.visibility_range = visibility_range
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.anonymize_agents(agents)

        # Link the nodes in a circular manner
        for i in range(num_nodes):
            self.nodes[i].right = self.nodes[(i + 1) % num_nodes]
            self.nodes[i].left = self.nodes[(i - 1 + num_nodes) % num_nodes]

        divisions = num_nodes / len(agents)
        place = 0
        for i in range(0, num_nodes, int(divisions)):
            self.nodes[i].owner = agents[place]
            self.nodes[i].soldiers = starting_soldiers
            place += 1
            if place >= len(agents):
                break

    def anonymize_agents(self, agents):
        alph = "abcdefghijklmnopqrstuvwxyz"
        self.anon_to_name = {alph[i]: agents[i] for i in range(len(agents))}
        self.name_to_anon = {agents[i]: alph[i] for i in range(len(agents))}

    def fight_right(self, node):
        rnode = node.right
        if rnode.right.owner == node.owner:
            rrnode = rnode.right
            if rnode.soldiers > node.soldiers + rrnode.soldiers:
                node.owner = "N"
                rrnode.owner = "N"
                rnode.soldiers += node.soldiers + rrnode.soldiers
                node.soldiers = 0
                rrnode.soldiers = 0
                rnode.split_left(self.max_soldiers)
                return 1
            else:
                node.owner = "N"
                rrnode.soldiers += node.soldiers + rnode.soldiers
                node.soldiers = 0
                rnode.soldiers = 0
                rrnode.split_left(self.max_soldiers)
                return 2
        else:
            if rnode.soldiers > node.soldiers:
                node.owner = rnode.owner
                node.soldiers += rnode.soldiers
                rnode.soldiers = 0
                node.split_right(self.max_soldiers)
                return 1
            elif rnode.soldiers < node.soldiers:
                rnode.owner = node.owner
                rnode.soldiers += node.soldiers
                node.soldiers = 0
                rnode.split_left(self.max_soldiers)
                return 1

    def fight_left(self, node):
        lnode = node.left
        if lnode.left.owner == node.owner:
            ll_node = lnode.left
            if lnode.soldiers > node.soldiers + ll_node.soldiers:
                node.owner = "N"
                ll_node.owner = "N"
                lnode.soldiers += node.soldiers + ll_node.soldiers
                node.soldiers = 0
                ll_node.soldiers = 0
                lnode.split_right(self.max_soldiers)
                return -1
            else:
                node.owner = "N"
                ll_node.soldiers += node.soldiers + lnode.soldiers
                node.soldiers = 0
                lnode.soldiers = 0
                ll_node.split_right(self.max_soldiers)
                return -2
        else:
            if lnode.soldiers > node.soldiers:
                node.owner = lnode.owner
                node.soldiers += lnode.soldiers
                lnode.soldiers = 0
                node.split_left(self.max_soldiers)
                return -1
            elif lnode.soldiers < node.soldiers:
                lnode.owner = node.owner
                lnode.soldiers += node.soldiers
                node.soldiers = 0
                lnode.split_right(self.max_soldiers)
                return -1

    def resolve(self, agent_name, right):
        c = random.randint(0, self.num_nodes - 1)
        agent = self.name_to_anon[agent_name]
        if right == 1:
            for i in range(c, c + self.num_nodes):
                node = self.nodes[i % self.num_nodes]
                if node.soldiers > self.max_soldiers:
                    node.soldiers = self.max_soldiers
                if node.owner == node.right.owner or node.owner == "N":
                    continue
                else:
                    skip = self.fight_right(node)
                    i += skip
        else:
            for i in range(c, c - self.num_nodes, -1):
                node = self.nodes[i % self.num_nodes]
                if node.soldiers > self.max_soldiers:
                    node.soldiers = self.max_soldiers
                if node.owner == node.left.owner or node.owner == "N":
                    continue
                else:
                    skip = self.fight_left(node)
                    i += skip

    def get_losers(self):
        surviving_agents = {node.owner for node in self.nodes}
        defeated_agents = set(self.name_to_anon.keys()) - surviving_agents
        return {self.anon_to_name[agent] for agent in defeated_agents}

    def print_nodes(self):
        for node in self.nodes:
            print(f"{node.index}: {node.owner}, {node.soldiers} soldiers")

if __name__ == "__main__":
    agents = ["Alice", "Bob"]
    world = World(10, agents, 1000, 50, 1)
    world.print_nodes()
