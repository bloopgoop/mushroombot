import random
import math

class MapleAI():
    def __init__(self, alpha=0.5, epsilon=0.4, bias=4):
        """
        Initializes an AI with an empty Q-learning dictionary,
        an alpha rate and an epsilon rate

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value

            - `state` is a tuple of player position and time since last mob respawn -> ( (x, y), secs )
            - `action` is a tuple of movement and skill
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon
        self.bias = bias

        movements = ['left_fj', 'right_fj', 'down_j', 'ascend']
        skills = ['main_attack']

        self.actions = []

        for movement in movements:
            for skill in skills:
                self.actions.append((movement, skill))

    def stop_training(self):
        self.epsilon = 0
        self.alpha = 0
        self.bias = 0

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        if (state, action) in self.q:
            return self.q[state, action]
        else:
            return 0


    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate) - bias

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """

        self.q[state, action] = self.q[state, action] + (self.alpha * (reward + future_rewards - old_q)) - self.bias
        return

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """

        if not self.actions:
            return 0
        
        max = -math.inf
        for action in self.actions:
            if (state, action) not in self.q:
                self.q[state, action] = 0
            
            if self.q[state, action] > max:
                max = self.q[state, action]

        return max

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        # Check max future reward
        max = self.best_future_reward(state)
        print("chooseaction max", max)
        
        # Epsilon greedy
        if epsilon == True:
            random_number = random.random()

            # If random number falls within 0 - epsilon
            if random_number <= self.epsilon:
                return random.choice(self.actions)
        
        # Greedy
        for action in self.actions:
            if (state, action) not in self.q:
                self.q[state, action] = 0

            if self.q[state, action] == max:
                return action
