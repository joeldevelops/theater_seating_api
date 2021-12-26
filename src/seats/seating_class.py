class Seating:
    def __init__(self, groups, layout):
        self.row = 0
        self.column = 0
        self.groups = groups # treat groups like a queue
        self.layout = layout


    def rtl(self):
        return self.row % 2 == 0 # Right to left on even rows


    def rank_seating_layout(self):
        return self.layout


    def next_group(self):
        for i in range(len(self.groups)):
            if self.groups[i] is not None:
                return i

        return None



    def remaining_seats_in_row(self):
        """
        Return the seats left in the current row. The current value of self.column
        will always be a valid seat.
        """
        if self.rtl():
            return len(self.layout[self.row]) - self.column
        else:
            return self.column + 1


    async def seat_row(self):
        go_to_next = False
        while self.next_group() is not None:
            i = self.next_group()
            print (i)
            print (self.groups)
            if self.groups[i] <= self.remaining_seats_in_row():
                await self.seat_group(self.groups[i], i+1)
                self.groups[i] = None
            else:
                for k in range(i, len(self.groups)):
                    if self.groups[k] == self.remaining_seats_in_row():
                        await self.seat_group(self.groups[k], k+1)
                        self.groups[k] = None
                        go_to_next = True
                        break # favor equal size groups when possible
                
                if go_to_next:
                    go_to_next = False
                    continue

                for n in range(i, len(self.groups)):
                    if self.groups[n] < self.remaining_seats_in_row():
                        await self.seat_group(self.groups[n], n+1)
                        self.groups[n] = None

    
    async def seat_group(self, group, group_position):
        for i in range(group):
            self.layout[self.row][self.column] = group_position

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