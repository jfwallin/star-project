

import numpy as np
from starGraphics import starGraphics as sg
from project import project as project
from astronomy import astronomy as astronomy
from starData import starData as starData

class astrolabe:

    def __init__(self):
        self.s = starData()
        self.p = project()
        self.a = astronomy()
       
        pltCircle = 1.0 

        self.pltSize = 1.1 * pltCircle
        self.pltLimit = pltCircle 
        self.pltStellarMagnitudeLimit = 4.8

        self.pltConstellationLines = 1
        self.pltNebula = 0
        self.pltConstellationBoundaries = 0
        self.pltConstellationLabels = 1
        self.pltEclipticLine = 1
        self.pltDecLines = 0
        self.pltRALines = 0
        self.pltDateCircle = 1
  
        self.starWheelRete = 1
        self.starWheelPlate = 2
        self.skymap = 3
        self.astrolabeReteStars = 4
        self.astrolabePlate = 5
        self.southernStarWheelRete = 6
        self.southernStarWheelPlate = 7
        lat = 53 
        lon = 0
        #self.a.setLatLong(lat, lon)
 
        xx = self.starWheelPlate
        xx = self.starWheelPlate


        xx = self.starWheelRete
        self.createPlot(xx, lat)

        xx = self.starWheelPlate
        self.createPlot(xx, lat)

        xx = self.southernStarWheelRete
