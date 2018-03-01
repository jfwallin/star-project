from operator import itemgetter



class starData:
    
    def __init__(self):

        self.readAstrolabeStars()        
        self.readStars()
        self.indexStars()
        self.readLines()
        self.lookupStarsInGroups()
        self.constellationBoundaries()
        self.nebula()

    def readAstrolabeStars(self):
        fn = "starNames.dat"
        f = open(fn, "r")
        self.astars = []
        for l in f:
            aa = l.strip().split(", ")
            aa[3] = int(aa[3])
            aa[4] = int(aa[4])
            aa[9] = int(aa[9])
            for k in range(5,9):
                aa[k] = float(aa[k])
            self.astars.append(aa)
        f.close()



    def readStars(self):
        fn1 = "stars.dat"

        lines = []
        f1 = open(fn1,"r")
        for l in f1:
            lines.append(l.strip())
        f1.close()

        ss = []
        for i in range(len(lines)/4):
            l1 = i*4
            l2 = l1 + 1
            l3 = l1 + 2
            l4 = l1 + 3
        
            v = [lines[l2], lines[l3], lines[l4]]    
            vv = lines[l1].split()
            v.append(int(vv[0]))
            v.append(int(vv[1]))
            v.append(float(vv[2]))
            v.append(float(vv[3]))
            v.append(float(vv[4]))
            v.append(float(vv[5]))
            v.append(int(vv[6]))
            ss.append(v)


        stars = sorted(ss, key=itemgetter(1,9,3))
        self.stars = stars


    def printStars(self):
        for  s in self.stars:
            sfinal = ""
            for ss in s:
              sfinal = sfinal + str(ss) + ", "
            sfinal = sfinal.strip().strip()
            print sfinal



    def indexStars(self):

        constellationStartIndex = {}
        constellationEndIndex = {}
        currentConstellation = "dddd"
        for ii in range(len(self.stars)):
            s= self.stars[ii]
            if s[1] != currentConstellation:
                constellationEndIndex[currentConstellation] = ii ###-1
                currentConstellation = s[1]
                constellationStartIndex[s[1]] = ii

        constellationEndIndex[ s[1]] = len(self.stars)
        self.constellationStartIndex = constellationStartIndex
        self.constellationEndIndex = constellationEndIndex

        #for c in constellationStartIndex:
        #    print c, constellationStartIndex[c], constellationEndIndex[c]


    def readLines(self):

        lines = []
        fn2 = "jwlines.dat"
        f2 = open(fn2, "r")
        for l in f2:
            lines.append(l.strip())
        f2.close()

        ct= 0
        flines = []
        for l in lines:
            if len(l) > 0:
                if l.find("#") > -1:
                    a = l.split("#")
                    if len(a[0]) > 0:
                        b = a[0]
                    else:
                        b = ""
                else:
                    b = l
            else:
                b = ""
    
            if len(b) > 0:
                flines.append(b + " ")
                ct =ct+ 1

        lgroups = []
        g = ""
        for l in flines:
            if l.find(";") == -1:
                g = g + l
            else:
                g = g + l
                lgroups.append( " " + g + " ")
                g = ""

        self.lgroups = lgroups


    def lookupStarsInGroups(self):

        self.constellationLines = []
        
        for g in self.lgroups:
            gg = g.split()

            cline = []
            for ii in range(len(gg)/2):
                ref = gg[ii*2]
                ss = gg[ii*2+1]
                #print ii, ref, ss
                
                match = 0
                if ref != "HD":
                    for kk in range( self.constellationStartIndex[ref], self.constellationEndIndex[ref]):
                        ll = self.stars[kk][9]
                        if ll == int(ss):
                            match = kk
                            #print "match = ",kk

                else:
                    ref = ""
                    for kk in range( 0, len(self.stars)):
                        ll = self.stars[kk][3]
                        if ll == int(ss):
                            match = kk
                            #print "2match = ",kk
                
                #print self.stars[match]
                cline.append([self.stars[match][5], self.stars[match][6]])
                
                if match == 0:
                    print ref, ss
                    print "nope"
                    exit()
            self.constellationLines.append(cline)
                    
#        for c in self.constellationLines:
#            print c
    
    def constellationBoundaries(self):

        ll = []
        fn = "bound_20.dat"
        f = open(fn, "r")
        for l in f:
            ll.append(l.strip().split())
        f.close()


        self.constellationBoundaries = []
        cnames = []
        boundary = []
        currentConstellation = ""
        for i in range(len(ll)):
            cpt = ll[i]
            if  cpt[2]  != currentConstellation:
                self.constellationBoundaries.append([currentConstellation, boundary])
                boundary = []
                boundary.append(cpt[0:2])
                currentConstellation = cpt[2]
            else:
                boundary.append(cpt[0:2])
 

    def nebula(self):
        
        self.nebula = []
        fn = "nebulae.dat"
        f = open(fn, "r")
        for l in f:
            v = l.strip().split()
            self.nebula.append(v)
#            print v

#        for h in self.constellationBoundaries:
#            print h



if __name__ == "__main__":
    s = starData()


    
