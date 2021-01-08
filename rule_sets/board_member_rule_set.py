from .rule_set_factory import RuleSetFactory
import operator

class BoradMemberRuleSet(RuleSetFactory):
    company_status_lt_a = ['pre-seed', 'seed']
    company_status_gt_a = ['a+', 'b', 'c']
    board_role_list = ['management', 'investors', 'independent']
    annotation_values = []

    def __init__(self, data, verbose):
        super().__init__(data, verbose)
        self._category = self.categories[1]
        self.ruleset = [
            'IF (company_stage = any stage) and All founders are on the board',
            'IF (company_stage = any stage) and founders control the majority of the board over 51%',
            'IF (company_stage = any stage) and None of the co-founders are on the board',
            'IF (company_stage = pre-seed or seed) and There are even board seats',
            'IF (company_stage = pre-seed or seed)  and Some co-founders are on board but co-founders hold the majority of the board',
            'IF (company_stage = pre-seed or seed)  and . if board size is more than >5 or equal =1',
            'IF (company_stage = pre-seed or seed) and There are even board seats',
            'IF (company_stage = any stage)  and (# board seats are odd)',
            'IF (company_stage >= series A+)  and number of board seats (management = investors = independent) & number of board seat is odd',
            'IF (company_stage >= series A+)  and number of board seats (management = investors = independent) & number of board seat is even',
            'IF (company_stage >= series A+)  and number of co-founder on board & independent>= 1 & number of board seats (management > investors or independent) and board size is odd',
            'IF (company_stage >= series A+)  and number of co-founder on board & independent>= 1 & number of board seats (management > investors or independent) and board size is even',
            'IF (company_stage >= series A+)  and number of co-founder & independent on board>= 1 & number of board seats (management & independent < investors ) & board size is odd',
            'IF (company_stage >= series A+)  and number of co-founder & independent on board>= 1 & number of board seats (management & independent < investors ) & board size is even',
            'IF (company_stage >= series A+)  and number of co-founder & VC on board>= 1 & number of board seats (management & VC <independent ) & board size is odd',
            'IF (company_stage >= series A+)  and number of co-founder & VC on board>= 1 & number of board seats (management & VC <independent ) & board size is even',
        ]
        self.annotations = [
            {'annotation': 'All founders are on the board and they have majority control', 'status': self.status[2], 'rule': self.rule_founders_on_board_majority_control},
            {'annotation': 'Some of the founders are on the board but they have majority control', 'status': self.status[2], 'rule': self.rule_some_founders_on_board_majority_control},
            {'annotation': 'None of the founders are on the board of directors', 'status': self.status[0], 'rule': self.rule_no_founders_on_board},
            {'annotation': 'The majority of the board is controlled by non-founders', 'status': self.status[0], 'rule': self.rule_pre_seed_or_seed_even_board_seat},
            {'annotation': 'Some of the co-founders are on the board, the majority control by founders and the number of board seats are odd', 'status': self.status[2], 'rule': self.rule_some_founders_on_board_majority_control_odd_board_seat},
            {'annotation': 'The board size is {} is higher than typical for a [pre-seed or seed] company stage', 'status': self.status[1], 'rule': self.rule_nontypical_board_size},
            {'annotation': 'The number of board seats are even', 'status': self.status[1], 'rule': self.rule_even_board_seat},
            {'annotation': 'The number of board seats, {} are odd', 'status': self.status[2], 'rule': self.rule_odd_board_seat},
            {'annotation': 'Board of directors composition is: [e.g.1] management, [e.g.1] investor, [e.g.1] independent and the board size is odd', 'status': self.status[2], 'rule': self.rule_equal_board_role_odd_seat},
            {'annotation': 'Board of directors composition is: [e.g.2] management, [e.g.2] investor, [e.g.2] independent and the board size is even', 'status': self.status[1], 'rule': self.rule_equal_board_role_even_seat},
            {'annotation': 'Board of directors composition is: [e.g.2] management, [e.g.1] investor, [e.g.1] independent and the board size is odd', 'status': self.status[2], 'rule': self.rule_composed_board_role_odd_seat},
            {'annotation': 'Board of directors composition is: [e.g.1] management, [e.g.1] investor, [e.g.1] independent and the board size is even	', 'status': self.status[1], 'rule': self.rule_composed_management_board_role_even_seat},
            {'annotation': 'Board of directors composition is: [e.g.1] management, [e.g.3] investor, [e.g.1] independent and the board size is odd', 'status': self.status[2], 'rule': self.rule_composed_independent_board_role_odd_seat},
            {'annotation': 'Board of directors composition is: [e.g.2] management, [e.g.3] investor, [e.g.1] independent and the board size is even', 'status': self.status[1], 'rule': self.rule_composed_independent_board_role_even_seat},
            {'annotation': 'Board of directors composition is: [e.g.1] management, [e.g.1] investor, [e.g.3] independent and the board size is odd', 'status': self.status[2], 'rule': self.rule_composed_investors_board_role_odd_seat},
            {'annotation': 'Board of directors composition is: [e.g.1] management, [e.g.1] investor, [e.g.2] independent and the board size is odd', 'status': self.status[1], 'rule': self.rule_composed_investors_board_role_even_seat}
        ]
    
    # helpers
    def founders_on_board(self):
        founders = self.data['founders']
        for founder in founders:
            if not founder['board_member']:
                return False
        return True
    
    def some_founders_on_board(self):
        founders = self.data['founders']
        for founder in founders:
            if founder['board_member']:
                return True
        return False

    def founders_hold_majority_shares(self):
        founders = self.data['founders']
        total_founder_shares = 0
        for founder in founders:
            total_founder_shares += founder['shares']
        return total_founder_shares > 50

    def has_any_status(self):
        if self.data['profile']['current_stage'] in self.company_status_lt_a + self.company_status_gt_a: 
            return True
        return False
    
    def check_company_status_lt_a(self):
        if self.data['profile']['current_stage'].lower() in self.company_status_lt_a:
            return True
        return False

    def check_company_status_gt_a(self):
        if self.data['profile']['current_stage'].lower() in self.company_status_gt_a:
            return True
        return False
    
    def no_founders_on_board(self):
        founders = self.data['founders']
        for founder in founders:
            if founder['board_member']:
                return False
        return True


    def even_board_seat(self):
        if len(self.data['finantials'][0]['boards']) % 2:
            return False
        return True        

    def borad_role_management_number(self):
        board_members = self.data['finantials'][0]['boards']
        management = [borad_member for borad_member in board_members if borad_member['board_role'] == self.board_role_list[0]]
        return len(management)
    
    def borad_role_investors_number(self):
        board_members = self.data['finantials'][0]['boards']
        investors = [borad_member for borad_member in board_members if borad_member['board_role'] == self.board_role_list[1]]
        return len(investors)
    
    def borad_role_independent_number(self):
        board_members = self.data['finantials'][0]['boards']
        independent = [borad_member for borad_member in board_members if borad_member['board_role'] == self.board_role_list[2]]
        return len(independent)

    def annotation_info_gen(self, index):
        annotation_item = self.annotations[index]
        annotation_message = annotation_item['annotation'].format(*self.annotation_values)
        return [annotation_item['status'], annotation_message] if not self._verbose else [annotation_item['status'], annotation_message, self._category, self.ruleset[index]]

    #######################################################################################

    # rules
    def rule_founders_on_board_majority_control(self):
        if self.has_any_status() and self.founders_on_board():
            return True
        return False 
    
    def rule_some_founders_on_board_majority_control(self):
        if self.has_any_status() and self.founders_hold_majority_shares():
            return True
        return False

    def rule_no_founders_on_board(self):
        if self.has_any_status() and self.no_founders_on_board():
            return True
        return False

    def rule_pre_seed_or_seed_even_board_seat(self):
        # pre-seed or seed
        if self.check_company_status_lt_a() and self.even_board_seat():
            return True
        return False

    def rule_some_founders_on_board_majority_control_odd_board_seat(self):
        # pre-seed or seed
        if self.check_company_status_lt_a() and self.some_founders_on_board() and self.founders_hold_majority_shares():
            return True
        return False
        
    def rule_nontypical_board_size(self):
        # pre-seed or seed
        board_size = len(self.data['finantials'][0]['boards'])
        self.annotation_values.append(board_size)
        if self.check_company_status_lt_a() and board_size > 5 or board_size == 1:
            return True
        return False

    def rule_even_board_seat(self):
        # pre-seed or seed
        if self.check_company_status_lt_a() and self.even_board_seat():
            return True
        return False
    
    def rule_odd_board_seat(self):
        self.annotation_values.append(len(self.data['finantials'][0]['boards']))
        if self.has_any_status() and not self.even_board_seat():
            return True
        return False

    def rule_equal_board_role_odd_seat(self):
        # A+
        if self.check_company_status_gt_a() and (self.borad_role_management_number() == self.borad_role_investors_number() == self.borad_role_management_number()) and not self.even_board_seat():
            return True
        return False

    def rule_equal_board_role_even_seat(self):
        # A+
        if self.check_company_status_gt_a() and (self.borad_role_management_number() == self.borad_role_investors_number() == self.borad_role_management_number()) and self.even_board_seat():
            return True
        return False

    def rule_composed_board_role_odd_seat(self):
        managements = self.borad_role_management_number()
        independents = self.borad_role_independent_number()
        investors = self.borad_role_investors_number()
        # A+
        if (
            self.check_company_status_gt_a() and
            self.some_founders_on_board() and 
            independents and
            (managements > investors or managements > independents) and
            not self.even_board_seat()
            ):
            return True
        return False

    def rule_composed_management_board_role_even_seat(self):
        managements = self.borad_role_management_number()
        independents = self.borad_role_independent_number()
        investors = self.borad_role_investors_number()
        # A+
        if (
            self.check_company_status_gt_a() and
            self.some_founders_on_board() and 
            independents and
            (managements > investors or managements > independents) and
            self.even_board_seat()
            ):
            return True
        return False

    def rule_composed_independent_board_role_odd_seat(self):
        managements = self.borad_role_management_number()
        independents = self.borad_role_independent_number()
        investors = self.borad_role_investors_number()
        # A+
        if (
            self.check_company_status_gt_a() and
            self.some_founders_on_board() and 
            independents and
            (managements < investors or independents < investors) and
            not self.even_board_seat()
            ):
            return True
        return False

    def rule_composed_independent_board_role_even_seat(self):
        managements = self.borad_role_management_number()
        independents = self.borad_role_independent_number()
        investors = self.borad_role_investors_number()
        # A+
        if (
            self.check_company_status_gt_a() and
            self.some_founders_on_board() and 
            independents and
            (managements < investors or independents < investors) and
            self.even_board_seat()
            ):
            return True
        return False

    def rule_composed_investors_board_role_odd_seat(self):
        managements = self.borad_role_management_number()
        independents = self.borad_role_independent_number()
        investors = self.borad_role_investors_number()
        # A+
        if (
            self.check_company_status_gt_a() and
            self.some_founders_on_board() and 
            investors and
            (managements < independents or investors < independents) and
            not self.even_board_seat()
            ):
            return True
        return False

    def rule_composed_investors_board_role_even_seat(self):
        managements = self.borad_role_management_number()
        independents = self.borad_role_independent_number()
        investors = self.borad_role_investors_number()
        # A+
        if (
            self.check_company_status_gt_a() and
            self.some_founders_on_board() and 
            investors and
            (managements < independents or investors < independents) and
            self.even_board_seat()
            ):
            return True
        return False

    #######################################################################################
    
    def annotage(self):
        output = []
        for index in range(len(self.annotations)):
            self.annotation_values = []
            if self.annotations[index]['rule']():
                output.append(self.annotation_info_gen(index))
        return self.empty_annotation_info() if not len(output) else output
