from flask import Flask, request, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from sqlalchemy.dialects import postgresql
import json
import os
import ast

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Plane():
    # id = db.Column(db.Integer, primary_key=True)
    # seatsGrid = db.Column(postgresql.ARRAY(db.Integer, dimensions=2))
    # pasengers = db.Column(db.Integer)

    def __init__(self,seatsGrid, passengers):
        self.seats = []
        self.seatsGrid = seatsGrid
        Plane.filled = 0
        Plane.passengers = passengers
    
    def create_seats(self):
        for li in self.seatsGrid:
            if li == self.seatsGrid[0]:
                c_first = leftComp(li)
                c_first.create_seats()
                self.seats.append(c_first)
                break

        if len(self.seatsGrid) > 2:
            for li in self.seatsGrid[1:-1]:
                c_mid = middleComp(li)
                c_mid.create_seats()
                self.seats.append(c_mid)

        for li in self.seatsGrid:
            if li == self.seatsGrid[-1]:
                c_end = rightComp(li)
                c_end.create_seats()
                self.seats.append(c_end)
                break

    def print_seats(self):
        max_row = self.get_max_rows()
        for i in range(max_row):
            for comp in self.seats:
                if i < len(comp.space):
                    r = comp.space[i]
                    print(r, end="  " * max_row)
                else:
                    for j in range((len(comp.space[0]))):
                        print(end="          ")
            print()

    def allocate_seats(self):
        counter = 0
        max_row = self.get_max_rows()
        while counter < 3 and Plane.filled < Plane.passengers:
            row_num=0
            while row_num < max_row :
                for comp in self.seats:
                    if row_num < len(comp.space) and counter ==0:
                        comp.fill_aisle_seats(row_num)
                    if row_num < len(comp.space) and counter ==1:
                        comp.fill_window_seats(row_num)
                    if row_num < len(comp.space)and counter ==2:
                        comp.fill_middle_seats(row_num)
                row_num+=1
            counter +=1

    def get_max_rows(self):
        max_row = 0
        for comp in self.seats:
            if len(comp.space) > max_row:
                max_row = len(comp.space)
        return max_row
        
class Seat(Plane):
    def __init__(self):
        self.space = []
    
    def fill_seat(self,passenger):
        if len(self.space) == 1:
            pass
        else:
            self.space.append(passenger)
            Plane.filled +=1

    def __repr__(self):
        return f"{self.space}"

class Comp(Plane):
    def __init__(self,layout):
        self.layout = layout
        self.space = []

    def create_seats(self):
        for i in range(self.layout[1]):
            row = []
            for i in range(self.layout[0]):
                s = Seat()
                row.append(s)
            self.space.append(row)

    def __repr__(self):
        return f"{self.space}"

    def fill_middle_seats(self,row_num):
        middle_seats = self.space[row_num][1:-1]
        for seat in middle_seats:
            if Plane.filled < Plane.passengers:
                seat.fill_seat(Plane.filled)

class leftComp(Comp):
    def fill_aisle_seats(self,row_num):
        self.space[row_num][-1].fill_seat(Plane.filled)

    def fill_window_seats(self,row_num):
        self.space[row_num][0].fill_seat(Plane.filled)
         
class rightComp(Comp):
    def fill_aisle_seats(self,row_num):
        self.space[row_num][0].fill_seat(Plane.filled)

    def fill_window_seats(self,row_num):
        self.space[row_num][-1].fill_seat(Plane.filled)
        
class middleComp(Comp):
    def fill_aisle_seats(self,row_num):
        self.space[row_num][0].fill_seat(Plane.filled)                     
        self.space[row_num][-1].fill_seat(Plane.filled)

    def fill_window_seats(self,row_num):
        pass

@app.route('/')
def home():
    return render_template('index.html')

# Create a Plane
@app.route('/seats',methods=['POST','GET'])
def create_plane():
    if request.method == "POST":
        seatsGrid = ast.literal_eval(request.form['seatsGrid'])
        passengers = ast.literal_eval(request.form['Passengers'])
        

        new_plane = Plane(seatsGrid, passengers)
        new_plane.create_seats()
        new_plane.allocate_seats()

        # json_seats = json.dumps(new_plane.seats)
        return render_template('result.html', seats = new_plane.seats)

if __name__ == '__main__':
    app.run(debug=True)
