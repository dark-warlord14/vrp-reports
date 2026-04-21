# Security: Custom Tab Scroll Inference

| Field | Value |
|-------|-------|
| **Issue ID** | [40064099](https://issues.chromium.org/issues/40064099) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Scroll, UI>Browser>Mobile>CustomTabs |
| **Platforms** | Android |
| **Reporter** | ph...@gmail.com |
| **Assignee** | si...@google.com |
| **Created** | 2023-04-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

## Short summary

Using Chrome's support for URL text fragment directives, Custom Tab's onGreatestScrollPercentage callback or extraCommand functionality and a bug that we discovered in Custom Tab's Bottom Bar feature, it is possible for a malicious application to infer whether a specific string is included on a website, thus attacking user's confidentiality in a similar fashion to an XS-Leak attack, opening a gap in the Same Origin Policy. The attack requires user interaction.

## Attack details

Chrome supports URL text fragment directives [1], which allow specifying a text snippet inside a URL. The text fragment that is specified in the URL is then highlighted on the website. Chrome also scrolls to the corresponding fragment if it is out of the screen. Furthermore, Custom Tabs also support the extraCallback callback [2]. Chrome fires the onVerticalScroll event whenever the user vertically scrolls within the Custom Tab. The value of "isDirectionUp" in the bundle that is sent in this event informs the application if the user scrolled up or down. When the user scrolls beyond the maximum position they have already scrolled, the getGreatestScrollPercentage event is fired containing the percentage of the maximum scroll, where 0 is the start of the page and 100 is the end of the page. Alternatively, one can also use the extraCommand function of the CustomTabsClient with "getGreatestScrollPercentage" as a parameter to query the greatest scroll position. The events are not fired when an automatic scroll, as performed by Chrome when scrolling triggered by the URL text fragment directive, is triggered. Instead, it is only fired when an actual scroll event is performed by the user. If the user is at the beginning of the page and performs a scroll up, the maximum scroll position does not change, hence only the onVerticalScroll event with isDirectionUp=true is fired. If however, Chrome performs an automatic scroll to the middle of the page and the user scrolls up, both events are fired. This is, because the maximum, which was 0 before the scroll due to Chrome not updated the value when an automatic scrolling is performed, is increased by manual scrolling.

Custom Tab's bottom toolbar (also called secondary toolbar) [3] can be used to add RemoteViews to the bottom of the Tab. Due to a bug that we discovered in the bottom toolbar, it is possible to make the content inside the toolbar arbitrarily big, thus overlaying the web content of the Custom Tab. The toolbar itself stays at a fixed height. The web content is only overlaid with the background color of the website inside the Custom Tab. This behaviour can be seen in the attached image. Notice that the content height of the toolbar needs to be smaller than the web content that is displayed, otherwise scrolling does not have any effect. For instance, the size of the secondary toolbar can be chosen as the size of the web content subtracted by 1. This height can easily be determined by querying the height of a full-size View in an activity of the application.

A malicious application can open a target website in a Custom Tab and include the requested URL text fragment directive in the URL. It can furthermore hide the web content by setting the height of the bottom toolbar to be the height of the web content subtracted by 1. If the string included in the URL text fragment is present on the page, the browser automatically scrolls to the corresponding position. The attacker then lure the user into scrolling up inside the web window by displaying some information in the bottom bar, as shown in the attached picture. The bug in the bottom bar allows the attacker to hide that sensitive user information is displayed in the Custom Tab. By putting custom content inside the bottom bar, it is also possible to distract the user from noticing that a Custom Tab is indeed opened. An attacker can furthermore hide all information indicating that a Custom Tab is opened except for the hostname of the website currently opened and the "vertical more" icon at the top right corner, making it hard for the user to grasp that they are operating in a web context.

When the user scrolls up, an onVerticalScroll event with isDirectionUp=up event is fired. The malicious application now waits for a short amount of time (e.g. 500ms) for an onGreatestScrollPercentageIncreased event. If this event is fired, the browser performed an automatic scroll and the text fragment appears on the page. If, however, the event is not fired, the user is at the beginning of the page, hence, the text segment could not be found.

Information about the maximum scroll position is only available if the “Help improve Chrome’s features and performance” feature is activated. This is, however, the default value and needs to be disabled explicitly.

## Security Implications

Since the state is shared between the Custom Tab and the underlying browser, this attack can be used to open a gap in the enforcement of the Same Origin Policy. A cross-origin/cross-context resource (aka the malicious application) can infer information about another, unrelated origin (the website loaded in the Custom Tab). Because websites are opened in a Custom Tab in a top-level context, usage of SameSite Lax cookies does not prevent the attack.

One possible attack allows inferring the user's activity on the Google account. By querying search terms on <https://myactivity.google.com/myactivity?pli=1>, it is possible to query if the user has searched for a specific search term within a specific time interval. By querying `https://timeline.google.com/maps/timeline`, it is even possible to infer whether the user has visited a specific location on a specific date. To check if the user has visited the place "Street" on March 2, 2023, for example, the URL `https://timeline.google.com/maps/timeline?hl=de&pli=1&pb=!1m2!1m1!1s2023-03-02&#:~:text=Street` can be launched in the Custom Tab.

Proposed Mitigation Strategies  

**-------------------------** -----

As a first mitigation, the content inside the bottom bar must limited to a fixed maximum height so that the web content cannot be hidden. We are furthermore of the opinion that sharing the scroll behaviour of a user on a page with an unrelated, potentially malicious entity, i.e., an application that launches the Custom Tab, is potentially dangerous, since it could introduce additional violations of the Same Origin Policy. It is thus advisable to remove this feature altogether or restrict it to websites for which a relation between the launching application and the website exists and can be checked, for example through the use of Digital Asset Links.

[1] <https://web.dev/text-fragments/>  

[2] <https://developer.android.com/reference/androidx/browser/customtabs/CustomTabsCallback#extraCallback(java.lang.String,android.os.Bundle)>  

[3] [https://developer.android.com/reference/androidx/browser/customtabs/CustomTabsIntent.Builder#setSecondaryToolbarViews(android.widget.RemoteViews,int[],android.app.PendingIntent)](https://developer.android.com/reference/androidx/browser/customtabs/CustomTabsIntent.Builder#setSecondaryToolbarViews(android.widget.RemoteViews,int%5B%5D,android.app.PendingIntent))

**VERSION**  

Chrome Version: 111.0.5563.116 stable  

Operating System: Android 13, tested on a Pixel 4

**REPRODUCTION CASE**  

The source code of the PoC Android application can be found at <https://gitfront.io/r/user-9841371/km3AMfhhx5sC/ct-scroll-poc/>. The PoC can be used to infer whether the user has visited a specific location on a specific date. One can enter the date and location to query and then click "Open Custom Tab". The button launches `https://timeline.google.com/maps/timeline?hl=de&pli=1&pb=!1m2!1m1!1s<date>&#:~:text=<location>` with the corresponding date and location. As soon as a scroll event is registered, the application displays the result.

**CREDIT INFORMATION**  

Reporter credit: Philipp Beer (TU Wien)

## Attachments

- [ct_hiding.png](attachments/ct_hiding.png) (image/png, 40.3 KB)

## Timeline

### [Deleted User] (2023-04-18)

[Comment Deleted]

### za...@google.com (2023-04-21)

Hi eirage@ I see you are listed as owner in chrome custom tabs directory, can you help investigate this bug? Note that I have not reproduced his bug because I do not have the device or the system. Thanks for your time. 

[Monorail components: UI>Browser>Mobile>CustomTabs]

### za...@google.com (2023-04-21)

Hi eirage@ I see you are listed as owner in chrome custom tabs directory, can you help investigate this bug? Note that I have not reproduced this bug because I do not have the device or the system. Thanks for your time.

### [Deleted User] (2023-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ei...@chromium.org (2023-04-24)

sinansahin@, could you please take a look? Thanks

### za...@google.com (2023-04-25)

Hi sinansahin@ can you please help investigate this bug? Thanks. 

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### si...@google.com (2023-04-25)

+Kevin and Victor, this is potentially serious.

### kg...@google.com (2023-04-25)

+Theresa as well

### kg...@google.com (2023-04-25)

Thank you for the report and for bringing this to our attention! We are investigating ways in which we could mitigate this.

@zackhan, from a security point of view, we would like your perspective on the point being made in relation to the CCT functionality of communicating scroll information and it opening a gap in the Same Origin Policy. Based on the bug report we understand that using Chrome's URL text fragment directives and Custom Tab's onGreatestScrollPercentage there is the potential for malicious actors to infer if certain information is available on the webpage if the web page is automatically scrolled to where the content might be located and the onGreatestScrollPercentage callback is being called. If we would disable the onGreatestScrollPercentage (and other related APIs) functionality for pages that were automatically scrolled using Chrome's support for URL text fragment directives, would the Same Origin Policy point being made here still be a concern?

### tw...@chromium.org (2023-04-25)

cc'ing  zackhan@google.com for #12

### ph...@gmail.com (2023-04-26)

Can you please add squarcina@gmail.com to the issue so that he has read permissions? Thank you in advance!

### za...@google.com (2023-04-26)

Tagging Amy here to give more input per our discussion yesterday. amyressler@ can you help confirm the question per https://crbug.com/chromium/1434438#c12? Thanks. 

### si...@google.com (2023-05-01)

Friendly ping. Does the approach suggested in https://crbug.com/chromium/1434438#c12 sound reasonable?

### ct...@chromium.org (2023-05-01)

For this specific infoleak the approach in https://crbug.com/chromium/1434438#c12 seems reasonable. Adding bokan@ and the Blink>Scroll component for visibility by the Scroll-to-Text folks. It may also be good to audit through any other CCT API that might give some inspection of the tab state that could be used for XS-Leaks -- I don't think we considered the CCT attack surface when first launching this feature.

[Monorail components: Blink>Scroll]

### ct...@chromium.org (2023-05-01)

[Empty comment from Monorail migration]

### si...@google.com (2023-05-03)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-05-03)

#12 seems like a reasonable approach to me as well.

You could also consider doing it for any fragment scrolling since that also has potential to reveal information about a user. However, with element-id fragments the information is likely to be less sensitive than page content and is under the page's control so less severe than text fragments. Additionally, fragments might be required on some pages (as they can be used for routing) which would require this mitigation more often so maybe not worth the tradeoff.

### tw...@chromium.org (2023-05-03)

cthomp@ / bokan@ -- wanted to get your thoughts on another option we're considering that could apply to both text fragments and element-id fragments.

Custom Tabs engagement signals send both scroll direction callbacks and the max scroll percentage reached when a scroll event ends if the max position reached has increased since the last callback. Currently these are sent for any scroll interactions.

We could instead wait until the user has scrolled farther down on the page at least once before sending the scroll direction or max scroll percentage callbacks. Because scroll percentage is only reported on scroll end, this would make it harder for the attacker to infer whether the first scroll position that is reported is because of a fragment scroll or because the user manually scrolled/flung the page.

Do you think that would be a sufficient mitigation? 

Kevin did raise the point that if the first scroll percentage reported is e.g. 80-90%, an attacker may decide the text fragment was 'likely' on the page even if they wouldn't know for sure.

> Additionally, fragments might be required on some pages (as they can be used for routing) which would require this mitigation more often so maybe not worth the tradeoff.

We didn't find stats on this from some quick poking around but suspect that pages loaded with element id fragments are more common. Therefore disabling engagement signals all together for pages loaded with element id fragments wouldn't be desirable from a product perspective. The information that could be gleaned also seems more limited.

### bo...@chromium.org (2023-05-03)

> Kevin did raise the point that if the first scroll percentage reported is e.g. 80-90%, an attacker may decide the text fragment was 'likely' on the page even if they wouldn't know for sure.

I tend to have similar concerns; it adds a bit of noise but my suspicion is that this could still be largely exploited in practice. i.e. assuming users aren't flinging, I'd expect a scroll from top to end in the 10-20% so if you get anything other than that you can assume the fragment was likely scrolled.

Of course, the numbers will depend on the length of the page and the location of the fragment - maybe the combination of page length and content dependence and user scrolling behavior (i.e. do they repeatedly fling so the first scrollend happens far down?) makes this sufficiently fuzzy as to not be practical? Not sure how we'd determine that though.

Another idea, could we delay the first scroll callbacks if a text fragment is used by X seconds? i.e. if a text fragment was used, wait some amount of time so that it's more likely a user would have scrolled themselves further down the page by then. 

In the limit - on a very long page - if the text fragment is somewhere far far down then I can't think of any mitigations aside from hiding scroll entirely where an attacker couldn't reliably tell based on the first scroll end. But perhaps pages of that length are sufficiently rare, and containing sensitive information even more so, that it's less of an issue?

### tw...@chromium.org (2023-05-03)

>  I'd expect a scroll from top to end in the 10-20% so if you get anything other than that you can assume the fragment was likely scrolled.

fwiw, users don't have to 'stop' scrolling at each screen of content. If you keep scrolling down the page without it coming to a complete rest, we won't send the callbacks.

> In the limit - on a very long page

We send a scroll percent, not the actual position so unless the attacker knows it's a very long page and therefore reaching e.g. 80% in a single scroll callback called by a gesture would be uncommon then the length of the page may not particularly matter.

We could also do a hybrid:
  - text fragments: disable engagement signal callbacks when URLs are loaded with text fragments. Very rare, therefore very small impact on legitimate CCT clients.
  - element id fragments: don't send engagement signal callbacks until the user has scrolled farther down on the page at least (we're actually thinking this behavior is fine for all pages). May still allow for some inference, but what can be inferred is less sensitive.

### kg...@google.com (2023-05-04)

[Empty comment from Monorail migration]

### ad...@google.com (2023-05-11)

[Empty comment from Monorail migration]

### si...@google.com (2023-05-11)

We've discussed this in https://docs.google.com/document/d/16VU2XtC5f6iCIxyntFYssb0vkJu3yjB3tg4tgcdnPCo/edit?usp=sharing. Access is currently limited.

The summary is, to mitigate this issue we are going to:
- Disable Engagement Signals callbacks on any page that has a text fragment directive (#:~:). This will apply even if this isn't the initial URL that the Custom Tab is opened with.
- For any other page with a fragment directive using DOM ids (#id), we will only start sending callbacks once there is a down scroll. We can consider doing this for other pages too.

Please let me know if you have any concerns with these plans.

### kg...@google.com (2023-05-17)

Hi cthomp@, amyressler@, zackhan@ we are planning to go ahead with the solution proposed in https://crbug.com/chromium/1434438#c26 . Could you please review it from a security perspective and let us know if this solution is ok with you?

### kg...@google.com (2023-05-23)

Hi cthomp@, amyressler@, zackhan@ , pinging on this as we want to go ahead with implementing the proposal from https://crbug.com/chromium/1434438#c11. Could you please review it from a security perspective?

### es...@chromium.org (2023-05-23)

Second security shepherd here -- I can take a look at the proposal; can you please add me to the doc in c26?

### si...@google.com (2023-05-23)

I've shared the doc with you. Thanks!

### es...@chromium.org (2023-05-23)

Note: https://crbug.com/chromium/1439896 is a similar bug in that tricking the user into interacting with the bottom bar can leak something to the embedding app. In the case of https://crbug.com/chromium/1439896, the leaked information is the URL. In practice this seems like it would be used for similar purposes (leaking whether a user is signed into a particular site). I'm not aware of any real ideas for effective mitigation for that issue.

> For any other page with a fragment directive using DOM ids (#id), we will only start sending callbacks once there is a down scroll. We can consider doing this for other pages too.

This seems like a weak mitigation because, as noted upthread, the attacker can probably infer information, or at least make educated guesses, from a combination of timing and scroll percentage. Is there a reason we can't disable Engagement Signals callbacks on any URL that has a fragment, not just a text fragment (#:~:)?

### tw...@chromium.org (2023-05-23)

While we don't have existing data on this (or haven't found any), our assumption is that element id fragments are more prevalent so removing engagement signals for those sites would have a greater negative impact on utility of the APIs. The information gleaned is also more limited (may reveal sign-in state but not much else?) compared to text fragments, so our thinking was that might be a lower severity and therefore reasonable to make a different security/privacy trade-off. 

We met with Rohit on this from the Privacy side on May 11. Happy to grab some time with security as well if that's be helpful!

### ro...@google.com (2023-05-24)

Chiming in from privacy side. I confirm that the proposal that Theresa and team have to mitigate the inference issue by either disabling/limiting (or also "adding noise" which we briefly talked about) to the callbacks to remove any deterministic inference of page content to the embedder is LGTM. Orthogonally, I remember that we also covered, the infinite scroll use-cases (during the early design phase) which we thought can be used as a proxy to infer the signed-in state. So, with that in mind I think we should continue to cover cases where we could unintentionally reveal the same. Thanks.

### es...@chromium.org (2023-05-25)

Ok, that makes sense. I'm okay with that for security too. Would be good to have a security FAQ entry or similar documentation for these loopholes, I think that was mentioned on https://crbug.com/chromium/1439896.

### ad...@google.com (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/47cba7b069864e580caa8b51c17985087cb03a48

commit 47cba7b069864e580caa8b51c17985087cb03a48
Author: Sinan Sahin <sinansahin@google.com>
Date: Tue Jun 06 20:25:06 2023

[CT] Pause Engagement Signals on pages with text fragments

Bug: 1434438
Change-Id: Ie0eacbbca3053dc7aa0e70e75976084425f3ca5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4595859
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Kevin Grosu <kgrosu@google.com>
Commit-Queue: Sinan Sahin <sinansahin@google.com>
Cr-Commit-Position: refs/heads/main@{#1154036}

[modify] https://crrev.com/47cba7b069864e580caa8b51c17985087cb03a48/chrome/android/java/src/org/chromium/chrome/browser/customtabs/content/RealtimeEngagementSignalObserver.java
[modify] https://crrev.com/47cba7b069864e580caa8b51c17985087cb03a48/chrome/android/junit/src/org/chromium/chrome/browser/customtabs/content/RealtimeEngagementSignalObserverUnitTest.java


### si...@google.com (2023-06-06)

[Empty comment from Monorail migration]

### si...@google.com (2023-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-07)

Merge review required: M115 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### si...@google.com (2023-06-07)

1. This fixes a medium severity security bug.
2. https://chromium-review.googlesource.com/c/chromium/src/+/4595859
3. Yes
4. No
5. N/A
6. No

### am...@chromium.org (2023-06-08)

Hello, thank you for landing a fix for this issue! Security issues should be closed as Fixed as soon as the resolving CL is landed. This allows the automation to add the appropriate merge labels (based on severity and impact) in a timely fashion and get the issue into the security merge review queue. I've updated this as Fixed accordingly. 

Since this fix just landed < 24 hours ago, we'll need this to get a bit more bake time on Canary before considering backmerge. I'll revisit tomorrow or Friday for merge review. 

### kg...@google.com (2023-06-08)

amyressler@ fixing this bug has multiple parts so we will need to land follow up CLs (which we are working on) to fully fix it. Should we keep it open until all the CLs land?

### am...@chromium.org (2023-06-08)

apologies for jumping ahead here -- yes, if there are forthcoming fixes to fully resolve this issue, we should indeed leave it open until all CLs are landed. 


### kg...@google.com (2023-06-08)

No worries and thanks for opening it back up! We will let you know once all the CLs land.

### gi...@appspot.gserviceaccount.com (2023-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4aa7270e3d5a992f057a0c74e3c6ecdc7333988c

commit 4aa7270e3d5a992f057a0c74e3c6ecdc7333988c
Author: Sinan Sahin <sinansahin@google.com>
Date: Fri Jun 09 00:17:38 2023

[CT] Only send scroll signals once there has been a down scroll

Bug: 1434438
Change-Id: Iac1c50ca2117d079bc71294e0bd7290dc0278c86
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4601835
Reviewed-by: Kevin Grosu <kgrosu@google.com>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Sinan Sahin <sinansahin@google.com>
Cr-Commit-Position: refs/heads/main@{#1155254}

[modify] https://crrev.com/4aa7270e3d5a992f057a0c74e3c6ecdc7333988c/chrome/android/java/src/org/chromium/chrome/browser/customtabs/content/RealtimeEngagementSignalObserver.java
[modify] https://crrev.com/4aa7270e3d5a992f057a0c74e3c6ecdc7333988c/chrome/android/junit/src/org/chromium/chrome/browser/customtabs/content/RealtimeEngagementSignalObserverUnitTest.java


### gi...@appspot.gserviceaccount.com (2023-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fbed4def3e7c09d07d9a33d88bb957ebaa101a03

commit fbed4def3e7c09d07d9a33d88bb957ebaa101a03
Author: Sinan Sahin <sinansahin@google.com>
Date: Sat Jun 10 01:50:39 2023

[CT] Limit bottom controls height for bottom bar

The maximum bottom bar height is 120dp. However, the bottom controls
were not limited by the bottom bar height. This could shrink the web contents height.

This CL ensures the bottom controls height is set based on the bottom
bar height instead of the child view.

Bug: 1434438
Change-Id: Ia36a8b3b222bf169ac5bda0740c735466244eeb4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4606514
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Reviewed-by: Kevin Grosu <kgrosu@google.com>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Sinan Sahin <sinansahin@google.com>
Cr-Commit-Position: refs/heads/main@{#1155852}

[modify] https://crrev.com/fbed4def3e7c09d07d9a33d88bb957ebaa101a03/chrome/android/java/src/org/chromium/chrome/browser/customtabs/CustomTabBottomBarDelegate.java


### si...@google.com (2023-06-10)

3 CLs have landed to fix the issue.

### [Deleted User] (2023-06-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-10)

[Empty comment from Monorail migration]

### si...@google.com (2023-06-13)

Do I need to do anything else at this time to merge the fix back, or is this already in merge review?

### am...@chromium.org (2023-06-13)

Hi sinansahin@ I was just making sure the last of the CLs had sufficient bake time before reviewing so that all were covered and to lessen merge review and any related complications

https://chromium-review.googlesource.com/c/chromium/src/+/4595859
https://chromium-review.googlesource.com/c/chromium/src/+/4601835
https://chromium-review.googlesource.com/c/chromium/src/+/4606514

each approved for merge to M115, please merge to branch 5790 at your earliest convenience (by EOD Friday, 16 June) so this fix can be included in the next M115/beta update as well as the M115/Stable RC being cut on Tuesday, 20 June (but you may want to merge earlier, thus the Friday deadline since Monday is a US holiday) 


### gi...@appspot.gserviceaccount.com (2023-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/551a809a5669389b1a21557328b98e2fc7ef0d31

commit 551a809a5669389b1a21557328b98e2fc7ef0d31
Author: Sinan Sahin <sinansahin@google.com>
Date: Wed Jun 14 19:04:33 2023

[CT] Pause Engagement Signals on pages with text fragments

(cherry picked from commit 47cba7b069864e580caa8b51c17985087cb03a48)

Bug: 1434438
Change-Id: Ie0eacbbca3053dc7aa0e70e75976084425f3ca5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4595859
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Kevin Grosu <kgrosu@google.com>
Commit-Queue: Sinan Sahin <sinansahin@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1154036}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4611968
Cr-Commit-Position: refs/branch-heads/5790@{#759}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/551a809a5669389b1a21557328b98e2fc7ef0d31/chrome/android/java/src/org/chromium/chrome/browser/customtabs/content/RealtimeEngagementSignalObserver.java
[modify] https://crrev.com/551a809a5669389b1a21557328b98e2fc7ef0d31/chrome/android/junit/src/org/chromium/chrome/browser/customtabs/content/RealtimeEngagementSignalObserverUnitTest.java


### gi...@appspot.gserviceaccount.com (2023-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1c63cabd6731ec4fa6e0b8e0da670b4294bcbf7d

commit 1c63cabd6731ec4fa6e0b8e0da670b4294bcbf7d
Author: Sinan Sahin <sinansahin@google.com>
Date: Wed Jun 14 20:36:15 2023

[CT] Only send scroll signals once there has been a down scroll

(cherry picked from commit 4aa7270e3d5a992f057a0c74e3c6ecdc7333988c)

Bug: 1434438
Change-Id: Iac1c50ca2117d079bc71294e0bd7290dc0278c86
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4601835
Reviewed-by: Kevin Grosu <kgrosu@google.com>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Sinan Sahin <sinansahin@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1155254}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4615351
Auto-Submit: Sinan Sahin <sinansahin@google.com>
Commit-Queue: Kevin Grosu <kgrosu@google.com>
Cr-Commit-Position: refs/branch-heads/5790@{#761}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/1c63cabd6731ec4fa6e0b8e0da670b4294bcbf7d/chrome/android/java/src/org/chromium/chrome/browser/customtabs/content/RealtimeEngagementSignalObserver.java
[modify] https://crrev.com/1c63cabd6731ec4fa6e0b8e0da670b4294bcbf7d/chrome/android/junit/src/org/chromium/chrome/browser/customtabs/content/RealtimeEngagementSignalObserverUnitTest.java


### gi...@appspot.gserviceaccount.com (2023-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7dce8c54d3e33e3fc15820eb0f8b1359cb943c9b

commit 7dce8c54d3e33e3fc15820eb0f8b1359cb943c9b
Author: Sinan Sahin <sinansahin@google.com>
Date: Wed Jun 14 23:46:26 2023

[CT] Limit bottom controls height for bottom bar

The maximum bottom bar height is 120dp. However, the bottom controls
were not limited by the bottom bar height. This could shrink the web contents height.

This CL ensures the bottom controls height is set based on the bottom
bar height instead of the child view.

(cherry picked from commit fbed4def3e7c09d07d9a33d88bb957ebaa101a03)

Bug: 1434438
Change-Id: Ia36a8b3b222bf169ac5bda0740c735466244eeb4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4606514
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Reviewed-by: Kevin Grosu <kgrosu@google.com>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Sinan Sahin <sinansahin@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1155852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4617149
Auto-Submit: Sinan Sahin <sinansahin@google.com>
Commit-Queue: Kevin Grosu <kgrosu@google.com>
Cr-Commit-Position: refs/branch-heads/5790@{#770}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/7dce8c54d3e33e3fc15820eb0f8b1359cb943c9b/chrome/android/java/src/org/chromium/chrome/browser/customtabs/CustomTabBottomBarDelegate.java


### si...@google.com (2023-06-15)

I've merged all 3 CLs to 115.

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations, Philipp! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1434438?no_tracker_redirect=1

[Multiple monorail components: Blink>Scroll, UI>Browser>Mobile>CustomTabs]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064099)*
