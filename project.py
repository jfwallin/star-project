
import time
import math
import ephem
import numpy as np
import copy

class project:

    def __init__(self):   #, projection=1, raZero=0, decZero=90):
        polarStereoGraphic = 1
        raZero = 0
        decZero = 90
        decMax = -23.5
        projection = 1
        rMax = 1.
        self.setProjection(projection, raZero, decZero, decMax, rMax)
        


    def setProjection(self, projection=1, raZero=0, decZero=90, decMax = -23.5, rMax=1):
        self.raZero = raZero
        self.decZero = decZero
        self.projection = projection
        self.decMax = decMax
        d = (90 - decMax) * math.pi / 180.
        xtmp = math.sin(d)
        ytmp = math.cos(d) + 1
        #self.decScale = xtmp / ytmp * rMax 
        self.decScale = ytmp / xtmp * rMax 

        self.raDelta = 0  # this is used to offset the location so zero is in the right quadrant
        self.raDirection = -1  # direction of the RA projection angle
        self.raRotation = 12  # hours of rotation

        self.projectToPolar = self.projectToStereo
        self.polarToRADec = self.stereoToRADec

        self.projectToPolar = self.projectToSimplePolar
        self.polarToRADec = self.simplePolarToRADec

    def projectToStereo(self, r, d):
    #def projectToPolarStereoGraphic(self, r, d):

        # convert the position in to radians associated with a polar plot
        r = (r + self.raRotation) / 24 * 360. * math.pi / 180.
        d = (90 - d) * math.pi / 180.
        
        # ra and dec are in radians
        # the idea of this project is to project through a point one unit 
        # above the current y location - hence the cos(d) + 1 below
        xtmp = math.sin(d)
        ytmp = math.cos(d) + 1
        rtmp = xtmp / ytmp
        rtmp = rtmp * self.decScale

        ra_corrected = self.raDirection * r + self.raDelta
        x = rtmp * math.cos(ra_corrected)
        y = rtmp * math.sin(ra_corrected)
        return x, y

    def stereoToRADec(self, x, y):
        r = math.sqrt(x*x + y*y)
        r = r / self.decScale

        ra_corrected  = math.atan2(y, x)

        ra = (ra_corrected - self.raDelta)/self.raDirection  # ra in radians
        ra = ra * 180.0 / math.pi
        ra = ra - (self.raRotation*15) 
        ra = ra % (360.)
        ra = ra / 15.

        r2 = r * r
        xx = -(1.0 - r2) / (1 + r2)
        ddd = math.acos(xx) * 180./math.pi
        dec = ddd - 90.
        return ra, dec

############

    def projectToSimplePolar(self, r, d):

        # convert the position in to radians associated with a polar plot
        ra = (r + self.raRotation) / 24 * 360. * math.pi / 180.
        dec = (90 - d) * math.pi / 180.
        
        # ra and dec are in radians
        rtmp = (90.-d)/(90-self.decMax)
        #print d, rtmp, self.decScale
        #rtmp = rtmp * self.decScale

        ra_corrected = self.raDirection * ra + self.raDelta
        x = rtmp * math.cos(ra_corrected)
        y = rtmp * math.sin(ra_corrected)
        return x, y

    def simplePolarToRADec(self, x, y):
        r = math.sqrt(x*x + y*y)
        #r = r / self.decScale

        ra_corrected  = math.atan2(y, x)

        ra = (ra_corrected - self.raDelta)/self.raDirection  # ra in radians
        ra = ra * 180.0 / math.pi
        ra = ra - (self.raRotation*15) 
        ra = ra % (360.)
        ra = ra / 15.

        dec =90 -  r * (90-self.decMax)

        return ra, dec

##########




    def projectStars(self, starList, xIndex, yIndex):
        pStarList = copy.deepcopy(starList)
        for i in range(len(pStarList)):
            s = pStarList[i]
            r = s[xIndex]
            d = s[yIndex]
            x, y = self.projectToPolar( r, d)

            pStarList[i][xIndex] = x
            pStarList[i][yIndex] = y

        return pStarList

    
    def projectConstellationLines(self, constellationLines):
        pConstellationLines = copy.deepcopy(constellationLines)
        for j in range(len(constellationLines)):
            c = pConstellationLines[j]
            for i in range(len(c) ):
                r = c[i][0]
                d = c[i][1]
                x, y = self.projectToPolar( r, d)
                pConstellationLines[j][i][0] = x
                pConstellationLines[j][i][1] = y

        return pConstellationLines
            

    def projectConstellationBoundaries(self, constellationBoundaries):
        pConstellationBoundaries = copy.deepcopy(constellationBoundaries)
        for  j in range(len(constellationBoundaries)):  #constellationBoundaries:
            c = pConstellationBoundaries[j]
            label = c[0]
            lines = c[1]
            for i in range(len(lines)):
                l = lines[i]
                r = float(l[0]) 
                d = float(l[1])
                x, y = self.projectToPolar( r, d)
                pConstellationBoundaries[j][1][i][0] = str(x)
                pConstellationBoundaries[j][1][i][1] = str(y)

        return pConstellationBoundaries



    def projectNebula(self, nebula):
        pNebula = copy.deepcopy(nebula)
        for j in range(len(pNebula)):
            c = pNebula[j]
            r = float(c[4])
            d = float(c[5])
            x, y = self.projectToPolar( r, d)
                
            pNebula[j][4] = x
            pNebula[j][5] = y

        return pNebula

    def projectSimpleLine(self, simpleLine):
        pSimpleLine = copy.deepcopy(simpleLine)
        for j in range(len(pSimpleLine)):
            c = pSimpleLine[j]
            r = c[0]
            d = c[1]
            x, y = self.projectToPolar( r, d)
            pSimpleLine[j][0] = x
            pSimpleLine[j][1] = y
            
        return pSimpleLine
 

    def createDecLine(self, dec):
        
        npts = 300
        dLine = []
        for i in range(npts):
            r = 24.0  * float(i) / float(npts-1) 
            d = dec
            x, y = self.projectToPolar( r, d)
            dLine.append( [x,y])

        return dLine


if __name__ == "__main__":
    p = project()
    r = 17.5
    d = -23.77
    d = 78 

    for r in range(1,23):
      d = -23.5
      print "origional = ", r, d
      #print r*15.0, r*15.*math.pi/180.
      x, y = p.projectToPolar(float(r), d)
      print "xy = ", x,y, math.sqrt(x*x+y*y)
      ra, dec =    p.polarToRADec(x, y) 
      print "final = ",ra, dec
      print "----"
