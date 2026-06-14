# Security: fullscreen notification spoof (repro issue 882812)

| Field | Value |
|-------|-------|
| **Issue ID** | [40051242](https://issues.chromium.org/issues/40051242) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2020-01-15 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 81.0.4028.0 (Official Build) canary (64-bit)  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Go to <http://lbstyle.github.io/ni.html>
2. Click on the button

the bubble can show up over fullscreen mode and hide the fullscreen notification.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 336 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 717.1 KB)

## Timeline

### ct...@chromium.org (2020-01-16)

Can't repro on macOS, but can kind of repro on Windows. I managed to get this to partially trigger once, but now I can't repro it again (even after clearing browsing data, which should make the permission prompt show up again).

What I saw:
* Click button
* Fullscreen mode starts
* The permission prompt for registering a protocol handler is shown with a very long protocol string (web+moo<...>ooo).
* The full screen notification is shown over the top.

This is on a Windows Server 2016 VM (but I'm not sure why Windows 7 would make a difference there).

Reporter: Could you provide more steps for reproducing this, or a recording of what you're seeing when you test this on your machine?

### ch...@gmail.com (2020-01-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-16)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2020-01-16)

Thanks! I'm not sure why I can't repro it (might have something to do with my VM environment).

+engedy@ for permissions UI and +avi@ from the previous bug. Do we think there's an edge case missing from the previous fix, or is this a very particular race condition?

### pb...@google.com (2020-01-16)

Based on the bug report tagging the bug with OS - Windows and M81 labels for better tracking. 



### av...@chromium.org (2020-01-16)

We have dialogs kick windows out of fullscreen. I don’t recall if we made bubbles do so too. I think we should.

### av...@chromium.org (2020-01-16)

Browser::RegisterProtocolHandler() calls WebContents::ForSecurityDropFullscreen(), so we should be doing this already. Is it some kind of race?

### ct...@chromium.org (2020-01-16)

Yeah, I thought this would already be handled. The fact that I can't repro it locally makes me think it's a race.

### av...@chromium.org (2020-01-16)

I’m wondering if there’s a more general race with fullscreen; https://crbug.com/chromium/1020026 is something similar with a popup, where dropping fullscreen works fine on Mac/Linux but doesn’t consistently work on Windows.

Who knows fullscreen on Windows?

### ct...@chromium.org (2020-01-16)

+robliao@: Do you know who we should ask about Windows fullscreen? 

### ro...@chromium.org (2020-01-16)

Adding mgiuca@ and miu@ who own the ExclusiveAccessBubble per
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/exclusive_access/OWNERS

### es...@chromium.org (2020-01-21)

mgiuca or miu, could you please take a look? (Arbitrarily assigning to mgiuca to get an owner on this bug.)

Also, reporter: does this repro only on Canary/M81, or on earlier versions of Chrome as well?

[Monorail components: UI>Browser>FullScreen]

### ch...@gmail.com (2020-01-21)

This repro on all versions of Chrome. 
Shouldn’t be higher than Severity-Low as in https://crbug.com/chromium/882812 ?

### av...@chromium.org (2020-01-21)

I have a pretty slow machine, and I can repro this pretty well. It's definitely a race, as we're getting a request to show the bubble and then we're going fullscreen.

Idea to kill the race: Record the timestamp when WebContents::ForSecurityDropFullscreen() is called, whether or not the WebContents is in fullscreen. If a request for fullscreen comes in, if it's within n seconds of the call to ForSecurityDropFullscreen() then cancel it.

That value of n could be chosen to coincidentally match the duration of the showing of the fullscreen bubble, or it could not.

### av...@chromium.org (2020-01-21)

I’m pondering this.

Right now, the call chain looks like:

Blink’s FullscreenController::EnterFullscreen() → RenderFrameHostImpl::EnterFullscreen() → WebContentsImpl::EnterFullscreenMode().

The problem is that WebContentsImpl::EnterFullscreenMode() is what would say, “hey, wait, nope”, but this call chain assumes success all the way. The spec says that there is a fullscreenerror that can be fired, and that shows up in Fullscreen::ContinueRequestFullscreen(), but that’s only wired up for failures entirely within Blink. Right now, once the fullscreen check clears in Blink, Blink assumes that the browser’s _always_ able to successfully enter fullscreen.

I need to poke and see if there’s a good path back to return a failure to enter fullscreen.

### en...@chromium.org (2020-01-22)

An alternative approach here would be to close the currently visible permission prompt (and clear any queued permission requests) when entering web-initiated full screen mode. Any objections to that?

### en...@chromium.org (2020-01-22)

Independently of full screen, do we want to limit the maximum width of permission bubbles? I haven't seen any restrictions the maximum length of the protocol handler scheme, so I suppose we can't address the problem from that direction.

### sh...@chromium.org (2020-01-22)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2020-01-22)

Re https://crbug.com/chromium/1042210#c16:

So that would be, like, WebContentsDelegate::DidDropFullscreenForSecurity() to correspond to the WebContents::ForSecurityDropFullscreen()? Then we make Browser::DidDropFullscreenForSecurity() go through everything that could possibly be interfering with the bubble?

That’s possible, but I’m pondering https://crbug.com/chromium/1020026 where it looks like this is happening with a popup, we have the same race (I think) but I’m not sure that Browser could do something.

### av...@chromium.org (2020-01-22)

Another possibility is for the browser process to push the state of “fullscreen isn’t allowed until <time>” to the renderer, where fullscreen.cc’s RequestFullscreenConditionsMet() could deny it, but I’m not fond of pushing a security-type fix to the renderer.

### mg...@chromium.org (2020-01-22)

avi@ can I assign this to you? (Pre-emptively doing that..)

I haven't worked on this area for three years. I'd like to remove myself from OWNERS. Are you an appropriate replacement?

### av...@chromium.org (2020-01-23)

I’m totally a good owner for this bug.

I’m less sure about the fullscreen bubble in general.

### en...@chromium.org (2020-01-23)

Re https://crbug.com/chromium/1042210#c19:

Did you mean to write DidEnterFullscreenForSecurity? If yes, then that's indeed what I had in mind. We have a bunch of full-screen related methods [1] in WebContentsObserver, but it is not clear to me if any of them can be relied on for security measures.

Also, at the risk of stating the obvious, IIUC, the problem here is very basic compared to https://crbug.com/chromium/1020026, and there are no race conditions are involved. It is just that we only have logic in place to "kill fullscreen when a permission bubble is triggered", but no logic to "kill the permission bubble when fullscreen is triggered".

Re https://crbug.com/chromium/1042210#c20:

I would also be happy with that. We could still perform the authoritative check on the browser side, so it wouldn't be that bad. The only risk is that if we use asynchronous IPC to inform the renderer of state changes, Blink could be telling websites that going to fullscreen succeeded, when, in fact, it did not. But I don't really expect such a race to occur often during benevolent usage?

### av...@chromium.org (2020-01-23)

The thing with https://crbug.com/chromium/1042210#c19 is that setting up two parallel mechanisms, one in each direction, invites duplication errors, whereas making one mechanism work both backward and forward in time is simpler.

Re https://crbug.com/chromium/1042210#c20, creating yet another race feels like it’ll just punt variants of this bug forward in time for me-of-a-year-from-now to handle.

### av...@chromium.org (2020-01-27)

Re https://crbug.com/chromium/1042210#c14:

Yes. If we say "if there was a 'drop fullscreen for security' event less than five seconds ago, deny fullscreen" then that fixes this bug and 1020026.

There is some plumbing to be done there. As per https://crbug.com/chromium/1042210#c15, the renderer does all the checking and assumes that once it hands the request off to the browser it'll always succeed. I'm going to plumb the ability to say "no" in, and implement this.

### mi...@chromium.org (2020-01-27)

Hey avi@: You'll probably want to consult with the Blink/Web platform owners of fullscreen (that's not me).

