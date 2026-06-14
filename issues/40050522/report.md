# Security: Injecting styles via copy-and-paste

| Field | Value |
|-------|-------|
| **Issue ID** | [40050522](https://issues.chromium.org/issues/40050522) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS, Blink>Editing |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | xi...@chromium.org |
| **Created** | 2019-10-24 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

An issue in sanitizer can (perhaps) lead to XSS via copy&paste. The destination element needs to be contenteditable.

**VERSION**  

Chrome Version: 77.0.3865.90 stable  

Operating System: macOS

**REPRODUCTION CASE**  

See <https://crbug.com/chromium/1011950> which was about injecting scripts via copy-and-paste, and has now been blocked.

<https://crbug.com/chromium/1017871#c2> of that bug states that CSS is also potentially injectable, and was not covered by that fix. We need to work out whether injection of CSS has any security risk, so I'm raising this for that sort of triage/consideration.

## Attachments

- [main.js](attachments/main.js) (text/plain, 2.9 KB)
- [css-leak.mp4](attachments/css-leak.mp4) (video/mp4, 801.7 KB)

## Timeline

### ad...@chromium.org (2019-10-24)

I'm adding reward_to-michal_at_bentkowski.info, but this is probably not eligible for an extra reward as it's already covered by https://crbug.com/chromium/1011950. However if we fix this separately in a different release I'd probably expect to credit it in the release notes.

### mi...@bentkowski.info (2019-10-24)

Injecting CSS might also have security implications. It is mainly used for exfiltrating data. 

Ways to abuse CSS injection have been recently nicely covered in this blog post: https://x-c3ll.github.io/posts/CSS-Injection-Primitives/

### jd...@chromium.org (2019-10-24)

Tentatively setting sev-medium, but this should be re-assessed once we've thought about it a bit more.

[Monorail components: Blink>CSS]

### xi...@chromium.org (2019-10-25)

Tested pasting "foo<style>*{color:red}</style>bar" with https://jsbin.com/mozidoxegi/edit?html,output in other browsers:

- Chrome: No style sanitization at all. everything else turns red.
- Firefox: Same as Chrome
- Safari: Sanitized as following. Basically <style> is computed and then moved as inline styles to the pasted elements

"<span style="caret-color: rgb(255, 0, 0); color: rgb(255, 0, 0);">foo</span><span style="caret-color: rgb(255, 0, 0); color: rgb(255, 0, 0);">bar</span>"

Safari's approach looks reasonable to me, as it applies the style properly to pasted elements while prevents it from being applied on the original content

### xi...@chromium.org (2019-10-25)

+adetaylor@

As you reviewed https://crbug.com/chromium/1011950, could you also take a look at the idea in #4? Thank you!

### ad...@google.com (2019-10-25)

xiaochengh@ Thanks for the testing and the proposed solution sounds good to me.

### dc...@chromium.org (2019-10-25)

[Empty comment from Monorail migration]

### dc...@chromium.org (2019-10-25)

We used to strip style tags but it looks like this was intentionally changed in https://bugs.chromium.org/p/chromium/issues/detail?id=121163#c31.

While computing the styles before inserting the pasted fragment would be the ideal approach, this was previously quite hard: the problem is we couldn't compute the style without doing layout. This required inserting the fragment into a dummy page, or other complicated solutions.

If there's a better way to do that now, then computing the style and including it inline is the best solution. I'm just worried about how complex it will be…

### mi...@bentkowski.info (2019-10-27)

As some sort of exercise, I decided to create a proof of concept of exfiltrating data using <style> and copy-and-paste. In the example, I was able to exfiltrate email address of currently logged in user of Gmail. The code is attached. I also attached a video, showcasing the exploit (and yes, rtuspzmvjsofpm92992@gmail.com is actually one of my throw-away accounts ;)).



### sh...@chromium.org (2019-11-08)

xiaochengh: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yo...@chromium.org (2019-11-15)

