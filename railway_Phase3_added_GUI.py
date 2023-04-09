from tkinter import *
from datetime import datetime, timedelta, time
from collections import OrderedDict
from copy import deepcopy


class Vehicle:
    """
    A class representing a vehicle object.

    Attributes
    ----------
    
    origin : str
        The start place of the vehicle.
    destination : str
        The destination of the vehicle.
    dep_time : datetime
        The time, when the vehicle starts its journey.
    capacity : int
        The free seats in this vehicle

    Methods
    -------
    Has getter and setter for every attribute.

    decrease_capacity(count) -> None:
        decreses capacity for the amount of count.
        when someone reserves, this function is called.
        the default value of count is 1.

    increase_capacity(count) -> None:
        increses capacity for the amount of count.
        when someone cancels his reservation, this function is called.
        the default value of count is 1.
    """

    
    def __init__(self, vehicle_type:str, origin:str, destination:str, dep_time:datetime, capacity:dict):
        self._vehicle_type:str = None
        self._origin:str = None
        self._destination:str = None
        self._dep_time:datetime = None
        self._capacity:dict = {}     # capacity is a dictionary with capacity of models and seat type as key.
        self._cancelation_request:list = []      # a list which contains requests for cancelation when the vehicle is full. Items are objs from Reservation class.
        self._age_limitation:int = 1000
        self.time_limit = False
        self.start_time = None
        self.end_time = None
        self.active_times_limitation = False
        self.active_times_limitation_for_else = False
        self.last_reservation:datetime = None
        self.reservation_step:timedelta = None
        self.reserves_in_this_step = 0
        self.reserve_limit = 0
        self.vehicle_type = vehicle_type
        self.origin = origin
        self.destination = destination
        self.dep_time = dep_time
        self.capacity = capacity
        self.primary_capacity:dict = deepcopy(capacity)
        self.const_primary_capacity:dict = deepcopy(capacity)


    @property
    def vehicle_type(self):
        return self._vehicle_type
    
    @vehicle_type.setter
    def vehicle_type(self, vehicle_type):
        self._vehicle_type = vehicle_type

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
    
    @property
    def age_limitation(self):
        return self._age_limitation
    
    @age_limitation.setter
    def age_limitation(self, age):
        self._age_limitation = age

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
    def __init__(self, name:str, age:int):
        self._name:str = None
        self._age:int = None
        self._last_cancelation:datetime = None
        self._reservation_date_record:list = []
        self.name = name
        self.age = age


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

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
    def __init__(self, user:User, vehicle:Vehicle, time:datetime, seat_type:str):
        self._user:User = None
        self._vehicle:Vehicle = None
        self._time:datetime = None
        self._seat_type:str = None
        self.user = user
        self.vehicle = vehicle
        self.time = time
        self.seat_type = seat_type


    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        self._user = user

    @property
    def vehicle(self):
        return self._vehicle
    
    @vehicle.setter
    def vehicle(self, vehicle:Vehicle):
        self._vehicle = vehicle

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
    - vehicles (OrderedDict): A dictionary that stores vehicle objects with their origin and destination as keys.
    - users (OrderedDict): A dictionary that stores user objects with their id as keys.
    - reservations (list): A list that stores reservation objects made by users.

    Methods:
    - add_vehicle(vehicle): Adds a vehicle object to the vehicles dictionary.
    - add_user(user): Adds a user object to the users dictionary.
    - book(reservation): Appends a reservation object to the reservations list.
    """

    one_hour = timedelta(hours= 1)
    thirty_days = timedelta(days= 30)

    def __init__(self):
        self._vehicles = OrderedDict()
        self._users = OrderedDict()
        self._reservations = []
        self._results = []
        self.rule_idx = 0
        

    def add_vehicle(self, cmd):
        if len(cmd) == 5:
            vehicle_type, origin, destination, dep_time, capacity = cmd      # vip seats should be 0.
            vip_seats_count = 0
            vip_seats_list = []
        elif (len(cmd) == 6 and cmd[-1] == '0'):
            vehicle_type, origin, destination, dep_time, capacity, vip_seats_count = cmd      # vip seats should be 0.
            vip_seats_count = int(vip_seats_count)
            vip_seats_list = []
        else:
            vehicle_type, origin, destination, dep_time, capacity, vip_seats_count, vip_seats_list = cmd
            vip_seats_list = vip_seats_list.split()
        
        # definition of vip_seats_dict down here, the 0 key shows the count of normal seats. other keys are the type o seat and their value is their capacity.
        vip_seats_dict = OrderedDict()
        vip_seats_dict['0'] = int(capacity)
        for i in range(1, int(vip_seats_count) + 1):
            vip_seats_dict[str(i)] = int(vip_seats_list[i - 1])
        self._vehicles[cmd[0] + ' ' + cmd[1] + ' ' + cmd[2]] = Vehicle(vehicle_type=vehicle_type, origin=origin, destination=destination, dep_time=datetime.strptime(dep_time, "%Y/%m/%d-%H:%M") , capacity=vip_seats_dict)

    def add_user(self, username):
        self._users[username] = User(username)

    def which_reservation(self, username, vehicle, origin, destination, seat_type) -> Reservation:
        for reservation in self._reservations:
            if (reservation.vehicle.vehicle_type == vehicle and reservation.vehicle.origin == origin and reservation.vehicle.destination == destination and reservation.user.name == username and reservation.seat_type == seat_type) or (vehicle == "Auto" and reservation.vehicle.origin == origin and reservation.vehicle.destination == destination and reservation.user.name == username and reservation.seat_type == seat_type):
                return reservation
        return None
            
    def is_there_same_cancelation(self, username, origin, destination, cancelation_time, command_list) -> bool:
        for cmd in command_list:
            if cmd[1] == username and cmd[2] == origin and cmd[3] == destination and datetime.strptime(cmd[0], "%Y/%m/%d-%H:%M") < cancelation_time:
                return True
        return False
    
    def decision_maker(self, reserve_time:datetime, origin, destination, seat_type, username) -> Vehicle:
        tmp_vehcile_dep_time:datetime = None
        suitable_vehicles:list = []
        if (username not in self._users.keys()) and seat_type != '0':
            return "Na Movafagh. Shoma reserve qabli nadarid va nemitavanid VIP reserve konid."
        if username in self._users.keys() and seat_type != '0':
            if len(self._users[username].reservation_date_record) == 0:
                return "Na Movafagh. Shoma reserve qabli nadarid va nemitavanid VIP reserve konid."
            if self._users[username].reservation_date_record[-1]  + Railway_System.thirty_days < reserve_time:
                return "Na Movafagh. Shoma reserve qabli nadarid va nemitavanid VIP reserve konid."

        for vehicle in self._vehicles.values():
            if vehicle.dep_time > reserve_time and vehicle.origin == origin and vehicle.destination == destination and (seat_type in vehicle.capacity.keys()):
                suitable_vehicles.append(vehicle)

        suitable_vehicles = sorted(suitable_vehicles, key=Railway_System.dep_time_key)

        for vehicle in suitable_vehicles:
            if vehicle.capacity[seat_type] != 0:
                return vehicle.vehicle_type
        if len(suitable_vehicles) == 0:
            return None
        else:
            return "Na Movafagh. Zarfiat vojood nadarad."


    def book(self, cmd):
        # getting input:
        if len(cmd) == 6:
            reserve_time_str, username, origin, destination, age, print_id = cmd
            seat_type = '0'
            vehicle = "Auto"
        elif len(cmd) == 7:
            reserve_time_str, username, origin, destination, vehicle_or_type, age, print_id = cmd
            if vehicle_or_type.isdigit():
                seat_type = vehicle_or_type
                vehicle = "Auto"
            else:
                seat_type = '0'
                vehicle = vehicle_or_type
        else:
            reserve_time_str, username, origin, destination, vehicle, age, seat_type, print_id = cmd
        reserve_time = datetime.strptime(reserve_time_str, "%Y/%m/%d-%H:%M")
        if vehicle == "Auto":
            vehicle = self.decision_maker(reserve_time, origin, destination, seat_type, username)
        queued_request:Reservation = 0
        age:int = int(age)
        reservation_validity = "Movafagh"
        if vehicle == None:
            reservation_validity = "Na Movafagh. Masir vojood nadarad."
        elif vehicle == "Na Movafagh. Zarfiat vojood nadarad.":
            reservation_validity = vehicle
        elif vehicle == "Na Movafagh. Shoma reserve qabli nadarid va nemitavanid VIP reserve konid.":
            reservation_validity = vehicle
        else:
            vehicle_name = vehicle + ' ' + origin + ' ' + destination

        
        # add user if not in users:
        if username not in self._users.keys():
            self._users[username] = User(username, age)
        else:
            self._users[username].age = age
        the_user:User = self._users[username]

        # checking if is there such a vehicle:
        if reservation_validity == "Movafagh":
            if (vehicle_name not in self._vehicles.keys()) and (Railway_System.capitalize_first_letter(vehicle_name) not in self._vehicles.keys()):
                reservation_validity = "Na Movafagh. Masir vojood nadarad."
            else:
                the_vehicle:Vehicle = self._vehicles[Railway_System.capitalize_first_letter(vehicle_name)]

        # checking time limits
        if reservation_validity == "Movafagh":
            reserve_clock = time(hour=int(reserve_time_str[-5:-3]), minute=int(reserve_time_str[-2:]))
            if the_vehicle.time_limit:
                if reserve_clock < the_vehicle.end_time and reserve_clock > the_vehicle.start_time:
                    reservation_validity = "Na Movafagh. Emkan reserve vojood nadarad."

        # checking if age is ok to reserve or not
        if reservation_validity == "Movafagh":
            if age > the_vehicle.age_limitation:
                reservation_validity = "Na Movafagh. Emkan reserve vojood nadarad."
        
        # checking whether the vehicle dep_time is valid to reserve
        if reservation_validity == "Movafagh":
            if the_vehicle.dep_time <= reserve_time:
                reservation_validity = "Na Movafagh. Masir vojood nadarad."
            
        # checking if user can buy a VIP or not:
        if reservation_validity == "Movafagh":
            if seat_type != '0':
                if len(the_user.reservation_date_record) == 0:
                    reservation_validity = "Na Movafagh. Shoma reserve qabli nadarid va nemitavanid VIP reserve konid."
                elif the_user.reservation_date_record[-1] + Railway_System.thirty_days < reserve_time:
                    reservation_validity = "Na Movafagh. Shoma reserve qabli nadarid va nemitavanid VIP reserve konid."

        # if reservation_validity == "Movafagh":
        #     if the_vehicle.capacity[seat_type] <= 0 and (the_vehicle.const_primary_capacity[seat_type] - the_vehicle.primary_capacity[seat_type]) > 0:
        #         reservation_validity = "Na Movafagh. Emkan reserve vojood nadarad."

        # checking if is there cancelation request in list or not:
        if reservation_validity == "Movafagh" and seat_type != '0':
            if len(the_vehicle.cancelation_request) != 0:
                queued_request:Reservation = the_vehicle.cancelation_request[0]
                the_vehicle.pop_cancelation_request(queued_request)
                self._reservations.remove(queued_request)
                the_vehicle.increase_capacity(seat_type=seat_type)
                queued_request.user.last_cancelation = reserve_time

        # checking capacity
        if reservation_validity == "Movafagh":
            if the_vehicle.capacity[seat_type] <= 0:
                reservation_validity = "Na Movafagh. Zarfiat vojood nadarad."

        # time per period operation for week
        if reservation_validity == "Movafagh":
            if the_vehicle.active_times_limitation:
                if the_vehicle.last_reservation != None:    
                    if (reserve_time - the_vehicle.last_reservation) > the_vehicle.reservation_step:
                        the_vehicle.reserves_in_this_step = 0
                    if the_vehicle.reserves_in_this_step > the_vehicle.reserve_limit:
                        reservation_validity = "Na Movafagh. Emkan reserve vojood nadarad."

        # time per period operation for else
        if reservation_validity == "Movafagh":
            if the_vehicle.active_times_limitation_for_else:
                if the_vehicle.last_reservation != None:
                    if the_vehicle.reservation_step == "rooz":
                        avail_time = the_vehicle.last_reservation + timedelta(days=1)
                        avail_time_str = datetime.strftime(avail_time, "%Y/%m/%d-%H:%M")
                        avail_time_str = avail_time_str[:10]
                        avail_time_str += "-00:00"
                        avail_time = datetime.strptime(avail_time_str, "%Y/%m/%d-%H:%M")
                        if avail_time < reserve_time:
                            the_vehicle.reserves_in_this_step = 0
                        if the_vehicle.reserves_in_this_step > the_vehicle.reserve_limit:
                            reservation_validity = "Na Movafagh. Emkan reserve vojood nadarad."
                    else:
                        avail_time = the_vehicle.last_reservation + timedelta(days=30)
                        avail_time_str = datetime.strftime(avail_time, "%Y/%m/%d-%H:%M")
                        avail_time_str = avail_time_str[:7]
                        avail_time_str += "/00-00:00"
                        avail_time = datetime.strptime(avail_time_str, "%Y/%m/%d-%H:%M")
                        if avail_time < reserve_time:
                            the_vehicle.reserves_in_this_step = 0
                        if the_vehicle.reserves_in_this_step >= the_vehicle.reserve_limit:
                            reservation_validity = "Na Movafagh. Emkan reserve vojood nadarad."
        

        # fianl action:
        if reservation_validity == "Movafagh":
            self._reservations.append(Reservation(user=the_user, vehicle=the_vehicle, time=reserve_time, seat_type=seat_type))
            the_user.add_reservation_record(reserve_time)
            the_vehicle.decrease_capacity(seat_type=seat_type)
            the_vehicle.reserves_in_this_step += 1
            the_vehicle.last_reservation = reserve_time
            # printing result
            if seat_type == '0':
                seat_type_text = "Normal"
            else:
                seat_type_text = "VIP" + seat_type
            if queued_request != 0:
                print("Reserve karbar " + username + " baraye belit " + vehicle.lower() + " model " + seat_type_text + " movafagh bood. Hamchenin Reserve karbar " + queued_request.user.name + " baraye in belit cancel shod.")
            else:
                print("Reserve karbar " + username + " baraye belit " + vehicle.lower() + " model " + seat_type_text + " movafagh bood.")

        else:
            print(reservation_validity)
            
    def cancel_reservation(self, cmd, command_list):
        if len(cmd) == 6:
            cancelation_time_str, username, origin, destination, cancel_shit_word, print_id = cmd
            vehicle = "Auto"
            seat_type = '0'
        elif len(cmd) == 7:
            if cmd[-3].isdigit():
                cancelation_time_str, username, origin, destination, vehicle_or_seat_type, cancel_shit_word, print_id = cmd
                seat_type = vehicle_or_seat_type
                vehicle = "Auto"
            else:
                cancelation_time_str, username, origin, destination, vehicle_or_seat_type, cancel_shit_word, print_id = cmd
                vehicle = vehicle_or_seat_type
                seat_type = '0'
        else:
            cancelation_time_str, username, origin, destination, vehicle, seat_type, cancel_shit_word, print_id = cmd
        cancelation_time = datetime.strptime(cancelation_time_str, "%Y/%m/%d-%H:%M")
        vehicle_name = vehicle + ' ' + origin + ' ' + destination
        vehicle_name = Railway_System.capitalize_first_letter(vehicle_name)
        cancelation_validity = "Movafagh"
        
        # checking whether the reservation exist or not:
        the_reservation:Reservation = self.which_reservation(username, Railway_System.capitalize_first_letter(vehicle), origin, destination, seat_type)
        if the_reservation == None:
            cancelation_validity = "Na Movafagh. Reserve vojood nadarad."
        else:
            the_vehicle:Vehicle = self._vehicles[vehicle_name]
            the_user:User = self._users[username]

        # checking if vehicle is gone or not:
        if cancelation_validity == "Movafagh":
            if the_vehicle.dep_time < cancelation_time:
                cancelation_validity = "Na Movafagh. The vehicle is gone."

        # checking if is such reservation in vehicle cancelation list:
        if cancelation_validity == "Movafagh":
            if (the_reservation in the_vehicle.cancelation_request):
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
                the_vehicle.increase_capacity(the_reservation.seat_type)
                the_user.last_cancelation = cancelation_time
                the_user.remove_from_reservation_record(the_reservation.time)
                print("Reserve karbar " + the_user.name + " baraye " + vehicle.lower() + " ba movafaghiat cancel shod.")
            else:
                the_vehicle.cancelation_request.append(the_reservation)
                print("Darkhast cancel reserve karbar " + the_user.name + " baraye belit " + vehicle.lower() + " VIP" + the_reservation.seat_type + " sabt shod.")
        else:
            print(cancelation_validity)

    def cut_the_capacity(self, cmd):
        self.rule_idx += 1
        print("Qanoon shomareye " + str(self.rule_idx) + " ba movafaghiat sabt shod.")
        vehicle_type = Railway_System.capitalize_first_letter(cmd[4])
        unavailable_percentage = 1 - (int(cmd[6]) / 100)
        
        # changes primary capacity
        for vehicle in self._vehicles.values():
            if vehicle.vehicle_type == vehicle_type:
                for key in vehicle.capacity.keys():
                    vehicle.primary_capacity[key] = vehicle.primary_capacity[key] - int(unavailable_percentage * vehicle.const_primary_capacity[key])
                    vehicle.capacity[key] = vehicle.capacity[key] - int(unavailable_percentage * vehicle.const_primary_capacity[key])

        # sacks passengers
        for reserve in reversed(self._reservations):
            if reserve.vehicle.vehicle_type == vehicle_type:
                if reserve.vehicle.capacity[reserve.seat_type] < 0:
                    reserve.vehicle.capacity[reserve.seat_type] += 1
                    self._reservations.remove(reserve)
                    if reserve.seat_type == '0':
                        print("Reserve karbar " + reserve.user.name + " baraye " + reserve.vehicle.vehicle_type.lower() + " model Normal be dadil qanoon " + str(self.rule_idx) + " cancel shod.")
                    else:
                        print("Reserve karbar " + reserve.user.name + " baraye " + reserve.vehicle.vehicle_type.lower() + " model VIP" + reserve.seat_type + " be dadil qanoon " + str(self.rule_idx) + " cancel shod.")




    def apply_age_limits(self, cmd):
        self.rule_idx += 1
        print("Qanoon shomareye " + str(self.rule_idx) + " ba movafaghiat sabt shod.")
        vehicle_type = Railway_System.capitalize_first_letter(cmd[2])
        age_limitation = int(cmd[6])
        vehicle:Vehicle = None
        reserve:Reservation = None
        for vehicle in self._vehicles.values():
            if vehicle.vehicle_type == vehicle_type:
                vehicle.age_limitation = age_limitation

        for reserve in self._reservations:
            if reserve.vehicle.vehicle_type == vehicle_type:
                if reserve.user.age > reserve.vehicle.age_limitation:
                    reserve.vehicle.capacity[reserve.seat_type] += 1
                    self._reservations.remove(reserve)
                    if reserve.seat_type == '0':
                        print("Reserve karbar " + reserve.user.name + " baraye " + reserve.vehicle.vehicle_type.lower() + " model Normal be dadil qanoon " + str(self.rule_idx) + " cancel shod.")
                    else:
                        print("Reserve karbar " + reserve.user.name + " baraye " + reserve.vehicle.vehicle_type.lower() + " model VIP" + reserve.seat_type + " be dadil qanoon " + str(self.rule_idx) + " cancel shod.")

    def apply_time_limit(self, cmd):
        vehicle_type = Railway_System.capitalize_first_letter(cmd[2])
        for vehicle in self._vehicles.values():
            if vehicle.vehicle_type == vehicle_type:
                vehicle.time_limit = True
                vehicle.start_time = time(hour=int(cmd[5]))
                vehicle.end_time = time(hour=int(cmd[7]))

    def apply_reserves_count_for_week(self, cmd):
        vehicle_type = Railway_System.capitalize_first_letter(cmd[4])
        times_per_step = int(cmd[7])
        time_step = timedelta(days=7)
        
        # activating rule
        # vehicle:Vehicle = None
        for vehicle in self._vehicles.values():
            if vehicle.vehicle_type == vehicle_type:
                vehicle.active_times_limitation = True
                vehicle.reservation_step = time_step
                vehicle.reserve_limit = times_per_step
                # vehicle.reserves_in_this_step = times_per_step

    def apply_reserves_count_for_else(self, cmd):
        vehicle_type = Railway_System.capitalize_first_letter(cmd[4])
        times_per_step = int(cmd[7])
        time_step = cmd[10]

        # vehicle:Vehicle = None
        for vehicle in self._vehicles.values():
            if vehicle.vehicle_type == vehicle_type:
                vehicle.active_times_limitation_for_else = True
                vehicle.reservation_step = time_step
                vehicle.reserve_limit = times_per_step

    def print_result(self):
        # to be honest, I messed up, I thought results should be printed with input order
        # print_ready_ls = sorted(self._results, key=Railway_System.idx_key)
        for item in self._results:
            print(item[0], sep='\n')
        

    @staticmethod
    def time_key(ls):
        return datetime.strptime(ls[0], "%Y/%m/%d-%H:%M")

    @staticmethod
    def dep_time_key(vehicle:Vehicle):
        return vehicle.dep_time
    
    @staticmethod
    def idx_key(ls):
        return ls[-1]
    
    @staticmethod
    def capitalize_first_letter(my_string:str):
        my_str = my_string.split()
        result = ''
        for word in my_str:
            char = word[0]
            char = char.capitalize()
            result += (char + word[1:])
            result += ' '
        return result[:-1]
    



def main_app():
    ali_baba = Railway_System()
    n = int(n_inp.get())
    print(n)
    vehicles_commands = []
    vehicles_validity = True
    for i in range(n):
        data = input().split()
        if len(data) != 6 and len(data) != 5:
            vehicles_validity = False
        vehicles_commands.append(data)
        if vehicles_validity:    
            if data[-1].isdigit() and data[-1] != '0' and data[-2].isdigit() != False:
                vehicles_commands[-1].append(input())

    if vehicles_validity:
        for cmd in vehicles_commands:
            ali_baba.add_vehicle(cmd)
        print("Done")
    else:
        print("Error")


    # if it didn't work, I will bring the whole block below under an if statement. if vehicles_validity...
    commands_list = []
    if vehicles_validity:
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
            if command[-2] != "cancel" and (command[1] != "Zarfiat" and command[2] != "reserve" and command[3] != "baraye") and (command[1] != "Reserve" and command[3] != "baraye" and command[4] != "afrad") and (command[1] != "Reserve" and command[3] != "Reserve" and command[4] != "sa'at") and (command[1] != "Emkan"):
                ali_baba.book(command)
            elif command[1] == "Zarfiat" and command[2] == "reserve" and command[3] == "baraye":
                ali_baba.cut_the_capacity(command)
            elif command[1] == "Reserve" and command[3] == "baraye" and command[4] == "afrad":
                ali_baba.apply_age_limits(command)
            elif command[1] == "Reserve" and command[3] == "dar" and command[4] == "sa'at":
                ali_baba.apply_time_limit(command)
            elif command[1] == "Emkan":
                if command[10] == "hafte":
                    ali_baba.apply_reserves_count_for_week(command)
                else:
                    ali_baba.apply_reserves_count_for_else(command)
            else:
                ali_baba.cancel_reservation(command, commands_list)


    # print("========================================================================================================")
    # ali_baba.print_result()


window = Tk()


def get_n():
    admin_name.pack_forget()
    admin_pass.pack_forget()
    enter_button.pack_forget()
    login_text = Label(window, text="logged in as {}\nHow many vehicle infos do you want to add?".format(admin_name.get()))
    login_text.pack()
    n_inp = Entry(window)
    n_inp.pack()
    sub_but = Button(window, text="Submit")
    sub_but.pack()
    sub_but.config(command=main_app)

window.geometry("600x360")
# making entry which does nothing
admin_name = Entry(window)
admin_name.pack()
admin_pass = Entry(window, show="*")
admin_pass.pack()
enter_button = Button(window, text="Enter", command=get_n)
enter_button.pack()




window.mainloop()


