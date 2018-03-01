
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import ephem


class astronomy:

    def __init__(self):
        x = 0
        self.setLocation(1)



    def setLocation(self, location):
        mtsu = ephem.Observer()
        mtsu.long =  '-86.37'
        mtsu.lat = '35.8522'
        mtsuname = "Murfreesboro TN"


        york = ephem.Observer()
        york.long = "-1.819"
        york.lat = "53.9623"
        yorkname = "York UK"

        keywest = ephem.Observer()
        keywest.long = "81.7840"
        keywest.lat = "24.5592"
        keywestname = "Key West FL"

        obs = ephem.Observer()
        if (location == 1):
            obs = mtsu
            name = mtsuname
        elif (location == 2):
            obs = york
            name = yorkname
        elif (location == 3):
            obs = keywest
            name = keywestname
        else:
            print "error in location"
            exit()

        self.obs = obs
        self.obs.pressure = 0
        self.obs.date = "2016/12/8 00:36:39.45"

    def createAltPath(self, alt, npts, hrotate):

        altLine = []
        alt = alt * math.pi / 180.
        for i in range(npts+1):
            az = float(i)/float(npts)  * 360 * math.pi/180.
            r, d = self.obs.radec_of(az, alt)
            rr = float(r) / (2.0*math.pi) * 24
            dd = float(d) * 180./math.pi
            rr = (rr + hrotate)%24.
            altLine.append([rr, dd])
        return altLine

    def createAzPath(self, az, altMin, npts, hrotate):

        azLine = []
        az = az * math.pi / 180.
        for i in range(npts+1):
            alt =  (90 - float(i)/float(npts)  * (90-altMin)) * math.pi/180.
            r, d = self.obs.radec_of(az, alt)
            rr = float(r) / (2.0*math.pi) * 24
            dd = float(d) * 180./math.pi
            rr = (rr + hrotate) % 24.
            azLine.append([rr, dd])
        return azLine



    def createEclipticPath(self):

        eline = []
        for i in range(361):
            l = str( 0 + i)
            b = ephem.Ecliptic(l, "0", epoch="2016")
            c = ephem.Equatorial(b)
            r = c.ra
            d = c.dec
            rr = float(r) / (2.0*math.pi) * 24
            dd = float(d) * 180./math.pi
            eline.append([rr, dd])
        return eline

    def createEclipticPole(self):
        b = ephem.Ecliptic("0", "90", epoch="2016")
        c = ephem.Equatorial(b)
        r = c.ra
        d = c.dec
        rr = float(r) / (2.0*math.pi) * 24
        dd = float(d) * 180./math.pi
        return rr, dd
   


if __name__ == "__main__":
    
    a = astronomy()
    print a.obs.sidereal_time()
    a.createEclipticPath()
#    ra, dec = a.createAltPath( 30, 30)

    a.dateCircle()
    
