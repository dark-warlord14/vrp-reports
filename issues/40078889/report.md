# Security: UXSS via dispatchEvent on iframes (subject to some conditions)

| Field | Value |
|-------|-------|
| **Issue ID** | [40078889](https://issues.chromium.org/issues/40078889) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ai...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2014-02-11 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Permits a page on an arbitrary site to retrieve the document element of any target page given the following conditions:

- the target page may be embedded in an iframe
- the target page has a handler for any window event
- the target page gets or sets any property of the event in the handler (any jQuery listener)
- the target page returns a dom node from the handler

The problem: dispatchEvent should complain when 'call'ed on iframe.contentWindow.  

In child.html is a (somewhat) plausible example vulnerable site - it relies on the automatic conversion of event handler return values to true/false to detect whether an action was taken for an event.  

This is exploited by calling the event handler directly (with a reference obtained from Function.prototype.caller) to obtain the dom node, giving me access to document.  

I personally wasn't able to come up with an exploit without relying on the site returning a dom node in the event handler (the final condition).

Needs an additional test in blink/trunk/LayoutTests/http/tests/security/cross-frame-access-call.html for "window.dispatchEvent.call(targetWindow, new CustomEvent('click'));".  

I don't have the knowledge to suggest a code patch.

**VERSION**  

Chromium: Version 32.0.1700.102 Ubuntu 12.10 (32.0.1700.102-0ubuntu0.12.10.1~20140128.878.1)  

Chrome: Version 32.0.1700.107 m (Windows 7 x64 SP1)

**REPRODUCTION CASE**

- Download parent.html and child.html
- Put them on two different web servers and edit the iframe src in parent.html  
  
  to point to the location of child.html. I will assume that
  - parent.html is at <http://127.0.0.1:8080/parent.html>
  - child.html is at <http://localhost:8000/child.html>
- Open <http://127.0.0.1:8080/parent.html>
- Observe "Stolen: stylesheet=ayti; CHILD\_SECRET"
- Note that the CHILD\_SECRET cookie should be inaccessible from the parent page.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

N/A

## Attachments

- [parent.html](attachments/parent.html) (text/html, 1.1 KB)
- [child.html](attachments/child.html) (text/html, 1.1 KB)
- [docsxss.html](attachments/docsxss.html) (text/html, 2.4 KB)

## Timeline

### ai...@gmail.com (2014-02-11)

Noticed a typo in parent.html - 'var t;' is unused.

To expand on child.html, it's mainly written to show how a real application might be vulnerable. A minimal case to work with parent.html would be:
  <script>
    document.cookie = 'CHILD_SECRET';
    window.addEventListener('click', function (e) {
      var _tmp = e.type;
      return document.querySelector('.click-handler');
    }, false);
  </script>

On the subject of 'real(ish) applications', an alternative vector of attack could be to (re)bind the event handler function if it contains references to 'this'.
e.g.
child.html:
  <script>
    MyEvtHandler = function () {
      this.utility = function (elt) { return elt.tagName; }
      this.handler = function (e) {
        var _tmp = e.type;
        var tag = this.utility(document.querySelector('.click-handler'));
        console.log(tag);
      }
    }
    var eh = new MyEvtHandler();
    window.addEventListener('click', eh.handler.bind(eh), false);
  </script>

parent.html:
  <script>
    [...]
    if (!haveGot) {
      haveGot = true;
      x = getType.caller
      x.bind({utility: function (elt) {window.aaa = elt}})({})
      // DOM element now stored in window.aaa
    }
    [...]
  </script>

Apologies if this should've gone in an attachment.

### jl...@chromium.org (2014-02-11)

Mike, could you please help triaging this bug?

### jl...@chromium.org (2014-02-11)

[Empty comment from Monorail migration]

### ai...@gmail.com (2014-02-12)

I think this is worse than I originally realised - the final condition is a stricter condition than the exploit requires.
The attachment shows how one can steal cookies from Google Drive (i.e. this is not just a hypothetical security flaw) - open the file, wait 5s, note document.cookie being alerted.
It wouldn't be hard to extend this to stealing documents.

To outline how this is done
 - The google docs JS sets up a generic handler on window for multiple events.
 - This generic handler calls a function (which calls another etc).
 - The event property 'get' happens about 3 calls deep into the child page.
 - We access the arguments for all of these functions via 'caller'.
 - We automate a traversal of any object arguments to find a DOM node, giving us document.

Note that the google doc itself is an empty spreadsheet and isn't specifically relevant to the exploit.
The problem itself is still the same - dispatchEvent should complain when 'call'ed on iframe.contentWindow.

### ai...@gmail.com (2014-02-12)

Actually attach the file.

### sc...@gmail.com (2014-02-12)

Goodness me. Nice work.

@abarth: you've been pretty active at fixing serious cross-origin violations like these in the past. Interested?

### ab...@chromium.org (2014-02-12)

Sure.  @mkwst: Feel free to reassign to me.

### cl...@chromium.org (2014-02-12)

[Empty comment from Monorail migration]

### mk...@chromium.org (2014-02-12)

I put up https://codereview.chromium.org/150203016/ as a quick fix. CCing Jochen for time-zone appropriate context.

### sc...@gmail.com (2014-02-12)

Cool! That was fast. I wonder if there are any other properties like this where we have missing checks?

### bu...@chromium.org (2014-02-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=166999

------------------------------------------------------------------------
r166999 | mkwst@chromium.org | 2014-02-12T11:02:06.417947Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-frame-access-dispatchEvent.html?r1=166999&r2=166998&pathrev=166999
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/scripts/code_generator_v8.pm?r1=166999&r2=166998&pathrev=166999
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-frame-access-dispatchEvent-expected.txt?r1=166999&r2=166998&pathrev=166999

Add cross-origin BindingsSecurity checks to 'EventTarget::dispatchEvent'.

BUG=342618

Review URL: https://codereview.chromium.org/150203016
------------------------------------------------------------------------

### in...@chromium.org (2014-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-12)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ai...@gmail.com (2014-02-13)

On the subject of other missing checks, that's probably what I'm going to poke at next if you don't get(/haven't got) there first :)

