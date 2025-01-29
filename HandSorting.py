class HandList(list):

    def __init__(self, *args):
        super().__init__(*args)

    def ret_sorted_by_results(self, flag: bool = False):
        return HandList(sorted(self, key=lambda hand: hand.hero_results, reverse=flag))

    def ret_pre_flop_tag_filtered(self, required_tags: list):
        filtered_lst = list()
        for tag in required_tags:
            filtered_lst.append(HandList(filter(lambda x: tag in x.preflop_tags["Hero_action_tags"], self)))
            if len(filtered_lst) > 1:
                filtered_lst[0] = HandList(filter(lambda x: x in filtered_lst[0], filtered_lst[-1]))
        return filtered_lst[0]

    def ret_pot_size_filtered(self, start, end):
        filtered_lst = HandList(filter(lambda x: start <= x.river_pot_size <= end, self))
        return filtered_lst

    def ret_hero_in_post_flop_filtered(self):
        filtered_lst = HandList(filter(lambda x: x.end_of_preflop_players_in["Hero"] and sum(x.end_of_preflop_players_in.values()) > 1, self))
        return filtered_lst

    def ret_hero_position_filtered(self, positions: list):
        filtered_lst = HandList(filter(lambda x: x.hero_position in positions, self))
        return filtered_lst

    def ret_hero_preflop_action_filtered(self, action: list):
        filtered_lst = HandList()
        for act in action:
            filtered_lst = filtered_lst + HandList(filter(lambda x: act in ' '.join(x.preflop_tags['Hero_action_tags']), self))
        return filtered_lst
