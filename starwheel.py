
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
        self.pltConstellationBoundaries = 1
        self.pltConstellationLabels = 1
        self.pltEclipticLine = 1
        self.pltDecLines = 0
        self.pltRALines = 0
        self.pltDateCircle = 1

        # plot the Rete
        self.g = sg(-pltSize, pltSize, -pltSize, pltSize, pltLimit)
        self.g.setStarListIndex(pltStellarMagnitudeLimit)

        decMax = -23.5
        lat = 30 
        decMax = -90 + lat 
        rMax = pltLimit
        self.plotRete(decMax, rMax)
        self.g.endPlot("rete")



        #plot the Plate
        self.g = sg(-pltSize, pltSize, -pltSize, pltSize, pltLimit)
        hrotate = 18.
        #self.g.drawBoundingCircle( "red")
        self.plotHorizon(hrotate)
        self.g.plate()
        self.g.endPlot("plate")
        
        

    def plotRete(self, decMax, rMax):

        self.p.setProjection(1, 0, 90, decMax, rMax )
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
            self.g.plotConstellationLabels2(pConstellationBoundaries)
            #self.g.plotConstellationLabels(pConstellationBoundaries)
        
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


 


if __name__ == "__main__":

    A = astrolabe()


#    decLine = p.createDecLine(0)
#    g.plotSimpleLine(decLine)

#    decLine = p.createDecLine(45)
#    g.plotSimpleLine(decLine)



