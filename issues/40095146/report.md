# Security: Leaking autofill password through XSS, bypassing Chrome protection

| Field | Value |
|-------|-------|
| **Issue ID** | [40095146](https://issues.chromium.org/issues/40095146) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | li...@gmail.com |
| **Assignee** | mu...@chromium.org |
| **Created** | 2019-05-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to leak autofilled/saved passwords in Chrome, even though there are protections against it.

**VERSION**  

Chrome Version: Version 74.0.3729.157 (Official Build) (64-bit)  

Operating System: OSX

**REPRODUCTION CASE**  

I created a login page here: <https://playground.zulln.se/poc/peterlogin/login.html>  

And a intentional XSS here: <https://playground.zulln.se/poc/peterlogin/xss.html>

Hosting the PoC on another domain here: <http://wwwxdropbox.com/poc/peterlogin/iframeleak.html>

If you click on the link or location.href the browser will not leak the autofilled password until any userinteraction on the page. However, if you click window.open-option it does.

This only works if you open the popup from within an iframe, so going to leak.html directly will not work.

All those files has also been attached to this report.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Linus Särud

## Attachments

- [peterlogin.zip](attachments/peterlogin.zip) (application/octet-stream, 3.6 KB)

## Timeline

### ts...@chromium.org (2019-05-23)

The problem isn't the XSS per-se, but rather if the autofiller is autofilling without a user gesture.

Embargo since report contains a link to a live site (even though owned by reporter).

[Monorail components: UI>Browser>Autofill]

### sh...@chromium.org (2019-05-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-07)

rogerm: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2019-06-07)

[Empty comment from Monorail migration]

### ba...@chromium.org (2019-06-07)

Mustaq, I saw you working on LocalFrameClientImpl::NotifyUserActivation(), which is the trigger that tells the password manager that there was a user gesture. Could you please take a look at this? This looks OOPIF related to me.

### ba...@chromium.org (2019-06-07)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-07)

(removing SecurityEmbargo given the live site is just a demo)

### rd...@chromium.org (2019-06-07)

Thanks for the report, Linus!  We're investigating a number of angles.  Quick question: are you able to reproduce this in a profile with no extensions installed?

### li...@gmail.com (2019-06-07)

Hm, I definitely was. Created a new profile for it which worked.

However, I now fail to reproduce this. I am pretty sure it worked by entering the URL directly in the address bar as well (which has no security implications), which does not work anymore either.

I have updated Chrome since the initial report, so possible this just got fixed somehow. Guess you could close this if you also fail to reproduce.

### rd...@chromium.org (2019-06-07)

In our testing, we noticed that it reproduced flakily, with different effectiveness on different profiles.  We'll continue digging to see if we can get to the bottom of it.  But if you were able to originally repro with no extensions, sounds like it's probably not any of the weirdness we do with those user gestures.

Thanks for the quick response!

### va...@chromium.org (2019-06-07)

I failed to reproduce in Chromium in any configuration. However, it's reproducible on Linux official branded build on ToT. Unfortunately StackTrace doesn't print anything  useful even with symbol_level=2.

### mu...@chromium.org (2019-06-10)

Thanks rdevlin.cronin@ for confirming that extension messaging is not related.

vasilii@: I presume Linux non-official builds didn't repro this for you, right?  Do you know if official build has any known difference in PWM behavior?


### ba...@chromium.org (2019-06-10)

The Password Manager relies on API keys but besides that there is no intended difference.

### va...@chromium.org (2019-06-11)

I think it's about speed optimization of the program. Even on Official Linux I can reproduce the bug after at least ~5 tries. Maybe I didn't try long enough otherwise.

### mu...@chromium.org (2019-06-11)

