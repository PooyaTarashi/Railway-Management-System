from datetime import datetime, timedelta
from collections import OrderedDict


class Train:
    """
    A class representing a train object.

    Attributes
    ----------
    origin : str
        The start place of the train.
    destination : str
        The destination of the train.
    dep_time : datetime
        The time, when the train starts its journey.
    capacity : int
        The free seats in this train

    Methods
    -------
    Has getter and setter for every attribute.

    decrease_capacity(count) -> None:
        decreses capacity for the amount if count.
        the default value of count is 1.
    """

    def __init__(self, origin:str, destination:str, dep_time:datetime, capacity:dict):
        self._origin:str = None
        self._destination:str = None
        self._dep_time:datetime = None
        self._capacity:dict = {}     # capacity is a dictionary with capacity of models and seat type as key.
        self._cancelation_request:list = []      # a list which contains requests for cancelation when the train is full. Items are objs from Reservation class.
        self.origin = origin
        self.destination = destination
        self.dep_time = dep_time
        self.capacity = capacity

    @property
    def origin(self):
        return self._origin
    
    @origin.setter
    def origin(self, origin):
        self._origin = origin

    @property
    def destination(self):
        return self._destination
    
    @destination.setter
    def destination(self, destination):
        self._destination = destination

    @property
    def dep_time(self):
        return self._dep_time
    
    @dep_time.setter
    def dep_time(self, dep_time):
        self._dep_time = dep_time

    @property
    def capacity(self):
        return self._capacity
    
    @capacity.setter
    def capacity(self, capacity):
        self._capacity = capacity    

    @property
    def cancelation_request(self):
        return self._cancelation_request

    def is_cancelation_in_list(self, reservation):
        if reservation in self._cancelation_request:
            return True
        return False

    def decrease_capacity(self, seat_type, count = 1):
        self._capacity[seat_type] -= count

    def increase_capacity(self, seat_type, count = 1):
        self._capacity[seat_type] += count

    def add_cancelation_request(self, reservation):
        self._cancelation_request.append(reservation)

    def pop_cancelation_request(self, reservation):
        self._cancelation_request.pop(0)

    def cancel_done(self):
        self._cancelation_request.pop(0)

class User:
    def __init__(self, name:str):
        self._name:str = None
        self._last_cancelation:datetime = None
        self._reservation_date_record:list = []
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def last_cancelation(self):
        return self._last_cancelation
    
    @last_cancelation.setter
    def last_cancelation(self, time:datetime):
        self._last_cancelation = time


    def add_reservation_record(self, time:datetime):
        self._reservation_date_record.append(time)

    def remove_from_reservation_record(self, time:datetime):
        self._reservation_date_record.remove(time)

    @property
    def reservation_date_record(self):
        return self._reservation_date_record

class Reservation:
    def __init__(self, user:User, train:Train, time:datetime, seat_type:str):
        self._user:User = None
        self._train:Train = None
        self._time:datetime = None
        self._seat_type:str = None
        self.user = user
        self.train = train
        self.time = time
        self.seat_type = seat_type


    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        self._user = user

    @property
    def train(self):
        return self._train
    
    @train.setter
    def train(self, train:Train):
        self._train = train

    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, time:datetime):
        self._time = time

    @property
    def seat_type(self):
        return self._seat_type
    
    @seat_type.setter
    def seat_type(self, seat_type):
        self._seat_type = seat_type

