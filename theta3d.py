import pygame
import math
import sys

#the Vec3 class

class Vec3:
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z

        #add and sub methods:

    def __add__(self,other):
        return Vec3(self.x+other.x,self.y+other.y,self.z+other.z)
        
    def __sub__(self, other):
        return Vec3(self.x-other.x, self.y-other.y, self.z-other.z)
        

    #scalar mul and div methods:

    def __mul__(self,scalar):
        return Vec3(self.x*scalar,self.y*scalar,self.z*scalar)
        
    def __truediv__(self,scalar):
        if scalar==0:
            scalar=1
        return Vec3(self.x/scalar,self.y/scalar,self.z/scalar)
        

    #length methods:

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
        
    def lengthSqrd(self):
        return self.x**2 + self.y**2 + self.z**2
        

    #normalize method:

    def normalize(self):
        l=self.length()
        if l==0:
            return Vec3(0,0,0)
        return self/l
        

    #dot production:

    def dot(self,other):
        return self.x * other.x + self.y * other.y + self.z * other.z
        

    #coss production:

    def cross(self, other):
        return Vec3(
        self.y * other.z - self.z * other.y,
        self.z * other.x - self.x * other.z,
        self.x * other.y - self.y * other.x
        )


    #utility methods:

    def toList(self):
        return [self.x,self.y,self.z]
        
    def toTuple(self):
        return (self.x,self.y,self.z)
        
    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"
        
    def __getitem__(self,index):
        coords = self.toList()
        return coords[index]


#the Mat4 (4x4 matirx) class

