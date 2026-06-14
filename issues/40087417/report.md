# Bad-cast to sandbox::bpf_dsl::(anonymous namespace)::ReturnResultExprImpl from invalid vptr;blink::ApplyStyleCommand::applyRelativeFontStyleChange;blink::ApplyStyleCommand::doApply

| Field | Value |
|-------|-------|
| **Issue ID** | [40087417](https://issues.chromium.org/issues/40087417) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Editing |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | yo...@chromium.org |
| **Created** | 2017-04-21 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=4596915422625792

Fuzzer: miaubiz_css_fuzzer
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f80890118c0
Crash State:
  Bad-cast to sandbox::bpf_dsl::(anonymous namespace)::ReturnResultExprImpl from invalid vptr
  blink::ApplyStyleCommand::applyRelativeFontStyleChange
  blink::ApplyStyleCommand::doApply
  
Sanitizer: cfi (CFI)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_cfi_chrome&range=460787:460815

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4596915422625792


Additional requirements: Requires Gestures

Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### me...@chromium.org (2017-04-21)

Nothing in the regression range stands out to me. 

[Monorail components: Blink>Editing]

### sh...@chromium.org (2017-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-22)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-23)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-04-24)

yosin: Can you please take a look or reassign as appropriate? Thanks.

### go...@chromium.org (2017-04-25)

A friendly reminder that M59 Beta  launch is coming soon! Your bug is labelled as Release Block Beta. All fixes need to be merged into the release branch (3071) latest by tomorrow, 04/26 4:00 PM PT in order to make into the desktop Beta final build cut. Thank you!

### aw...@google.com (2017-04-26)

[Empty comment from Monorail migration]

### yo...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

### yo...@chromium.org (2017-04-27)

Lower to Pri-2, since this issue caused by unusual HTML.

### sh...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-04-27)

+awhalley@, will this be a blocker for M58 Stable AU ramp up or respin?

### aw...@google.com (2017-04-27)

Nope, the milestone was set incorrectly. Fixed.

### pa...@chromium.org (2017-04-27)

#10: The idea is that malicious web page authors would purposefully write such unusual HTML, and cause the renderer to follow a bad virtual function pointer, giving the attacker control of the renderer process.

ojan, can you please take a look or assign a reasonable owner? Thanks!

### pa...@chromium.org (2017-04-27)

Also, it seems like perhaps CF is wrong, and this should be High severity.

### yo...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### yo...@chromium.org (2017-04-28)

Hit DCHECK(a.IsNotNull()) in ComparePositions(a, b) where both |a| and |b| are null position.

Here is stack trace:
ComparePositions(const blink::PositionTemplate<blink::EditingAlgorithm<blink::NodeTraversal> > & a, const blink::PositionTemplate<blink::EditingAlgorithm<blink::NodeTraversal> > & b) Line 260
>	ApplyStyleCommand::ApplyRelativeFontStyleChange(blink::EditingStyle * style, blink::EditingState * editing_state) Line 377
ApplyStyleCommand::DoApply(blink::EditingState * editing_state) Line 215
CompositeEditCommand::ApplyCommandToComposite(blink::EditCommand * command, blink::EditingState * editing_state) Line 191
CompositeEditCommand::ApplyStyle(const blink::EditingStyle * style, blink::EditingState * editing_state) Line 230
InsertTextCommand::DoApply(blink::EditingState * editing_state) Line 281
CompositeEditCommand::ApplyCommandToComposite(blink::CompositeEditCommand * command, const blink::VisibleSelectionTemplate<blink::EditingAlgorithm<blink::NodeTraversal> > & selection, blink::EditingState * editing_state) Line 212
TypingCommand::InsertTextRunWithoutNewlines(const WTF::String & text, bool select_inserted_text, blink::EditingState * editing_state) Line 618
TypingCommand::InsertText(const WTF::String & text, bool select_inserted_text, blink::EditingState * editing_state) Line 578
TypingCommand::DoApply(blink::EditingState * editing_state) Line 489
CompositeEditCommand::Apply() Line 143
TypingCommand::InsertText(blink::Document & document, const WTF::String & text, const blink::SelectionTemplate<blink::EditingAlgorithm<blink::NodeTraversal> > & passed_selection_for_insertion, unsigned int options, blink::TypingCommand::TextCompositionType composition_type, const bool is_incremental_insertion, blink::InputEvent::InputType input_type) Line 391
Editor::InsertTextWithoutSendingTextEvent(const WTF::String & text, bool select_inserted_text, blink::TextEvent * triggering_event, blink::InputEvent::InputType input_type) Line 1094
Editor::HandleTextEvent(blink::TextEvent * event) Line 287
EventHandler::DefaultTextInputEventHandler(blink::TextEvent * event) Line 2038
Node::DefaultEventHandler(blink::Event * event) Line 2289
HTMLElement::DefaultEventHandler(blink::Event * event) Line 1100
EventDispatcher::DispatchEventPostProcess(blink::EventDispatchHandlingState * pre_dispatch_event_handler_result) Line 288
EventDispatcher::Dispatch() Line 163
EventDispatchMediator::DispatchEvent(blink::EventDispatcher & dispatcher) Line 52
EventDispatcher::DispatchEvent(blink::Node & node, blink::EventDispatchMediator * mediator) Line 59
Node::DispatchEventInternal(blink::Event * event) Line 2144
EventTarget::DispatchEvent(blink::Event * event) Line 474
EventHandler::HandleTextInputEvent(const WTF::String & text, blink::Event * underlying_event, blink::TextEventInputType input_type) Line 2034
Editor::InsertText(const WTF::String & text, blink::KeyboardEvent * triggering_event) Line 1067
Editor::HandleEditingKeyboardEvent(blink::KeyboardEvent * evt) Line 84
Editor::HandleKeyboardEvent(blink::KeyboardEvent * evt) Line 89
KeyboardEventManager::DefaultKeyboardEventHandler(blink::KeyboardEvent * event, blink::Node * possible_focused_node) Line 302
EventHandler::DefaultKeyboardEventHandler(blink::KeyboardEvent * event) Line 1980
Node::DefaultEventHandler(blink::Event * event) Line 2273
HTMLElement::DefaultEventHandler(blink::Event * event) Line 1100
EventDispatcher::DispatchEventPostProcess(blink::EventDispatchHandlingState * pre_dispatch_event_handler_result) Line 288
EventDispatcher::Dispatch() Line 163
EventDispatchMediator::DispatchEvent(blink::EventDispatcher & dispatcher) Line 52
EventDispatcher::DispatchEvent(blink::Node & node, blink::EventDispatchMediator * mediator) Line 59
Node::DispatchEventInternal(blink::Event * event) Line 2144
EventTarget::DispatchEvent(blink::Event * event) Line 474
KeyboardEventManager::KeyEvent(const blink::WebKeyboardEvent & initial_key_event) Line 213
EventHandler::KeyEvent(const blink::WebKeyboardEvent & initial_key_event) Line 1975
blink_web.dll!blink::WebViewImpl::HandleCharEvent(const blink::WebKeyboardEvent & event) Line 1266
blink_web.dll!blink::PageWidgetDelegate::HandleInputEvent(blink::PageWidgetEventHandler & handler, const blink::WebCoalescedInputEvent & coalesced_event, blink::LocalFrame * root) Line 185
blink_web.dll!blink::WebViewImpl::HandleInputEvent(const blink::WebCoalescedInputEvent & coalesced_event) Line 2243
blink_web.dll!blink::WebViewFrameWidget::HandleInputEvent(const blink::WebCoalescedInputEvent & event) Line 94
content.dll!content::RenderWidgetInputHandler::HandleInputEvent(const blink::WebCoalescedInputEvent & coalesced_event, const ui::LatencyInfo & latency_info, content::InputEventDispatchType dispatch_type) Line 315
content.dll!content::RenderWidget::HandleInputEvent(const blink::WebCoalescedInputEvent & input_event, const ui::LatencyInfo & latency_info, content::InputEventDispatchType dispatch_type) Line 831
content.dll!content::RenderViewImpl::HandleInputEvent(const blink::WebCoalescedInputEvent & input_event, const ui::LatencyInfo & latency_info, content::InputEventDispatchType dispatch_type) Line 2667
content.dll!content::MainThreadEventQueue::HandleEventOnMainThread(const blink::WebCoalescedInputEvent & event, const ui::LatencyInfo & latency, content::InputEventDispatchType dispatch_type) Line 511
content.dll!content::QueuedWebInputEvent::Dispatch(content::MainThreadEventQueue * queue) Line 122
content.dll!content::MainThreadEventQueue::DispatchEvents() Line 392


### yo...@chromium.org (2017-04-28)

Here is DOM tree at DCHECK().
It seems CF attempt to replace OPTION element, outside of SELECT, by typed character.

BODY (editable) (focused)
SE	OPTION id="el0" (editable)
SE		#shadow-root
SE			#text "s\u817D\u441D\u2F57\uB8E3\u7E5D329736360\u7D5D\uBB48\u3804\uFAFB"
		#text "s"
		Q id="el2" (editable)
			INPUT id="el12" (editable)
				#shadow-root
					INPUT
						#shadow-root
							#text "Choose File"
			INPUT id="el13" (editable)
				#shadow-root
					#text "Reset"
			DATALIST id="el14" (editable)
				OPTION (editable)
					#shadow-root
						#text "\u817D\u441D\u2F57\uB8E3\u7E5D"
					#text "\u817D\u441D\u2F57\uB8E3\u7E5D"
				OPTION (editable)
					#shadow-root
						#text "329"
					#text "329"
				OPTION (editable)
					#shadow-root
						#text "736"
					#text "736"
				OPTION (editable)
					#shadow-root
						#text "360"
					#text "360"
				OPTION (editable)
					#shadow-root
						#text "\u7D5D\uBB48\u3804\uFAFB"
					#text "\u7D5D\uBB48\u3804\uFAFB"
		SUBMIT id="el6" (editable)
		INPUT id="el10" (editable)
			#shadow-root
				INPUT
					#shadow-root
						#text "Choose File"
		OUTPUT id="el11" (editable)
			INPUT id="el15" (editable)
				#shadow-root
					DIV id="inner-editor"
	CANVAS id="el1" style="width: 731px; height: 676px;" (editable)
	Q id="el3" (editable)
		<pseudo:before>
		<pseudo:after>
		WBR id="el4" (editable)
			B id="el5" (editable)
		Q id="el8" (editable)
			<pseudo:before>
			<pseudo:after>
		SPAN id="el9" (editable)
	CANVAS id="el7" style="width: 832px; height: 737px;" (editable)

### yo...@chromium.org (2017-04-28)

Here is minimal test case:

<!doctype html>
<div contenteditable><option></option></div>
<script>
const selection = getSelection();
selection.collapse(document.querySelector('option'), 0);
document.execCommand('bold');
document.execCommand('insertText', false, 'x');
</script>
</body>


We need to have "bold" command, to register typing style to apply typing style to
"insertText".

InsertTextCommand::DoApply() {
  ...
  // Handle the case where there is a typing style.
  if (EditingStyle* typing_style =
          GetDocument().GetFrame()->GetEditor().TypingStyle()) {
    typing_style->PrepareToApplyAt(end_position,
                                   EditingStyle::kPreserveWritingDirection);
    if (!typing_style->IsEmpty()) {
      ApplyStyle(typing_style, editing_state);
      if (editing_state->IsAborted())
        return;
    }
  }
  ...
}

We don't need to call ApplyStyle() when EndingSelection().IsNone()




### yo...@chromium.org (2017-04-28)

In review: http://crrev.com/2847763004

### bu...@chromium.org (2017-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4109e96377e75873e2e92308464313c0ff8f8008

commit 4109e96377e75873e2e92308464313c0ff8f8008
Author: yosin <yosin@chromium.org>
Date: Fri Apr 28 18:55:16 2017

Add DCHECK() to check ApplyStyleCommand::DoApply() to work on non-null range

This patch add DCHECK into |ApplyStyleCommand::DoApply()| to verify that we
don't apply |ApplyStyleCommand| to empty range to detect redundant command
execution for improving code health.

Actually, |ApplyStyleCommand::DoApply()| doesn't work with empty range, it
causes DCHECK for |Position.IsNull()| in |ComparePositions()|.

BUG=714311
TEST=n/a; no behavior changes

Review-Url: https://codereview.chromium.org/2848823002
Cr-Commit-Position: refs/heads/master@{#468077}

[modify] https://crrev.com/4109e96377e75873e2e92308464313c0ff8f8008/third_party/WebKit/Source/core/editing/commands/ApplyStyleCommand.cpp


### bu...@chromium.org (2017-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/89209614959b6d3b2d4c4e8b015232663b4fcd87

commit 89209614959b6d3b2d4c4e8b015232663b4fcd87
Author: yosin <yosin@chromium.org>
Date: Fri Apr 28 18:58:01 2017

Make InsertTextCommand not to apply typing style for empty selection

This patch makes |InsertTextCommand::DoApply()| not to call |ApplyStyle()| for
applying typing style when selection after inserting text is empty since
|ApplyStyle()| doesn't work with empty selection.

The https://crbug.com/chromium/714311 and the attached test case insert text into OPTION element to
get empty selection after insertion, since we can't place selection inside
OPTION element.

BUG=714311
TEST=run_webkit_unit_tests --gtest_filter=InsertTextCommandTest.WithTypingStyle

Review-Url: https://codereview.chromium.org/2847763004
Cr-Commit-Position: refs/heads/master@{#468080}

[modify] https://crrev.com/89209614959b6d3b2d4c4e8b015232663b4fcd87/third_party/WebKit/Source/core/editing/BUILD.gn
[modify] https://crrev.com/89209614959b6d3b2d4c4e8b015232663b4fcd87/third_party/WebKit/Source/core/editing/commands/InsertTextCommand.cpp
[add] https://crrev.com/89209614959b6d3b2d4c4e8b015232663b4fcd87/third_party/WebKit/Source/core/editing/commands/InsertTextCommandTest.cpp


### cl...@chromium.org (2017-04-29)

ClusterFuzz has detected this issue as fixed in range 468000:468086.

Detailed report: https://clusterfuzz.com/testcase?key=4596915422625792

Fuzzer: miaubiz_css_fuzzer
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f80890118c0
Crash State:
  Bad-cast to sandbox::bpf_dsl::(anonymous namespace)::ReturnResultExprImpl from invalid vptr
  blink::ApplyStyleCommand::applyRelativeFontStyleChange
  blink::ApplyStyleCommand::doApply
  
Sanitizer: cfi (CFI)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_cfi_chrome&range=460787:460815
Fixed: https://clusterfuzz.com/revisions?job=linux_cfi_chrome&range=468000:468086

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4596915422625792


Additional requirements: Requires Gestures

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-04-29)

ClusterFuzz testcase 4596915422625792 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-04-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-01)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5c9d124ac2131f4765f86902ff4cf711ed96c37e

commit 5c9d124ac2131f4765f86902ff4cf711ed96c37e
Author: vabr <vabr@chromium.org>
Date: Tue May 02 09:53:45 2017

Revert of Make InsertTextCommand not to apply style for empty selection (patchset #1 id:1 of https://codereview.chromium.org/2847763004/ )

Reason for revert:
Speculative revert, this seems to have broken some virtual/gpu/fast/canvas/ tests. More info on the associated bug.

BUG=717389

Original issue's description:
> Make InsertTextCommand not to apply typing style for empty selection
>
> This patch makes |InsertTextCommand::DoApply()| not to call |ApplyStyle()| for
> applying typing style when selection after inserting text is empty since
> |ApplyStyle()| doesn't work with empty selection.
>
> The https://crbug.com/chromium/714311 and the attached test case insert text into OPTION element to
> get empty selection after insertion, since we can't place selection inside
> OPTION element.
>
> BUG=714311
> TEST=run_webkit_unit_tests --gtest_filter=InsertTextCommandTest.WithTypingStyle
>
> Review-Url: https://codereview.chromium.org/2847763004
> Cr-Commit-Position: refs/heads/master@{#468080}
> Committed: https://chromium.googlesource.com/chromium/src/+/89209614959b6d3b2d4c4e8b015232663b4fcd87

TBR=xiaochengh@chromium.org,yoichio@chromium.org,yosin@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=714311

Review-Url: https://codereview.chromium.org/2853213002
Cr-Commit-Position: refs/heads/master@{#468590}

[modify] https://crrev.com/5c9d124ac2131f4765f86902ff4cf711ed96c37e/third_party/WebKit/Source/core/editing/BUILD.gn
[modify] https://crrev.com/5c9d124ac2131f4765f86902ff4cf711ed96c37e/third_party/WebKit/Source/core/editing/commands/InsertTextCommand.cpp
[delete] https://crrev.com/0cd36b0f1fa2b9778ec33ec9db4ad9bcba094c7e/third_party/WebKit/Source/core/editing/commands/InsertTextCommandTest.cpp


### bu...@chromium.org (2017-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6192661b83f875baac41bd4ff9c1d238a702d89c

commit 6192661b83f875baac41bd4ff9c1d238a702d89c
Author: vabr <vabr@chromium.org>
Date: Tue May 02 15:32:46 2017

Reland of Make InsertTextCommand not to apply style for empty selection (patchset #1 id:1 of https://codereview.chromium.org/2853213002/ )

Reason for revert:
Hmm, interestingly enough, the tests were still broken in the build which had the revert: https://build.chromium.org/p/chromium.webkit/builders/WebKit%20Linux%20Trusty%20%28dbg%29/builds/1512

So I am relanding it.

Original issue's description:
> Revert of Make InsertTextCommand not to apply style for empty selection (patchset #1 id:1 of https://codereview.chromium.org/2847763004/ )
>
> Reason for revert:
> Speculative revert, this seems to have broken some virtual/gpu/fast/canvas/ tests. More info on the associated bug.
>
> BUG=717389
>
> Original issue's description:
> > Make InsertTextCommand not to apply typing style for empty selection
> >
> > This patch makes |InsertTextCommand::DoApply()| not to call |ApplyStyle()| for
> > applying typing style when selection after inserting text is empty since
> > |ApplyStyle()| doesn't work with empty selection.
> >
> > The https://crbug.com/chromium/714311 and the attached test case insert text into OPTION element to
> > get empty selection after insertion, since we can't place selection inside
> > OPTION element.
> >
> > BUG=714311
> > TEST=run_webkit_unit_tests --gtest_filter=InsertTextCommandTest.WithTypingStyle
> >
> > Review-Url: https://codereview.chromium.org/2847763004
> > Cr-Commit-Position: refs/heads/master@{#468080}
> > Committed: https://chromium.googlesource.com/chromium/src/+/89209614959b6d3b2d4c4e8b015232663b4fcd87
>
> TBR=xiaochengh@chromium.org,yoichio@chromium.org,yosin@chromium.org
> # Not skipping CQ checks because original CL landed more than 1 days ago.
> BUG=714311
>
> Review-Url: https://codereview.chromium.org/2853213002
> Cr-Commit-Position: refs/heads/master@{#468590}
> Committed: https://chromium.googlesource.com/chromium/src/+/5c9d124ac2131f4765f86902ff4cf711ed96c37e

TBR=xiaochengh@chromium.org,yoichio@chromium.org,yosin@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=717389

Review-Url: https://codereview.chromium.org/2854123002
Cr-Commit-Position: refs/heads/master@{#468642}

[modify] https://crrev.com/6192661b83f875baac41bd4ff9c1d238a702d89c/third_party/WebKit/Source/core/editing/BUILD.gn
[modify] https://crrev.com/6192661b83f875baac41bd4ff9c1d238a702d89c/third_party/WebKit/Source/core/editing/commands/InsertTextCommand.cpp
[add] https://crrev.com/6192661b83f875baac41bd4ff9c1d238a702d89c/third_party/WebKit/Source/core/editing/commands/InsertTextCommandTest.cpp


### sh...@chromium.org (2017-05-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-05)

And $3,000 for this one from the VRP panel, along with the $500 fuzzer bonus. Thanks!

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bd2a15d23a22163e93b7510711f22322c5a4844c

commit bd2a15d23a22163e93b7510711f22322c5a4844c
Author: Yoshifumi Inoue <yosin@chromium.org>
Date: Wed May 10 09:02:11 2017

Reland of Make InsertTextCommand not to apply style for empty selection (patchset #1 id:1 of https://codereview.chromium.org/2853213002/ )

Reason for revert:
Hmm, interestingly enough, the tests were still broken in the build which had the revert: https://build.chromium.org/p/chromium.webkit/builders/WebKit%20Linux%20Trusty%20%28dbg%29/builds/1512

So I am relanding it.

Original issue's description:
> Revert of Make InsertTextCommand not to apply style for empty selection (patchset #1 id:1 of https://codereview.chromium.org/2847763004/ )
>
> Reason for revert:
> Speculative revert, this seems to have broken some virtual/gpu/fast/canvas/ tests. More info on the associated bug.
>
> BUG=717389
>
> Original issue's description:
> > Make InsertTextCommand not to apply typing style for empty selection
> >
> > This patch makes |InsertTextCommand::DoApply()| not to call |ApplyStyle()| for
> > applying typing style when selection after inserting text is empty since
> > |ApplyStyle()| doesn't work with empty selection.
> >
> > The https://crbug.com/chromium/714311 and the attached test case insert text into OPTION element to
> > get empty selection after insertion, since we can't place selection inside
> > OPTION element.
> >
> > BUG=714311
> > TEST=run_webkit_unit_tests --gtest_filter=InsertTextCommandTest.WithTypingStyle
> >
> > Review-Url: https://codereview.chromium.org/2847763004
> > Cr-Commit-Position: refs/heads/master@{#468080}
> > Committed: https://chromium.googlesource.com/chromium/src/+/89209614959b6d3b2d4c4e8b015232663b4fcd87
>
> TBR=xiaochengh@chromium.org,yoichio@chromium.org,yosin@chromium.org
> # Not skipping CQ checks because original CL landed more than 1 days ago.
> BUG=714311
>
> Review-Url: https://codereview.chromium.org/2853213002
> Cr-Commit-Position: refs/heads/master@{#468590}
> Committed: https://chromium.googlesource.com/chromium/src/+/5c9d124ac2131f4765f86902ff4cf711ed96c37e

TBR=xiaochengh@chromium.org,yoichio@chromium.org,yosin@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=717389

Review-Url: https://codereview.chromium.org/2854123002
Cr-Commit-Position: refs/heads/master@{#468642}
(cherry picked from commit 6192661b83f875baac41bd4ff9c1d238a702d89c)

Review-Url: https://codereview.chromium.org/2872243002 .
Cr-Commit-Position: refs/branch-heads/3071@{#499}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}

[modify] https://crrev.com/bd2a15d23a22163e93b7510711f22322c5a4844c/third_party/WebKit/Source/core/editing/BUILD.gn
[modify] https://crrev.com/bd2a15d23a22163e93b7510711f22322c5a4844c/third_party/WebKit/Source/core/editing/commands/InsertTextCommand.cpp
[add] https://crrev.com/bd2a15d23a22163e93b7510711f22322c5a4844c/third_party/WebKit/Source/core/editing/commands/InsertTextCommandTest.cpp


### aw...@google.com (2017-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-08-05)

This issue was migrated from crbug.com/chromium/714311?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087417)*