I think there already is a mechanism for the browser to say "no," but it is a passive one:

1. Renderer requests fullscreen.
2. Browser receives request.
   a. If the answer is yes, it configures the native browser window for fullscreen and then notifies the renderer of a resize (and that message contains a "is fullscreen" bit set to true).
   b. If the answer is no, the request is simply ignored with no UI change (i.e., the renderer gets no resize message with the "is fullscreen" bit set).

That said, some massive changes to the IPC mechanism have been made over the past few years. I can't seem to locate the relevant IPCs. There used to be something like a ViewMostMsg_Resize IPC, which is gone now.

Also, I suppose I could be giving you old info about how this all works. I'd suggest tracing the code paths for the request to confirm whether the "no response means the answer is no" scheme still applies.


### av...@chromium.org (2020-01-27)

I'm chatting with dtapuska now. I'm definitely going to wire things properly so that the page knows it failed to enter fullscreen.

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d1d25656154f09c4c7a689aaa2df0044d5e02f93

commit d1d25656154f09c4c7a689aaa2df0044d5e02f93
Author: Avi Drissman <avi@chromium.org>
Date: Fri Mar 06 21:28:58 2020

Prevent fullscreen while dialogs are up (1/2)

Chromium already drops fullscreen when a dialog is first displayed.
Extend that behavior so that a WebContents may not enter fullscreen
for the duration of a dialog's display.

