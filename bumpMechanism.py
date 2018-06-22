import rhinoscriptsyntax 
import math as m
import basicLinearEq as lin

class bump:
    def __init__(self,VERTS,NORMS,RISE,WIDTHRATIO):
        self.heights = RISE
        self.dims = WIDTHRATIO
        self.verts = VERTS
        self.norms = NORMS
        self.thick = 0
        self.faces = []
    def genBump(self,thick):
        mid = []
        for i in range(len(self.verts)):
            v = lin.vecUnitize(self.norms[i])
            pt = lin.vecAdd(self.verts[i],lin.vecScale(v,self.thick))
            mid.append(pt)
            self.verts.append(pt)
        self.faces.append(0,1,5,4)
        self.faces.append(1,2,6,5)
        self.faces.append(2,3,7,6)
        self.faces.append(3,0,4,7)
        self.faces.append(0,1,2,3)
        # TOP SECTION
        sum = [0,0,0]
        top = []
        for i in range(len(mid)):
            v = lin.vecUnitize(self.norms[i])
            pt = lin.vecAdd(mid[i],lin.vecScale(v,self.heights[i]))
            sum = lin.vecAdd(sum,pt)
            top.append(pt)
        cnt = lin.vecScale(sum,1/len(mid))
        for i in range(len(top)):
            v = lin.vecDiff(cnt,top[i])
            top[i] = lin.vecAdd(top[i],lin.vecScale(self.dims[i]))
            self.verts.append(top[i])
        self.faces.append(4,5,9,8)
        self.faces.append(5,6,10,9)
        self.faces.append(6,7,11,10)
        self.faces.append(7,4,11,8)
        self.faces.append(8,9,10,11)
        self.mesh = rs.AddMesh(self.faces,self.verts)
        return self.mesh

class meshBumps:
    def __init__(self,MESH,ATT,RISE,FREQ,LIMIT):
        self.mesh = MESH
        self.att = ATT
        self.freq = FREQ
        self.limit = LIMIT
        self.rise = RISE
        self.bumps = []
        self.verts = rs.MeshVertices(self.mesh)
        self.norms = rs.MeshVertNorms(self.mesh)
        self.faces = rs.MeshFaces(self.mesh)
        self.meshes = []
    def getBumps(self):
        for i in range(len(self.faces)):
            verts = []
            norms = []
            dims = []
            risen = []
            for i in range(len(self.faces)):
                for j in range(len(self.faces[i])):
                    vert = self.verts[self.faces[i][j]]
                    norm = self.norms[self.faces[i][j]]
                    verts.append(vert)
                    norms.append(norm)
                    sum = []
                    for k in range(len(self.att)):
                        sum = sum + lin.vecMag(lin.vecDiff(vert,self.att[k]))
                    f = sum/len(self.att)
                    dims.append(m.cos(self.freq*f/self.limit*m.pi/180))
                    risen.append(self.rise)
            self.bumps.append(bump(verts,norms,risen,dims)
        for i in range(len(self.bumps)):
            self.meshes.append(genBump(self.bumps[i]))

def Main():
    meshes = rs.GetObjects("please select meshes",rs.filter.mesh)
    pts = rs.GetObjects("please select points",rs.filter.point)
    rise = rs.GetReal("please enter bump height",2)
    freq = rs.GetReal("please enter frequence",50)
    for i in range(len(meshes)):
        meshTexture = meshBumps(meshes[i],pts,rise,freq,