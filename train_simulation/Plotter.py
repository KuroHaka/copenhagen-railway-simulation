import matplotlib.pyplot as plt
import numpy as np


class Plotter:								
        _x = 1
        _y = 1
        _y2 = 1
        _xname='x-axis'
        _yname='y-axis'
        _title='title'

        def __init__(self,x,y,y2,title,xlabel,ylabel):
                self._x = x
                self._y = y
                self._y2 = y2
                self._title = title
                self._xname = xlabel
                self._yname = ylabel
                plt.title(self._title)
                plt.xlabel(self._xname)
                plt.ylabel(self._yname)
                plt.plot(self._x,self._y, color="red")
                plt.plot(self._x, self._y2 ,color="blue")
                plt.show()
        


        
#test
d=1.5
x=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
trains=[3.1/d,3.2/d,3.1/d,3.3/d,3.1/d,2.1/d,2.2/d,2.2/d,2.1/d,2.5/d,2.7/d,2.6/d,2.5/d,2.3/d,2/d,2.1/d,2.2/d,2.5/d,2.6/d,2.5/d,3/d,3.1/d,3.2/d,3.1/d]
carriers=[1.4/d,1.3/d,1.4/d,1.3/d,1.5/d,2.2/d,2.5/d,3/d,2.5/d,2.2/d,2.1/d,2.3/d,2.4/d,2.2/d,2.8/d,3/d,2.7/d,2.6/d,2.1/d,1.6/d,1.4/d,1.5/d,1.4/d,1.3/d]


p1 = Plotter(x,trains,carriers,'Commuting time per hour','hour of the day' ,'red: commuting time with train \n blue: commuting time with carriers')
p1.showplot