I was able to repro consistently every time when the following conditions are met on official Dev/Beta/Stable builds:
[A] There has to be a keyboard input (mouse click activation doesn't work).
[B] The "window.open" button has to be clicked within 5 sec of [A] (i.e. before the expiry of transient user activation).

This is mysterious in two different ways:
1. From user activation perspective, there is no difference between mouse/keyboard.  I tried focusing the top frame or the child frame before [A]; keyboard input works all the time, mouse never works.
2. The newly opened window gets transient activation (navigator.userActivation.isActive) even with mouse click in [A].  (To test this in console, remember to turn off "Evaluate triggers user activation" option in console M76+.)

Can't repro on my local builds so still not sure who triggers activation notification.

### mu...@chromium.org (2019-06-11)

Slight correction to my #2 above: the newly opened window gets sticky activation (navigator.userActivation.hasBeenActive) only with keyboard input in [A].
(We have to open devtools using the menu to see this, otherwise the devtools hotkey activates the window.)

So there is really one mystery here: why keyboard activation state propagates to the new window and not mouse activation.


### mu...@chromium.org (2019-06-12)

I tried to debug further through a local official build, but the consistent repro steps for Dev/Beta/Stable (as in #16) doesn't work even on local official build.

### mu...@chromium.org (2019-06-13)

All my attempt to repro on a local build failed.  Without a stack trace, I can't proceed further.

visilii@: As per https://crbug.com/chromium/966562#c12, you were able to repro at least some of the time.  Could you check if you can grab the stack trace of LocalFrameClientImpl::NotifyUserActivation() when the bug reproduces?

### mu...@chromium.org (2019-06-13)

FYI: note that the steps https://crbug.com/chromium/966562#c16 repro consistently on Dev/Beta/Stable for me.  Just press <tab>s to focus the "window.open" button, then press <space>.

### va...@chromium.org (2019-06-13)

I wish I could. Unfortunately StackTrace didn't print anything interesting.

Tom, is it possible to get a stack trace in the renderer from locally built Official Linux Chrome? If it's not possible then may be there is a way to do it for official builds on other platforms?

### th...@chromium.org (2019-06-13)

Are you running the stripped binary?  If you have "symbol_level=2", StackTrace should do what you want.

Maybe if you run something like "stress -c 200" in the background while Chrome is running, the issue will be more easily reproducible?

### ba...@chromium.org (2019-06-17)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-06-17)

It just prints #0 0x562f0ccf6f79 <unknown> with "symbol_level=2". Right now I didn't reproduce it.

### jo...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### jo...@chromium.org (2019-06-18)

I can shed some light on the keyboard vs mouse thing:

There are three events per user interaction mousedown/click/mouseup and rawkeydown/key/rawkeyup

For mouse, we tie those three interactions together to one user activation by tracking the token here: https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/input/event_handler.h?rcl=172dccb9f76312aabc914be9dc0b8a93d6a20b75&l=451

For key events, we don't do that (which is probably a bug). I suspect that either the rawdown or key event create the new window, so at least the key up will create a new user activation, even though window.open should already have consumed it.

### mu...@chromium.org (2019-06-18)

jochen@: I think the situation is more complicated than that, it's more than just "joining" interactions.  When I am able to repro consistently with keyboard (see https://crbug.com/chromium/966562#c16), I can hit some random key (say "a"), wait a second, then click /with mouse/ on the button to open the popup.  Somehow the keyboard interaction in the first window still leaks to the second.  I couldn't dig out any more info!


### jo...@chromium.org (2019-06-18)

yeah, I didn't mean to imply that this is the only bug here, but just wanted to record that part of the problem appears to be the missing tracking of tokens for key presses..

I'll leave more comments when I get around to debug this more.

### mu...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-06-21)

I added a CHECK(false) to the appropriate place. The problem is now quite difficult to reproduce so I tried around 20 times. As I reproduced it, the crash was uploaded with ID 6254fc7336d736f6. Then I took the binary addresses from there and pushed them to 'addr2line' :
$ addr2line -C -f -e out/Release/chrome -C -p  0x083326f4  0x07364b0b 0x07570155 0x072c356c 0x0787900b 0x072c7262 0x085f5383 0x085e9fd0 0x0854c15f 0x0854b39e 0x0421bb42 0x0422b816

The stack trace is 
autofill::PasswordAutofillAgent::UserGestureObserved()::$_0::operator()() const at ./../../components/autofill/content/renderer/password_autofill_agent.cc:1086 (discriminator 6)
blink::LocalFrame::NotifyUserActivation(blink::LocalFrame*, blink::UserGestureToken::Status) at ./../../third_party/blink/renderer/core/frame/local_frame.cc:1525 (discriminator 4)
blink::KeyboardEventManager::KeyEvent(blink::WebKeyboardEvent const&) at ./../../third_party/blink/renderer/core/input/keyboard_event_manager.cc:189 (discriminator 2)
blink::WebViewImpl::HandleKeyEvent(blink::WebKeyboardEvent const&) at ./../../third_party/blink/renderer/core/exported/web_view_impl.cc:725 (discriminator 2)
blink::PageWidgetDelegate::HandleInputEvent(blink::PageWidgetEventHandler&, blink::WebCoalescedInputEvent const&, blink::LocalFrame*) at ./../../third_party/blink/renderer/core/page/page_widget_delegate.cc:151 (discriminator 2)
blink::WebViewImpl::HandleInputEvent(blink::WebCoalescedInputEvent const&) at ./../../third_party/blink/renderer/core/exported/web_view_impl.cc:1794
content::RenderWidgetInputHandler::HandleInputEvent(blink::WebCoalescedInputEvent const&, ui::LatencyInfo const&, base::OnceCallback<void (content::InputEventAckState, ui::LatencyInfo const&, std::__1::unique_ptr<ui::DidOverscrollParams, std::__1::default_delete<ui::DidOverscrollParams> >, base::Optional<cc::TouchAction>)>) at ./../../content/renderer/input/render_widget_input_handler.cc:422 (discriminator 2)
non-virtual thunk to content::RenderWidget::HandleInputEvent(blink::WebCoalescedInputEvent const&, ui::LatencyInfo const&, base::OnceCallback<void (content::InputEventAckState, ui::LatencyInfo const&, std::__1::unique_ptr<ui::DidOverscrollParams, std::__1::default_delete<ui::DidOverscrollParams> >, base::Optional<cc::TouchAction>)>) at ./../../content/renderer/render_widget.cc:1006 (discriminator 4)
content::QueuedWebInputEvent::Dispatch(content::MainThreadEventQueue*) at ./../../content/renderer/input/main_thread_event_queue.cc:627 (discriminator 2)
content::MainThreadEventQueue::DispatchEvents() at ./../../content/renderer/input/main_thread_event_queue.cc:422 (discriminator 4)
base::TaskAnnotator::RunTask(char const*, base::PendingTask*) at ./../../base/callback.h:97 (discriminator 6)
base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) at ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:368 (discriminator 2)


### mu...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-06-24)

The way to reproduce the bug is to press F5 and then quickly click the button. Deleting all browsing history increases the probability a lot.
For the stack trace above the event generating it is F5 key up:
[1:1:0624/153406.420490:INFO:keyboard_event_manager.cc(192)]  KeyboardEventManager::KeyEvent type=9, modifiers=1024, windows_key_code=116, dom_code=458814,  dom_key=2099205,  unmodified_text=0 0

I don't know why it was sent to the new tab actually. I definitely release it before the mouse click.

However, there is some other path different from https://crbug.com/chromium/966562#c30. It doesn't involve KeyboardEventManager::KeyEvent but still results in user action.

### va...@chromium.org (2019-06-24)

I debugged the code path from https://crbug.com/chromium/966562#c30. One needs to release F5 and mouse-left approximately simultaneously. The browser indeed sends the F5 Up event to the new tab causing user gesture.
[116235:116235:0624/174628.137070:INFO:web_contents_impl.cc(2316)] WebContentsImpl::PreHandleKeyboardEvent URLs https://playground.zulln.se/poc/peterlogin/xss.html#PGZvcm0gaWQ9ImZvciIgYWN0aW9uPSIiIG1ldGhvZD0iR0VUIj4KCTxpbnB1dCBpZD0idXNlciIgdHlwZT0idXNlcm5hbWUiIGlkPSJ1c2VybmFtZSI+Cgk8aW5wdXQgaWQ9InBhc3N3b3JkIiB0eXBlPSJwYXNzd29yZCIgaWQ9InBhc3N3b3JkIj4KCTxpbnB1dCB0eXBlPSJzdWJtaXQiPgo8L2Zvcm0+CgoKPHN2ZyBvbmxvYWQ9JwoJc2V0VGltZW91dChmdW5jdGlvbigpewoJCXB3ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInBhc3N3b3JkIikudmFsdWU7CgkJYWxlcnQoInlvdXIgcGFzc3dvcmQ6ICIgKyBwdyk7Cgl9LCAxMDAwKQonPg==

 With this I have 2 questions to knowledgeable people:
- How is a sole key-up event considered a user gesture?
- Why isn't F5 fully consumed by the browser as an accelerator?

Still trying trying to investigate a second path not involving KeyboardEventManager::KeyEvent.

### mu...@chromium.org (2019-06-24)

I agree both of these are bad!  But I don't think anyone have definitive answers.  These are old behavior, and I know that avi@ felt the "compat pain" of trying to fix this.

I have seen other user activation bugs related to keyup on F5 or on Ctrl-R, suggested a few things to try here: https://crbug.com/chromium/709765#c26.  Still need an expert opinion.


### va...@chromium.org (2019-06-24)

Bad news. There is another code path easily reproducible.
- open the "http://wwwxdropbox.com/poc/peterlogin/iframeleak.html" tab
- clear browsing data.
- refresh the tab
- any time later click the button.

Here is the stack trace in the renderer:
autofill::PasswordAutofillAgent::UserGestureObserved() at password_autofill_agent.cc:?
blink::LocalFrame::NotifyUserActivation(blink::LocalFrame*, blink::UserGestureToken::Status) at local_frame.cc:?
blink::WebScopedUserGesture::WebScopedUserGesture(blink::WebLocalFrame*) at web_scoped_user_gesture.cc:?
extensions::NativeRendererMessagingService::DeliverMessageToScriptContext(extensions::Message const&, extensions::PortId const&, extensions::ScriptContext*) at native_renderer_messaging_service.cc:?
extensions::ScriptContextSet::ForEach(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::RenderFrame*, base::RepeatingCallback<void (extensions::ScriptContext*)> const&) at script_context_set.cc:?
extensions::ScriptContextSetIterable::ForEach(content::RenderFrame*, base::RepeatingCallback<void (extensions::ScriptContext*)> const&) at script_context_set_iterable.cc:?
extensions::NativeRendererMessagingService::DeliverMessage(extensions::ScriptContextSetIterable*, extensions::PortId const&, extensions::Message const&, content::RenderFrame*) at native_renderer_messaging_service.cc:?
extensions::ExtensionFrameHelper::OnMessageReceived(IPC::Message const&) at extension_frame_helper.cc:?
content::RenderFrameImpl::OnMessageReceived(IPC::Message const&) at render_frame_impl.cc:?
IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) at ipc_channel_proxy.cc:?

