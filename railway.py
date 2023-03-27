from datetime import datetime, timedelta
from collections import OrderedDict

# now let's add second phase

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

    def __init__(self, origin:str, destination:str, dep_time:datetime, capacity:int):
        self._origin = None
        self._destination = None
        self._dep_time = None
        self._capacity = 0
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

    def decrease_capacity(self, count = 1):
        self._capacity -= count

    def increase_capacity(self, count = 1):
        self._capacity += count

class User:
    def __init__(self, name:str):
        self._name = None
        self._last_cancelation = None
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

class Reservation:
    def __init__(self, user:User, train:Train, time:datetime):
        self._user = None
        self._train = None
        self._time = None
        self.user = user
        self.train = train
        self.time = time


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

    def __init__(self):
        self._trains = OrderedDict()
        self._users = OrderedDict()
        self._reservations = []

    def add_train(self, cmd):
        origin, destination, dep_time, capacity = cmd
        self._trains[cmd[0] + ' ' + cmd[1]] = Train(origin=origin, destination=destination, dep_time=datetime.strptime(dep_time, "%Y/%m/%d-%H:%M") , capacity=int(capacity))

    def add_user(self, username):
        self._users[username] = User(username)

    def which_reservation(self, username, origin, destination) -> Reservation:
        for reservation in self._reservations:
            if reservation.train.origin == origin and reservation.train.destination == destination and reservation.user.name == username:
                return reservation

    def book(self, cmd):
        reserve_time_str, username, origin, destination = cmd
        reserve_time = datetime.strptime(reserve_time_str, "%Y/%m/%d-%H:%M")
        train_name = origin + ' ' + destination
        reservation_validity = True
        if train_name not in self._trains.keys():
            reservation_validity = False
        else:
            if reserve_time >= self._trains[train_name].dep_time:
                # print("reserve time is after trains start")
                reservation_validity = False
            if self._trains[train_name].capacity == 0:
                # print("Train out of capacity")
                reservation_validity = False
        
        if reservation_validity:
            if username not in self._users.keys():
                self.add_user(username)
            self._reservations.append(Reservation(user= self._users[username], train= self._trains[train_name] , time= reserve_time))
            self._trains[train_name].decrease_capacity()
            print("Movafagh")
        else:
            print("Na Movafagh")

    def cancel_reservation(self, cmd):
        cancelation_time_str, username, origin, destination = cmd[:-1]
        cancelation_time = datetime.strptime(cancelation_time_str, "%Y/%m/%d-%H:%M")
        train_name = origin + ' ' + destination
        cancelation_validity = True

        if (train_name not in self._trains.keys()) or (username not in self._users.keys()) or (self.which_reservation(username, origin, destination) == None):
            cancelation_validity = False
            # print("there is no such train or user or reservation")
        else:
            the_train:Train = self._trains[train_name]
            the_user:User = self._users[username]
            the_reservation:Reservation = self.which_reservation(username, origin, destination)
        
        if cancelation_validity and the_user.last_cancelation != None:
            if (the_user.last_cancelation + Railway_System.one_hour >= cancelation_time) or (cancelation_time < the_reservation.time):
                cancelation_validity = False
                # print("you have already canceled a train during last hour")
        elif cancelation_validity:
            if cancelation_time >= the_train.dep_time or (cancelation_time < the_reservation.time):
                # print("the train is gone! what do you want to cancel????")
                cancelation_validity = False

        if cancelation_validity:
            self._reservations.remove(the_reservation)
            the_train.increase_capacity()
            the_user.last_cancelation = cancelation_time
            print("Movafagh")
        else:
            print("Na Movafagh")


ali_baba = Railway_System()

n = int(input())
trains_commands = []
trains_validity = True
for i in range(n):
    data = input().split()
    if len(data) != 4:
        trains_validity = False
    trains_commands.append(data)

if trains_validity:
    for cmd in trains_commands:
        ali_baba.add_train(cmd)
    print("Done")
else:
    print("Error")


# if it didn't work, I will bring the whole block below under an if statement. if trains_validity...
if trains_validity:
    k = int(input())
    for i in range(k):
        data = input().split()
        if data[-1] != "cancel":
            ali_baba.book(data)
        else:
            ali_baba.cancel_reservation(data)

