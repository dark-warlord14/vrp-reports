# Cookies with SameSite=Strict; are sent for link rel="prerender" when requested from 3rd party site

| Field | Value |
|-------|-------|
| **Issue ID** | [40090228](https://issues.chromium.org/issues/40090228) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Cookies |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | is...@gmail.com |
| **Assignee** | ry...@chromium.org |
| **Created** | 2018-01-18 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36

Steps to reproduce the problem:
1. Start a webserver (say localhost:8080) issuing a SameSite=Strict; cookie for a domain. (See server code, in which case you browse to http://localhost:8080/set/strict)
2. Open a site that has <link rel="prerender" href="http://localhost:8080/link-prerender?with-args=123&arg2=456" />
3. Note that server recieves the SameSite cookie regardless if Strict is set

For #1 my server looks like (samesite.go):

package main

import (
	"net/http"
	"time"
        "encoding/csv"
	"log"
	"os"
	"sync"

	"github.com/gin-gonic/gin"
)

// CookieLogger logs the cookies to a csv file called cookeis.csv:

func CookieLogger() gin.HandlerFunc {
	f, err := os.Create("cookies.csv")
	if err != nil {
		log.Fatalf("error opening cookies.csv: %s\n", err)
	}

	w := csv.NewWriter(f)
	if err := w.Write([]string{"ip", "url", "ref", "cookie_name", "cookie_value"}); err != nil {
		log.Fatalf("error writing csv header %s\n", err)
	}

	var lock sync.RWMutex
	return func(c *gin.Context) {
		cookies := c.Request.Cookies()
		lock.Lock()
		w.Write([]string{c.Request.RemoteAddr, c.Request.RequestURI, c.Request.Referer(), "", ""})
		if cookies != nil && len(cookies) > 0 {
			for _, cookie := range cookies {
				w.Write([]string{c.Request.RemoteAddr, c.Request.RequestURI, c.Request.Referer(), cookie.Name, cookie.Value})
				w.Flush()
			}
		}
		lock.Unlock()
		c.Next()
	}
}

func main() {
	r := gin.Default()
	r.Use(CookieLogger())
	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "top.tmpl", gin.H{})
	})

	r.GET("/set/strict", func(c *gin.Context) {
		c.Header("Set-Cookie", "SS_STRICT=5678; Path=/; SameSite=Strict;")
		c.String(200, "OK")
	})

	r.GET("/set/lax", func(c *gin.Context) {
		c.Header("Set-Cookie", "SS_LAX=1234; Path=/; SameSite=Lax;")
		c.String(200, "OK")
	})

	r.GET("/set/none", func(c *gin.Context) {
		c.Header("Set-Cookie", "NO_SS=1234; Path=/;")
		c.String(200, "OK")
	})

	r.GET("/get/:test", func(c *gin.Context) {
		test := c.Param("test")
		c.String(http.StatusOK, "OK %s", test)
	})

	r.Run() // listen and serve on 0.0.0.0:8080
}

For #2 use: https://jsfiddle.net/3pcnmeuk/

For #3: output:
[::1]:59182,/link-prerender?with-args=123&arg2=456,,NO_SS,1234
[::1]:59182,/link-prerender?with-args=123&arg2=456,,SS_LAX,1234
[::1]:59182,/link-prerender?with-args=123&arg2=456,,SS_STRICT,5678

What is the expected behavior?
The cookie should not be sent. 

What went wrong?
The cookie should only be sent if the samesite attribute is set to none or lax

Did this work before? N/A 

Chrome version: 63.0.3239.132  Channel: stable
OS Version: OS X 10.12.4
Flash Version:

## Timeline

### mk...@chromium.org (2018-01-18)

We shouldn't be sending a `SameSite=Strict` cookie along with a cross-site prerender request. I'll dig into this a bit this morning.

[Monorail components: Internals>Network>Cookies]

### mk...@chromium.org (2018-01-18)

Looks like we're simply not setting the initiator correctly when triggering a prerender request. Digging into why that's not happening.

Amusingly, it looks like we're going to have a hard time covering this with layout tests, as prerender is all implemented in //chrome, and therefore not available in `content_shell`, which is pretty unfortunate. CCing yoav@ in case he has ideas on that bit in particular.

### mk...@chromium.org (2018-01-18)

`NavigationRequest::CreateBrowserInitiated` sets an initiator on outgoing requests based on the `frame_tree_node`. In the case of prerendering, we've apparently lost the link to the initiating frame.

I think one approach would be to thread an initiator from `PrerenderManager::AddPrerenderFromLinkRelPrerender` (which looks like the last place we have access to the initiating `WebContents`) through to `PrerenderContents`, where we create a `LoadURLParams` in `PrerenderContents::StartPrerendering`.