This is part 1: Extend the fullscreen IPC so that the browser can
decline a renderer's request to enter fullscreen.

Bug: 1042210, 1020026, 1037730
Change-Id: Iafba087b22c51bf3c8fb6f9a4ce02921d51f0044
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2041871
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#747870}

[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/frame_host/render_frame_host_delegate.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/frame_host/render_frame_host_delegate.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/frame_host/render_frame_host_impl.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/screen_orientation/screen_orientation_provider_unittest.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/content/browser/web_contents/web_contents_impl_unittest.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/public/mojom/frame/frame.mojom
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/frame/fullscreen_controller.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/frame/fullscreen_controller.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/fullscreen/fullscreen.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/fullscreen/fullscreen.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/html/media/html_media_element_event_listeners_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/html/media/html_video_element_persistent_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/html/media/video_auto_fullscreen_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/testing/fake_local_frame_host.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/core/testing/fake_local_frame_host.h
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/modules/media_controls/elements/media_control_display_cutout_fullscreen_button_element_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/modules/media_controls/media_controls_display_cutout_delegate_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/modules/media_controls/media_controls_orientation_lock_delegate_test.cc
[modify] https://crrev.com/d1d25656154f09c4c7a689aaa2df0044d5e02f93/third_party/blink/renderer/modules/media_controls/media_controls_rotate_to_fullscreen_delegate_test.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee

commit 1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee
Author: Avi Drissman <avi@chromium.org>
Date: Tue Mar 10 18:56:45 2020

Prevent fullscreen while dialogs are up (2/2)

Chromium already drops fullscreen when a dialog is first displayed.
Extend that behavior so that a WebContents may not enter fullscreen
for the duration of a dialog's display.

This is part 2: Modify WebContents::ForSecurityDropFullscreen() to
support a span of time that fullscreen is prohibited and modify all
callers to correctly request that span.

Bug: 1042210, 1020026, 1037730
Change-Id: I9d2ccc1e459cf37bfbf3499063d87d93ef9910e8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2044658
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#748808}

[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/custom_handlers/register_protocol_handler_permission_request.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/custom_handlers/register_protocol_handler_permission_request.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/chrome_native_file_system_permission_context.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/native_file_system_permission_request_manager.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/native_file_system_permission_request_manager.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/origin_scoped_native_file_system_permission_context.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/native_file_system/tab_scoped_native_file_system_permission_context.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/permissions/permission_request_manager_browsertest.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/browser.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/native_file_system_dialogs.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/native_file_system_dialogs.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/views/native_file_system/native_file_system_directory_access_confirmation_view.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/views/native_file_system/native_file_system_directory_access_confirmation_view.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/chrome/browser/ui/views/native_file_system/native_file_system_directory_access_confirmation_view_browsertest.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/BUILD.gn
[add] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/file_chooser_impl.cc
[add] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/file_chooser_impl.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/render_frame_host_delegate.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/render_frame_host_delegate.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/native_file_system/file_system_chooser.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/native_file_system/file_system_chooser.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/native_file_system/file_system_chooser_unittest.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/native_file_system/native_file_system_manager_impl.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/1a55a9d654522ebc4d54baa0aa0b8a9697e3c1ee/content/public/browser/web_contents.h


### av...@chromium.org (2020-03-10)

I believe these changes should fix this. PTAL and let me know.

### ch...@gmail.com (2020-03-11)

Fixed on 82.0.4083.0 Canary.

### av...@chromium.org (2020-03-11)

Whoo!!!!

### [Deleted User] (2020-03-11)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-16)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-03-20)

Shouldn't be higher than low severity as in https://crbug.com/chromium/882812? Thanks.

### na...@google.com (2020-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-26)

Congrats! The Panel decided to award $500 for this report! 

### na...@google.com (2020-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1042210?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051242)*
