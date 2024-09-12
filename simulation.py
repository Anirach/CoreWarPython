from world import World  # Ensure World is imported
from agent_details import AgentDetails  # Import AgentDetails class

class Simulation:
    def __init__(self, scale, agents, agent_lookup, per_turn, max_soldiers, start_count, visibility_range):
        self.world = World(scale, agents, max_soldiers, start_count, visibility_range)
        self.agent_lookup = agent_lookup
        self.per_turn = per_turn
        self.active_agents = set(agents)
        self.super_step = 0

    def run(self, steps):
        for i in range(steps):
            if len(self.active_agents) == 1:
                print(f"Agent {list(self.active_agents)[0]} WINS!!!")
                break
            self.make_turn(i)
            self.world.print_nodes()

    def make_turn(self, step):
        for agent in list(self.active_agents):
            self.super_step += 1
            self.update_state(agent, step)
            self.command_agent(agent, step)
            self.battle(agent, step)

    def battle(self, agent_name, step):
        right = self.determine_opponent(agent_name)
        losers = self.world.resolve(agent_name, right)
        self.active_agents.difference_update(losers)

    def determine_opponent(self, agent_name):
        # Logic to determine the opponent
        return "some_opponent"

    def update_state(self, agent, step):
        # Logic to update the state of the agent
        pass

    def command_agent(self, agent, step):
        # Logic to command the agent
        pass

if __name__ == "__main__":
    agents = ["Alice", "Bob"]
    agent_lookup = {
        "Alice": AgentDetails("alice_agent.py", "alice_folder", "red"),
        "Bob": AgentDetails("bob_agent.py", "bob_folder", "blue")
    }
    sim = Simulation(10, agents, agent_lookup, per_turn=100, max_soldiers=1000, start_count=50, visibility_range=2)
    sim.run(20)