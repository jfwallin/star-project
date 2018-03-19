
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
        self.decScale = ytmp / xtmp * rMax 

        self.raDelta = 0  # this is used to offset the location so zero is in the right quadrant
        self.raDirection = -1  # direction of the RA projection angle
        self.raRotation = 12  # hours of rotation

        if projection == 1:  # standard projection for an astrolabe
          self.projectToPolar = self.projectToStereo
          self.raDirection = 1  # direction of the RA projection angle
          self.polarToRADec = self.stereoToRADec
    
        elif projection == 2:  # standard projection for a starwheel
          self.projectToPolar= self.projectToSimplePolar
          self.polarToRaDec = self.simplePolarToRADec

        elif projection == 3:   # TBA - standard projection all sky map
          self.projectToPolar = self.projectToStarMap
          self.polarToRADec = self.starMapToRADec

        elif projection == 4:    # standard projection for southern starwheel
          self.raDirection = 1  # direction of the RA projection angle
          self.raRotation = 12  # hours of rotation
          self.projectToPolar= self.projectToSimplePolarSouthern
          self.polarToRaDec = self.simplePolarToRADecSouthern

        else:
          print "no project - error - exiting"
          exit()

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

############

    def projectToSimplePolarSouthern(self, r, d):

        # convert the position in to radians associated with a polar plot
        ra = (r + self.raRotation) / 24 * 360. * math.pi / 180.
        dec = (90 - d) * math.pi / 180.
        
        # ra and dec are in radians
        rtmp = -(90.+d)/(90-self.decMax)

        ra_corrected = self.raDirection * ra + self.raDelta
        x = rtmp * math.cos(ra_corrected)
        y = rtmp * math.sin(ra_corrected)
        return x, y

    def simplePolarToRADecSouthern(self, x, y):
        r = math.sqrt(x*x + y*y)
        #r = r / self.decScale

        ra_corrected  = math.atan2(y, x)

        ra = (ra_corrected - self.raDelta)/self.raDirection  # ra in radians
        ra = ra * 180.0 / math.pi
        ra = ra - (self.raRotation*15) 
        ra = ra % (360.)
        ra = ra / 15.

        dec = -90 +  r * (90-self.decMax)

        return ra, dec


##########

    def setTime(self, LST, lat):
      # lst in hours - converted into radians
      self.lst = LST * 15 * math.pi / 180.
      self.lat = lat * math.pi / 180.
      

      self.sLat = math.sin(self.lat)
      self.cLat = math.cos(self.lat)

      self.azDelta = math.pi /2.0
      self.azDirection = 1
        
    def projectToStarMap(self, r, d):
    #def projectToPolarStereoGraphic(self, r, d):
        
        ra = r * 15 * math.pi/ 180.
        dec = d * math.pi / 180.
        ha = (self.lst - ra) % (2.0 * math.pi)


        sDec = math.sin(dec)
        cDec = math.cos(dec)

        sAlt = sDec * self.sLat + cDec * self.cLat * math.cos(ha)
        Alt = math.asin(sAlt)
        cAlt = math.cos(Alt)

        cAz = (sDec - sAlt*self.sLat) / (cAlt * self.cLat)
        cAz = max(min(cAz, 1.0),-1.0)  # fix round off issues
        Az = math.acos(cAz)
        sHa = math.sin(ha)

        if sHa >= 0:
          Az = 2.0* math.pi - Az

        # go to the horizion = math.pi/2.0
        rtmp = (0.5*math.pi - Alt) / (0.5 * math.pi)
        az_corrected = self.azDirection * Az + self.azDelta

        x = rtmp * math.cos(az_corrected)
        y = rtmp * math.sin(az_corrected)

        return x, y




#sin(ALT) = sin(DEC)*sin(LAT)+cos(DEC)*cos(LAT)*cos(HA)
#ALT = asin(ALT) 
#
#                sin(DEC) - sin(ALT)*sin(LAT)
# cos(A)   =   ---------------------------------
#                    cos(ALT)*cos(LAT)
#
# A = acos(A)
#
#If sin(HA) is negative, then AZ = A, otherwise
#AZ = 360 - A


    def starMapToRADec(self, x, y):
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


    p1 = project()
    p1.setProjection(projection=3, raZero=0, decZero=90, decMax = -23.5, rMax=1)
    lst = 12.
    lat = 36.
    p1.setTime(lst, lat)

    for dec in range(0, 90, 10):
      x,y, = p1.projectToPolar(12., dec)
      print dec, x, y

    for ra in range(6,19):
      x,y, = p1.projectToPolar(float(ra), 0)
      print ra, x, y