The actual message is:
[1:1:0624/184224.597456:INFO:native_renderer_messaging_service.cc(323)] Extension message="{\"passwordLengths\":[]}"

In the browser the stack trace is 
$ addr2line -C -f -e out/Release/chrome -C -p 0x02f33581 0x02f3428f 0x02f33110 0x02f334ff 0x02f377a3 0x02e26396 0x0421cbf2 0x0422c8c6 0x0422c5c7 0x041e9925
extensions::ExtensionMessagePort::BuildDeliverMessageIPC(extensions::Message const&, extensions::ExtensionMessagePort::IPCTarget const&)::$_1::operator()() const at ./../../extensions/browser/api/messaging/extension_message_port.cc:533 (discriminator 6)
base::internal::Invoker<base::internal::BindState<std::__1::unique_ptr<IPC::Message, std::__1::default_delete<IPC::Message> > (extensions::ExtensionMessagePort::*)(extensions::Message const&, extensions::ExtensionMessagePort::IPCTarget const&), base::internal::UnretainedWrapper<extensions::ExtensionMessagePort>, extensions::Message>, std::__1::unique_ptr<IPC::Message, std::__1::default_delete<IPC::Message> > (extensions::ExtensionMessagePort::IPCTarget const&)>::Run(base::internal::BindStateBase*, extensions::ExtensionMessagePort::IPCTarget const&) [clone .cfi] at ./../../base/bind_internal.h:499 (discriminator 10)
extensions::ExtensionMessagePort::SendToPort(base::RepeatingCallback<std::__1::unique_ptr<IPC::Message, std::__1::default_delete<IPC::Message> > (extensions::ExtensionMessagePort::IPCTarget const&)>) at ./../../base/callback.h:131 (discriminator 8)
extensions::ExtensionMessagePort::DispatchOnMessage(extensions::Message const&) at ./../../extensions/browser/api/messaging/extension_message_port.cc:301 (discriminator 2)
extensions::MessageService::PostMessage(extensions::PortId const&, extensions::Message const&) at ./../../extensions/browser/api/messaging/message_service.cc:771 (discriminator 4)
extensions::ExtensionMessageFilter::OnMessageReceived(IPC::Message const&) at ./../../extensions/browser/extension_message_filter.cc:469 (discriminator 4)
base::TaskAnnotator::RunTask(char const*, base::PendingTask*) at ./../../base/callback.h:97 (discriminator 6)
base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) at ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:368 (discriminator 2)
base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() at ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219
_ZN4base12_GLOBAL__N_118WorkSourceDispatchEP8_GSourcePFiPvES3_$5e831a5ebb069a716f2a7de0faa6ae62.cfi at ./../../base/message_loop/message_pump_glib.cc:256 (discriminator 4)

