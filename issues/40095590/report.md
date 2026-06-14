# OOB in SwiftShader textureSize

| Field | Value |
|-------|-------|
| **Issue ID** | [40095590](https://issues.chromium.org/issues/40095590) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ni...@google.com |
| **Created** | 2019-07-03 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. Put the js file and poc.html,crash.html into same dir and setup a webserver. 
2. Run ./chrome --disable-gpu crash.html

What is the expected behavior?

What went wrong?
About the problem:
SwiftShader does not check the lod value when handle glsl function textureSize().

in third_party/swiftshader/src/Shader/SamplerCore.cpp:502
Vector4f SamplerCore::textureSize(Pointer<Byte> &texture, Float4 &lod)  <---lod is not checked
	{
		Vector4f size;
		for(int i = 0; i < 4; ++i)
		{
			Int baseLevel = *Pointer<Int>(texture + OFFSET(Texture, baseLevel));
			Pointer<Byte> mipmap = texture + OFFSET(Texture, mipmap) + (As<Int>(Extract(lod, i)) + baseLevel) * sizeof(Mipmap);
			size.x = Insert(size.x, As<Float>(Int(*Pointer<Short>(mipmap + OFFSET(Mipmap, width)))), i);
			size.y = Insert(size.y, As<Float>(Int(*Pointer<Short>(mipmap + OFFSET(Mipmap, height)))), i);
			size.z = Insert(size.z, As<Float>(Int(*Pointer<Short>(mipmap + OFFSET(Mipmap, depth)))), i);
		}

		return size;<---size contains the any memory value which lod point at. 
	}
The jit code show that we can control the register R8 by change the lod value:

0x00003ea27a15f85d:	mov    r8d,DWORD PTR [rax+rdx*1+0xcc4]
0x00003ea27a15f865:	movss  xmm3,xmm1
0x00003ea27a15f869:	movd   r9d,xmm3
0x00003ea27a15f86e:	add    r8d,r9d
0x00003ea27a15f871:	lea    r8,[r8+r8*2]
0x00003ea27a15f875:	shl    r8,0x6
0x00003ea27a15f879:	movsxd r8,r8d
0x00003ea27a15f87c:	movups xmm3,XMMWORD PTR [rsp+0x120]
=> 0x00003ea27a15f884:	movsx  r9,WORD PTR [rcx+r8*1+0x78] <-----handled lod value
0x00003ea27a15f88a:	movd   xmm4,r9d
0x00003ea27a15f88f:	insertps xmm3,xmm4,0x0

So we can call textureSize and pass into a choosen value to the lod to arbitrarily read.

About the exploit:
There is a problem that how can we get the memory value. 
To feed the memory value back, we can call textureSize in vertex shader and judge the value in every bit in a big swich loop(like guess every bit of a decimal number by dividing by 10).The next is making the return value as a color value by posting it to pixel shader, then draw it on the gl texture.Finally we can 
get it by reading the pixel.The poc.html is just a demo to demonstrate that we can read the value back.The real exploit maybe need a more complete color-based shader debugger.

To watch the crash, run crash.html.The crash log:

Received signal 11 SEGV_ACCERR 633072ea5f18
#0 0x555a5c84a32b (/home/lly/chrome/src/out/asan/chrome+0x8a8b32a)
#1 0x555a67b0f1e4 (/home/lly/chrome/src/out/asan/chrome+0x13d501e3)
#2 0x555a67859582 (/home/lly/chrome/src/out/asan/chrome+0x13a9a581)
#3 0x555a67b0dcb0 (/home/lly/chrome/src/out/asan/chrome+0x13d4ecaf)
#4 0x7fa612fae390 (/lib/x86_64-linux-gnu/libpthread-2.23.so+0x1138f)
#5 0x62a00001f1f0 <unknown>
  r8: 0000000000000000  r9: 00007fa5f1c64020 r10: 0000000000000000 r11: 0000000000000206
 r12: 00007fa5fc579c08 r13: 0000000000000000 r14: 0000000000000001 r15: 0000000000000000
  di: 00007fa5f523d810  si: 00007fa5f1c64020  bp: 00007fa5f2a639b0  bx: 00007fa5f2a638e0
  dx: 0000000000989680  ax: 000063300078c810  cx: 000000007270e000  sp: 00007fa5f2a63810
  ip: 000062a00001f1f0 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000633072ea5f18
[end of stack trace]
Calling _exit(1). Core file will not be generated

Did this work before? N/A 

Chrome version: 77.0.3833.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.1 KB)
- [utility.js](attachments/utility.js) (text/plain, 2.0 KB)
- [webgl-utils.js](attachments/webgl-utils.js) (text/plain, 10.0 KB)
- [crash.html](attachments/crash.html) (text/plain, 1.1 KB)

## Timeline

### cd...@gmail.com (2019-07-03)

It can be reached from chromium directly, does that mean it also affect the ANGLE?

### li...@chromium.org (2019-07-03)

Basing severity on this being an OOB read. nicolascapens, would you be able to help take a look? Feel free to re-assign if you're not the best person to own this--thanks!

[Monorail components: Internals>GPU>SwiftShader]

### ni...@google.com (2019-07-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-04)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-04)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader.git/+/1d4f5775ee060ce5c7471261dbf701b36b3180af

commit 1d4f5775ee060ce5c7471261dbf701b36b3180af
Author: Nicolas Capens <capn@google.com>
Date: Thu Jul 04 18:51:27 2019

Clamp GLSL textureSize() lod to mipmap range

https://crbug.com/chromium/980816

Change-Id: Ic4393668f82316e475baa5e753d891dfb1e30572
Reviewed-on: https://swiftshader-review.googlesource.com/c/SwiftShader/+/33728
Presubmit-Ready: Nicolas Capens <nicolascapens@google.com>
Kokoro-Presubmit: kokoro <noreply+kokoro@google.com>
Tested-by: Nicolas Capens <nicolascapens@google.com>
Reviewed-by: Alexis Hétu <sugoi@google.com>

[modify] https://swiftshader.googlesource.com/SwiftShader.git/+/1d4f5775ee060ce5c7471261dbf701b36b3180af/src/Shader/SamplerCore.cpp


### ni...@google.com (2019-07-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-05)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-15)

Requesting merge to beta M76 even though there is no obvious Chromium repository trunk commit here. Perhaps it was fixed in another ticket; please investigate.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-15)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@google.com (2019-07-15)

I don't think this requires a merge. The lod value is multiplied by sizeof(Mipmap), which is very large, before dereferencing. So only a sparse amount of memory can be accessed, and it will likely lead to crashing the GPU process before anything interesting is found. Also note that the GPU process is generally untrusted.

### ab...@google.com (2019-07-15)

Per #11, rejecting merge to M76

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $2,000 for this high quality report!

### cd...@gmail.com (2019-07-18)

Thanks for the reward, Cheers!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### cd...@gmail.com (2019-07-30)

Hi  natashapabrai@,
Will this one be assigned a CVE number?

### ad...@google.com (2019-09-06)

Assuming this affects all standard platforms so adding OS labels.

cdsrc2016@ - yes.

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/980816?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095590)*
