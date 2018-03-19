
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
        pltSize = pltSize = 1.1 * pltCircle
        pltLimit = pltCircle 

        pltStellarMagnitudeLimit = 4.8

        self.pltConstellationLines = 1
        self.pltNebula = 0
        self.pltConstellationBoundaries = 0
        self.pltConstellationLabels = 1
        self.pltEclipticLine = 1
        self.pltDecLines = 1
        self.pltRALines = 1
        self.pltDateCircle = 1
  

        # plot the Rete
        self.g = sg(-pltSize, pltSize, -pltSize, pltSize, pltLimit)
        self.g.setStarListIndex(pltStellarMagnitudeLimit)

        decMax = -23.5
        lat = 40 
        decMax = -90 + lat 
        rMax = pltLimit
        ptype = 2  # plot type
        self.plotRete(ptype, decMax, rMax)
        self.g.endPlot("rete")



        #plot the Plate
        self.g = sg(-pltSize, pltSize, -pltSize, pltSize, pltLimit)
        hrotate = 18.
        #self.g.drawBoundingCircle( "red")
        self.plotHorizon(hrotate)
        self.g.plate()
        self.g.endPlot("plate")
        
        

    def plotRete(self, ptype, decMax, rMax):

        self.p.setProjection(ptype, 0, 90, decMax, rMax )
        pStars = self.p.projectStars( self.s.stars, 5, 6)
        self.g.plotStars(pStars)
        #self.g.plotStarLabels(pStars, 2)
        #self.g.plotStarLabels(pStars, 1)

        aStars = self.p.projectStars( self.s.astars, 5, 6)
        self.g.plotAstrolabeStarLabels(aStars, 10)
        pConstellationBoundaries= self.p.projectConstellationBoundaries( self.s.constellationBoundaries)

        if self.pltConstellationLines:
            pConstellationLines = self.p.projectConstellationLines( self.s.constellationLines)
            self.g.plotConstellationLines(pConstellationLines)
        
        if self.pltNebula:
            pNebula = self.p.projectNebula( self.s.nebula)
            self.g.plotNebula(pNebula, 5)
        
        if self.pltConstellationBoundaries:
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


    def plotHorizon(self, hrotate):

        npts = 60
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



