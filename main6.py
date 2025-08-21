from theta3d import *
import pygame
import sys
import math

# === Pygame Setup ===
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("WASD Camera Movement")

# === Colors ===
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# === Create Triangles ===
v1 = Vertex(Vec3(0, 0.5, 0), color=red)
v2 = Vertex(Vec3(-0.5, -0.5, 0), color=red)
v3 = Vertex(Vec3(0.5, -0.5, 0), color=red)
triangle1 = Triangle(v1, v2, v3)

v4 = Vertex(Vec3(0, 0.5, 1), color=green)
v5 = Vertex(Vec3(-0.5, -0.5, 1), color=green)
v6 = Vertex(Vec3(0.5, -0.5, 1), color=green)
triangle2 = Triangle(v4, v5, v6)

triangleList = [triangle1, triangle2]

# === Renderer Setup ===
renderer = Renderer(width, height)

# === Camera Setup ===
cameraPos = Vec3(0, 0, 2)
cameraSpeed = 5
yaw = 0              # Horizontal angle in radians
pitch = 0            # Vertical angle in radians
turnSpeed = math.radians(90)  # Degrees per second
cameraUp = Vec3(0, 1, 0)

# === Projection Matrix ===
fov = math.radians(90)
aspectRatio = width / height
near = 0.1
far = 1000
projectionMatrix = Mat4.perspective(fov, aspectRatio, near, far)

# === Main Loop ===
clock = pygame.time.Clock()
running = True
while running:
    deltaTime = clock.get_time() / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input Handling
    keys = pygame.key.get_pressed()

    # Camera turning (arrow keys)
    if keys[pygame.K_LEFT]:
        yaw -= turnSpeed * deltaTime
    if keys[pygame.K_RIGHT]:
        yaw += turnSpeed * deltaTime
    if keys[pygame.K_UP]:
        pitch += turnSpeed * deltaTime
    if keys[pygame.K_DOWN]:
        pitch -= turnSpeed * deltaTime

    # Clamp pitch to prevent camera flipping
    pitch = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, pitch))

    # Update cameraDirection based on yaw and pitch
    dirX = math.cos(pitch) * math.sin(yaw)
    dirY = math.sin(pitch)
    dirZ = -math.cos(pitch) * math.cos(yaw)
    cameraDirection = Vec3(dirX, dirY, dirZ).normalize()

    # WASD Movement
    if keys[pygame.K_w]:
        cameraPos += cameraDirection * cameraSpeed * deltaTime
    if keys[pygame.K_s]:
        cameraPos -= cameraDirection * cameraSpeed * deltaTime
    if keys[pygame.K_a]:
        right = cameraDirection.cross(cameraUp).normalize()
        cameraPos -= right * cameraSpeed * deltaTime
    if keys[pygame.K_d]:
        right = cameraDirection.cross(cameraUp).normalize()
        cameraPos += right * cameraSpeed * deltaTime

    # View and MVP Matrix
    target = cameraPos + cameraDirection
    viewMatrix = Mat4.lookAt(cameraPos, target, cameraUp)
    mvp = projectionMatrix * viewMatrix

    # === Clear Screen ===
    screen.fill(black)

    # === Render Triangles with Depth Sorting ===
    renderer.renderTriangles(screen, triangleList, mvp)

    # === Display ===
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
