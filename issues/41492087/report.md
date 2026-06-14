# In Chrome for Android, attackers can display a tel bubble on the Main Page and hijack the domain shown in the Main Page's Address Bar.

| Field | Value |
|-------|-------|
| **Issue ID** | [41492087](https://issues.chromium.org/issues/41492087) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>Intents, UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | lu...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2024-01-17 |
| **Bounty** | $500.00 |

## Description

---

### Report description


In Chrome for Android, attackers can display a tel bubble on the Main Page and hijack the domain shown in the Main Page's Address Bar.


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome (Android)


---

### The problem


#### Please describe the technical details of the vulnerability

After the victim visits a page with the following HTML content, clicking the Home Button will display the Chrome for Android homepage content in the viewport. However, it will trigger the attacker's tel intent, showing a bubble on the homepage. Additionally, the URL in the Address Bar on the homepage will be fixed to the attacker's domain, as if the homepage has been hijacked.
```
<script>
    onblur = () => {
        window.location.href="tel://123";
    }    
    // window.open("adout:blank", "_self");
</script>
```
https://ath3r1s.top:9997/onblur.html


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Displaying a tel bubble on the MainPage and hijacking the Address Bar.


---

### The cause


#### What version of Chrome have you found the security issue in?

120-0-6099-144


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Security UI Spoofing


#### How would you like to be publicly acknowledged for your report?

Ath3r1s




## Attachments

- [2024-01-17 17-45-34.mp4](attachments/2024-01-17 17-45-34.mp4) (video/mp4, 4.6 MB)
- [index.html](attachments/index.html) (text/plain, 135 B)
- [back.gif](attachments/back.gif) (image/gif, 411.4 KB)
- [blank.gif](attachments/blank.gif) (image/gif, 1.1 MB)
- [override.gif](attachments/override.gif) (image/gif, 1.1 MB)
- [trace_blur_repro_java.json.gz](attachments/trace_blur_repro_java.json.gz) (application/octet-stream, 30.5 KB)
- [trace_no_repro_java.json.gz](attachments/trace_no_repro_java.json.gz) (application/octet-stream, 26.3 KB)
- [tabswitcher.gif](attachments/tabswitcher.gif) (image/gif, 240.5 KB)
- [tabswitcher2.gif](attachments/tabswitcher2.gif) (image/gif, 243.7 KB)
- [tabswitcher3.gif](attachments/tabswitcher3.gif) (image/gif, 328.3 KB)
- [omnibox.gif](attachments/omnibox.gif) (image/gif, 283.8 KB)

## Timeline

### lu...@gmail.com (2024-01-17)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2024-01-17)

[Empty comment from Monorail migration]

### za...@google.com (2024-01-18)

Hi creis@, this bug is related to spoofing, can you please help take a look. Note that I did not successfully reproduce it due to my lack of an android environment at the moment so I set the foundin label to the extend stable milestone, but our reporter attached a screen recording. Can you please take a look and help triage? Feel free to reassign it back to me if you think it's not related to spoofing. Thank you! 

[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2024-01-18)

[Empty comment from Monorail migration]

### cr...@chromium.org (2024-01-18)

I'm not much help with tel: spoofing on Android.  Maybe mthiesse@ can take a look?

The video does look concerning, especially showing the attacker's URL above the NTP around 0:19.

[Monorail components: Mobile>Intents]

### mt...@chromium.org (2024-01-19)

Hmm interesting, looking into it. Not sure if this is one bug or two - I think I know why the message is being shown over the home page, but I don't know how the URL of the page behind the home page gets onto the home page or why we show a URL in this case at all as we should always be on about:newtab...

cc hanxi for start surface.

[Monorail components: UI>Browser>Mobile>Start]

### [Deleted User] (2024-01-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2024-01-19)

[Empty comment from Monorail migration]

### mt...@chromium.org (2024-01-19)

Pretty sure this is caused by https://crbug.com/chromium/1346353. The page is still considered visible while start surface is occluding it and is thus still allowed to trigger external nav. We should fix start surface here.

hanxi, can you please triage. Still not sure what's going on with the URL, probably worth looking into that too.

### ha...@google.com (2024-01-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2024-01-22)

One thing I want to point out is: it is NTP in the demo, not start surface. Only NTP has a home button on the top left corner, while start surface doesn't have (profile icon is shown at that location on start surface). I don't think the issue at https://crbug.com/chromium/1519106#c10 is related to this bug.

When pressing the home button, showing NTP is expected. However, it is very strange that the previous URL shown on the NTP's toolbar. Adding toolbar owners.

### en...@google.com (2024-01-22)

it may not be tied to start, indeed.

if i go to chrome settings, and override the home page with "about:blank", the issue reproduces.

surprisingly this is tied to "home" button alone, e.g. if i open "about:blank", then navigate to the demo page, and use gestures to navigate back, the issue won't reproduce.

however there is a pretty nasty side effect - it looks like this mechanism overwrites location bar data. at first glance it seems to just produce unexpected artifact in suggestions, likely not dangerous, but definitely bad.

### ha...@chromium.org (2024-01-22)

[Empty comment from Monorail migration]

### en...@google.com (2024-01-22)

CC: Wenyu - so far this appears to be linked to the home button alone..

### we...@google.com (2024-01-22)

HomeButton did something special - on phones it'll unfocus the omnibox, then does the navigation to the homepage URL. Since this repros regardless what URL we set, maybe could be relevant?
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/top/ToolbarLayout.java;l=765;drc=ca3478a884cd4d1c5d7897ded9838773ca1c4fd3




### en...@google.com (2024-01-22)

attempted bisect to look for possible culprit. 
this appears to be a very old problem.

### en...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### en...@google.com (2024-01-23)

1. i can confidently rule out the Omnibox - we don't play a role in this, although we are impacted by this (see "override" gif above).

2. i can say with moderate confidence that the LocationBar is not involved either. i am still investigating this to be sure.

3. i have moderate confidence this impacts Tabs, too - this is where the Omnibox sources the page URL from (which results in bogus URL reported on NTP, see the "override" gif above)

i managed to capture the backtrace triggering the navigation:

main[1] where
  [1] org.chromium.components.external_intents.ExternalNavigationHandler.maybeAskToLaunchApp (ExternalNavigationHandler.java:2,304)
  [2] org.chromium.components.external_intents.ExternalNavigationHandler.shouldOverrideUrlLoadingInternal (ExternalNavigationHandler.java:1,732)
  [3] org.chromium.components.external_intents.ExternalNavigationHandler.shouldOverrideUrlLoading (ExternalNavigationHandler.java:594)
  [4] org.chromium.components.external_intents.InterceptNavigationDelegateImpl.shouldOverrideUrlLoading (InterceptNavigationDelegateImpl.java:314)
  [5] org.chromium.components.external_intents.InterceptNavigationDelegateImpl.shouldIgnoreNavigation (InterceptNavigationDelegateImpl.java:171)
  [6] android.os.MessageQueue.nativePollOnce (native method)
  [7] android.os.MessageQueue.next (MessageQueue.java:335)
  [8] android.os.Looper.loopOnce (Looper.java:161)
  [9] android.os.Looper.loop (Looper.java:288)
  [10] android.app.ActivityThread.main (ActivityThread.java:7,815)
  [11] java.lang.reflect.Method.invoke (native method)
  [12] com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run (RuntimeInit.java:548)
  [13] com.android.internal.os.ZygoteInit.main (ZygoteInit.java:910)

not sure where this comes from though

### pn...@chromium.org (2024-01-23)

I believe this is a race condition where the navigation to chrome-native://newtab commits before the attempted navigation to tel://123 starts and fails. NavigationRequest::OnRequestFailedInternal  calls FrameTreeNode::DidStopLoading which I think is where we inadvertently overwrite the navigation entry back to https://ath3r1s.top:9997/onblur.html
Java reads the the new nav entry and updates accordingly.
I have some traces illustrating this issue I can upload tomorrow if that's helpful.

### en...@google.com (2024-01-23)

this comes from:
01-22 16:24:40.075 17812 17812 E chromium:   00000000047edd3b  navigation_interception::InterceptNavigationDelegate::ShouldIgnoreNavigation(content::NavigationHandle*)  intercept_navigation_delegate.cc:0:0
01-22 16:24:40.075 17812 17812 E chromium:   00000000022088ef  navigation_interception::(anonymous namespace)::CheckIfShouldIgnoreNavigationOnUIThread(content::NavigationHandle*)  intercept_navigation_delegate.cc:0:0
01-22 16:24:40.075 17812 17812 E chromium:   0000000001d2befb  base::RepeatingCallback<bool (content::NavigationHandle*)>::Run(content::NavigationHandle*) const &  intercept_navigation_throttle.cc:0:0
01-22 16:24:40.075 17812 17812 E chromium:   00000000022087e3  navigation_interception::InterceptNavigationThrottle::RunCheckAsync()             intercept_navigation_throttle.cc:0:0
01-22 16:24:40.075 17812 17812 E chromium:   0000000000482ecf  base::OnceCallback<void ()>::Run() &&                                             at_exit.cc:0:0


and that comes from:

01-22 16:26:53.883 18268 18268 E chromium:   RELADDR   FUNCTION                                                                          FILE:LINE
01-22 16:26:53.883 18268 18268 E chromium:   00000000021ead23  navigation_interception::InterceptNavigationDelegate::MaybeCreateThrottleFor(content::NavigationHandle*, navigation_interception::SynchronyMode)  intercept_navigation_delegate.cc:0:0
01-22 16:26:53.883 18268 18268 E chromium:   00000000021ea71f  ChromeContentBrowserClient::CreateThrottlesForNavigation(content::NavigationHandle*)  chrome_content_browser_client.cc:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000002b478bf  content::NavigationThrottleRunner::RegisterNavigationThrottles()                  ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000002b212f7  content::NavigationRequest::WillStartRequest()                                    ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000002b1f403  content::NavigationRequest::BeginNavigationImpl()                                 ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000002b1e6f3  content::NavigationRequest::BeginNavigation()                                     ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000002b4e7c7  content::Navigator::OnBeginNavigation(content::FrameTreeNode*, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::BeginNavigationParams>, scoped_refptr<network
::SharedURLLoaderFactory>, mojo::PendingAssociatedRemote<content::mojom::NavigationClient>, scoped_refptr<content::PrefetchedSignedExchangeCache>, int, mojo::PendingReceiver<content::mojom::NavigationRendererCancellationListener>)  ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000002b8036f  content::RenderFrameHostImpl::BeginNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::BeginNavigationParams>, mojo::PendingRemote<blink::mojom::Blob
URLToken>, mojo::PendingAssociatedRemote<content::mojom::NavigationClient>, mojo::PendingRemote<blink::mojom::PolicyContainerHostKeepAliveHandle>, mojo::PendingReceiver<content::mojom::NavigationRendererCancellationListener>)  ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000001f2b2e3  content::mojom::FrameHostStubDispatch::Accept(content::mojom::FrameHost*, mojo::Message*)  ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   000000000003dd93  mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)             ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000000045b7f  mojo::MessageDispatcher::Accept(mojo::Message*)                                   ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   000000000003f413  mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)              ??:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000000045553  IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)  ipc_mojo_bootstrap.cc:0:0
01-22 16:26:53.883 18268 18268 E chromium:   0000000000045d73  base::internal::Invoker<base::internal::BindState<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC:
:ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*)  ipc_mojo_bootstrap.cc:0:0

