# Security: Integer overflow allocating shared memory in AudioInputRendererHost::OnCreateStream

| Field | Value |
|-------|-------|
| **Issue ID** | [40079268](https://issues.chromium.org/issues/40079268) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Audio |
| **Reporter** | aa...@gmail.com |
| **Assignee** | wj...@chromium.org |
| **Created** | 2014-04-03 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

I believe a potential buffer write overflow may occur in the browser process due to an integer overflow condition when allocating shared memory in AudioInputRendererHost::OnCreateStream.

The shared memory in 'entry->shared\_memory' is allocated with size 'segment\_size \* entry->shared\_memory\_segment\_count' bytes. The variables used in this multiplication are both 32 bit integers that are individually calculated from values provided by the renderer in an AudioInputHostMsg\_CreateStream\_Config message. On a multiplication integer overflow, the size of the shared memory allocation may be less than expected by AudioInputSyncWriter::Write, possibly even less than the segment size. As a result, when AudioInputSyncWriter::Write attempts to write a segment to the shared memory buffer a write overflow may occur.

As a demonstration, I have written a patch simulating a compromised renderer process sending cooked values in an AudioInputHostMsg\_CreateStream\_Config message. The result is a 'segment\_size' of 131074, a 'entry->shared\_memory\_segment\_count' of 32768, and a shared memory allocation of 65536. This results in a write of 131058 bytes in AudioInputSyncWriter::Write at an offset from the base address of the 65536 byte shared memory region, which is a write overflow. The source patch and asan output from a test run are attached.

The bytes written to the overflow memory region will generally come from audio samples. I believe an attacker might exercise some control over the content of these bytes by manipulating audio recording parameters and the offset of the memory location for the overflow so that any predictable values in the audio samples might be written to a desired location. A somewhat more remote possibility is that an attacker might attempt to exercise some measure of control over the content of the audio samples by playing specific tones from the computer speaker while the recording is taking place. Note that I have not experimentally checked the feasibility of either of these methods.

**VERSION**  

Chrome Version:  

git source hash 0760c783b421753c2bbeba410d9051c37f728f61  

with the attached patch applied for descriptive logging and to simulate a compromised renderer process  

64 bit asan release build  

Operating System:  

OS X 10.9.1 (13B42)  

Note that I believe this issue may be present on other operating systems, and in 32 bit compilations as well.

**REPRODUCTION CASE**  

The attached patch was applied to git source hash 0760c783b421753c2bbeba410d9051c37f728f61 and compiled into a 64 bit asan release binary.  

The provided audio.html file was served from localhost port 8000 using python -m SimpleHTTPServer.  

Chrome was started as follows:  

out/Release/Chromium.app/Contents/MacOS/Chromium <http://localhost:8000/audio.html> &> out.log  

After chrome was started, "Allow" was clicked to permit use of the microphone by the audio.html page.  

After this, the asan chrome build terminated with the heap buffer overflow reported in the attached asan log.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 9.1 KB)
- [audio.html](attachments/audio.html) (text/html, 127 B)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 3.1 KB)
- [run1.patch](attachments/run1.patch) (application/octet-stream, 4.3 KB)
- [run2.patch](attachments/run2.patch) (application/octet-stream, 4.1 KB)

## Timeline

### js...@chromium.org (2014-04-03)

@wjia - This calculation should be using the CheckedNumeric template from base/numerics.

### aa...@gmail.com (2014-04-03)

I also wanted to add that, while in my demonstration the bytes written to the overflow region are audio samples, there is additionally some metadata written to the media::AudioInputBuffer, via the 'params' attribute, in AudioInputSyncWriter::Write.  The contents of this metadata might potentially be easier for an attacker to control than the contents of the audio samples.  If it makes a significant difference I could potentially attempt to write a demo where this metadata is written to an overflow region.

### mb...@chromium.org (2014-04-03)

It looks like this was introduced in r161328, so it should impact beta and stable.

### in...@chromium.org (2014-04-03)

[Empty comment from Monorail migration]

### [Deleted User] (2014-04-03)


+ Dale.

We pass important audio parameters from content via IPC msg to the browser to setup things correct, it will be a design problem if it is possible for the hackers to manipulating the audio parameters.

