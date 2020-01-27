from collections import namedtuple
Transition = namedtuple('Transition', 'input_symbol new_state output_symbol')
ActiveState = namedtuple('ActiveState', 'state sym number')


class FinalTransducer:
    def __init__(self, start_state):
        self._states = self.states
        self.start_state = start_state
        self.ways = []
        self.tree = dict()
        self.count = 0
        self.all_states = list()

    def get_ways(self, word: str, active_state: ActiveState):
        if len(word) == 0:
            word = 'e'
        states = [x for x in self.states[active_state.state] if x.input_symbol == word[0] or x.input_symbol == 'e']
        active_state = ActiveState(active_state.state, active_state.sym, self.count)
        self.all_states.append(active_state)
        self.count += 1
        for state in states:
            self.tree[self.count] = active_state.number
            if state.input_symbol == 'e':
                self.get_ways(str(word), ActiveState(state.new_state, 'e', ''))
            else:
                self.get_ways(str(word[1:]), ActiveState(state.new_state, word[0], ''))

    def get_words(self, input_word):
        self.get_ways(input_word, ActiveState(self.start_state, self.count, ''))

        self.all_states = sorted(self.all_states, key=lambda x: x.number)

        end_states = []
        for s in self.all_states:
            if s.state == 3:
                end_states.append(s)

        self.get_good_ways(input_word, end_states)

        result = set()
        for way in self.ways:
            start = self.start_state
            out_words = []
            for state in way[1:]:
                out_sym = [x.output_symbol for x in self.states[start] if x.new_state == state[0] and x.input_symbol == state[1]]
                if len(out_words) == 0:
                    for sym in out_sym:
                        out_words.append(sym)
                else:
                    words = [x for x in out_words]
                    for word in words:
                        for sym in out_sym:
                            out_words.append(word + sym)
                        out_words.remove(word)
                start = state[0]
            for x in out_words:
                result.add(x.replace('e', ''))
        return result

    def get_good_ways(self, input_word, end_states):
        for end_state in end_states:
            prev = end_state.number
            state = self.all_states[prev]
            way = [(state.state, state.sym)]
            while prev != 0:
                state = self.all_states[self.tree[prev]]
                way.append((state.state, state.sym))
                prev = self.tree[prev]
            word = [x[1] for x in way if x[1] != 'e' and x[1] != 0]
            word.reverse()
            word = ''.join(word)
            if word != input_word:
                continue
            way.reverse()
            self.ways.append(way)

    @property
    def states(self):
        return {

            1: (Transition('a', 3, 'e'), Transition('b', 7, 'e')),

            2: (Transition('a', 7, 'e'), Transition('b', 3, 'e')),

            3: (Transition('a', 9, 'e'), Transition('b', 10, 'e'), Transition('e', 11, 'a'), Transition('e', 12, 'b')),

            4: (Transition('e', 3, 'a'), Transition('e', 7, 'b')),

            5: (Transition('e', 7, 'a'), Transition('e', 3, 'b')),

            6: (Transition('e', 3, 'a'), Transition('e', 3, 'b')),

            7: (Transition('a', 5, 'e'), Transition('b', 4, 'e'), Transition('e', 1, 'b'), Transition('e', 2, 'a')),

            8: (Transition('a', 8, 'e'), Transition('a', 7, 'e'), Transition('b', 8, 'e'), Transition('b', 7, 'e')),

            9: (Transition('e', 3, 'b'), Transition('e', 3, 'a')),

            10: (Transition('e', 3, 'b'), Transition('e', 3, 'a')),

            11: (Transition('a', 3, 'e'), Transition('b', 3, 'e')),

            12: (Transition('b', 3, 'e'), Transition('a', 3, 'e'))
        }
