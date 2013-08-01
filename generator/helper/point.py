# The MIT License (MIT)
#
# Copyright (c) 2011, 2013 OpenWorm.
# http://openworm.org
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the MIT License
# which accompanies this distribution, and is available at
# http://opensource.org/licenses/MIT
#
# Contributors:
#      OpenWorm - http://openworm.org/people.html
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import with_statement
'''
Created on Jul 29, 2013

@author: serg
'''
import math
from generator.Const import Const
class Vector3D(object):
    def __init__(self,x,y,z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    def  __sub__(self, p1):
        return Point(self.x - p1.x, self.y - p1.y, self.z - p1.z)
    def __add__(self, p1):
        x = self.x + p1.x
        y = self.y + p1.y
        z = self.z + p1.z
        return Vector3D(x,y,z)
    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    def __mul__(self, scalar):
#         self.x *= scalar
#         self.y *= scalar
#         self.z *= scalar
        return Vector3D(self.x * scalar, self.y  *scalar, self.z * scalar)
    @staticmethod 
    def cross_prod(a,b):
        '''
        As I understood we're using left side system of coordinates
        '''
        return Vector3D(a.z * b.y - a.z * b.z, a.x * b.z - a.z * b.x, a.y * b.x - a.x * b.y)
    def normalize(self):
        l = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        self.x /= l
        self.y /= l
        self.z /= l 
    
class Point(Vector3D):
    '''
    classdocs
    '''
    def __init__(self, x, y, z,index=-1, planes=None):
        '''
        Constructor
        '''
        Vector3D.__init__(self,x,y,z)
        self.index = int(index)
        if planes != None:
            self.faces = self.find_planes(planes)
    def getX(self):
        return self.x * Const.TRANF_CONST * Const.r0   
    def getY(self):
        return self.y * Const.TRANF_CONST * Const.r0   
    def getZ(self):
        return self.z * Const.TRANF_CONST * Const.r0   
    def find_planes(self, plains):
        self.faces_l = filter(lambda p: self.index in p.vertices, plains)
    def get_normal(self):
        self.n = self.faces_l[0].getNormal()
        if len(self.faces_l) > 1:
            for i in range(1,len(self.faces_l),1):
                self.n = self.n + self.faces_l[i].getNormal()
        self.n.normalize()
        return self.n
    @staticmethod
    def find_common_plane(p1,p2):
        common_faces = []
        for p in p1.faces_l:
            if p in p2.faces_l:
                common_faces.append(p)
        return common_faces
        
    