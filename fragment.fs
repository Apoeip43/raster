#version 330
uniform float   iTime;
uniform vec2    iResolution;
uniform int     MAXITER;
out vec4 fragColor;

struct complex {
    float x;
    float y;
};

complex squarec(complex c){
    complex result;
    result.x = c.x*c.x - c.y*c.y;
    result.y = 2*c.x*c.y;
    return result;
}

complex sumc(complex a, complex b){
    complex result;
    result.x = a.x + b.x;
    result.y = a.y + b.y;
    return result;
}

float absc(complex c) {
    return sqrt(c.x*c.x + c.y*c.y);
}

void calc_mandelbrot(float init_x, float init_y) {
    complex init_pos;

    init_pos.x = init_x;
    init_pos.y = init_y;
    
    int it = 0;
    complex z = init_pos;
    while (it < MAXITER) {
        if (absc(z) > 2){
            float res = 2*float(it)/MAXITER;
            fragColor = vec4(res,res,res,1.0);
            return;
        }
        z = sumc(squarec(z), init_pos);
        it++;
    }
    fragColor = vec4(0,0,0,1.0);
    return;
}

void main() {
    // Normalize pixel coordinates (0..1)
    vec2 uv = gl_FragCoord.xy / iResolution;
    // Centered coordinates (-1..1)
    // vec2 p = (uv - 0.5) * 2.0;
    // normalize it again to be x (-2..1) y (-1.12 .. 1.12)
    float xmax = -0.713409425;
    float xmin = -0.748373388;
    float ymax = 0.222862401;
    float ymin = 0.196705151;
    
    float x = mix(xmin, xmax, uv.x);
    float y = mix(ymin, ymax, uv.y);
    vec2 p = vec2(x, y);
    
    // Simple animated color bands
    // float r = 0.5 + 0.5 * cos(6.28318 * (p.x * 0.5) + iTime * 0.7);
    // float g = 0.5 + 0.5 * cos(6.28318 * (p.y * 0.5) - iTime * 1.1);
    // float b = 0.5 + 0.5 * cos(6.28318 * ((p.x + p.y) * 0.25) + iTime * 0.3);

    calc_mandelbrot(p.x, p.y);

    // fragColor = vec4(r, g, b, 1.0);
}