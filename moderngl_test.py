import time
import numpy as np 
import glfw
import moderngl

# -- Window and GL context --
if not glfw.init():
    raise SystemExit("GLFW init failed")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

window = glfw.create_window(1200, 900, "Python Shader Play", None, None)
if not window:
    glfw.terminate()
    raise SystemExit("Window creation failed")
glfw.make_context_current(window)

# -- ModernGL context --
ctx = moderngl.create_context()

# -- Shaders --
with open("vertex.vs") as fh:
    vs = fh.read()

with open("fragment.fs") as fh:
    fs = fh.read()


prog = ctx.program(vertex_shader=vs, fragment_shader=fs)

# Full-screen triangle
vertices = np.array([
    -1.0, -1.0,
     3.0, -1.0,
    -1.0,  3.0
], dtype="f4")
vbo = ctx.buffer(vertices.tobytes())
vao = ctx.simple_vertex_array(prog, vbo, "in_pos")

start_frame = 0
fps_timer = time.perf_counter()
end_frame = time.perf_counter()
TARGET_FPS = 60
TARGET_FPS_TIME = 1.0/TARGET_FPS
framecount = 0
print("\033[s")


while not glfw.window_should_close(window):

    # glfw.swap_interval(1)s
    glfw.poll_events()

    start_frame = time.perf_counter()

    width, height = glfw.get_framebuffer_size(window)
    ctx.viewport = (0, 0, width, height)
    ctx.clear(0.02, 0.02, 0.03)

    # prog["iTime"].value = float(time.perf_counter() - start)
    prog["iResolution"].value = (float(width), float(height))
    prog["MAXITER"].value = int(300)

    vao.render(moderngl.TRIANGLES)
    glfw.swap_buffers(window)
    
    # Limit FPS to 60
    end_frame = time.perf_counter()
    elapsed = (end_frame - start_frame)
    if elapsed < TARGET_FPS_TIME and elapsed > 0:
        glfw.wait_events_timeout(TARGET_FPS_TIME-elapsed)

    framecount += 1
    if time.perf_counter() - fps_timer >= 1:
        print(f"\033[u\033[2KFPS: {framecount}, et: {elapsed} tg: {TARGET_FPS_TIME}\n\tsf: {start_frame}, ef: {end_frame}")
        framecount = 0
        fps_timer = time.perf_counter()
        



glfw.terminate()
