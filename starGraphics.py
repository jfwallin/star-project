import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from project import project as project
from astronomy import astronomy as astronomy
import ephem

import descartes
from shapely.geometry import Polygon 




class starGraphics:

    def __init__(self, xmin, xmax, ymin, ymax, rmax):

        figureSize = 10.
        aspectratio = 0
        margin = 0.1
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.Rmax = rmax

        self.p = project()
        self.a = astronomy()

        self.mapColor = "white"
        self.mapCircleColor = "black"
        self.decCircleColor = "black"
        self.raCircleColor = "black"
        self.plateCircleColor = "black"
        self.horizonLineColor = "black"
        self.starColor = "black"
        self.constellationLineColor = "black"
        self.constellationBoundaryColor = "red"


        fig = plt.figure( figsize=(figureSize, figureSize))
        fig.patch.set_facecolor(self.mapColor)
        self.ax = fig.add_subplot(111)  #,aspect='equal')

        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        #ax.set_frame_on(False)
        #self.ax.set_frame_on(True)
        self.ax.set_frame_on(False)

        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.tight_layout()

#        circle1 = plt.Circle( (0,0), self.Rmax, color=self.mapCircleColor, fill=False)
#        self.ax.add_artist(circle1)


        dr = 0.05
        rr = self.Rmax + dr 
        #circle1 = plt.Circle( (0,0), rr, color=self.mapCircleColor, fill=False)
        #self.ax.add_artist(circle1)
          
        circle1 = plt.Circle( (0,0), rr-dr, color=self.mapCircleColor, fill=False)
        self.ax.add_artist(circle1)

        circle1 = plt.Circle( (0,0), rr+dr, color=self.mapCircleColor, fill=False)
        self.ax.add_artist(circle1)




    def endPlot(self,fname="None"):
        #self.drawBoundingCircle("black")
        if fname <> "None":
          pdfName = fname+  ".pdf"
          svgName = fname + ".svg"
          plt.savefig(pdfName, dpi=300)
          plt.savefig(svgName, dpi=300)
        
        plt.show()

    def setStarListIndex(self, limitingMag):
        self.xIndex = 5  # index for the RA in the Bright Star Catalog
        self.yIndex = 6  # index of the Dec in the Bright Star Catalog
        self.sizeIndex = 7  # index of the stellar Magnitude in the Bright Star Catalog
        self.limitingMag = limitingMag

        #          -1  0   1   2   3   4   5   6
