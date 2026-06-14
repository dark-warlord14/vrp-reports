# WebM crash in vp8_setup_intra_recon()

| Field | Value |
|-------|-------|
| **Issue ID** | [40084020](https://issues.chromium.org/issues/40084020) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Media |
| **CVE IDs** | CVE-2010-4203 |
| **Reporter** | sc...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2010-10-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached files will cause a memory access error when loaded as a WebM video.  

Credit: Timothy B. Terriberry

**VERSION**  

Chrome Version: [7.0.517.41] + [stable]  

Operating System: [Linux, Ubuntu 9.04 32-bit]

**REPRODUCTION CASE**  

.webm file attached  

It sad-tabs Chrome

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

gdb $ mozdbg  

--[ REGISTERS ]  

rax: 0x7f7f7f7f rbx: 0x12dcf4000 rcx: 0xffffffffffffffff  

rdx: 0x6 rsi: 0x7f7f0000 rdi: 0x300000000  

rbp: 0x12dcf3860 rsp: 0x12dcf3838 rip: 0x7fff863d346e

--[ FAULTING INSTRUCTION ]  

0x7fff863d346e <memset+58>: mov BYTE PTR [rdi],al

--[ FRAME ]  

#0 0x00007fff863d346e in memset ()  

#1 0x0000000101632f2d in \_\_inline\_memset\_chk (\_\_dest=0x300000000, \_\_val=127, \_\_len=6) at \_string.h:80  

#2 0x0000000101632c38 in vp8\_setup\_intra\_recon (ybf=0x11b7ee9e0) at /Users/cdiehl/Mozilla/trunk/media/libvpx/vp8/common/setupintrarecon.c:20  

#3 0x0000000101639957 in vp8\_decode\_frame (pbi=0x11b7ea220) at /Users/cdiehl/Mozilla/trunk/media/libvpx/vp8/decoder/decodframe.c:829  

#4 0x000000010164196b in vp8dx\_receive\_compressed\_data (ptr=0x11b7ea220, size=29, source=0x13924b800 "1\003", time\_stamp=0) at /Users/cdiehl/Mozilla/trunk/media/libvpx/vp8/decoder/onyxd\_if.c:346  

#5 0x0000000101647851 in vp8\_decode (ctx=0x13670c800, data=0x13924b800 "1\003", data\_sz=29, user\_priv=0x0, deadline=0) at /Users/cdiehl/Mozilla/trunk/media/libvpx/vp8/vp8\_dx\_iface.c:424  

#6 0x00000001016495ec in vpx\_codec\_decode (ctx=0x13dfc4398, data=0x13924b800 "1\003", data\_sz=29, user\_priv=0x0, deadline=0) at /Users/cdiehl/Mozilla/trunk/media/libvpx/vpx/src/vpx\_decoder.c:127

## Attachments

- [7.webm](attachments/7.webm) (application/octet-stream; charset=binary, 100.8 KB)

## Timeline

### sc...@gmail.com (2010-10-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-10-21)

Andrew -- once John has blessed the libvpx patch that fixes this, we need to get it checked in and merged to M7 and M8 ASAP.
We need the fix to hit the M7 refresh patch which is due in under a couple of weeks.

Mozilla is fixing this in their next 4.0 Beta, which could be out in a couple of days. We need to not be too far after.

### sc...@gmail.com (2010-10-21)

John -- if you could share the URL to the WebM changeset once it has been committed, that would be awesome!

### fb...@chromium.org (2010-10-22)

Is this bug already fixed in Chrome 8?

### sc...@gmail.com (2010-10-22)

Frank -- I was hoping you could tell us that :) Do you still maintain the ffmpeg part of Media?

### jk...@google.com (2010-10-22)

This patch was change 928 on review.webmproject.org[1].

I applied this change on top of what chromium is currently using (v0.9.2-35-ga8a38bc)[2] so that if you checkout v0.9.2-36-g09bcc1f you will get ONLY this patch on top of what you've currently tested. It will also be included in our Aylesbury release (next week).

[1]: https://review.webmproject.org/#change,928
[2]: http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/libvpx/README.chromium?revision=60399&view=markup

### fb...@chromium.org (2010-10-22)

@scarybeasts I reproduced it in chromium 8 for Windows 7.
For some reason its not fatal in media_bench
media_bench --stream=video 7.webm
* Stream #0: libvpx (libvpx VP8)
  Stream #1: vorbis (Vorbis)
Error: avcodec_decode returned -22 for 7.webm
Yes, I still maintain ffmpeg which statically links libvpx.


### sc...@chromium.org (2010-10-22)

Alright this will be a bit tricky to fix since our latest FFmpeg configuration contains WAV which we *do not* want to bring into Mstone-7

We've never had to do this in the past but it looks like we'll have to make a branch ffmpeg and libvpx for for the 517 sources, update the buildspec to point at that, then merge in the change there

talking with TPM people right now for best place to store this stuff

### sc...@gmail.com (2010-10-22)

@fbarchard: we need this fix committed to trunk and merged to M7 and M8. Is that something you can help with? We have a bit of a deadline going because this is a security bug.

### sc...@gmail.com (2010-10-22)

Thanks for taking care of the merging, Andrew.

### fb...@chromium.org (2010-10-22)

[Comment Deleted]

### fb...@chromium.org (2010-10-22)

I'd suggest we check in 2 CL's for ffmpeg chrome trunk
chrome7 binaries
chrome8 binaries
We can do the same for chromium if you also want binaries for chromium


### fb...@chromium.org (2010-10-22)

Confirmed the fix.  7.webm comes up as green (uninitialized) with the patch

### fb...@chromium.org (2010-10-22)

chrome7 ffmpeg binaries
\\filer\home\fbarchard\dll\chrome7

chrome8 ffmpeg binaries
\\filer\home\fbarchard\dll\chrome


### fb...@chromium.org (2010-10-23)

Waiting on andrew for new checkin procedure.
Normally at this point I'd check into trunk, roll, test it, then roll into branches.
In the mean time, the other configurations... chromium7 chromium are built and testing.
Will just put them in \\filer\home\fbarchard\dll\ for now.

### sc...@gmail.com (2010-10-23)

will the other platforms (Mac, Linux, Chrome OS) be taken care of? Talk of "binaries" makes me nervous.

### sc...@chromium.org (2010-10-23)

Done and testing a local build of 517 and 552 right now.

Sources + libraries have been merged in and linux/mac will auto-build and I've also checked in frank's windows binaries for 517 and 552.

Writing a post mortem.

### sc...@chromium.org (2010-10-23)

Doesn't crash on 517 linux.

### sc...@chromium.org (2010-10-23)

OK should be fixed now for all platforms.  Will keep testing.

### in...@chromium.org (2010-10-23)

Thanks a lot Andrew for helping in making video more secure. 

### sc...@gmail.com (2010-10-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-04)

[Empty comment from Monorail migration]

### g....@gmail.com (2010-11-06)

Is there a CVE allocated for this issue?

Cheers,
Giuseppe.

### fb...@chromium.org (2010-11-16)

http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2010-4203

### sc...@gmail.com (2010-12-02)

Eventually traced lineage of this discovery to Christoph Diehl; payment to him is now in the electronic system.

### sc...@gmail.com (2011-01-06)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/60055?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084020)*
