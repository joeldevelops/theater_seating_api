class Seating:
    def __init__(self, groups, layout):
        self.row = 0
        self.column = 0
        self.groups = [] # treat groups like a queue
        self.layout = layout

        for i in range(len(groups)):
            if type(groups[i]) is list:
                self.groups.append({
                  'size': groups[i][1],
                  'position': i+1,
                  'preference': groups[i][0]
                })
            else:
                self.groups.append({
                  'size': groups[i],
                  'position': i+1,
                  'preference': None
                })


    def rtl(self):
        return self.row % 2 == 0 # Right to left on even rows


    def rank_seating_layout(self):
        return self.layout


    def print_layout(self):
        for r in range(len(self.layout)):
            row = []
            for c in range(len(self.layout[r])):
                row.append(self.layout[r][c]["group"])
            
            print(row)


    def remaining_seats_in_row(self):
        """
        Return the seats left in the current row. The current value of self.column
        will always be a valid seat.

        :return: int
        """
        if self.rtl():
            return len(self.layout[self.row]) - self.column
        else:
            return self.column + 1


    async def seat_row(self):
        """
        Seat the groups for a given row. Uses look ahead logic to
        seat group members together.

        :return: array of groups to sit in a given row
        """
        group_seats_allocated = False
        row_placement = []
        row_sum = len(self.layout[self.row]) - self.remaining_seats_in_row()
        while row_sum < len(self.layout[self.row]) and len(self.groups) > 0:
            group = self.groups[0]

            if group["size"] <= len(self.layout[self.row]) - row_sum:
                row_placement.append(self.groups.pop(0))
                row_sum += row_placement[-1]["size"]
                # await self.seat_group(self.groups[i], i+1)
            else:
                for k in range(len(self.groups)):
                    if self.groups[k]["size"] == len(self.layout[self.row]) - row_sum:
                        row_placement.append(self.groups.pop(k))
                        row_sum += row_placement[-1]["size"]
                        group_seats_allocated = True
                        break # favor equal size groups when possible
                
                if group_seats_allocated:
                    group_seats_allocated = False
                    continue

                for n in range(len(self.groups)):
                    if self.groups[n]["size"] < len(self.layout[self.row]) - row_sum:
                        row_placement.append(self.groups.pop(n))
                        row_sum += row_placement[-1]["size"]
                        group_seats_allocated = True
                        break
                
                # Making it here means we need to wrap the group
                if not group_seats_allocated:
                    group_seats_allocated = False
                    row_placement.append(self.groups.pop(0))
                    row_sum += row_placement[-1]["size"]

        return row_placement


    async def row_modifiers(self, row, placement):
        options = []
        column = 0
        for i in range(len(placement)):
            options.append([])
            for n in range(placement[i]["size"]):
                if len(self.layout[row][column]["modifiers"]) > 0:
                    options[i].extend(self.layout[row][column]["modifiers"])
                column += 1

        return options


    async def group_preference(self, row, placement):
        """
        Handles shuffling groups within a row to meet preferences.
        Shuffling does not happen outside of a row to preserve group order.

        :row_placement: list of groups in row to shuffle
        :return: list of groups in row
        """
        def swap(i, n):
            placement[i], placement[n] = placement[n], placement[i]
        row_modifiers = await self.row_modifiers(row, placement)
        shuffle = []
        for i in range(len(placement)):
            for k in range(len(row_modifiers)):
                if placement[i]["position"] != placement[k]["position"]:
                    if placement[i]["preference"] != placement[k]["preference"]:
                        if any(placement[i]["preference"] in m for m in row_modifiers[k]):
                            shuffle.append([i, k])
        
        for group in range(len(shuffle)):
            swap(group[0], group[1])

        return placement

    
    async def seat_group(self, group_size, group_position):
        """
        Seat a singular group once we've accounted for preferences and group size.

        :group_size: The number of group members to sit
        :group_position: The position this group occupies in the seating queue
        """
        for i in range(group_size):
            self.layout[self.row][self.column]["group"] = group_position

            if self.rtl():
                self.column += 1
            else:
                self.column -= 1

            end_of_row = self.column > len(self.layout[self.row]) - 1 or self.column < 0
            if end_of_row:
                self.row += 1

                # columns could be various sizes within the same rank.
                # reset when going left to right to ensure proper size.
                if self.column != 0 and self.row < len(self.layout) - 1:
                    self.column = len(self.layout[self.row]) - 1
                elif self.column < 0:
                    self.column = 0