#        self.maglist = [120, 90, 60, 30,  10,  1, 0]
#        self.maglist = [240, 120, 90, 60, 30,  10,  1, 0]
#        self.maglist = [70, 50, 35, 22,  10,  1, 0]
        self.maglist = [30, 22, 15, 10, 6,  1, 0]


    def drawBoundingCircle(self, colorname):
        print "DUCK"
        circle1 = plt.Circle( (0,0), self.Rmax, linewidth=5, color=colorname, fill=False)
        self.ax.add_artist(circle1)


    def inPlotBounds(self, x, y):
        r = x*x + y*y
        if r > self.Rmax * self.Rmax :
            return False
        else:
            return True


    def plotStars(self, starList):
        xx = []
        yy = []
        ss = []
        for s in starList:
            x = s[self.xIndex]
            y = s[self.yIndex]
            mag = s[self.sizeIndex]
            size = (int(mag) + 1)
            if size < 0:
                size = 0
            if size > 6:
                size = 6

            if mag < self.limitingMag and self.inPlotBounds(x,y):
                xx.append(x)
                yy.append(y)
                ss.append(self.maglist[size])
        self.starColor = "blue"
        plt.scatter(xx,yy,s=ss,color=self.starColor)

    def plotSimpleLine(self, sline):
        xx = []
        yy = []
        for pt in sline:
            x = pt[0]
            y = pt[1]
            if self.inPlotBounds(x,y):
                xx.append(x)
                yy.append(y)
            else:
                plt.plot(xx, yy, '-',color=self.horizonLineColor, markersize=-100,marker="", linewidth=1)
                xx = []
                yy = []
            plt.plot(xx, yy, '-',color=self.horizonLineColor,markersize=-100,marker="", linewidth=1)


    def plotConstellationLines(self, constellationLines):
        
        for c in constellationLines:
            xx = []
            yy = []
            for i in range(len(c) ):
                x = float(c[i][0])
                y = float(c[i][1])
                if self.inPlotBounds(x,y):
                    xx.append(x)
                    yy.append(y)
                else:
                    plt.plot(xx, yy, '-',color=self.constellationLineColor,markersize=-100,marker="", linewidth=0.5)
                    xx = []
                    yy = []

            plt.plot(xx, yy, '-',color=self.constellationLineColor,markersize=-100,marker="", linewidth=0.5)



    def plotConstellationBoundaries(self, constellationBoundaries):
        
        for c in constellationBoundaries:  #constellationBoundaries:
            label = c[0]
            if label <> "":
              label = c[0]
              lines = c[1]
              xx = []
              yy = []
              for l in lines:
                  x = float(l[0])
                  y = float(l[1])
                  if self.inPlotBounds(x,y):                                        
                      xx.append(x)
                      yy.append(y)
                  else:
                      plt.plot(xx, yy, '-', color=self.constellationBoundaryColor, markersize=-100,marker="", linewidth=0.5)
                      xx = []
                      yy = []
              plt.plot(xx, yy, '-', color=self.constellationBoundaryColor, markersize=-100,marker="", linewidth=0.5)


    def plotNebula(self, nebula, limitingMag):
        
        xx = []
        yy = []
        a = []
        b = []
        ang = []
        labels = []
        mags = []
        for c in nebula:
            label = c[1]
            mnumber = c[2]
            ra = float(c[4])
            dec = float( c[5])
            mag = float(c[6])
            major = float(c[7])
            minor = float(c[8])
            angle = c[9]
            major = 0.02
            minor = 0.01

            if mag < limitingMag:
#                print mag, ra, dec
                xx.append(ra)
                yy.append(dec)
                a.append(major)
                b.append(minor)
                ang.append(angle)
                mags.append(mag)
                if mnumber != "0":
                    labels.append("M "+mnumber)
                else:
                    labels.append(c[0])
                

        for i in range(len(xx)):
            x1 = xx[i]
            y1 = yy[i]
            ll = labels[i]            
            w = a[i]
            h = b[i]
            aa = ang[i]
            m = mags[i]

            if self.inPlotBounds(x1,y1):
                plt.text(x1, y1, ll, horizontalalignment="center", verticalalignment="center", fontsize=14)
                ee = patches.Ellipse(xy=[x1, y1], width=w, height=h, angle=aa)
            #plt.gca().add_artist(ee)