class Mat4:
    def __init__(self,matrix=None):
        self.identityM =[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.zeroM =[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        if matrix == None:
            self.matrix=self.zeroM
        elif (len(matrix) != 4) and (len(matrix[0] != 4)):
            self.matrix=matrix[:]
            raise ValueError("Mat4 must have 4 list elements (which contain 4 elements)")
        else:
            self.matrix=matrix
    
    #acsess helpers:
    
    def __getitem__(self,index):
        row, col = index
        return self.matrix[row][col]
    
    def __setitem__(self,index,value):
        row,col = index
        self.matrix[row][col]=value
    

    #identity and zero method:

    def identity(self):
        return Mat4(matrix=self.identityM)
    
    def zero(self):
        return Mat4(matrix=self.zeroM)
    

    #operation methods:

    def __mul__(self,other):
        if isinstance(other, Mat4):
            output=Mat4()
            for row in range(4):
                for col in range(4):
                    sum=0
                    for k in range(4):
                        sum+=self[row,k]*other[k,col]
                    output[row,col] = sum
            return output
        elif isinstance(other, Vec4):
            x = self[0, 0] * other.x + self[0, 1] * other.y + self[0, 2] * other.z + self[0, 3] * other.w
            y = self[1, 0] * other.x + self[1, 1] * other.y + self[1, 2] * other.z + self[1, 3] * other.w
            z = self[2, 0] * other.x + self[2, 1] * other.y + self[2, 2] * other.z + self[2, 3] * other.w
            w = self[3, 0] * other.x + self[3, 1] * other.y + self[3, 2] * other.z + self[3, 3] * other.w
            return Vec4(x,y,z,w)
        else:
            raise TypeError("Unsupported operand for Mat4 * {}".format(type(other)))
    
    
    def translate(self,tx,ty,tz):
        output = self.identity()
        output[0,3]=tx
        output[1,3]=ty
        output[2,3]=tz
        return output
    
    def scale(self,sx,sy,sz):
        output=self.identity()
        output[0,0]=sx
        output[1,1]=sy
        output[2,2]=sz
        return output
    
    #angle is in radians
    def rotateX(self,angle):
        output = self.identity()
        output[1,1]=math.cos(angle)
        output[1,2]=-math.sin(angle)
        output[2,1]=math.sin(angle)
        output[2,2]=math.cos(angle)
        return output
    
    def rotateY(self,angle):
        output=self.identity()
        output[0,0]=math.cos(angle)
        output[0,2]=math.sin(angle)
        output[2,0]=-math.sin(angle)
        output[2,2]=math.cos(angle)
        return output

    def rotateZ(self,angle):
        output=self.identity()
        output[0,0]=math.cos(angle)
        output[0,1]=-math.sin(angle)
        output[1,0]=math.sin(angle)
        output[1,1]=math.cos(angle)
        return output
    
    def transpose(self):
        output=Mat4()
        for i in range(4):
            for j in range(4):
                output[j,i]=self[i,j]
        return output
    
    #provided by chatgpt
    def inverseAffine(self):
        # Step 1: Extract rotation (upper-left 3x3)
        R = [[self[i, j] for j in range(3)] for i in range(3)]

        # Step 2: Transpose rotation (Rᵀ = inverse of rotation)
        R_T = [[R[j][i] for j in range(3)] for i in range(3)]

        # Step 3: Extract translation vector
        T = [self[i, 3] for i in range(3)]

        # Step 4: Compute inverse translation = -Rᵀ * T
        T_inv = [
            -sum(R_T[i][j] * T[j] for j in range(3)) for i in range(3)
        ]

        # Step 5: Build the inverse matrix
        inv = self.identity()
        for i in range(3):
            for j in range(3):
                inv[i, j] = R_T[i][j]
            inv[i, 3] = T_inv[i]

        return inv
    

    #veiw matrices:

    #eye,target, and up are all Vec3 objects. Also provided by chatgpt, but uses my Vec3 calss
    @staticmethod
    def lookAt(eye,target,up):
        z=(eye-target).normalize()
        x=up.cross(z).normalize()
        y=z.cross(x)

        tx=-x.dot(eye)
        ty=-y.dot(eye)
        tz=-z.dot(eye)

        return Mat4(matrix=[[x.x,x.y,x.z,tx],
                            [y.x,y.y,y.z,ty],
                            [z.x,z.y,z.z,tz],
                            [0,0,0,1]])

    #also chatgpt. Example use: proj = Mat4.perspective(fov=math.radians(60), aspect=16/9, near=0.1, far=100.0)
    @staticmethod
    def perspective(fov,aspect,near,far):
        f=1/math.tan(fov/2)
        nf=1/(near-far)

        return Mat4([[f/aspect,0,0,0],
                    [0,f,0,0],
                    [0,0,(far+near)*nf,2*far*near*nf],
                    [0,0,-1,0]])

#position is a Vec3 object
class Vertex:
    def __init__(self,position,color=(255,255,255)):
        self.position=position
        self.color=color


#v1,v2, and v3 are all vertex objects
class Triangle:
    def __init__(self,v1,v2,v3):
        self.v1=v1
        self.v2=v2
        self.v3=v3
    
    #easy acsess:

    def getVertexList(self):
        return [self.v1,self.v2,self.v3]
    
    def extractVectors(self):
        output=[]
        for vert in self.getVertexList():
            output.append(vert.position)
        return output


class Vec4:
    def __init__(self,x,y,z,w=1):
        self.x=x
        self.y=y
        self.z=z
        self.w=w
    
    #easy acsess:

    def toVec3(self):
        if self.w!=0:
            return Vec3(self.x/self.w, self.y/self.w, self.z/self.w)
        else:
            return Vec3(self.x,self.y,self.z)
    
    def toList(self):
        return [self.x,self.y,self.z,self.w]
    
    def toTuple(self):
        return (self.x,self.y,self.z,self.w)
    
    def __getitem__(self,index):
        output=0
        if (0<index) and (index<4):
            output = self.toList()[index]
        else:
            raise IndexError("index must be from 0 through 3 inclusive")
        return output
    
    def __setitem__(self,index,value):
        if (0<index) and (index<4):
            if index==0:
                self.x=value
            if index==1:
                self.y=value
            if index==2:
                self.z
            if index==3:
                self.w
        else:
            raise IndexError("index must be from 0 through 3 inclusive")
    
    #operations:

    def __mul__(self,scalar):
        return Vec4(self.x*scalar, self.y*scalar, self.z*scalar, self.w*scalar)
    
    def __add__(self,other):
        return Vec4(self.x+other.x, self.y+other.y, self.z+other.z, self.w+other.w)
    
    def __repr__(self):
        return f"Vec4({self.x},{self.y},{self.z},{self.w})"


class Renderer:
    def __init__(self, screenWidth,screenHeight):
        self.width=screenWidth
        self.height=screenHeight

    #triangle is a triangle object
    def projectTriangle(self,triangle,mvpMatrix):
        vec3s=triangle.extractVectors()
        vec4s=[]
        for vec3 in vec3s:
            x=vec3.x
            y=vec3.y
            z=vec3.z
            vec4=Vec4(x,y,z,1.0)
            vec4s.append(vec4)
        
        clipSpaceVecs=[]
        for vec4 in vec4s:
            transformed=mvpMatrix*vec4
            clipSpaceVecs.append(transformed)
        
        ndcCoords=[]
        for v in clipSpaceVecs:
            ndc=v.toVec3()
            ndcCoords.append(ndc)
        
        screenCoords=[]
        for ndc in ndcCoords:
            screenX=(ndc.x+1)*.5*self.width
            screenY=(1-ndc.y)*.5*self.height #y is fliped
            screenCoords.append((screenX,screenY))
        
        return screenCoords
    
    def drawTriangle(self,surface,triangle,mvpMatrix,color=(255,255,255)):
        screenCoords=self.projectTriangle(triangle,mvpMatrix)
        #print(screenCoords)

        intCoords=[]
        for (x,y) in screenCoords:
            intCoord=(round(x),round(y))
            intCoords.append(intCoord)
        pygame.draw.polygon(surface,color,intCoords)

    def computeTriangleDepth(self, triangle, mvpMatrix):
        vec3s = triangle.extractVectors()
        avg_z = 0
        for v in vec3s:
            vec4 = Vec4(v.x, v.y, v.z, 1.0)
            transformed = mvpMatrix * vec4
            # Convert to NDC
            if transformed.w != 0:
                ndc_z = transformed.z / transformed.w
            else:
                ndc_z = transformed.z
            avg_z += ndc_z
        return avg_z / 3
    
    def renderTriangles(self, surface, triangleList, mvpMatrix):
        # Compute depth for each triangle
        sortedTriangles = sorted(
            triangleList,
            key=lambda tri: self.computeTriangleDepth(tri, mvpMatrix),
            reverse=True  # farthest first
        )

        for tri in sortedTriangles:
            self.drawTriangle(surface, tri, mvpMatrix, color=tri.v1.color)  # Or another color logic


        
        