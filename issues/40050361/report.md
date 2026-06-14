# Security: "universal" XSS via copy&paste

| Field | Value |
|-------|-------|
| **Issue ID** | [40050361](https://issues.chromium.org/issues/40050361) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Editing |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | xi...@chromium.org |
| **Created** | 2019-10-07 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

An issue in sanitizer can lead to XSS via copy&paste. The destination element needs to be contenteditable.

**VERSION**  

Chrome Version: 77.0.3865.90 stable  

Operating System: macOS

**REPRODUCTION CASE**  

The issue is kind of crazy and I cannot quite understand how it works, so I'll just share some observations.

I have created a JSBin, in which you can input some HTML in the textarea, then copy it and paste it in a yellow DIV with CONTENTEDITABLE to see how it gets transformed. It's here: <https://jsbin.com/mozidoxegi/edit?html,output>

The main example is: <math><xss style=display:block>t<style>X<a title="</style><img src onerror=alert(1)>">.<a>.

When you try to copy it and paste in the yellow div (but not at the very end - no idea why!), it gets transformed to the following code:

```
t  
<style>  
  X<a title="  
</style>  
<img src="" onerror="alert(1)">  
"&gt;.  
<a>.</a>  
aaa  

```

So the <img> that was originally within title attribute in <a>, is now a new tag and make the XSS execute.

The interesting thing is that when you look at the original code, the <xss> tag has a style="display:block" attribute... and if you delete it, the example no longer works.

I confirmed that the example works in a few rich editors, including composing message in GMail.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Michal Bentkowski of Securitum

## Attachments

- [ScreenFlow.mp4](attachments/ScreenFlow.mp4) (video/mp4, 7.7 MB)
- [copyandpaste.html](attachments/copyandpaste.html) (text/plain, 904 B)

## Timeline

### mp...@google.com (2019-10-08)

Interesting. I improved the JSBin a little bit to this: https://jsbin.com/rucajeduri/1/edit?html,output.

I tried pasting into the (middle of the) text of a new GMail message, but it didn't trigger any XSS. Can you elaborate on how you got that to work? Or does the web page itself have to perform the "copy" in order for the paste to cause an XSS vuln?

### mi...@bentkowski.info (2019-10-08)

In case of GMail, the actual code execution is blocked by CSP. When you look at the console, you can see an error "Refused to execute inline event handler because it violates the following Content Security Policy directive ..." being shown. The <img src onerror=alert(1)> element can also be seen in the DOM tree. So in the real world, a CSP bypass would also be needed.

But another way to confirm that we can inject arbitrary tags in GMail is to use <style>, for instance:

<math><xss style=display:block>t<style>X<a title="</style><style>*{background:red}</style>">.<a>.

After pasting it, everything turns red :) In real case, CSS injection could be abused to perform some leaks.

### aj...@google.com (2019-10-08)

Hi Michal,