#        plt.plot(xx, yy, 'g-',markersize=-100,marker="", linewidth=2)

                
    def plotStarLabels(self, starList, limitingMag):

        xx = []
        yy = []
        ss = []
        for s in starList:
            x1 = s[self.xIndex]
            y1 = s[self.yIndex]
            mag = s[self.sizeIndex]

            dx = 0.01
            if mag < limitingMag:
                if self.inPlotBounds(x1,y1):
                    plt.text(x1-dx, y1+dx, s[0], horizontalalignment="center", verticalalignment="center", fontsize=18)
   

    def plotAstrolabeStarLabels(self, starList, limitingMag):

        xx = []
        yy = []
        ss = []
        for s in starList:
            #print "XXXXXXXX", s
            x1 = s[self.xIndex]
            y1 = s[self.yIndex]
            mag = s[self.sizeIndex]
            starLabel = s[10]
            theta = np.arctan2(y1,x1)*180./np.pi + 90.
            halign = s[-1]
            #print starLabel
            ra = s[5]
            dec = s[6]
            

            tnew = (theta - 45.0)*np.pi/180.
            dx = 0.013
            dy = 0.013
            dx = 0
            dy = 0.0
            x1 = x1 + dx*np.cos(tnew) - dy*np.sin(tnew)
            y1 = y1 + dx*np.sin(tnew) + dy*np.cos(tnew)
            fsize = 4
            halign= "left"
            #if mag < limitingMag:
            valign = u'center'
            if 1 == 1:
                if self.inPlotBounds(x1,y1):
                    plt.text(x1+dx, y1+dx, starLabel, rotation=theta, horizontalalignment=halign, verticalalignment=valign, fontsize=fsize)
   


    def plotConstellationLabels(self, constellationBoundaries):

        fo = "planisphere_constellations.txt"
        ff2 = open(fo, "w")
        fn = "constellatlion_list.txt"
        ff = open(fn,"r")
        clist = ff.readlines()
        ff.close()
        for ic in range(len(constellationBoundaries)):
            
            c = constellationBoundaries[ic]
            label = c[0]
            lines = c[1]
            xcenter = 0
            ycenter = 0
            label1 = clist[ic-1].strip()
            label = label1.upper()
            label_out = label
            if label.find(" ") > -1:
              ll = label.split(" ")
              label = ll[0] + "\n " + ll[1]
            for l in lines:
                x = float(l[0])
                y = float(l[1])
                xcenter = xcenter + x
                ycenter = ycenter + y
            if len(lines) > 0:
                xcenter = xcenter / float(len(lines))
                ycenter = ycenter / float(len(lines))                
                theta = np.arctan2(ycenter,xcenter)*180./np.pi + 90.
                # figure out the RA and Dec based on the xcenter and ycenter 

                if self.inPlotBounds(xcenter, ycenter):
                    label = label.upper()
                    plt.text(xcenter, ycenter, label, rotation=theta, horizontalalignment="center", verticalalignment="center", fontsize=6)
                    
                    lra, ldec = self.p.polarToRADec(xcenter, ycenter)
                    #print "label ra,dec = ", lra, ldec
                    lra = int(lra * 100)/100.
                    ldec = int(ldec * 100) / 100.
                    theta = int(theta*10)/10.
                    sss = label_out + ", " + str(lra) + ", " + str(ldec) + ", " + str(theta) + "\n"
                    ff2.write(sss)
        ff2.close()

    def plotConstellationLabels2(self, constellationBoundaries):
        fo = "planisphere_constellations.txt"
        ff = open(fo, "r")
        clist = ff.readlines()
        ff.close()
        for ic in range(len(clist)):
            c = clist[ic].split(", ")
            label = c[0]
            lra = float(c[1])
            ldec = float(c[2])
            #projectToPolar
            xcenter, ycenter = self.p.projectToPolar( lra, ldec)

            theta= float(c[3])
            if label.find(" ") > -1:
              ll = label.split(" ")
              label = ll[0] + "\n " + ll[1]
              #if self.inPlotBounds(xcenter, ycenter):
            if 1 == 1:
              plt.text(xcenter, ycenter, label, rotation=theta, horizontalalignment="center", verticalalignment="center", fontsize=5)

     



    def plotDecCircles(self, decList):
        
        ra = 0.
        for dec in decList:
          x, y = self.p.projectToPolar(ra, float(dec))
          rr = np.sqrt(x*x + y*y)
          c1 = plt.Circle((0, 0), radius=rr, color=self.decCircleColor,fill=False)
          plt.gca().add_artist(c1)

    def plotRaLines(self, raHours, decMax):
        for theta in raHours:
          x, y = self.p.projectToPolar(float(theta), decMax)
          xx = [0, x]
          yy = [0, y]
          plt.plot(xx, yy, '-',color=self.raCircleColor, markersize=-100,marker="", linewidth=2)


    def plotCircle(self, r1, r2, plt):
        c1 = plt.Circle((0, 0), radius=r1*3, color=self.mapCircleColor,fill=False)
        c2 = plt.Circle((0, 0), radius=r2*3, color=self.mapCircleColor,fill=False)
        plt.gca().add_artist(c1)
        plt.gca().add_artist(c2)

    def plotRectangle(self, r1, r2, plt):
        c1 = patches.Rectangle((-r1*3, -r1*3), 2*r1*3, 2*r1*3, color='k',fill=False)
        c2 = patches.Rectangle((-r2*3, -r2*3), 2*r2*3, 2*r2*3, color='k',fill=False)
        plt.gca().add_artist(c1)
        plt.gca().add_artist(c2)

    def plotGnomonLine(self, plt, gnomonBase):
        xstart = 0
        ystart = 0
        xend = 0
        yend = gnomonBase
        plt.plot([xstart, xend], [ystart, yend],color='k')


    def plotLabels(self, plt,ax, plotSize, location, name):
        #    print location, name
        x1 = 0
        y1 = 0 - plotSize/3.3
        plt.text(x1, y1, "Local Solar Time", horizontalalignment="center", verticalalignment="center", fontsize=14)

        x1 = 0
        y1 = 0 - plotSize/2.5
        plt.text(x1, y1, name, horizontalalignment="center", verticalalignment="center", fontsize=20)
        
        lo = str(location.long).split(":")
        la = str(location.lat).split(":")
        lon = str(lo[0]) + u'\N{DEGREE SIGN}' + "" + str(lo[1]) + "'"
        lat = str(la[0]) + u'\N{DEGREE SIGN}' + "" + str(la[1]) + "'"
        ll = "Latitude = " + lat + "  Longitude=" + lon
        x1 = 0
        y1 = 0 - plotSize/2
        plt.text(x1, y1, ll, horizontalalignment="center", verticalalignment="center", fontsize=14)



    def listConstellation(self, constellationBoundaries):
   
        fn = "constellatlion_list.txt"
        ff = open(fn,"r")
        clist = ff.readlines()
        ff.close()

        for ii in range(len(constellationBoundaries)):  #constellationBoundaries:
            c = constellationBoundaries[ii]
            label = c[0]
            lines = c[1]
            xcenter = 0
            ycenter = 0
            for l in lines:
                x = float(l[0])
                y = float(l[1])
                xcenter = xcenter + x
                ycenter = ycenter + y
            
            if len(lines) > 0:
                xcenter = xcenter / float(len(lines))
                ycenter = ycenter / float(len(lines))        
            theta = 0
            ss = label + ", " + clist[ii-1].strip() + ", " + str(xcenter) + ", " + str(ycenter) + ", 0.0"
            #print ss
            #print label, clist[ii-1], xcenter, ycenter, theta

    #plt.plot([xstart, xend], [ystart, yend],color='k')


    def dateCircle(self):
 
        self.sun = ephem.Sun()
  
        #     J   F   M   A   M   J   J   A   S   O   N
        dn = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        mlist = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        dlist = [5, 10, 15, 20, 25, 30]


        # calculate the tick marks for the outer ring
        yy = "2018"
        mboundaries = []
        fiveticks = []
        otherticks = []

        # loop over all the months
        for m in range(1,13):
            if m < 10:
                mm = "0" + str(m)
            else:
                mm = str(m)
            dd = "2018" + "/" + mm + "/" + str( dn[m-1] )

            # find the boundaries for the end of each month
            sra = self.sun_location(dd) 
            mboundaries.append([m, float(sra)])
  
            # find the boundaries starting at the beginning of each month at 5 day intervals
            for dl in dlist:
                if dl < dn[m-1]:
                    dd = "2018" + "/" + mm + "/" + str(dl) 
                    sra = self.sun_location(dd) 
                    fiveticks.append([m, dl, float(sra)])


            # find the daily tick marks for the whole year
            for dl in range(dn[m-1]):
                if dl%5 > 0:
                    dd = "2018" + "/" + mm + "/" + str(dl) 
                    sra = self.sun_location(dd)
                    otherticks.append([m, dl, float(sra)])
         
        rr = 1.05
        dr = 0.05
        tl1 = -1 
        tl2 = 0.7
        tl3 = 0.9
        tt1 = 0.7
        r1 = rr - dr
        r2 = rr - dr * tl1
        lw = 1
        fs = 6
        

        # use the RA to figure out the angle theta - note that the RA stored is in radians, so
        # convert to hours first before doing the computation.
        hourOffset = 0.  #12.
        for dd in mboundaries:
            ra = (dd[1] *180./np.pi / 15. + hourOffset) % 24
            dec = 0.
            x1, y1 = self.p.projectToPolar(ra, dec)
            theta = np.arctan2(x1,y1)
            #theta = dd[1]  # fix this
            xx = [ r1*np.sin(theta), r2*np.sin(theta)]
            yy = [ r1*np.cos(theta), r2*np.cos(theta)]
            plt.plot(xx,yy,color=self.plateCircleColor, linewidth=lw)


        r2 = rr - dr * tl2
        for dd in fiveticks:
            ra = (dd[2] *180./np.pi / 15. + hourOffset) % 24.
            dec = 0.
            x1, y1 = self.p.projectToPolar(ra, dec)
            theta = np.arctan2(x1,y1)
            #theta = dd[2]  # fix this
            xx = [ r1*np.sin(theta), r2*np.sin(theta)]
            yy = [ r1*np.cos(theta), r2*np.cos(theta)]
            plt.plot(xx,yy,color=self.plateCircleColor,linewidth=lw) 
            xt = (rr-dr*(1.0 - tt1))*np.sin(theta)
            yt = (rr-dr*(1.0 - tt1))*np.cos(theta)
            if dd[1] < 30:
              rot = 180. - theta*180./np.pi
              plt.text(xt, yt, str(dd[1]), verticalalignment="center", horizontalalignment="center", rotation=rot, fontsize=fs)


        r2 = rr - dr * tl3
        for dd in otherticks:
            ra = (dd[2] *180./np.pi / 15.  + hourOffset)%24.
            dec = 0.
            x1, y1 = self.p.projectToPolar(ra, dec)
            theta = np.arctan2(x1,y1)
            #theta = dd[2]  # fix this
            xx = [ r1*np.sin(theta), r2*np.sin(theta)]
            yy = [ r1*np.cos(theta), r2*np.cos(theta)]
            plt.plot(xx,yy,color=self.plateCircleColor, linewidth=lw)

      
        ptsize = 0.0138889
        psize = fs  #10
        pspace = -4 
        rt = rr + dr * 0.5
        dtheta = -np.arctan((psize+pspace)*ptsize/rt)
        
        
        for m_id in range(len(mboundaries)):
          mmm = m_id
          if mmm == 0:
            mmm = 12
          dd = "2018" + "/" + str(mmm) + "/15" 
        
          sra = self.sun_location(dd)
          #theta_center= sra
          tout = mlist[m_id  - 1]
          wlength = len(tout)
          #theta = theta_center - dtheta * wlength/2
          #tnew = theta
          ra = (sra * 180./np.pi / 15. + hourOffset) % 24.
          dec = 0.
          x1, y1 = self.p.projectToPolar(ra, dec)
          theta = np.arctan2(x1,y1) - dtheta * wlength/2
          tnew = theta
          
          for t in tout:
              tnew = tnew + dtheta
              x2 = rt * np.sin(tnew)
              y2 = rt * np.cos(tnew)
              rot = 180. - tnew * 180./np.pi 
              plt.text(x2,y2, t, verticalalignment="center", horizontalalignment="center", rotation=rot, fontsize=fs)

        #plt.show()



        return 

    def sun_location(self, sdate):
        self.sun.compute(sdate)
        return self.sun.ra # + np.pi


    def plate(self):

        lw = 1
        pltLimit = 1
        decMax = -23.5
        lat = 30 
        decMax = -90 + lat 
        rMax = pltLimit
        self.p.setProjection(1, 0, 90, decMax, rMax )
   #     self.plotRete(decMax, rMax)