Can we involve anyone who knows IPC security?

### in...@chromium.org (2014-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-03)

[Empty comment from Monorail migration]

### da...@chromium.org (2014-04-03)

You can't trust anything coming in via IPC message.  It must be sanitized.

### wj...@chromium.org (2014-04-03)

https://codereview.chromium.org/214343006/ has been uploaded for review.

### bu...@chromium.org (2014-04-03)

------------------------------------------------------------------
r261549 | wjia@chromium.org | 2014-04-03T22:23:45.484349Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/media/audio_input_renderer_host.cc?r1=261549&r2=261548&pathrev=261549

Check shared memory size before allocating it.

This will prevent overflow from multiplication.

BUG=359454

Review URL: https://codereview.chromium.org/214343006
-----------------------------------------------------------------

### in...@chromium.org (2014-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-03)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-05)

Aaron, how would you like to credited in the release notes.

### aa...@gmail.com (2014-04-05)

You can just use my name: Aaron Staple
Thanks!

### ti...@chromium.org (2014-04-17)

Merge-Approved for M34 (via dxie@).

Merge-Requested for M35.

### in...@chromium.org (2014-04-17)

merged to r34 in r264647

### bu...@chromium.org (2014-04-17)

------------------------------------------------------------------
r264647 | inferno@chromium.org | 2014-04-17T21:35:48.300246Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/browser/renderer_host/media/audio_input_renderer_host.cc?r1=264647&r2=264646&pathrev=264647

Merge 261549 "Check shared memory size before allocating it."

> Check shared memory size before allocating it.
> 
> This will prevent overflow from multiplication.
> 
> BUG=359454
> 
> Review URL: https://codereview.chromium.org/214343006

TBR=wjia@chromium.org

Review URL: https://codereview.chromium.org/241503004
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-17)

Merge-Requested for M35.


### bu...@chromium.org (2014-04-18)

------------------------------------------------------------------
r264795 | laforge@chromium.org | 2014-04-18T15:39:10.975944Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/browser/renderer_host/media/audio_input_renderer_host.cc?r1=264795&r2=264794&pathrev=264795

Revert 264647
> Merge 261549 "Check shared memory size before allocating it."
> 
> > Check shared memory size before allocating it.
> > 
> > This will prevent overflow from multiplication.
> > 
> > BUG=359454
> > 
> > Review URL: https://codereview.chromium.org/214343006
> 
> TBR=wjia@chromium.org
> 
> Review URL: https://codereview.chromium.org/241503004

TBR=inferno@chromium.org
Review URL: https://codereview.chromium.org/243263002
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-18)