### mu...@chromium.org (2019-06-24)

Thanks vasilii@, for helping us link this to two root causes.  We knew about both bugs separately, still haven't figured out any solution for any of them :(
[a] Extension messaging (https://crbug.com/chromium/957633) is the cause for the easier-to-repro path (as per https://crbug.com/chromium/966562#c35).
[b] Keyup user activation on hotkeys (https://crbug.com/chromium/709765) is hard to repro here (as per https://crbug.com/chromium/966562#c33) but it has other dependencies.

For this particular bug, [a] is more important.  But [b] is also important for other cases.

### rd...@chromium.org (2019-06-24)

[a] would be solved if we could optionally restrict a user gesture to a particular v8 context.  Is that doable?

### mu...@chromium.org (2019-06-24)

Let's discuss this in https://crbug.com/chromium/957633.

### va...@chromium.org (2019-06-26)

To me [b] is more important. The attack vector:
- on evil site the user it tricked to press any key.
- on keydown a new window/tab is opened with a legitimate page.
- keyup is handled in the new tab causing the password being revealed.
- the evil site can steal the password and close the tab.

It all happens instantaneously.

### mu...@chromium.org (2019-07-02)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-07-09)

For [b], we need to fix only a part of https://crbug.com/chromium/709765 (key up only).  Filed a new bug for that.

### mu...@chromium.org (2019-07-10)

https://crbug.com/chromium/982413 is now fixed, so keyup activation trigger [b] is now gone.

Now we will need to focus on the remaining cause [a] through https://crbug.com/chromium/957633.





### li...@chromium.org (2019-08-07)

Friendly ping from the security marshal. Just want to make sure active progress is being made to close out this bug. Thanks!

### mk...@chromium.org (2019-08-07)

[Empty comment from Monorail migration]

### nz...@chromium.org (2019-08-08)

This bug has two parts. One parts was addressed as part of https://crbug.com/chromium/982413 (which seems to be more serious compared to the other case) and the other one is being discussed in https://crbug.com/chromium/957633. So I'll close this for now.

### sh...@chromium.org (2019-08-08)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-13)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M77. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-13)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nz...@chromium.org (2019-08-13)

There is no need for merge as https://crbug.com/chromium/982413 already landed before branching of 77. Maybe I should have marked this bug as duplicate to disable this automatic flow.

### sh...@chromium.org (2019-08-14)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-10-09)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-10-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-10)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 91 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-10)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-18)

Congrats! The Panel decided to reward $1,000 for this report

### na...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/966562?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/982413]
[Monorail blocking: crbug.com/chromium/957633]
[Monorail mergedinto: crbug.com/chromium/982413]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095146)*