#        circle1 = plt.Circle( (0,0), self.Rmax, linewidth=lw, color=self.plateCircleColor, fill=False)
#        self.ax.add_artist(circle1)
        #self.plotHorizon(18.0)


        n = 100
        p = []
        for i in range(n):
            t = float(i)/float(n-1) * 2.0 * np.pi
            x = ( np.sin(t))
            y = ( np.cos(t))
            p.append( (x,y))

        circleShape = Polygon(p)
        n = 100 
        hrotate = 18
        altLine = self.a.createAltPath( 0.0, n, hrotate)
        pAltLine = self.p.projectSimpleLine(altLine)

        horizonShape = Polygon(pAltLine)
        plateShape = circleShape.difference(horizonShape)

        ax = plt.gca()
        ax.add_patch(descartes.PolygonPatch(plateShape, fc='b', ec='k', alpha=0.2))
        #ax.add_patch(descartes.PolygonPatch(ll1, fc='r', ec='k', alpha=0.2))




        rhr = rMax * 0.93
        for hr in range(24):
          theta = float(hr) * 15. * np.pi / 180.
          x = rhr * np.sin(-theta)
          y = rhr * np.cos(-theta)
          rot = 180. + float(hr)  * 15.
          hhh = hr % 12
          if hhh <> 0:
            ss = str(hhh)
          elif hr == 0:
            ss ="MID\n NIGHT"
          else:
            ss = "NOON"
          if hr > 14 or hr < 10:
            plt.text(x, y, ss, fontsize="7", verticalalignment="center", horizontalalignment="center", rotation=rot, color=self.plateCircleColor)
 
          dth = 4.0
          theta = (float(hr) * 15. + dth) * np.pi / 180. 
          x = rhr * np.sin(-theta)
          y = rhr * np.cos(-theta)
          rot = 180. + float(hr)  * 15.
          if hr > 0 and hr < 11:
            ss = "AM"
          elif  hr > 12 and hr < 24:
            ss = "PM"
          else:
            ss = ""
          if hr > 14 or hr < 10:
            plt.text(x, y, ss, fontsize="7", color=self.plateCircleColor, verticalalignment="center", horizontalalignment="center", rotation=rot)
      
        # 15 minute marks
        rhr = rMax 
        rhr2 = rMax * 0.985
        rhr3 = rMax * 0.96
        for fm in range(0, 24*4):
          theta = float(fm)/4.0 * 15. * np.pi / 180.
          x1 = rhr * np.sin(-theta)
          y1 = rhr * np.cos(-theta)
          if fm % 4 > 0:
            x2 = rhr2 * np.sin(-theta)
            y2 = rhr2 * np.cos(-theta)
          else:
            x2 = rhr3 * np.sin(-theta)
            y2 = rhr3 * np.cos(-theta)
          rot = 180. + float(hr)  * 15.
          plt.plot([x1,x2], [y1,y2], linewidth=2, color=self.plateCircleColor)

#          plt.text(x, y, "x", fontsize=36, verticalalignment="center", horizontalalignment="center", rotation=rot)
  

        #quote = "When I heard the learn'd astronomer, \n When the proofs, the figures, were arranged in columns before me, \n When I was shows the charts and diagrams, to add, divide, and measure them, \n When I sitting heard the astronomer where he lectured with much applause from the lecture-room, \n How soon unaccountable I became tired and sick, \n Till rising and glidering out I wander'd off by myself, \n In the mystical moist night-air, and from time to time, \n Look'd up in perfect silence at the star. \n  Walt Whitman, The Learn'd Astronomer"
        #plt.text(-0.5, 0.4, quote, fontsize=5, verticalalignment = "center", horizontalalignment="left")


        quote = "For my part, I know nothing with certainty, \n but the sight of the stars makes me dream.  \n - Vincent Van Gogh"
        plt.text(-0.0, 0.5, quote, fontsize=10, verticalalignment = "center", horizontalalignment="center")

    def plotHorizon(self, hrotate):

        npts = 60
        altLine = self.a.createAltPath( 0.0, npts, hrotate)
        pAltLine = self.p.projectSimpleLine(altLine)
        self.plotSimpleLine(pAltLine)

     


      


