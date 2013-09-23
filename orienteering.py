

from random import shuffle,randint

from math import sin,cos,radians,sqrt,atan2,degrees

from copy import copy

def main ():

   routes      = makeRoutes(20,[20,30,40,50      ])
   routes.extend(makeRoutes( 4,[20,30,40,50,60   ]))
   routes.extend(makeRoutes( 4,[20,30,40,50,60,70]))
   routes.extend(makeRoutes( 2,[ 5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]))


   printRoutes(routes)





def makeRoutes (routeCount, segmentLengths):

   bounds = Bounds(-50, 50, -100, 0)
   startDistances=[20,40,60,80,100]


   degMod = 5


   routes = []

   for trial in range(routeCount):




      start = Point(0 , -startDistances[randint(0,len(startDistances)-1)] )
      goal  = Point([10,-10][trial<routeCount/2], 0 )



      route = Route(start, goal, segmentLengths, degMod, bounds)

      routes.append(route)

   return routes


def printRoutes (routes):
   for route in routes:
      route.printOut()

   #print
   #print "-"*35




class Route(object):


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
   #             20
   #              |
   #              |
   #              |
   #             40
   #              |
   #              |
   #              |
   #             60
   #              |
   #              |
   #              |
   #             80
   #              |
   #              |
   #              |
   #             100
   #
   #


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

   tolerance = .5/12  # 1/2 inch


   def __init__(self, start, goal, segmentLengths, degMod, bounds):

      self.start = copy(start)
      self.goal = copy(goal)

      count = len(segmentLengths)



      self.segments = count*[0]

      while True:
         shuffle(segmentLengths)


         # print "restart",start.north,segmentLengths,
         p = copy(self.start)
         for i in range(count-2):
            d = segmentLengths[i]

            trys = 0
            while True:
               while True:
                  b = randint(0,360/degMod - 1) * degMod
                  if i==0 and (b <= 10 or abs(b-180) <= 10 or 360-b <= 10):
                     continue  # the first segment should not be too close to the rope
                  break

               segment = Segment(d, b)

               newP = copy(p).addSegment(segment)

               if bounds.contains(newP):
                  break

               trys += 1
               if trys > 100:
                  break;

            if trys > 100:
               continue

            self.segments[i] = segment
            p = newP


         # compute next to last point

         intersections = circleIntersect (p, segmentLengths[-2],goal,segmentLengths[-1])


         validRoute = False
         for  penultimateP in intersections :
            if not bounds.contains(penultimateP):
               #print "intersect point out of bounds"
               continue

            b = int(round((360+ p.bearingTo(penultimateP))/degMod )*degMod)%360
            self.segments[-2] = Segment(segmentLengths[-2], b)
            p.addSegment(self.segments[-2])

            b = int(round((360+penultimateP.bearingTo(goal        ))/degMod )*degMod)%360
            self.segments[-1] = Segment(segmentLengths[-1], b)
            p.addSegment(self.segments[-1])

            error = p.distTo(goal)

            if error < self.tolerance:
               validRoute = True
               break

         if validRoute:
            break


      self.check()

   def printOut (self):


      startIndex = -self.start.north/20 - 1


      #print
      #print "-"*35
      #print
      print "Start Point: %s (%d feet)"%(chr(ord("A")+startIndex),-self.start.north)
      print
      print "     Bearing    Distance"
      print "    (magnetic)   (feet) "
      print "    ----------  --------"
      for i,segment in enumerate(self.segments):
         print "%2d. %10d  %8d"%(i+1, segment.bearing, segment.distance)
      print
      print self.goalMessages[self.goal.east<0] + self.goalMessageSuffixes[randint(0,len(self.goalMessageSuffixes)-1)]+"."
      print "$"


   def check (self):
      p = copy(self.start)
      for segment in self.segments:

         p.addSegment(segment)

      err = p.distTo(self.goal)
      if err > self.tolerance :
         print p
         print self.goal
         print err * 12
         exit(-1)




def bearing (p0, p1):
   return degrees(atan2(  p0.east - p1.east , p0.north - p1.north  ))



def circleIntersect (p0,r0,p1,r1):

   d = p0.distTo(p1)

   if d == 0:
      # circles have the same center
      # in this case there are either no solutions or infinte soloutions
      # neither works for us
      return []

   if d > r0 + r1:
      #points are too far apart - no solution
      return []

   if d <  abs(r0 - r1):
      #points are too close together - one circle is entirely in the other - no solution
      return []


   a = (r0**2 - r1**2 + d**2 ) / (2 * d)

   h = sqrt( r0**2 - a**2 )

   e0 = p0.east
   n0 = p0.north

   e1 = p1.east
   n1 = p1.north


   n2 = n0 + a *( n1 - n0 ) / d
   e2 = e0 + a *( e1 - e0 ) / d

   n3 = n2 + h *( e1 - e0 ) / d
   e3 = e2 - h *( n1 - n0 ) / d

   result = [Point(e3,n3)]


   if h>0:
      n3 = n2 - h *( e1 - e0 ) / d
      e3 = e2 + h *( n1 - n0 ) / d
      result.append(Point(e3,n3))


   return result




class Point(object):

    def __init__(self, e, n):
        self.east = e
        self.north = n


    def addSegment (self, segment):
       self.east  += segment.distance * sin(radians(segment.bearing))
       self.north += segment.distance * cos(radians(segment.bearing))
       return self

    def bearingTo (self,p):
       return degrees(atan2(  p.east - self.east , p.north - self.north  ))

    def distTo (self,p):
       de = self.east  - p.east
       dn = self.north - p.north

       return sqrt(de**2 + dn **2)



    def __str__(self):
       return "east=%f north=%f"%(self.east,self.north)





class Segment(object):
   def __init__(self, distance, bearing):
       self.distance = distance
       self.bearing  = bearing

class Bounds(object):
   def __init__(self, eastMin, eastMax, northMin, northMax):
       self.eastMin = eastMin
       self.eastMax = eastMax
       self.northMin = northMin
       self.northMax = northMax

   def contains (self, p):
      return p.north <= self.northMax and p.north >= self.northMin and p.east >= self.eastMin and p.east <= self.eastMax







main()