#        self.createPlot(xx, lat)

        xx = self.southernStarWheelPlate
        self.createPlot(xx, lat)



    def createPlot(self, plotType, lat):

      self.g = sg(-self.pltSize, self.pltSize, -self.pltSize, self.pltSize, self.pltLimit)
      self.g.setStarListIndex(self.pltStellarMagnitudeLimit)
      rMax = self.pltLimit
      hrotate = 18.

      if lat > 33:
        decMax = -90 + lat 
      else:
        decMax = -23.5


      # plot the Rete
      if plotType == self.starWheelRete:
        ptype = 2  # plot type
        self.p.setProjection(ptype, 0, 90, decMax, rMax )
        self.plotRete(ptype, decMax, rMax)
        #self.plotHorizon(hrotate)
        self.g.endPlot("rete")

      #plot the Plate
      elif plotType == self.starWheelPlate:
        hrotate = 18.
        #self.g.drawBoundingCircle( "red")
        ptype = 2
        self.p.setProjection(ptype, 0, 90, decMax, rMax )
        #self.plotHorizon(hrotate)
        self.g.plate(ptype,lat,decMax, rMax)
        self.g.endPlot("plate")
        
        # plot the skymap
      elif plotType == self.skymap:
        ptype = 3
        self.p.setProjection(ptype, 0, 90, decMax, rMax )
        self.plotStarMap(lat)
        self.g.endPlot("skymap")
      
      elif plotType == self.astrolabeReteStars:
        ptype = 1  # plot type
        self.p.setProjection(ptype, 0, 90, decMax, rMax )
        self.plotRete(ptype, decMax, rMax)
        self.g.endPlot("rete")
        
      elif plotType == self.southernStarWheelRete:
        ptype = 4  # plot type
        self.p.setProjection(ptype, 0, 90, decMax, rMax )
        self.plotRete(ptype, decMax, rMax)
        self.g.endPlot("south-rete")
 
       #plot the Plate
      elif plotType == self.southernStarWheelPlate:
        hrotate = 18
        #self.g.drawBoundingCircle( "red")
        ptype = 4
        self.p.setProjection(ptype, 0, 90, decMax, rMax )
        #self.plotHorizon(hrotate)
        #self.g.plate(ptype,lat,decMax, rMax)
        self.plotRete(ptype, decMax, rMax)
        #self.g.plate(ptype, lat, decMax, rMax)
        self.g.endPlot("south-plate")

      else:
        print "no such plot type"
        exit()


        




        

    def plotStarMap(self, lat):

        lst = 9.
        self.p.setTime(lst, lat)
        pStars = self.p.projectStars( self.s.stars, 5, 6)
        self.g.plotStars(pStars)
        #self.g.plotStarLabels(pStars, 2)
        #self.g.plotStarLabels(pStars, 1)

        aStars = self.p.projectStars( self.s.astars, 5, 6)
        self.g.plotAstrolabeStarLabels(aStars, 10)
        

        if self.pltConstellationLines:
            pConstellationLines = self.p.projectConstellationLines( self.s.constellationLines)
            self.g.plotConstellationLines(pConstellationLines)
        
        if self.pltNebula:
            pNebula = self.p.projectNebula( self.s.nebula)
            self.g.plotNebula(pNebula, 5)
        
        if self.pltConstellationBoundaries:
            pConstellationBoundaries= self.p.projectConstellationBoundaries( self.s.constellationBoundaries)
            self.g.plotConstellationBoundaries(pConstellationBoundaries)

        if self.pltConstellationLabels:
            self.plotConstellationLabels()  
        
        if self.pltEclipticLine:
            eclipLine = self.a.createEclipticPath()
            pEclipLine = self.p.projectSimpleLine(eclipLine)
            self.g.plotSimpleLine(pEclipLine)

        self.pltDecLines = 1
        if self.pltDecLines:
            decList = [90, 80, 70, 60, 50, 40, 30, 20, 10, 0, -10, -20]
            decList = [80, 70, 60, 50, 40, 30, 20, 10, 0, -10, -20]
            decList = [80, 60, 40, 20]
            self.plotDecEllipses(decList)

        self.pltRALines = 1
        if self.pltRALines:
            #raHours = [0]
            decMax = -90 + lat 
            raHours = range(0,24)
            self.plotRaCurves( raHours, decMax)
        
        #if self.pltDateCircle:
        #    self.g.dateCircle()


 

    def plotRete(self, ptype, decMax, rMax):

        pStars = self.p.projectStars( self.s.stars, 5, 6)
        self.g.plotStars(pStars)
        #self.g.plotStarLabels(pStars, 2)
        #self.g.plotStarLabels(pStars, 1)

        aStars = self.p.projectStars( self.s.astars, 5, 6)
        self.g.plotAstrolabeStarLabels(aStars, 10)

        if self.pltConstellationLines:
            pConstellationLines = self.p.projectConstellationLines( self.s.constellationLines)
            self.g.plotConstellationLines(pConstellationLines)
        
        if self.pltNebula:
            pNebula = self.p.projectNebula( self.s.nebula)
            self.g.plotNebula(pNebula, 5)
        
        if self.pltConstellationBoundaries:
            pConstellationBoundaries= self.p.projectConstellationBoundaries( self.s.constellationBoundaries)
            self.g.plotConstellationBoundaries(pConstellationBoundaries)

        if self.pltConstellationLabels:
            self.plotConstellationLabels()  
  
        if self.pltEclipticLine:
            eclipLine = self.a.createEclipticPath()
            pEclipLine = self.p.projectSimpleLine(eclipLine)
            self.g.plotSimpleLine(pEclipLine)

        if self.pltDecLines:
            decList = [90, 80, 70, 60, 50, 40, 30, 20, 10, 0, -10, -20]
            self.g.plotDecCircles(decList)

        if self.pltRALines:
            #raHours = [0]
            raHours = range(0,24)
            self.g.plotRaLines( raHours, decMax)
        
        if self.pltDateCircle:
            self.g.dateCircle()



    def plotDecEllipses(self, decList):
      for dec in decList:
        sline = []
        for ra in np.arange(0,24, 0.5):
          x, y = self.p.projectToPolar(ra, float(dec))
          sline.append([x,y])
        self.g.plotSimpleLine(sline)

    def plotRaCurves(self, raList, decMax):
      for ra in raList:
        sline = []
        for dec in np.arange(90,decMax, -5):
          x, y = self.p.projectToPolar(ra, float(dec))
          sline.append([x,y])
        self.g.plotSimpleLine(sline)




    def plotHorizon(self, hrotate):

        npts = 70
        altLine = self.a.createAltPath( 0.0, npts, hrotate)
        pAltLine = self.p.projectSimpleLine(altLine)
        self.g.plotSimpleLine(pAltLine)


    def plotConstellationLabels(self): 

        cLabelList = []
        fn = "constellation_list.txt"
        ff = open(fn,"r")
        clist = ff.readlines()
        ff.close()
        for cc in clist:
          c = cc.split(", ")
          sname = c[0]
          label = c[1]
          lra = float(c[2])
          ldec = float(c[3])
          xcenter, ycenter = self.p.projectToPolar(lra, ldec) 
          theta = np.arctan2(ycenter,xcenter)*180./np.pi + 90.

          cLabelList.append([xcenter, ycenter, theta, label.upper()])
  
        self.g.plotConstellationLabels(cLabelList)



if __name__ == "__main__":

    A = astrolabe()


#    decLine = p.createDecLine(0)
#    g.plotSimpleLine(decLine)

#    decLine = p.createDecLine(45)
#    g.plotSimpleLine(decLine)