class Railway_System:
    """
    A class representing a railway system.

    Attributes:
    - trains (OrderedDict): A dictionary that stores train objects with their origin and destination as keys.
    - users (OrderedDict): A dictionary that stores user objects with their id as keys.
    - reservations (list): A list that stores reservation objects made by users.

    Methods:
    - add_train(train): Adds a train object to the trains dictionary.
    - add_user(user): Adds a user object to the users dictionary.
    - book(reservation): Appends a reservation object to the reservations list.
    """

    one_hour = timedelta(hours= 1)
    thirty_days = timedelta(days= 30)

    def __init__(self):
        self._trains = OrderedDict()
        self._users = OrderedDict()
        self._reservations = []
        self._results = []

    def add_train(self, cmd):
        if len(cmd) == 4:
            origin, destination, dep_time, capacity = cmd      # vip seats should be 0.
            vip_seats_count = 0
            vip_seats_list = []
        elif (len(cmd) == 5 and cmd[-1] == '0'):
            origin, destination, dep_time, capacity, vip_seats_count = cmd      # vip seats should be 0.
            vip_seats_count = int(vip_seats_count)
            vip_seats_list = []
        else:
            origin, destination, dep_time, capacity, vip_seats_count, vip_seats_list = cmd
            vip_seats_list = vip_seats_list.split()
        
        # definition of vip_seats_dict down here, the 0 key shows the count of normal seats. other keys are the type o seat and their value is their capacity.
        vip_seats_dict = OrderedDict()
        vip_seats_dict['0'] = int(capacity)
        for i in range(1, int(vip_seats_count) + 1):
            vip_seats_dict[str(i)] = int(vip_seats_list[i - 1])
        self._trains[cmd[0] + ' ' + cmd[1]] = Train(origin=origin, destination=destination, dep_time=datetime.strptime(dep_time, "%Y/%m/%d-%H:%M") , capacity=vip_seats_dict)

    def add_user(self, username):
        self._users[username] = User(username)

    def which_reservation(self, username, origin, destination, seat_type) -> Reservation:
        for reservation in self._reservations:
            if reservation.train.origin == origin and reservation.train.destination == destination and reservation.user.name == username and reservation.seat_type == seat_type:
                return reservation
        return None
            
    def is_there_same_cancelation(self, username, origin, destination, cancelation_time, command_list) -> bool:
        for cmd in command_list:
            if cmd[1] == username and cmd[2] == origin and cmd[3] == destination and datetime.strptime(cmd[0], "%Y/%m/%d-%H:%M") < cancelation_time:
                return True
        return False

    def book(self, cmd):
        # getting input:
        if len(cmd) == 5:
            reserve_time_str, username, origin, destination, print_id = cmd
            seat_type = '0'
        else:
            reserve_time_str, username, origin, destination, seat_type, print_id = cmd
        reserve_time = datetime.strptime(reserve_time_str, "%Y/%m/%d-%H:%M")
        train_name = origin + ' ' + destination
        queued_request:Reservation = 0
        reservation_validity = "Movafagh"

        # add user if not in users:
        if username not in self._users.keys():
            self._users[username] = User(username)
        the_user:User = self._users[username]
        
        # checking if is there such a train:
        if train_name not in self._trains.keys():
            reservation_validity = "Na Movafagh. Masir vojood nadarad."
        else:
            the_train:Train = self._trains[train_name]

        # checking whether the train dep_time is valid to reserve
        if reservation_validity == "Movafagh":
            if the_train.dep_time <= reserve_time:
                reservation_validity = "Na Movafagh. Masir vojood nadarad."
            
        # checking if user can buy a VIP or not:
        if reservation_validity == "Movafagh":
            if seat_type != '0':
                if len(the_user.reservation_date_record) == 0:
                    reservation_validity = "Na Movafagh. Shoma reserve qabli nadarid va nemitavanid VIP reserve konid."
                elif the_user.reservation_date_record[-1] + Railway_System.thirty_days < reserve_time:
                    reservation_validity = "Na Movafagh. Shoma reserve qabli nadarid va nemitavanid VIP reserve konid."

        # checking if is there cancelation request in list or not:
        if reservation_validity == "Movafagh" and seat_type != '0':
            if len(the_train.cancelation_request) != 0:
                queued_request:Reservation = the_train.cancelation_request[0]
                the_train.pop_cancelation_request(queued_request)
                self._reservations.remove(queued_request)
                the_train.increase_capacity(seat_type=seat_type)
                queued_request.user.last_cancelation = reserve_time

        # checking capacity
        if reservation_validity == "Movafagh":
            if the_train.capacity[seat_type] == 0:
                reservation_validity = "Na Movafagh. Zarfiat vojood nadarad."

        # fianl action:
        if reservation_validity == "Movafagh":
            self._reservations.append(Reservation(user=the_user, train=the_train, time=reserve_time, seat_type=seat_type))
            the_user.add_reservation_record(reserve_time)
            the_train.decrease_capacity(seat_type=seat_type)
            # printing result
            if seat_type == '0':
                seat_type_text = "Normal"
            else:
                seat_type_text = "VIP" + seat_type
            if queued_request != 0:
                self._results.append(["Reserve karbar " + username + " baraye belit model " + seat_type_text + " movafagh bood. Hamchenin Reserve karbar " + queued_request.user.name + " baraye in belit cancel shod.", print_id])
            else:
                self._results.append(["Reserve karbar " + username + " baraye belit model " + seat_type_text + " movafagh bood.", int(print_id)])

        else:
            self._results.append([reservation_validity, print_id])
            


    def cancel_reservation(self, cmd, command_list):
        if len(cmd) == 6:
            cancelation_time_str, username, origin, destination, cancel_shit_word, print_id = cmd
            seat_type = '0'
        else:
            cancelation_time_str, username, origin, destination, seat_type, cancel_shit_word, print_id = cmd
        cancelation_time = datetime.strptime(cancelation_time_str, "%Y/%m/%d-%H:%M")
        train_name = origin + ' ' + destination
        cancelation_validity = "Movafagh"
        
        # checking whether the reservation exist or not:
        the_reservation:Reservation = self.which_reservation(username, origin, destination, seat_type)
        if the_reservation == None:
            cancelation_validity = "Na Movafagh. Reserve vojood nadarad."
        else:
            the_train:Train = self._trains[train_name]
            the_user:User = self._users[username]

        # checking if train is gone or not:
        if cancelation_validity == "Movafagh":
            if the_train.dep_time < cancelation_time:
                cancelation_validity = "Na Movafagh. The train is gone."

        # checking if is such reservation in train cancelation list:
        if cancelation_validity == "Movafagh":
            if (the_reservation in the_train.cancelation_request):
                cancelation_validity = "Na Movafagh. Darkhast cancel shoma qablan sabt shode ast."

        # checking last cancelation
        if cancelation_validity == "Movafagh":
            if the_user.last_cancelation == None:
                pass
            elif ((the_user.last_cancelation + Railway_System.one_hour) > cancelation_time):
                cancelation_validity = "Na Movafagh. Shoma dar 1 sa'at akhir darkhast cancel dashtid."

        # the fianl part:
        if cancelation_validity == "Movafagh":
            if the_reservation.seat_type == '0':
                self._reservations.remove(the_reservation)
                the_train.increase_capacity(the_reservation.seat_type)
                the_user.last_cancelation = cancelation_time
                the_user.remove_from_reservation_record(the_reservation.time)
                self._results.append(["Reserve karbar " + the_user.name + " ba movaghiat cancel shod.", print_id])
            else:
                the_train.cancelation_request.append(the_reservation)
                self._results.append(["Darkhast cancel reserve karbar " + the_user.name + " baraye belit VIP" + the_reservation.seat_type + " sabt shod.", print_id])
        else:
            self._results.append([cancelation_validity, print_id])

    def print_result(self):
        # to be honest, I messed up, I thought results should be printed with input order
        # print_ready_ls = sorted(self._results, key=Railway_System.idx_key)
        for item in self._results:
            print(item[0], sep='\n')
        

    @staticmethod
    def time_key(ls):
        return datetime.strptime(ls[0], "%Y/%m/%d-%H:%M")
    
    @staticmethod
    def idx_key(ls):
        return ls[-1]
    
    


ali_baba = Railway_System()

n = int(input())
trains_commands = []
trains_validity = True
for i in range(n):
    data = input().split()
    if len(data) != 5 and len(data) != 4:
        trains_validity = False
    trains_commands.append(data)
    if data[-1].isdigit() and data[-1] != '0' and data[-2].isdigit() != False:
        trains_commands[-1].append(input())

if trains_validity:
    for cmd in trains_commands:
        ali_baba.add_train(cmd)
    print("Done")
else:
    print("Error")


# if it didn't work, I will bring the whole block below under an if statement. if trains_validity...
commands_list = []
if trains_validity:
    k = int(input())
    for i in range(k):
        data = input().split()
        data.append(i)
        commands_list.append(data)
        
    # print(*commands_list, sep='\n')
    # print("====================================================================================================")
    commands_list = sorted(commands_list, key=Railway_System.time_key)        
    # print(*commands_list, sep='\n')

        
    for command in commands_list:
        if command[-2] != "cancel":
            ali_baba.book(command)
        else:
            ali_baba.cancel_reservation(command, commands_list)


# print("========================================================================================================")
ali_baba.print_result()