I see that the iframe containing the script on jsbin has sandbox allow-same-origin and allow-scripts. Can you refine your example and attach files (and maybe a recording) showing how this might allow a pasted script to affect a containing iframe? (see, for instance https://crbug.com/474857).

### aj...@google.com (2019-10-08)

[Empty comment from Monorail migration]

### aj...@google.com (2019-10-08)

yosin@ & xiachengh@ could you please take a look at this report? Feel free to CC in more specific people if that makes sense. Cheers!

[Monorail components: Blink>Editing]

### mi...@bentkowski.info (2019-10-08)

I have hosted a page at: https://bentkowski.info/8cd936e4ec0257f3c727cd31d6916dfa/ that showcases the issues.

I'm also attaching a video and source of the hosted page. Hope it clear things up.
In this video I'm showing that I can XSS GMail, Wikipedia and Blogger.com when pasting the maliciously constructed string.

### sh...@chromium.org (2019-10-08)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2019-10-10)

Confirmed  this behavior on Windows. yosin@ I've set you as owner. Could you take a look.

### sh...@chromium.org (2019-10-10)

[Empty comment from Monorail migration]

### xi...@chromium.org (2019-10-16)

The culprit seems to be CompositeEditCommand::MoveParagraphs()

https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/editing/commands/composite_edit_command.cc?type=cs&g=0&l=1496

  // FIXME: This is an inefficient way to preserve style on nodes in the
  // paragraph to move. It shouldn't matter though, since moved paragraphs will
  // usually be quite small.
  DocumentFragment* fragment =
      start_of_paragraph_to_move.DeepEquivalent() !=
              end_of_paragraph_to_move.DeepEquivalent()
          ? CreateFragmentFromMarkup(
                GetDocument(),
                CreateMarkup(start.ParentAnchoredEquivalent(),
                             end.ParentAnchoredEquivalent(),
                             kDoNotAnnotateForInterchange,
                             ConvertBlocksToInlines::kConvert,
                             kDoNotResolveURLs, constraining_ancestor),
                "")
          : nullptr;

Here, in order to move a few paragraphs to a different location of the document, we serialize the range and re-parse it into a DocumentFragment to be inserted at somewhere else. This results in a <script> element in the parsed document, and hence XSS.

### xi...@chromium.org (2019-10-16)

Ideas below, and discussion requested:

It seems pretty hard to preserve style on elements without serialization & re-parsing. So I'm not going to change this pattern. So to fix this issue, we should pass a |kDisallowScriptingAndPluginContent| flag to |CreateFragmentFromMarkup()|. There are two options:

1. Simply add it into the line, which is my preferred option. However, this breaks the case where the paragraphs being moved contain script, in which case the script will be stripped after moving. An example is at https://jsfiddle.net/qy74r5pd/

However, I don't think there's any reasonable use case to put scripts into contenteditable. So I guess we won't break any valid use case -- but I'm not sure.

2. Set the |kDisallowScriptingAndPluginContent| flag only when we are handling a paste. This doesn't break other editing commands, but I don't like the code complexity.

### yo...@chromium.org (2019-10-16)

Let's use option 1 and watching bug report from M78 canary.

BTW, why do we still have "onerror" after "paste" command?

ClipboardCommands::GetFragmentFromClipboard() creates Document Fragment from clipboard with kDisallowScriptingAndPluginContent. So, pasted document fragment should not have scripting attributes.

It is better to remove scripting attributes, etc. from fragments returned by ClipboardCommands::GetFragmentFromClipboard() rather than changing CompositeEditCommand::MoveParagraphs().



### xi...@chromium.org (2019-10-16)

#13:

The test case utilizes a difference between different parsing modes.

(1) The clipboard html is in a <math> tag, so it's not parsed as normal HTML. As a result, the parsed DOM looks like
<style>
  "X"
  <a title="</style><img src onerror=alert(1)>">
  ..

Note that the injected script still stays in the title attribute, and isn't runnable so far.

----

Then it's serialized into '<style>X<a title="</style><img src onerror=alert(1)>">"> ...'

(2) In the second time, it's parsed as normal HTML, which parses the "<a title=" as a text node under <style>, and closes the <style> after seeing "</style>". So the parsed DOM looks like:

<style>
  "X<a title=\""
</style>
<img src onerror=alert(1)>

That's how the script gets injected.

### yo...@chromium.org (2019-10-17)

Thanks for explanation!
This is fundamental issue of |CompositeEditCommand::MoveParagraphs()|.
Removing script attribute during |MovePararaphs()| is the solution otherwise we should rewrite |MoveParagraphs()| not to use serialization.

xiaochengh@ has the patch http://crrev.com/c/1863757


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0e4161fc6073f1cab302bcb61f379445b2954f19

commit 0e4161fc6073f1cab302bcb61f379445b2954f19
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Thu Oct 17 07:00:55 2019

Block scripts in CompositeEditCommand::MoveParagraphs()

CompositeEditCommand::MoveParagraphs() serializes part of the DOM
tree, remove it, and then re-parse and reinsert it at another place.
Currently, this may result in unexpected script running, including
XSS injections.

As there's no valid use case of putting script inside contenteditable,
this patch simply blocks scripts from being parsed here to ensure no
unexpected script running.

Bug: 1011950
Change-Id: I542538ee864535f1253d7f09a929d5dcfe598ee0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1863757
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#706806}

[modify] https://crrev.com/0e4161fc6073f1cab302bcb61f379445b2954f19/third_party/blink/renderer/core/editing/commands/composite_edit_command.cc
[add] https://crrev.com/0e4161fc6073f1cab302bcb61f379445b2954f19/third_party/blink/web_tests/editing/pasteboard/paste-xss-injection.html


### xi...@chromium.org (2019-10-17)

Fixed by #16.

Note that this doesn't fix the style injection shown in #2, which seems to be a totally different issue.

Actually, stylesheets injection seems allowed in general. Just put "foo <style>*{color:red}</style> bar" into clipboard and paste, and you'll notice the entire page turning red.

### sh...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-21)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-23)

Congrats! The Panel decided to award $2,000 for this report :) 