Omnibox, Start, LocationBar do not play any role in this. Passing over to the Navigation team for further investigation.

[Monorail components: -UI>Browser>Mobile>Start -UI>Browser>Omnibox UI>Browser>Navigation]

### cr...@chromium.org (2024-01-23)

mthiesse@: It looks like you might be familiar with InterceptNavigationDelegate::ShouldIgnoreNavigation?  (That's in components/navigation_interception, not part of the content/ navigation logic.)  We can certainly help if navigation code is something wrong there.

pnoland@ / https://crbug.com/chromium/1519106#c20: Uploading traces would be great.  I don't think FrameTreeNode::DidStopLoading normally updates NavigationEntries, so I'm curious where the entry is changing.  Thanks!

### pn...@chromium.org (2024-01-23)

Added traces; one for a repro case and one for a non-repro. I'm not positive where the navigation entry is being updated, I was just eyeballing the differences between the two traces. Both traces have FrameTreeNode::DidStopLoading, but in the repro trace:
* There are signs of Java processing a url update event (notably, LocationBarModel.updateVisibleGurl)
* There's a subsequent call to NotifyNavigationStateChanged(). 
* There's a call to DiscardSpeculativeRFH under OnRequestFailedInternal (perhaps not important)

FWIW I can also repro this issue when navigating from the demo site to about:blank.



### en...@google.com (2024-01-23)

re https://crbug.com/chromium/1519106#c20: i think this would address only one of many related issues, e.g.

- focusing the omnibox while visiting the page,
- tapping the tab switcher and returning to the page,

it sometimes shows the popup - and sometimes takes me straight to the dialer. 
i think the problem is in the fact we're attempting to open something other than the URL. the race described earlier essentially means "the results are inconsistent".

attached a few examples to show what i mean. Note that the race Patrick brought up means that we may either show the bubble or open dialer directly in all of these cases (i have seen this happen). 

this is not scoped to the home button.

- tabswitcher: upon returning to the same tab we may show bubble or open dialer directly (shows bubble)
- tabswitcher2: upon returning to a different tab we may show bubble or open dialer directly (shows bubble)
- tabswitcher3: upon entering tab switcher we may show bubble or open dialer directly (opens dialer)
- omnibox: upon tapping the omnibox we may show bubble or open dialer directly (opens dialer).

it seems like we may have to devise a more sophisticated fix.

### en...@google.com (2024-01-23)

... note that the same behavior (showing bubble or opening dialer) impacts also options available from the menu, e.g. 
- open settings
- open recent tabs
- open history
- open downloads
- opening share hub
etc.

### mt...@chromium.org (2024-01-23)

Whether the navigation launches the phone or not depends on whether the page was granted a user gesture before you blur it (it's not racy as far as I can tell).

It appears some methods of causing the page blur hide the page before sending onblur, so things like opening history will not cause the dialer to open or show the bubble as they hide the tab, but recent tabs doesn't hide before blurring so will.

There's also definitely a navigation bug here where when you navigate to about:blank via the URL bar, the navigation in onblur hijacks this user-initiated navigation and aborts it.

The other bug is that while the new tab page is open the page behind it is still 'visible' - sorry for thinking this was https://crbug.com/chromium/1346353 with start surface, I'm pretty sure it's just an identical bug for NTP.

### mt...@chromium.org (2024-01-23)

So to be clear, there are two bugs here:

1. Native Pages don't hide the page under them, so they still think they're visible (easy to repro with NTP or recent tabs).

2. navigation in onblur aborts some other navigations like navigation to about:blank, and presumably the navigation to the recents page. In the about:blank case this causes the navigation to be aborted, and in the NativePage case, this causes the URL to be wrong.

### en...@google.com (2024-01-23)

Hmm.. you mention it's a problem with native pages.

I'm not sure this aligns with what i've seen with regard to the Omnibox, Tab switcher or sharing hub.

at first glance it seems to me that the webcontents focus events are driving onblur events.. if i hook up a physical keyboard and press <tab> i end up in dialer without accessing any of the buttons..

### mt...@chromium.org (2024-01-24)

It's true that focus events drive onblur, but visibility is not focus. If you open dev tools on the page, then open recent tabs or the NTP you'll see that document.hidden continues to return false while the page is behind the Native Page.


### aj...@google.com (2024-02-02)

->  mthiesse as security issues need owners - feel free to assign to someone else who can make progress

### mt...@chromium.org (2024-02-02)

Theresa, does anybody own Native Pages? The visibility bug seems most pressing to fix.

I'm not sure who would own the user navigation to about:newtab getting intercepted by the onblur navigation, maybe creis@ can help with that?

### tw...@chromium.org (2024-02-02)

> Theresa, does anybody own Native Pages?

This sounds like it sits somewhere between TabImpl (and its native page related code) + navigation stack code. Not sure anyone has that specific combo of expertise, but we can probably get there together :)

cc'ing Fred in case Tabs team has time to pick this up. 

>  you'll see that document.hidden continues to return false while the page is behind the Native Page.

Michael, is this for the previous webpage?   (e.g. if I was on google.com and clicked home button to go to NTP, document would be for google.com?)

> 1. Native Pages don't hide the page under them, so they still think they're visible (easy to repro with NTP or recent tabs).

This is surprising to me in general... I would have thought once we navigated away from the real webpage that prior page would be considered hidden. 

TabImpl#loadUrl is where we #maybeShowNativePage as well as call WebContents#getNavigationController#loadUrl(). From a TabImpl perspective, I don't conceptually think of native pages as "hiding" the pages beneath them but rather as separate pages in the navigation stack that are displayed with Java UI instead of C++ renderer. (this is in contrast to things like "sad tab" which do actually take the place of the webpage and do _not_ have their own entry in the nav stack).


How/where does a document typically get marked as hidden? 

### mt...@chromium.org (2024-02-02)

> Michael, is this for the previous webpage?   (e.g. if I was on google.com and clicked home button to go to NTP, document would be for google.com?)

That's correct, the google.com document stays live (and thinks it's visible) under the NTP.

