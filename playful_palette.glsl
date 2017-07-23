// Inspired by the SIGGRAPH 2017 paper by Maria (Masha) Shugrina, Jingwan Lu, and Stephen DiVerdi.
// https://www.youtube.com/watch?v=kapQfn7K0fQ&feature=share

#define NUM_BLOBS 3

// Define all colours and positions of the nuclei
vec4 colors[NUM_BLOBS] = vec4[](vec4(1.0, 0.0, 0.0, 1.0), vec4(0.0, 0.0, 1.0, 1.0), vec4(0.7, 0.5, 0.2, 1.0));
vec3 positions[NUM_BLOBS] = vec3[](vec3(100, 100, 50), vec3(200, 200, 50), vec3(150, 100, 30));

// Define background colour
vec4 backgroundcol = vec4(1.0, 1.0, 1.0, 1.0);

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
	vec2 uv = fragCoord.xy / iResolution.xy;
    fragColor = vec4(1.0, 1.0, 1.0 ,1.0);
    
    // Implement mouse behavior
    vec2 mouse = iMouse.xy;
    
    float mindist = 100000000.0;
    int minindex = -1;
    for(int i=0; i<NUM_BLOBS; i++)
    {
    	float dist = distance(positions[i].xy, mouse.xy);   
        if(dist<mindist)
        {
    		minindex = i;
        	mindist = dist;
        }
    }
    if(mouse.xy != vec2(0.0, 0.0))
        positions[minindex].xy = mouse.xy;
       
    // Metaball computation
    float contribution = 0.0;
    
    // Gradient computation
    vec4 weight_num = vec4(0.0, 0.0, 0.0, 1.0);
    float weight_denom = 0.0;
    
    for(int i=0; i<NUM_BLOBS; i++)
    {
       	// Calculate gradient based on distance from nuclei
        float dist = distance(positions[i].xy, fragCoord.xy);
        float fraction = positions[i].z/dist;
        float temp = 1.0/(dist*dist);
        weight_num += temp*colors[i];
        weight_denom += temp;
        
        contribution += fraction;
    }
    
    // Metaball computation
    if(contribution>1.0)
    	fragColor = weight_num/weight_denom;
    else
        // Antialiasing computation
        fragColor = mix(backgroundcol, weight_num/weight_denom, smoothstep(0.0,1.0, clamp(contribution-0.96, 0.0, 1.0)/0.04));
}
