from theta3d import *
import pygame
import math

# === Setup ===
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mouse Look Test")
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

clock = pygame.time.Clock()
running = True

# === Camera state ===
cameraPos = Vec3(0, 0, 3)
cameraUp = Vec3(0, 1, 0)
yaw = math.radians(-90)
pitch = 0.0
cameraSpeed = 5.0
mouseSensitivity = 0.002

# === Projection (example values) ===
fov = 60
aspect = 800 / 600
znear = 0.1
zfar = 100.0
projectionMatrix = Mat4.perspective(math.radians(fov), aspect, znear, zfar)

# === Triangle to render ===
triangle = Triangle(Vertex(Vec3(-0.5, -0.5, 0)), Vertex(Vec3(0.5, -0.5, 0)), Vertex(Vec3(0, 0.5, 0)))
red = (255, 0, 0)
black = (0, 0, 0)

# === Main loop ===
while running:
    deltaTime = clock.get_time() / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Escape key to quit
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    # === Camera Movement ===
    # Get cameraDirection from yaw and pitch
    dx, dy = pygame.mouse.get_rel()
    yaw += dx * mouseSensitivity
    pitch -= dy * mouseSensitivity
    pitch = max(-math.pi / 2 + 0.01, min(math.pi / 2 - 0.01, pitch))

    dirX = math.cos(pitch) * math.cos(yaw)
    dirY = math.sin(pitch)
    dirZ = math.cos(pitch) * math.sin(yaw)
    cameraDirection = Vec3(dirX, dirY, dirZ).normalize()

    # WASD movement
    right = cameraDirection.cross(cameraUp).normalize()
    if keys[pygame.K_w]:
        cameraPos += cameraDirection * cameraSpeed * deltaTime
    if keys[pygame.K_s]:
        cameraPos -= cameraDirection * cameraSpeed * deltaTime
    if keys[pygame.K_a]:
        cameraPos -= right * cameraSpeed * deltaTime
    if keys[pygame.K_d]:
        cameraPos += right * cameraSpeed * deltaTime

    # View and MVP matrix
    target = cameraPos + cameraDirection
    viewMatrix = Mat4.lookAt(cameraPos, target, cameraUp)
    mvp = projectionMatrix * viewMatrix

    # === Render ===
    screen.fill(black)
    dummy=Renderer(800,600)
    dummy.drawTriangle(screen, triangle, mvp, red)
    triangle2 = Triangle(Vertex(Vec3(0, -0.5, 0.2)), Vertex(Vec3(0.5, -0.5, 0)), Vertex(Vec3(0, 0.1, 0)))
    dummy.drawTriangle(screen, triangle2, mvp, (0,100,50))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