For short time solution, let's simply remove <style> elements from Document Fragment to be pasted in ClipboardCommands::GetFragmentFromClipboard() returned from CreateFragmentFromMarkupWithContext(). This can be done by Document::getElementsByTagName().

For long time solution, in addition to removing <style> tag, we set inline style to elements in fragment.

Let's do short time solution to fix this security issue.

### yo...@chromium.org (2019-11-16)

Discuss more with xiaochenghu@, simply remove <style> elements causes issue [1].
Before fixing [1], Blink excluded <style> elements when pasting. After fixing [1], Blink inserts <style> elements.

It seems Safari does[2[:
1. Creating Page
2. Parse markup text into Page
3. Serialize into document fragment from the Page with inserting inline style
4. Inserting fragment at selection excluding <style> element.

I'm not sure why we didn't do this way for fixing [1].

[1] http://crbug.com/121163: Pasting from Excel spreadsheet does not keep all formatting.
[2] https://trac.webkit.org/changeset/223440 introduces sanitizeMarkup()


https://trac.webkit.org/browser/webkit/trunk/Source/WebCore/editing/markup.cpp



177	std::unique_ptr<Page> createPageForSanitizingWebContent()
178	{
179	    auto pageConfiguration = pageConfigurationWithEmptyClients(PAL::SessionID::defaultSessionID());
180	   
181	    auto page = makeUnique<Page>(WTFMove(pageConfiguration));
182	    page->setIsForSanitizingWebContent();
183	    page->settings().setMediaEnabled(false);
184	    page->settings().setScriptEnabled(false);
185	    page->settings().setPluginsEnabled(false);
186	    page->settings().setAcceleratedCompositingEnabled(false);
187	
188	    Frame& frame = page->mainFrame();
189	    frame.setView(FrameView::create(frame, IntSize { 800, 600 }));
190	    frame.init();
191	
192	    FrameLoader& loader = frame.loader();
193	    static char markup[] = "<!DOCTYPE html><html><body></body></html>";
194	    ASSERT(loader.activeDocumentLoader());
195	    auto& writer = loader.activeDocumentLoader()->writer();
196	    writer.setMIMEType("text/html");
197	    writer.begin();
198	    writer.insertDataSynchronously(String(markup));
199	    writer.end();
200	    RELEASE_ASSERT(page->mainFrame().document()->body());
201	
202	    return page;
203	}
205	String sanitizeMarkup(const String& rawHTML, MSOListQuirks msoListQuirks, Optional<WTF::Function<void(DocumentFragment&)>> fragmentSanitizer)
206	{
207	    auto page = createPageForSanitizingWebContent();
208	    Document* stagingDocument = page->mainFrame().document();
209	    ASSERT(stagingDocument);
210	
211	    auto fragment = createFragmentFromMarkup(*stagingDocument, rawHTML, emptyString(), DisallowScriptingAndPluginContent);
212	
213	    if (fragmentSanitizer)
214	        (*fragmentSanitizer)(fragment);
215	
216	    return sanitizedMarkupForFragmentInDocument(WTFMove(fragment), *stagingDocument, msoListQuirks, rawHTML);
217	}


### xi...@chromium.org (2019-11-19)

[Empty comment from Monorail migration]

### dc...@chromium.org (2019-11-22)

yosin, to give some background, the solution implemented in https://chromium-review.googlesource.com/c/chromium/src/+/1922919 (using a dummy document to sanitize the paste) was originally considered, but a number of Blink engineers felt it was too hacky.

But given that we want this feature (for improved paste) and the security issues, it seems like this is the best solution.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a

commit d96236b5d2bad68a0cc8f62501ba15c38c8cf96a
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Fri Nov 22 21:18:34 2019

Sanitize style elements in clipboard markup

This patch sanitizes clipboard markup before pasting it into document
by removing all pasted style elements and serializing them onto
elements as inline style. In this way, we stop stylesheets in clipboard
markup from being applied to the original elements in the document.

This patch follows the same approach as in WebKit [1]:
- First create a dummy document to insert the markup
- Then computes style and layout in the dummy document
- Re-serialize the dummy document as the markup to be inserted. This
  reuses the code path that we serialize a selection range into
  clipboard, where we need to serialize element computed style into
  inline styles so that the element styles are preserved.
- Make sure all style elements are removed before inserting markup
  into document

This patch also adds a complete test to ensure that content pasted from
Excel is still properly styled, which is the main reason we used to
preserve style elements in clipboard markup [2].

[1] https://trac.webkit.org/changeset/223440
[2] http://crbug.com/121163

Bug: 1017871
Change-Id: I3bb5a4ae7530a3fdef5ba251975e004857c06f1e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1922919
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/master@{#718281}

[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/commands/clipboard_commands.cc
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/commands/replace_selection_command.cc
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/commands/replace_selection_command_test.cc
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/editing_style_utilities.cc
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/editing_style_utilities.h
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/serializers/create_markup_options.cc
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/serializers/create_markup_options.h
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/serializers/serialization.cc
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/serializers/serialization.h
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/serializers/styled_markup_accumulator.cc
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/serializers/styled_markup_accumulator.h
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/renderer/core/editing/serializers/styled_markup_serializer.cc
[add] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/web_tests/editing/pasteboard/paste-from-excel.html
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/web_tests/editing/pasteboard/paste-head-contents-expected.txt
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/web_tests/editing/pasteboard/paste-head-contents.html
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/web_tests/editing/pasteboard/paste-xss-injection.html
[modify] https://crrev.com/d96236b5d2bad68a0cc8f62501ba15c38c8cf96a/third_party/blink/web_tests/editing/pasteboard/preserve-underline-color-expected.txt


### xi...@chromium.org (2019-11-22)

Fixed in M80.

adetaylor: Could you help with re-assessing the security severity, and clearing the Security_Needs_Attention-Severity label? Thanks!

### mi...@bentkowski.info (2019-11-22)

Hey, the fix can be bypassed using similar trick to the one that was shown in https://crbug.com/chromium/1011950.

Reproduction steps:
1. Go to https://jsbin.com/mozidoxegi/edit?html,output
2. Copy to clipboard the following code:

	A<math>B<a style=display:block>C<title>D<a id="</title><svg><style>*{background:red}</style>">c

3. Put cursor in the yellow box - but make sure it is not at the very end.
4. Paste from clipbard; everything turns red.


It seems the problem is that after CompositeEditCommand::MoveParagraphs(), HTMLStyleElement is removed, but the same doesn't happen for SVGStyleElement.

### xi...@chromium.org (2019-11-22)

Thanks for the quick catch!

And... In fact CompositeEditCommand::MoveParagraphs() doesn't strip HTMLStyleElement, either. The good old attack in crbug.com/1011950#c2 still works

### xi...@chromium.org (2019-11-23)

Sorry please ignore https://crbug.com/chromium/1017871#c18.

Didn't update my local checkout when testing...

### ad...@chromium.org (2019-11-23)

I think Medium seems about right from the discussions. I'll keep it at that.

### mi...@bentkowski.info (2019-11-23)

Also one more issue: when the pasted style contains an @import rule, then the tab crashes with "Aw, Snap!". In the console I'm getting:

    Received signal 11 SEGV_MAPERR 000000000000

I think that @import should be ignored in pasted content. This is also what Safari does.

The code I'm pasting is: 

    <style>@import'https://example.com';</style>


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b

commit f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b
Author: Owen Min <zmin@chromium.org>
Date: Mon Nov 25 20:08:58 2019

Revert "Sanitize style elements in clipboard markup"

This reverts commit d96236b5d2bad68a0cc8f62501ba15c38c8cf96a.

Reason for revert: This may cause "WebKit Linux Leak" failure
First failure: https://ci.chromium.org/p/chromium/builders/ci/WebKit%20Linux%20Leak/7276

Original change's description:
> Sanitize style elements in clipboard markup
> 
> This patch sanitizes clipboard markup before pasting it into document
> by removing all pasted style elements and serializing them onto
> elements as inline style. In this way, we stop stylesheets in clipboard
> markup from being applied to the original elements in the document.
> 
> This patch follows the same approach as in WebKit [1]:
> - First create a dummy document to insert the markup
> - Then computes style and layout in the dummy document
> - Re-serialize the dummy document as the markup to be inserted. This
>   reuses the code path that we serialize a selection range into
>   clipboard, where we need to serialize element computed style into
>   inline styles so that the element styles are preserved.
> - Make sure all style elements are removed before inserting markup
>   into document
> 
> This patch also adds a complete test to ensure that content pasted from
> Excel is still properly styled, which is the main reason we used to
> preserve style elements in clipboard markup [2].
> 
> [1] https://trac.webkit.org/changeset/223440
> [2] http://crbug.com/121163
> 
> Bug: 1017871
> Change-Id: I3bb5a4ae7530a3fdef5ba251975e004857c06f1e
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1922919
> Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
> Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
> Reviewed-by: Kent Tamura <tkent@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#718281}

TBR=yosin@chromium.org,tkent@chromium.org,xiaochengh@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 1017871, 1027386
Change-Id: I1d500647d6227c9be3ae14d9604ba702e9c29834
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1933452
Reviewed-by: Owen Min <zmin@chromium.org>
Reviewed-by: Xiaocheng Hu <xiaochengh@chromium.org>
Commit-Queue: Owen Min <zmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#718778}

[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/commands/clipboard_commands.cc
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/commands/replace_selection_command.cc
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/commands/replace_selection_command_test.cc
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/editing_style_utilities.cc
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/editing_style_utilities.h
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/serializers/create_markup_options.cc
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/serializers/create_markup_options.h
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/serializers/serialization.cc
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/serializers/serialization.h
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/serializers/styled_markup_accumulator.cc
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/serializers/styled_markup_accumulator.h
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/renderer/core/editing/serializers/styled_markup_serializer.cc
[delete] https://crrev.com/219d095da1dae034bb4de66bfb5bf252a70bd9af/third_party/blink/web_tests/editing/pasteboard/paste-from-excel.html
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/web_tests/editing/pasteboard/paste-head-contents-expected.txt
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/web_tests/editing/pasteboard/paste-head-contents.html
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/web_tests/editing/pasteboard/paste-xss-injection.html
[modify] https://crrev.com/f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b/third_party/blink/web_tests/editing/pasteboard/preserve-underline-color-expected.txt


### xi...@chromium.org (2019-11-25)

Michal: Thanks for the other catch!

By default, @import is already disabled in pasting. Even without the patch (https://crbug.com/chromium/1017871#c15), we can already see @import rules stripped from pasted style elements.

The crash is due to the dummy page trying to create a WebURLLoaderFactory, which current fails due to the empty clients provided. Providing a mock object that doesn't load anything should be enough.

### xi...@chromium.org (2019-11-25)

Or setting a flag to the dummy document to prevent imports. It should also work.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4886f590400a0fd3e4756333e69784c5dd313580

commit 4886f590400a0fd3e4756333e69784c5dd313580
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Mon Nov 25 23:54:46 2019

Reland "Sanitize style elements in clipboard markup"

This reverts commit f6953a5e9d62cde66ea6edd2f4f46d1dcee7940b.

Reason for revert: Manually destroyed the dummy page to ensure no leak

Original change's description:
> Revert "Sanitize style elements in clipboard markup"
>
> This reverts commit d96236b5d2bad68a0cc8f62501ba15c38c8cf96a.
>
> Reason for revert: This may cause "WebKit Linux Leak" failure
> First failure: https://ci.chromium.org/p/chromium/builders/ci/WebKit%20Linux%20Leak/7276
>
> Original change's description:
> > Sanitize style elements in clipboard markup
> >
> > This patch sanitizes clipboard markup before pasting it into document
> > by removing all pasted style elements and serializing them onto
> > elements as inline style. In this way, we stop stylesheets in clipboard
> > markup from being applied to the original elements in the document.
> >
> > This patch follows the same approach as in WebKit [1]:
> > - First create a dummy document to insert the markup
> > - Then computes style and layout in the dummy document
> > - Re-serialize the dummy document as the markup to be inserted. This
> >   reuses the code path that we serialize a selection range into
> >   clipboard, where we need to serialize element computed style into
> >   inline styles so that the element styles are preserved.
> > - Make sure all style elements are removed before inserting markup
> >   into document
> >
> > This patch also adds a complete test to ensure that content pasted from
> > Excel is still properly styled, which is the main reason we used to
> > preserve style elements in clipboard markup [2].
> >
> > [1] https://trac.webkit.org/changeset/223440
> > [2] http://crbug.com/121163
> >
> > Bug: 1017871
> > Change-Id: I3bb5a4ae7530a3fdef5ba251975e004857c06f1e
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1922919
> > Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
> > Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
> > Reviewed-by: Kent Tamura <tkent@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#718281}
>
> TBR=yosin@chromium.org,tkent@chromium.org,xiaochengh@chromium.org
>
> # Not skipping CQ checks because original CL landed > 1 day ago.
>
> Bug: 1017871, 1027386
> Change-Id: I1d500647d6227c9be3ae14d9604ba702e9c29834
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1933452
> Reviewed-by: Owen Min <zmin@chromium.org>
> Reviewed-by: Xiaocheng Hu <xiaochengh@chromium.org>
> Commit-Queue: Owen Min <zmin@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#718778}

TBR=yosin@chromium.org,tkent@chromium.org,zmin@chromium.org,xiaochengh@chromium.org

Cq-Include-Trybots=luci.chromium.try:layout_test_leak_detection

Bug: 1017871, 1027386
Change-Id: Ia56ee941979cad71e2bac06998c7ac417b4731bd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1934650
Reviewed-by: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#718896}

[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/commands/clipboard_commands.cc
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/commands/replace_selection_command.cc
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/commands/replace_selection_command_test.cc
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/editing_style_utilities.cc
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/editing_style_utilities.h
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/serializers/create_markup_options.cc
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/serializers/create_markup_options.h
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/serializers/serialization.cc
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/serializers/serialization.h
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/serializers/styled_markup_accumulator.cc
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/serializers/styled_markup_accumulator.h
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/renderer/core/editing/serializers/styled_markup_serializer.cc
[add] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/web_tests/editing/pasteboard/paste-from-excel.html
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/web_tests/editing/pasteboard/paste-head-contents-expected.txt
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/web_tests/editing/pasteboard/paste-head-contents.html
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/web_tests/editing/pasteboard/paste-xss-injection.html
[modify] https://crrev.com/4886f590400a0fd3e4756333e69784c5dd313580/third_party/blink/web_tests/editing/pasteboard/preserve-underline-color-expected.txt


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7d16958ff0de76a5420397d1d0448a9d8e68e05d

commit 7d16958ff0de76a5420397d1d0448a9d8e68e05d
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Nov 26 00:06:38 2019

Strip SVGStyleElement in ReplaceSelectionCommand

crrev.com/c/1922919 added a stylesheet sanitizer for clipboard, but left
a loophole for SVGStyleElement. This patch also strips it.

Bug: 1017871
Change-Id: Icc6c513f79597c191f732cd63a98cc59afe1fc69
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1931412
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#718902}

[modify] https://crrev.com/7d16958ff0de76a5420397d1d0448a9d8e68e05d/third_party/blink/renderer/core/editing/commands/replace_selection_command.cc
[add] https://crrev.com/7d16958ff0de76a5420397d1d0448a9d8e68e05d/third_party/blink/web_tests/editing/pasteboard/mathml-sanitizer-bypass.html
[delete] https://crrev.com/69f722944e1875ef429bfea2cdeccef6824a29e7/third_party/blink/web_tests/editing/pasteboard/paste-xss-injection.html


### mi...@bentkowski.info (2019-11-26)

It seems that the bypass via <svg><style> no longer works (but I'll keep trying to find more ways ;)).

But I can still trigger the crash and it seems to me that @import at-rules are processed. 

I'm using https://jsbin.com/mozidoxegi/edit?html,output again and when I try to copy
	
	foo<style>@import'data:,*{background:red}'</style>bar

Then "foobar" has red background when being pasted. 

Also, when copying and pasting 

	foo<style>@import'https://anyting'</style>bar

Then I'm getting the "Aw, Snap" error as I mentioned earlier.

I'm testing it on MacOS 10.14.6, on https://cr-rev.appspot.com/719066 downloaded from https://download-chromium.appspot.com/.

### xi...@chromium.org (2019-11-26)

Hi Michal,

So far I've landed two patches that (i) adds general style sanitization for pasting, and (ii) removes SVGStyleElement from ReplaceSelectionCommand.

I'm still working on the third patch to ban import rules during sanitization: crrev.com/c/1935429. You may test again after it is landed.

(Hopefully there won't be a fourth one)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a94963cedd74ba312af09970cf8e91a5b89dce9d

commit a94963cedd74ba312af09970cf8e91a5b89dce9d
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Wed Nov 27 22:14:31 2019

Disable CSS @import rules in clipboard markup sanitization

While clipboard markup is allowed to carry style sheets to style the
elements to be pasted (e.g., when copying from Excel), @import rules
should be disabled for security reasons.

This patch disables @import rules when sanitizing the markup in a dummy
document to make sure we don't initiate any stylesheet loading during
the process.

Bug: 1017871
Change-Id: I484341dc34e2ceea1891a18ac158ed2cc4920c9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1935429
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/master@{#719779}

[modify] https://crrev.com/a94963cedd74ba312af09970cf8e91a5b89dce9d/third_party/blink/renderer/core/css/parser/css_parser_context.cc
[modify] https://crrev.com/a94963cedd74ba312af09970cf8e91a5b89dce9d/third_party/blink/renderer/core/css/parser/css_parser_context.h
[modify] https://crrev.com/a94963cedd74ba312af09970cf8e91a5b89dce9d/third_party/blink/renderer/core/css/parser/css_parser_impl.cc
[modify] https://crrev.com/a94963cedd74ba312af09970cf8e91a5b89dce9d/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/a94963cedd74ba312af09970cf8e91a5b89dce9d/third_party/blink/renderer/core/editing/serializers/serialization.cc
[add] https://crrev.com/a94963cedd74ba312af09970cf8e91a5b89dce9d/third_party/blink/web_tests/editing/pasteboard/block-stylesheet-import-rules.html
[add] https://crrev.com/a94963cedd74ba312af09970cf8e91a5b89dce9d/third_party/blink/web_tests/editing/resources/all-red.css


### xi...@chromium.org (2019-11-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-28)

[Empty comment from Monorail migration]

### mi...@bentkowski.info (2019-12-01)

Just for the record: the fix now seems fine to me.

### na...@google.com (2019-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-03)

Requesting merge to beta M79 because latest trunk commit (719779) appears to be after beta branch point (706915).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-03)

This bug requires manual review: We are only 6 days from stable.
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
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-12-03)

Security TPM note: I'd like to merge this into M79, but I regard this as a substantial change which introduces some risk, so if we end up saving this for M80 that's OK with me.

### go...@chromium.org (2019-12-03)

Rejecting merge to M79 per https://crbug.com/chromium/1017871#c36 as we're trying to be super careful with merges due to upcoming holidays.



### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Thanks for all the help on this report! The Panel decided to reward $10,000 for this report! Nice work!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### mi...@bentkowski.info (2019-12-10)

Thanks, that's an amazing reward!

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-04-29)

[Empty comment from Monorail migration]

### is...@google.com (2020-04-29)

This issue was migrated from crbug.com/chromium/1017871?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>CSS, Blink>Editing]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050522)*
