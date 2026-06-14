# Memory corruption with bad Vorbis streams (from CERT)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086501](https://issues.chromium.org/issues/40086501) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-12-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

CERT sent us a large number of WEBM files that cause trouble / crash / etc. Chrome. The worst of the problem seems to be a couple of memory corruptions in the ffmpeg Vorbis codec.  

This bug will track the problems in the Vorbis codec. Additional bugs will be filed for any remaining issues.

**VERSION**  

Chrome Version: all -- including trunk, M8 stable, M9 beta, etc.  

Operating System: All; I can reproduce various crashes on Linux.

**REPRODUCTION CASE**  

Attaching two test cases for the two different fixes I have that apply to the Vorbis code.

out.webm.68798.1929 - memory corruption rendering the channel floor buffer  

out.webm.139771.2965 - memory corruption rendering the channel residue buffer

## Attachments

- [out.webm.139771.2965](attachments/out.webm.139771.2965) (application/octet-stream; charset=binary, 578.1 KB)
- [out.webm.68798.1929](attachments/out.webm.68798.1929) (application/octet-stream; charset=binary, 578.1 KB)

## Timeline

### bu...@chromium.org (2010-12-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70202

------------------------------------------------------------------------
r70202 | cevans@chromium.org | Mon Dec 27 15:40:24 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=70202&r2=70201&pathrev=70202

Pick up Vorbis fix.

BUG=68115
TEST=See bug

Review URL: http://codereview.chromium.org/6069005
------------------------------------------------------------------------

### sc...@gmail.com (2010-12-27)

Fixed in the ffmpeg trunks/deps (r70200) and DEPS rolled on trunk (r70202)

### sc...@gmail.com (2010-12-29)

[Empty comment from Monorail migration]

### ch...@gmail.com (2011-01-04)

scarybeasts@ are you planning to merge this to m8?

### sc...@gmail.com (2011-01-04)

This merge is complicated. It needs a source code merge + maybe DEPS fiddle (for Linux / Mac). For Windows, it needs Frank to do a custom ffmpeg binary build and check that in.

### bu...@chromium.org (2011-01-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70412

------------------------------------------------------------------------
r70412 | fbarchard@chromium.org | Tue Jan 04 01:52:27 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/tools/media_bench/media_bench.cc?r1=70412&r2=70411&pathrev=70412

check for codec null pointer when printing error message
BUG=68115
TEST=media_bench.exe --verbose=48 --stream=audio out.webm.68798.1929 should print Error: Could not open codec (NULL) for c:\work\out.webm.68798.1929

Review URL: http://codereview.chromium.org/6044008
------------------------------------------------------------------------

### sc...@chromium.org (2011-01-06)

mini-update: ffmpeg branches have been created but we're holding off until next week

### sc...@chromium.org (2011-01-06)

merged into m8:
http://src.chromium.org/viewvc/chrome?view=rev&revision=70585

needs windows binaries

m9 will get merged next week

### sc...@gmail.com (2011-01-06)

@scherkus: awesome!! I build on Linux with a sync to latest on the buildspec: svn://chrome-svn/chrome-internal/trunk/tools/buildspec/branches/552

Confirmed that the new vorbis_dec.c file was picked up, and the two test case files no longer cause sad tabs in the resultant Release build.


### dw...@cert.org (2011-01-06)

When Windows binaries are available, I will rerun my ffmpeg relevant test cases (including hopefully redundant ones) to confirm.

### bu...@chromium.org (2011-01-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70625

------------------------------------------------------------------------
r70625 | scherkus@chromium.org | Thu Jan 06 10:48:49 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/552/binaries/win/avformat-52.dll?r1=70625&r2=70624&pathrev=70625
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/552/binaries/win/avutil-50.dll?r1=70625&r2=70624&pathrev=70625
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/552/binaries/win/avcodec-52.dll?r1=70625&r2=70624&pathrev=70625

Checking in updated Chromium FFmpeg Windows DLLs for 552 as a result of r70585.

BUG=68115
TEST=files in bug report don't crash

------------------------------------------------------------------------

### sc...@chromium.org (2011-01-06)

Windows binaries committed for Chromium m8 as r70625

### bu...@chromium.org (2011-01-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70632

------------------------------------------------------------------------
r70632 | scherkus@chromium.org | Thu Jan 06 12:06:30 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avformat-52.dll?r1=70632&r2=70631&pathrev=70632
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avcodec-52.dll?r1=70632&r2=70631&pathrev=70632
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avutil-50.dll?r1=70632&r2=70631&pathrev=70632

Checking in updated Chromium FFmpeg binaries due to r70200.

BUG=68115
TEST=bug report files don't crash
TBR=cevans
Review URL: http://codereview.chromium.org/6130002
------------------------------------------------------------------------

### sc...@chromium.org (2011-01-06)

Chromium m10 binaries committed as r70632

Will update DEPS as soon as everything looks good to go!
http://codereview.chromium.org/6059011/

### bu...@chromium.org (2011-01-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70664

------------------------------------------------------------------------
r70664 | scherkus@chromium.org | Thu Jan 06 14:13:42 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avformat-52.dll?r1=70664&r2=70663&pathrev=70664
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avcodec-52.dll?r1=70664&r2=70663&pathrev=70664
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avutil-50.dll?r1=70664&r2=70663&pathrev=70664

Another attempt at updated Chromium FFmpeg binaries due to r70200.

This time they include the libvpx encoder for remoting.

BUG=68115
TEST=bug report files don't crash
TBR=cevans

------------------------------------------------------------------------

### bu...@chromium.org (2011-01-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70684

------------------------------------------------------------------------
r70684 | scherkus@chromium.org | Thu Jan 06 15:44:19 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=70684&r2=70683&pathrev=70684

Rolling FFmpeg DEPS to 70632 to pick up new binaries.

BUG=68115
TEST=files in bug report don't crash

Review URL: http://codereview.chromium.org/6059011
------------------------------------------------------------------------

### sc...@chromium.org (2011-01-07)

Alright I think we're done with M8, M9 and M10!!

### bu...@chromium.org (2011-01-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70709

------------------------------------------------------------------------
r70709 | scherkus@chromium.org | Thu Jan 06 18:27:16 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/597/binaries/win/avformat-52.dll?r1=70709&r2=70708&pathrev=70709
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/597/binaries/win/avutil-50.dll?r1=70709&r2=70708&pathrev=70709
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/597/binaries/win/avcodec-52.dll?r1=70709&r2=70708&pathrev=70709

Checking in updated Chromium FFmpeg Windows DLLs for 597 as a result of r70707.

BUG=68115
TEST=files in bug report don't crash

------------------------------------------------------------------------

### sc...@chromium.org (2011-01-07)

I think we're good to update the status on this one -- pass off to QA for verification?

### sc...@gmail.com (2011-01-07)

Has the ffmpeg source code change also been merged to M9? If so, we can put the bug to FixUnreleased.

### sc...@gmail.com (2011-01-07)

The ffmpeg source change didn't make it to M9 branch yet. I'll take care of that for you when the branch re-opens.

### sc...@gmail.com (2011-01-07)

The rewards panel discussed this case, and the reward came out at 2 x $500 -- two relatively distinct Vorbis bugs, rewarded each at the lower $500 level due to the large number of duplicates, etc.

In instances where an individual is unable to accept the reward or nominate a charity, the reward money will go to our default charity of Red Cross.

### sc...@gmail.com (2011-01-08)

ffmpeg source change already merged to M9 by Andrew.

### sc...@gmail.com (2011-01-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-24)

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

### bu...@chromium.org (2013-03-11)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/68115?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/67777]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086501)*