> TabImpl#loadUrl is where we #maybeShowNativePage as well as call WebContents#getNavigationController#loadUrl(). From a TabImpl perspective, I don't conceptually think of native pages as "hiding" the pages beneath them but rather as separate pages in the navigation stack that are displayed with Java UI instead of C++ renderer. (this is in contrast to things like "sad tab" which do actually take the place of the webpage and do _not_ have their own entry in the nav stack).

Maybe a more "correct" implementation would navigate the tab under the Native Page to about:blank so it's not live, and navigate back on the about:blank page when you navigate back on the Native Page. I'm guessing we don't do this for visual glitch reasons or performance reasons? Hiding the page is probably a reasonable compromise.

> How/where does a document typically get marked as hidden?

Cases I'm aware of are another tab becoming visible (which hides the previous one), or the activity becoming hidden.

### mt...@chromium.org (2024-02-02)

Noticed that this is already fixed on Canary, probably an unintentional fix in navigation stack? I'm bisecting.

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1519106?no_tracker_redirect=1

[Multiple monorail components: Mobile>Intents, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

### mt...@chromium.org (2024-02-05)

This was fixed by https://crbug.com/chromium/1220337. Do we want to consider back-porting this fix? +rakina

### ra...@google.com (2024-02-06)

Sure, we've been experimenting with navigation queueing since M119 and recently enabled it by default. Should we enable it on M119 onwards?

### mt...@chromium.org (2024-02-06)

Probably a question for our TPMs, but sgtm. I think just changing M121 behavior is sufficient though given it's already shipping on stable.

### am...@google.com (2024-02-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-14)

Thank you for your report. I've reduced the severity rating for this report due to the minimal impact and the low potential for exploitability or security implications to a user from this issue. Because we were able to make a security beneficial change due to your report, the Chrome VRP would like to extend to you a $500 thank you reward. A member of the p2p-vrp payments team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-05-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41492087)*
