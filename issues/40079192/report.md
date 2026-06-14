# ASSERTION FAILED: !webMediaPlayer(), Heap-use-after-free in blink::WebMediaPlayerClientImpl::load

| Field | Value |
|-------|-------|
| **Issue ID** | [40079192](https://issues.chromium.org/issues/40079192) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Audio |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ac...@chromium.org |
| **Created** | 2014-03-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest chrome asan build.

**REPRODUCTION CASE**  

Required movie file attached.

<script>
function start() {
o169=document.createElement('audio');
o169.setAttribute('src', 'mov\_bbb.ogg');
o169.load();
o266=document.createElement('track');
o169.appendChild(o266)
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in debug.txt

## Attachments

- [debug.txt](attachments/debug.txt) (text/plain, 13.4 KB)
- [mov_bbb.ogg](attachments/mov_bbb.ogg) (application/octet-stream, 600.1 KB)

## Timeline

### in...@chromium.org (2014-03-25)

Sheriff, please upload movie file with testcase. Sheriffbot will not create a testcase for this correctly (due to need of the movie file as attachment.

### in...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### jw...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-25)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6671035994734592.

- Your friendly ClusterFuzz

### ac...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### ac...@chromium.org (2014-03-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6671035994734592

Uploader: clusterfuzz@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61100005a300
Crash State:
  - crash stack -
  blink::WebMediaPlayerClientImpl::load
  WebCore::HTMLMediaElement::loadResource
  - free stack -
  content::WebMediaPlayerImpl::~WebMediaPlayerImpl
  content::WebMediaPlayerImpl::~WebMediaPlayerImpl
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=258508:258595

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97EkFyh-5xb-ZJ9kX_bGrCwqKTeRZzMYeQcw-FlbMTNZZ-FTc2Elh0VueloorxMouMVTehGheH7Zf8XoyVI4GYxZ9aviMm-BLp-bbeyEDCETJNdd83YJWYByxkhEJAyF8Z9clcjP8XlaGUQtFNw8Ph19_n0Ig



### ac...@chromium.org (2014-03-26)

Patch in the commit queue.(https://codereview.chromium.org/211373009/)

### bu...@chromium.org (2014-03-26)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=170003

------------------------------------------------------------------
r170003 | acolwell@chromium.org | 2014-03-26T02:14:41.234062Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/media/track/track-insert-after-load-crash-expected.txt?r1=170003&r2=170002&pathrev=170003
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/media/track/track-insert-after-load-crash.html?r1=170003&r2=170002&pathrev=170003
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLMediaElement.cpp?r1=170003&r2=170002&pathrev=170003

Fix a crash caused by track insertion after load().

This patch fixes a crash caused by stale LoadMediaResource flag in
m_pendingActionFlags when load() is explicitly called on a media
element. The insertion of a <track> element triggers the crash by
triggering the scheduling of the m_loadTimer, which ends up using the
stale flag data when the timer fires. The fix is to clear the
LoadMediaResource flag from m_pendingActionFlags when a new load is
initiated.

BUG=356352
TEST=LayoutTests/media/track/track-insert-after-load-crash.html

Review URL: https://codereview.chromium.org/211373009
-----------------------------------------------------------------

### in...@chromium.org (2014-03-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-27)

ClusterFuzz has detected this issue as fixed in range 259803:259825.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6671035994734592

Uploader: clusterfuzz@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61100005a300
Crash State:
  - crash stack -
  blink::WebMediaPlayerClientImpl::load
  WebCore::HTMLMediaElement::loadResource
  - free stack -
  content::WebMediaPlayerImpl::~WebMediaPlayerImpl
  content::WebMediaPlayerImpl::~WebMediaPlayerImpl
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=258508:258595
Fixed: https://cluster-fuzz.appspot.com/revisions?range=259803:259825

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97EkFyh-5xb-ZJ9kX_bGrCwqKTeRZzMYeQcw-FlbMTNZZ-FTc2Elh0VueloorxMouMVTehGheH7Zf8XoyVI4GYxZ9aviMm-BLp-bbeyEDCETJNdd83YJWYByxkhEJAyF8Z9clcjP8XlaGUQtFNw8Ph19_n0Ig

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-04-01)

Does this affect m34 ? i am suspecting CF regression range which says it is not.

### in...@chromium.org (2014-04-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-01)

This code looks old, assuming that it impacts stable. If not, we can remove Release-0-M34 label.

### ac...@chromium.org (2014-04-01)

Have you actually reproduced the issue in M34? This shouldn't have affected M34 since I'm pretty sure the regression was triggered by my changes in http://src.chromium.org/viewvc/blink?revision=169669&view=revision . I believe the code before that just silently dealt with this scenario. The assert was added by my change so it shouldn't have been firing before that.

### bu...@chromium.org (2014-04-01)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=170601

------------------------------------------------------------------
r170601 | inferno@chromium.org | 2014-04-01T21:11:22.101441Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/core/html/HTMLMediaElement.cpp?r1=170601&r2=170600&pathrev=170601
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/media/track/track-insert-after-load-crash-expected.txt?r1=170601&r2=170600&pathrev=170601
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/media/track/track-insert-after-load-crash.html?r1=170601&r2=170600&pathrev=170601

Merge 170003 "Fix a crash caused by track insertion after load()."

> Fix a crash caused by track insertion after load().
> 
> This patch fixes a crash caused by stale LoadMediaResource flag in
> m_pendingActionFlags when load() is explicitly called on a media
> element. The insertion of a <track> element triggers the crash by
> triggering the scheduling of the m_loadTimer, which ends up using the
> stale flag data when the timer fires. The fix is to clear the
> LoadMediaResource flag from m_pendingActionFlags when a new load is
> initiated.
> 
> BUG=356352
> TEST=LayoutTests/media/track/track-insert-after-load-crash.html
> 
> Review URL: https://codereview.chromium.org/211373009

TBR=acolwell@chromium.org

Review URL: https://codereview.chromium.org/218393020
-----------------------------------------------------------------

### in...@chromium.org (2014-04-01)

i didn't reproduce it in m34. but i just merged to m34. does it have any bad consequence or do we need to revert. otherwise, we can let it be in.

### ac...@chromium.org (2014-04-01)

I don't know what the impact of the change would be on M34. The fix was designed for ToT there have been quite a number of change to HTMLMediaElement since M34 branch cut. I think it would be safer to revert the merge.

### ti...@chromium.org (2014-04-04)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-13)

Congratulations - $1000 for this one.

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M34 label.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-05-27)

Speculatively setting Security-Impact after merging to appease clusterfuzz.

### cl...@chromium.org (2014-07-02)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

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

This issue was migrated from crbug.com/chromium/356352?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079192)*