### sh...@chromium.org (2019-10-24)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-24)

Requesting merge to beta M78 because latest trunk commit (706806) appears to be after beta branch point (693954).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-24)

This bug requires manual review: Request affecting a post-stable build
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
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-10-24)

xiaochengh@ pls help answer the questions in https://crbug.com/chromium/1011950#c25 and also confirm the fix is complete ? you mentioned it doesnt fix the issue in https://crbug.com/chromium/1011950#c2. 

### xi...@chromium.org (2019-10-24)

srinivassista@: The fix is complete for the issue given in the original bug report. The case in #2 appears to be a different one which is not XSS, and I'm actually not sure if it should be counted as a security issue or not, as I don't have enough security background knowledge to judge.


1. Does your merge fit within the Merge Decision Guidelines?

Yes

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/1863757

3. Has the change landed and been verified on master/ToT?

Yes

4. Why are these changes required in this milestone after branch?

It's a medium severity security fix

5. Is this a new feature?

No

6. If it is a new feature, is it behind a flag using finch?

No

### sr...@google.com (2019-10-24)

+adetaylor@ to review https://crbug.com/chromium/1011950#c27 with regards to completeness of the fix. 

Adrian, is this critical to be included in stable re-spin ?  

Adding merge-review-79 label as well so we can get it merged to M79 for qualification.

### ad...@chromium.org (2019-10-24)

I'd say this isn't a good candidate to merge to M78. It's assessed as medium severity (which seems about right to me) and, although the fix is completely trivial, there's probably a 0.1% chance that some insane enterprise product is relying on the old behavior. So let's get it into M79 and no further back. Sound good?

Regarding https://crbug.com/chromium/1011950#c2 and the possible incompleteness of the fix, let's leave this crbug about the JavaScript injection. I've raised a separate bug, https://crbug.com/chromium/1017871, about CSS injection, as I'm also not sure if it's an actual risk.

### sr...@google.com (2019-10-25)

thanks adetaylor@ , rejecting the merge for M78, and adding govind@ and pbommana@ to take it through M79.

### go...@chromium.org (2019-10-25)

CL listed at #16 is already in M79 branch 3945, branched at chromium revision 706915. No merge needed to M79. 

### ad...@google.com (2019-10-25)

SGTM.

### mi...@bentkowski.info (2019-10-27)

I'm probably a bit late for the discussion but I think that the argument for the merge is that the exploit is now essentially public because of this test: https://cs.chromium.org/chromium/src/third_party/blink/web_tests/editing/pasteboard/paste-xss-injection.html

So if someone pays attention to commits in Chromium, she or he can easily recreate the bug.

### na...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-30)

Re https://crbug.com/chromium/1011950#c33 thanks for the comment! And yes - and we know that people will try to do exactly that. (Fortunately it involves copy+paste or it'd be much more serious, and we'd be merging.) We're balancing the inevitability of people spotting this, against the risks of merge which, as per https://crbug.com/chromium/1011950#c29, are low but not non-existent. To merge things straight to a stable release bypasses a lot of our testing, and if we get it wrong we break the internet for a very large number of people, so the bar to merge things is extremely high.

### ad...@google.com (2019-12-01)

Assuming affects all Blink platforms.

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1011950?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050361)*
