# Heap buffer overflow in Webaudio FFTFrame::doFFT

| Field | Value |
|-------|-------|
| **Issue ID** | [40095939](https://issues.chromium.org/issues/40095939) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | cr...@google.com |
| **Created** | 2011-10-05 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

buffer overflow?

**VERSION**  

Chrome Version: stable + trunk  

Operating System: linux 64bit

**REPRODUCTION CASE**  

data:text/html,<script>new webkitAudioContext(1, 1, 22050)</script>

higher third parameter makes allocation larger.

first parameter can go up to 10, second parameter can go up to third parameter

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==6220== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffe4481c7f at pc 0x7ffff597d859 bp 0x7fffd8459370 sp 0x7fffd8459340  

READ of size 1 at 0x7fffe4481c7f thread T5  

#0 0x7ffff597d859 in WebCore::FFTFrame::doFFT(float\*) ???:0  

#1 0x7ffff59d711c in WebCore::HRTFKernel::HRTFKernel(WebCore::AudioChannel\*, unsigned long, double, bool) ???:0

0x7fffe4481c7f is located 1 bytes to the left of 512-byte region [0x7fffe4481c80,0x7fffe4481e80)  

allocated by thread T5 here:  

#0 0x7ffff5dfe8ba in malloc *asan\_rtl*  

#1 0x7ffff2045f4b in WTF::fastMalloc(unsigned long) ???:0  

#2 0x7ffff27c3073 in WebCore::AudioArray<float>::allocate(unsigned long) ???:0

--

Warning: set address range perms: large range [0x28585b908000, 0x28587b908000) (noaccess)  

Thread 6:  

Invalid read of size 8  

at 0x4D617AC: memcpy (mc\_replace\_strmem.c:635)  

by 0x29870FA: WebCore::FFTFrame::doFFT(float\*)  

by 0x29A73B6: WebCore::extractAverageGroupDelay(WebCore::AudioChannel\*, unsigned long)  

Address 0x11ceded8 is 40 bytes before a block of size 512 alloc'd  

at 0x4D5D49B: malloc (vg\_replace\_malloc.c:904)  

by 0x17894E9: WTF::fastMalloc(unsigned long)  

by 0x198A840: WebCore::AudioBus::AudioBus(unsigned int, unsigned long, bool)

Address 0xb963c674ba66f2bc is not stack'd, malloc'd or (recently) free'd  

Process terminating with default action of signal 11 (SIGSEGV)  

General Protection Fault  

at 0x4D616D0: memcpy (mc\_replace\_strmem.c:635)  

by 0x29870FA: WebCore::FFTFrame::doFFT(float\*)

## Attachments

- [audio-vg.txt](attachments/audio-vg.txt) (text/x-c; charset=us-ascii, 5.9 KB)
- [audio-asan.txt](attachments/audio-asan.txt) (text/plain; charset=us-ascii, 4.2 KB)
- [1left.html](attachments/1left.html) (text/plain; charset=us-ascii, 60 B)

## Timeline

### in...@chromium.org (2011-10-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-05)

@palmer: perhaps you could help Chris Rogers take a quick look? This is super similar to the area we did some work on (doFFT), I hope we didn't miss anything :)

### sc...@gmail.com (2011-10-05)

@palmer: perhaps you could help Chris Rogers take a quick look? This is super similar to the area we did some work on (doFFT), I hope we didn't miss anything :)

### in...@chromium.org (2011-10-05)

upstreamed - https://bugs.webkit.org/show_bug.cgi?id=69447

### in...@chromium.org (2011-10-05)

[Empty comment from Monorail migration]

### pa...@google.com (2011-10-05)

The problem was that low sample rates cause not enough FFT bytes to be allocated; other code assumes the sample rate is always at least 44100. The patch is simple and crogers will commit it soon.

### in...@chromium.org (2011-10-06)

http://trac.webkit.org/changeset/96843

### js...@chromium.org (2011-10-07)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-07)

[Empty comment from Monorail migration]

### mi...@gmail.com (2011-10-07)

hi,

the bug is still there for samplerates 48001 through 88199 (2x44100-1)

I believe the reason is, on line 432 in third_party/WebKit/Source/WebCore/platform/audio/AudioBus.cpp:

430    double sampleRateRatio = sourceSampleRate / destinationSampleRate;
431    int sourceLength = resamplerSourceBus->length();
432    int destinationLength = sourceLength / sampleRateRatio;

destinationLength is the truncated value of the division, and the other code will 
attempt to touch areas outside the end of the buffer.

for 48001 asan says:
0x7fe9ef49587f is located 1 bytes to the left of 1112-byte region [0x7fe9ef495880,0x7fe9ef495cd8)

for 88199 asan says:
0x7fe9ecf7587f is located 3 bytes to the right of 2044-byte region [0x7fe9ecf75080,0x7fe9ecf7587c)

changing it to:
432    int destinationLength = (sourceLength / sampleRateRatio) + 1;

removes the crash.

cheers,
miaubiz

crash:
data:text/html,<script>new webkitAudioContext(1, 1, 48001)</script>
data:text/html,<script>new webkitAudioContext(1, 1, 88199)</script>

nocrash:
data:text/html,<script>new webkitAudioContext(1, 1, 48000)</script>
data:text/html,<script>new webkitAudioContext(1, 1, 88200)</script>



### in...@chromium.org (2011-10-07)

reopening for analysis

### in...@chromium.org (2011-10-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-11)

[Empty comment from Monorail migration]

### cr...@google.com (2011-10-12)

Should be fixed in:
http://trac.webkit.org/changeset/97214

### cr...@google.com (2011-10-12)

[Empty comment from Monorail migration]

### cr...@google.com (2011-10-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-12)

Thanks Chris for merging. Wow, we might have missed this beta by 4 min. But there is one more.

http://trac.webkit.org/changeset/97217

### ka...@google.com (2011-10-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

Thanks for catching this. $1000

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### mi...@gmail.com (2011-10-20)

not to be a greedy bastard, but wasn't this two separate bugs, c#0 and c#10.


### in...@chromium.org (2011-10-20)

Miaubiz, you are right. These are two seperate bugs. Increasing reward.

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/99211?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095939)*