### sc...@gmail.com (2014-02-13)

@aidanphs: go for it! It'd be our pleasure to consider each bug for reward separately :)

### dh...@google.com (2014-02-19)

Merge requested for M33

### la...@google.com (2014-02-25)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-04)

mkwst@ - can you please merge this to M33 ASAP? We have a release being cut tomorrow.

### bu...@chromium.org (2014-03-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168445

------------------------------------------------------------------------
r168445 | mkwst@chromium.org | 2014-03-05T07:53:48.762432Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/bindings/scripts/code_generator_v8.pm?r1=168445&r2=168444&pathrev=168445
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/http/tests/security/cross-frame-access-dispatchEvent-expected.txt?r1=168445&r2=168444&pathrev=168445
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/http/tests/security/cross-frame-access-dispatchEvent.html?r1=168445&r2=168444&pathrev=168445

Merge 166999 "Add cross-origin BindingsSecurity checks to 'Event..."

> Add cross-origin BindingsSecurity checks to 'EventTarget::dispatchEvent'.
> 
> BUG=342618
> 
> Review URL: https://codereview.chromium.org/150203016

TBR=mkwst@chromium.org

Review URL: https://codereview.chromium.org/187313004
------------------------------------------------------------------------

### mb...@chromium.org (2014-03-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-07)

aidanphs - how would you like to be credited in our release notes? We'll go with "Credit to aidanphs" unless you tell us otherwise. Thanks.

### ai...@gmail.com (2014-03-07)

aidanhs (minus the 'p') is my usual handle :)

### ti...@chromium.org (2014-04-14)

My apologies for the delay here - $3000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-06)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### ai...@gmail.com (2014-05-07)

Thanks!

### cl...@chromium.org (2014-05-21)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/342618?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078889)*