Removing merge and release labels. CheckedNumeric did not make the cut into M34 but did make M35 (see https://crbug.com/chromium/364703), hence the revert.

Spoke with jschuh@ and this can wait for M35.

### ka...@google.com (2014-04-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-21)

------------------------------------------------------------------
r265054 | wjia@chromium.org | 2014-04-21T20:22:14.412725Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/content/browser/renderer_host/media/audio_input_renderer_host.cc?r1=265054&r2=265053&pathrev=265054

Merge 261549 "Check shared memory size before allocating it."

> Check shared memory size before allocating it.
> 
> This will prevent overflow from multiplication.
> 
> BUG=359454
> 
> Review URL: https://codereview.chromium.org/214343006

TBR=wjia@chromium.org

Review URL: https://codereview.chromium.org/245753002
-----------------------------------------------------------------

### aa...@gmail.com (2014-04-23)

I spent a little bit of time investigating the potential exploitability of this issue, via two separate methods.  (Note the following examples use 32 bit non asan builds on osx).

The fist method was to write a null byte sequence of arbitrary length to a memory region mapped to the right of the audio sample shared memory region.  I carefully chose values sent by the renderer in an AudioInputHostMsg_CreateStream message so that the browser would write 0xbeef bytes from audio samples into the memory region to the right of the shared memory region.  And I added an AudioInputHostMsg_SetVolume message to set the volume to zero, causing all audio data to contain only null bytes.  The memory mapping for this run was:

mapped file            11025000-11047000 [  136K] rw-/rwx SM=ALI  /private/var/folders/zz/zyxvpxvq6csfxvn_n0000000000000/T/.org.chromium.Chromium.lWEajg
MALLOC_LARGE           11047000-11075000 [  184K] rw-/rwx SM=PRV  DefaultMallocZone_0x86c4000

The log is:

segment_size: 188143
entry->shared_memory_segment_count: 251111
segment_size * entry->shared_memory_segment_count: 136617
entry->shared_memory address: 11025000
[New Thread 0x190f of process 53500]
[New Thread 0x3a03 of process 53500]
[New Thread 0x3b03 of process 53500]
[New Thread 0x3c03 of process 53500]

Program received signal SIGTRAP, Trace/breakpoint trap.
[Switching to Thread 0x190f of process 53500]
0x02e37ab9 in ?? ()
(gdb) c
Continuing.
writing zeroes from 0x11025010 to 0x11052eef

Since 0x11052eef - 0x11047000 == 0xbeef, 0xbeef null bytes were written to the MALLOC_LARGE region.

The patch used to generate this run is run1.patch

The second method was an attempt to write arbitrary content to the first word following the audio sample shared memory region, using specially formulated metadata for the ‘params’ attribute of an AudioInputBuffer.  My strategy was to use the two most significant bytes of params.volume and the two least significant bytes of params.size to form a word of configurable content.  Each of the attributes volume and size may be set via ipc form the renderer, but each may be restricted to a specific set of values (at least in this exploit scenario).  Combining bytes from the two attributes results in a larger (though still restricted) set of possible values.

In my test I attempted to write the value 0xbff13fed to the word following the shared memory region.  I tried to do this by overflowing the shared memory size calculation to result in a mapped size equal to shared_memory_segment_count_.  As a result the shared_memory_segment_size_ in AudioInputSyncWriter is calculated as 1, and this causes AudioInputSyncWriter::Write to increase the memory offset it writes to by one byte each time it is called.  So if the shared memory is at address 0x11351000, AudioInputSyncWriter::Write will write an AudioInputParameters followed by many bytes of audio data starting at address 0x11351000.  Then on the next call AudioInputSyncWriter::Write will write an AudioInputParameters followed by many bytes of audio data starting at address 0x11351001, etc, up until address 0x11351000 + mapped_size - 1.  On each such write, the seventh through tenth bytes of the AudioInputParameters comprise the word 0xbff13fed.  Here is the memory mapping for my experimental run:

Here was the memory layout of my test run, showing a MALLOC_LARGE region following the shared memory region:
mapped file            11351000-11391000 [  256K] rw-/rwx SM=ALI  /private/var/folders/zz/zyxvpxvq6csfxvn_n0000000000000/T/.org.chromium.Chromium.XRWYf0
MALLOC_LARGE           11391000-113b8000 [  156K] rw-/rwx SM=PRV  DefaultMallocZone_0x86c4000

Here is an abridged log from my run:

segment_size: 49153
entry->shared_memory_segment_count: 262144
segment_size * entry->shared_memory_segment_count: 262144
entry->shared_memory address: 11351000
set 0x11351006 to 0xbff13fed
set 0x11351007 to 0xbff13fed
set 0x11351008 to 0xbff13fed
set 0x11351009 to 0xbff13fed
set 0x1135100a to 0xbff13fed
set 0x1135100b to 0xbff13fed
…
set 0x11390df3 to 0xbff13fed
set 0x11390df4 to 0xbff13fed
set 0x11390df5 to 0xbff13fed
set 0x11390df6 to 0xbff13fed
set 0x11390df7 to 0xbff13fed

Program received signal SIGBUS, Bus error.
0x11341bb4 in ?? ()
(gdb)

Unfortunately this attempt failed with a SIGBUS before writing 0xbff13fed to my target address 0x11391000.  I believe the sigbus occurred because the MALLOC_LARGE region became corrupted with audio sample data.  Other types of target memory regions may be less susceptible than a heap region to crashing due to corrupt values. However, because of the long runtime of an exploit with a long sequence of AudioInputSyncWriter::Write calls (over a day for this example) I am not planning to investigate further.

The patch used to generate this run is run2.patch.

### ti...@chromium.org (2014-05-12)

+inferno@, jschuh@ for c#24

### ti...@chromium.org (2014-05-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-11)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/359454?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079268)*