That turns into a lot of ductwork, adding the initiator onto `LoadURLParams` struct, and then routing it through `NavigationController` => `NavigationEntry` (which requires changing the serialized navigation entry, etc) => (lots of things that I'm scared to trace all the way through because it's complicated) => `NavigationRequest::CreateBrowserInitiated`.

+creis@, as I think they had ideas about this when I tried to do something similar a long time ago to fix https://crbug.com/chromium/626243, and +clamy@, as they might have a better idea than tacking the initiator onto this path?

Thanks!

### cl...@chromium.org (2018-01-18)

@mkwst: yes this is a common plumbing problem we've been having lately. What I would like to do is move the creation of NavigationRequest to a place where we have access to the LoadURLParams (ie in NavigationController), so that we can give teh params to it right away when we create it, instead of having to store them in the NavigationEntry. creis@, wdyt?

### sh...@chromium.org (2018-01-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-18)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-01-19)

We are not going to get something merged back to 64. 65 is a reasonable stretch goal as a merge target. Adjusting milestones accordingly.

@clamy:
> What I would like to do is move the creation of NavigationRequest to a place
> where we have access to the LoadURLParams (ie in NavigationController)

This would make my life easier for this specific problem. If it's a reasonable thing for y'all to do in general, that sounds like a good plan. What kind of timeline would y'all be looking at for that refactoring?

### cl...@chromium.org (2018-01-19)

This is not something that would be merged in 65 so if you're looking at a merge in 65, you will need to do the plumbing through NavigationEntry.

### mk...@chromium.org (2018-01-19)

> This is not something that would be merged in 65 so if you're looking at a merge in 65, you will need to do the plumbing through NavigationEntry.

I agree. :) If you're planning on doing the refactoring anyway, and it'll make it into 66, that seems like the right way to do things. If your refactoring wouldn't make 66, then I'll start plumbing (assuming that that's the right way to do things in the status quo, which was my original question).

### cl...@chromium.org (2018-01-19)

I'm hoping to have this in M66. However we have quite a large number of refactorings to make, so not 100% that it will make it.

### cl...@chromium.org (2018-01-19)

FYI, I've filed https://crbug.com/chromium/803859 for the refactor.

### cr...@chromium.org (2018-01-20)

I like clamy@'s proposal in https://crbug.com/chromium/803859.  If we can wait for that to fix this bug, I think it will make things much easier.  (It's not clear to me that all the plumbing mentioned in https://crbug.com/chromium/803365#c3 would be safe to merge to M65 anyway, even with a relatively recent branch cut.)

### mk...@chromium.org (2018-01-22)

Merging to 65 seemed like a reasonable stretch goal, but I agree that it's looking non-trivial.

What would y'all like me to do? I can do the plumbing through `NavigationEntry` as suggested above, or I can wait for y'all to refactor things and plumb that way. If me poking at NavigationEntry would get in the way of the refactoring, then I'm happy to hold off. If not, and the refactoring is risky for M66, then I'll start on that work.

### cl...@chromium.org (2018-01-22)

I think we can have the refactor for M66: I do think it's doable in 6 weeks.

### sh...@chromium.org (2018-02-05)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2018-02-07)

Marking this bug as blocked on https://crbug.com/chromium/803859.

clamy@: Branch point is in ~3 weeks. If you have a WIP patch, could you point me at it so I can try to put together a dependent patch to save some time? Thanks! :)

### cl...@chromium.org (2018-02-07)

I'm working on one. I hope to have something by EOW.

### cl...@chromium.org (2018-02-12)

I have a draft CL at https://chromium-review.googlesource.com/c/chromium/src/+/904988. We still can't create the NavigationRequest from the LoadURLParams (CL was too big already to include this), but it should make the plumbing easier. Still WIP though.

### sh...@chromium.org (2018-02-21)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2018-02-27)

@mkwst: The CL linked here will very likely not make it into M66 (it's big and reviewers are busy). You might want to look at an alternative plumbing to fix the bug in 66 by using the NavigationEntry (see suggested filename there for an example).

### mm...@chromium.org (2018-03-30)

Friendly ping from the security sheriff. There is a CL proposed in c#18 and an additional info in c#20. Could you please take a look?

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9

commit ea99ea1dc01c5bbf058c18abe50008147e5b7ae9
Author: clamy <clamy@chromium.org>
Date: Mon May 28 13:54:23 2018

Move NavigationRequest creation to NavigationController: 2/3

This CL moves the NavigationRequest creation to the NavigationController. The
Navigator will now take a NavigationRequest as an argument to Navigate instead
of the pending NavigationEntry.

Summary of the changes:
1) Navigator
 - NavigatorImpl::NavigateToEntry and NavigatorImpl::NavigateToPendingEntry are
   removed in favor of Navigate which takes as argument a NavigationRequest. The
   NavigationController is now responsible for creating the NavigationRequest and
   passing it to Navigator::Navigate to have the navigation start.
 - NavigatorImpl::RequestNavigation, which currently creates the
   NavigationRequest is removed. Instead, the NavigationRequest is created in
   NavigationControllerImpl::CreateNavigationRequest.

