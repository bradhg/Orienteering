

from random import shuffle,randint

from math import sin,cos,radians,sqrt,atan2,degrees



def makeRoutes ():
   degMod = 5

   count = 4

   segmentLengths = [20,30,40,50]
   startDistances=[20,40,60,80,100]


   goalMessages = ["Every scout should ","We want scouts to "]

   goalMessageSuffixes =[
      "Be Prepared",
      "be Trustworthy",
      "be Loyal",
      "be Helpful",
      "be Friendly",
      "be Courteous",
      "be Kind",
      "be Obedient",
      "be Cheerful",
      "be Thrifty",
      "be Brave",
      "be Clean",
      "be Reverent",
   ]


   runs = 20

   for trial in range(runs):

      bearings = count*[0]




      start = randint(0,len(startDistances)-1)

      startDistance = startDistances[start]




      #
      #      N          0
      #    W   E    270   90
      #      S         180
      #
      #
      #     g        0         g
      #              |
      #              |
      #              |
      #              A
      #              |
      #              |
      #              |
      #              B
      #              |
      #              |
      #              |
      #              C
      #              |
      #              |
      #              |
      #              D
      #              |
      #              |
      #              |
      #              E
      #
      #


      goalNumber = [0,1][trial<runs/2]

      goalN = 0
      goalE = [10,-10][goalNumber]








      while True:
         shuffle(segmentLengths)
         #print "restart",startDistance,segmentLengths,
         e = 0
         n = -startDistance
         for i in range(count-2):
            d = segmentLengths[i]
            while True:
               b = randint(0,360/degMod - 1) * degMod

               de = d * sin(radians(b))
               dn = d * cos(radians(b))

               newN = n + dn
               newE = e + de


               if newN <= 0 and newN >= -100 and newE >= -50 and newE <= 50:
                  break

            n=newN
            e=newE
            bearings[i] = b

         dist = distPoints(n,e,goalN,goalE)


         # compute next to last point

         newPoint = circleIntersect (n,e,segmentLengths[-2],goalN,goalE,segmentLengths[-1])

         if newPoint == None:
            #print "no intersect"
            continue
         [newN,newE] = newPoint

         if newN > 0 or newN < -100 or newE < -50 or newE > 50:
            #print "points out of bounds"
            continue

         bearings[-2] = int(round((360+degrees(atan2(  newE -  e    , newN  - n   )))/degMod )*degMod)%360
         bearings[-1] = int(round((360+degrees(atan2(  goalE - newE , goalN - newN)))/degMod )*degMod)%360


         b = bearings[-2]
         d = segmentLengths[-2]

         de = d * sin(radians(b))
         dn = d * cos(radians(b))

         n += dn
         e += de


         b = bearings[-1]
         d = segmentLengths[-1]

         de = d * sin(radians(b))
         dn = d * cos(radians(b))

         n += dn
         e += de

         error = distPoints(n,e,goalN,goalE)


         if error > .5/12:
            #print " rounding cause error > 1/2 inch"
            continue

         break



      print
      print "-"*35
      print
      print "Start Point: %s (%d feet)"%(chr(ord("A")+start),startDistance)
      print
      print "    Bearing    Distance"
      print "   (magnetic)   (feet) "
      print "   ----------  --------"
      for i in range(count):
         print "%d. %10d  %8d"%(i+1,bearings[i],segmentLengths[i])
      print
      print goalMessages[goalNumber]+goalMessageSuffixes[trial % (len(goalMessageSuffixes)-1)]+"."
      print

   print
   print "-"*35


def distPoints (x0,y0,x1,y1):
   dx = x0-x1
   dy = y0-y1

   return sqrt(dx**2 + dy **2)


def circleIntersect (x0,y0,r0,x1,y1,r1):

   d = distPoints(x0,y0,x1,y1)

   if d > r0 + r1:
      #points are too far apart - no solution
      return None

   if d <=  abs(r0 - r1):
      #points are too close together - no solution
      return None

   a = (r0**2 - r1**2 + d**2 ) / (2 * d)

   h = sqrt( r0**2 - a**2 )


   x2 = x0 + a *( x1 - x0 ) / d
   y2 = y0 + a *( y1 - y0 ) / d

   x3 = x2 + h *( y1 - y0 ) / d
   y3 = y2 - h *( x1 - x0 ) / d

   return [x3,y3]


makeRoutes()

