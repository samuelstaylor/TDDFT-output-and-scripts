from OpenGL.GL import *
from OpenGL.GLUT import *

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(100, 100)
glutCreateWindow(b"OpenGL Test")

glEnable(GL_DEPTH_TEST)
print("OpenGL context works!")