2) NavigationController
 - HandleRendererDebugURL is called from NavigateWithoutEntry and handles
   navigation to a renderer debug URL. Navigations to a renderer debug URL do not
   require a NavigationRequest. They cannot commit, hence why we can't have a
   committed NavigationEntry for a renderer debug URL.

The next CLs will cleanup the internals of NavigationController.

Bug: 803365
Change-Id: I8b01384324ccfdca451baf1e645ac7d0869e8d47
Reviewed-on: https://chromium-review.googlesource.com/957735
Commit-Queue: Camille Lamy <clamy@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#562250}
[modify] https://crrev.com/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9/content/browser/frame_host/navigation_controller_delegate.h
[modify] https://crrev.com/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9/content/browser/frame_host/navigation_controller_impl.h
[modify] https://crrev.com/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9/content/browser/frame_host/navigator.cc
[modify] https://crrev.com/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9/content/browser/frame_host/navigator.h
[modify] https://crrev.com/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9/content/browser/frame_host/navigator_delegate.cc
[modify] https://crrev.com/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9/content/browser/frame_host/navigator_delegate.h
[modify] https://crrev.com/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9/content/browser/frame_host/navigator_impl.cc
[modify] https://crrev.com/ea99ea1dc01c5bbf058c18abe50008147e5b7ae9/content/browser/frame_host/navigator_impl.h


### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/21718cc2274ec87c679d9a14643d440148966cdd

commit 21718cc2274ec87c679d9a14643d440148966cdd
Author: clamy <clamy@chromium.org>
Date: Wed Jun 13 13:34:24 2018

Move NavigationRequest creation to NavigationController 3/3

This CL creates a new function in NavigationController following the move of
the NavigationRequest creation to the NavigationController. This function,
NavigateWithoutEntry is called for new navigations, for which we don't have a
NavigationEntry. It creates a pending NavigationEntry and a single
NavigationRequest based on the LoadURLParams, then asks the Navigator to
navigate to it. This allows the creation of NavigationRequests based on
LoadURLParams in a function that has access to LoadURLParams.

This is part of a larger refactoring effort. I plan to follow up this
CL by additional work:
1) Adding another method for creating NavigationRequests that only uses the
LoadURLParams and does not depend on the pending NavigationEntry.

2) Introduce a NavigateToExistingEntry method that will be used for navigations
to existing NavigationEntries.

3) Unifying code in StartHistoryNavigationInNewChild and NavigateFromFrameProxy
with NavigateToExistingEntry and NavigateWithoutEntry.

4) Removing the pending NavigationEntry and instead create NavigationEntries
from the NavigationRequests when the navigation commits.

Bug: 803365, 803859
Change-Id: I325ddbab2309ce88c138e7e92755aa31cc6c4617
Reviewed-on: https://chromium-review.googlesource.com/904988
Commit-Queue: Camille Lamy <clamy@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#566817}
[modify] https://crrev.com/21718cc2274ec87c679d9a14643d440148966cdd/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/21718cc2274ec87c679d9a14643d440148966cdd/content/browser/frame_host/navigation_controller_impl.h


### bu...@chromium.org (2018-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3cb9bea95cc71183d56666baf06bbedf7d2e527b

commit 3cb9bea95cc71183d56666baf06bbedf7d2e527b
Author: clamy <clamy@chromium.org>
Date: Tue Jul 10 12:42:02 2018

Introduce NavigateToExistingPendingEntry in NavigationController

Following the introduction of NavigateWithoutEntry in
https://chromium-review.googlesource.com/c/chromium/src/+/904988, this
CL introduces a new function in NavigationController,
NavigateToExistingPendingEntry. This function should be used when requesting a
navigation to an existing NavigationEntry.

Bug: 803365, 803859
Change-Id: I2b1901c0e63934aac4df9837104dcb3f8f28fdc0
Reviewed-on: https://chromium-review.googlesource.com/1089052
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Camille Lamy <clamy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#573693}
[modify] https://crrev.com/3cb9bea95cc71183d56666baf06bbedf7d2e527b/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/3cb9bea95cc71183d56666baf06bbedf7d2e527b/content/browser/frame_host/navigation_controller_impl.h


### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-09-04)

I believe the changes needed in NavigationController for this bug are now landed, so removing the dependency on the refactoring of NavigationController.

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-11-02)

That Go program resulted in Gin causing Go to panic with a memoryError. :)

So, I faked it using Apache 2's Header directive in <Location> blocks. I was not able to reproduce the bug. Chrome never even requests my given rel="prerender" link, as observed in the Network panel of Dev Tools.

I suspect this is because we have turned off Prerendering? (https://bugs.chromium.org/p/chromium/issues/detail?id=678332)

If that's correct, then this bug is Fixed, right? +pasko

This is one of our oldest Medium severity security bugs (287 days), so I'd like to get it resolved either way soon. Thanks!

### is...@gmail.com (2018-11-02)

I just re-tested and saw the issue still, odd that gin panic'd, i just rebuilt the same exact code and it worked fine.

ip,url,ref,cookie_name,cookie_value
[::1]:41916,/set/strict,,,
[::1]:41916,/favicon.ico,http://localhost:8080/set/strict,,
[::1]:41916,/favicon.ico,http://localhost:8080/set/strict,SS_STRICT,5678
[::1]:41916,/link-prerender?with-args=123&arg2=456,,,
[::1]:41916,/link-prerender?with-args=123&arg2=456,,SS_STRICT,5678


Chrome Version (Ubuntu 16.04): Version 70.0.3538.77 (Official Build) (64-bit).

Did you attempt to do it from the same exact browser tab? I noticed it did not work if I loaded the /set/strict in one tab, then loaded the jsfiddle in a second tab.

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-01-21)

re #32: this is nostate-prefetch ([1], [2]) that gets triggered with <link rel=prerender> - it still sends requests with cookies. We do not have tests for SameSite=Strict. Those requests are not piped to the opener's devtools instance, server logs would be a better source of confirmation about the headers.

clamy: is there something remaining TBD in crbug.com/803859 to unblock this?


[1] noatate-prefetch dev docs:
    https://developers.google.com/web/updates/2018/07/nostate-prefetch

[2] nostate-prefetch design doc: http://goo.gl/EJjTCM

### cl...@chromium.org (2019-01-23)

The work needed in NavigationControllerImpl was completed.

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-07-26)

Forgot to reassign it properly in the past. Sorry.

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2020-01-07)

Secondary security sheriff here: Now that the NavigationControllerImpl work is complete, is there anything else blocking this work?

### tb...@chromium.org (2020-01-07)

Is this bug different than https://crbug.com/chromium/831725? ryansturm@ can you PTAL since you fixed the other one too. Thanks :)

### is...@gmail.com (2020-01-07)

Looks the same to me... however my ticket is older, yet the other ticket got fixed & rewarded...?

### ry...@chromium.org (2020-01-07)

Looks the same to me. I don't know how the reward program works. I think security sheriff would know better.

### cr...@chromium.org (2020-01-07)

If it turns out an earlier rewarded report is the same issue, I think we often try to reward the earlier one as well.  pabrai@, would that be the case here (based on your https://crbug.com/831725#c35)?

ryansturm@: Can you confirm that the repro steps discussed here are fixed as of your r665383 (77.0.3811.0)?  If so, feel free to mark this fixed and we can follow up about the reward.  Thanks!

### cr...@chromium.org (2020-01-07)

Oops, actually CC'ing pabrai@ for my question in https://crbug.com/chromium/803365#c50.

### ry...@chromium.org (2020-01-07)

I just checked that the behavior described in this bug no longer occurs in M79 Stable. The cookies are not sent for prerender requests to sites that have the cookie marked as same site strict. The duped bug has extremely similar behavior as well, the only difference being that the other bug tests the difference between strict and lax and doesn't use localhost in the test. 

### mm...@chromium.org (2020-01-07)

Marking as fixed, then.

### ry...@chromium.org (2020-01-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-08)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-09)

Adding this for the Panel to consider at our next meeting. 

### sh...@chromium.org (2020-01-11)

Not requesting merge to beta (M80) because latest trunk commit (573693) appears to be prior to beta branch point (722274). If this is incorrect, please replace the Merge-na label with Merge-Request-80. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-23)

Congrats the Panel decided to reward $2,000 for this report!

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### is...@gmail.com (2020-01-23)

Great thanks!

### ad...@google.com (2020-01-30)

isaac.dawson@: I'm going to amend the M77 release notes to credit you and the other reporter jointly for this discovery. How would you like to be credited?

### is...@gmail.com (2020-02-01)

Great, first name last name is fine, thanks again!

### [Deleted User] (2020-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-06-01)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/803365?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090228)*
