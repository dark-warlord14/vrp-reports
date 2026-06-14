# Stale form associated element pointer in Document object

| Field | Value |
|-------|-------|
| **Issue ID** | [40086664](https://issues.chromium.org/issues/40086664) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ch...@gmail.com |
| **Created** | 2011-01-05 |
| **Bounty** | $1,000.00 |

## Description

Credit to Serg Glazunov

Opening this to track the second instance of <http://code.google.com/p/chromium/issues/detail?id=65577>

upstream bug for this is <https://bugs.webkit.org/show_bug.cgi?id=51905>

**VULNERABILITY DETAILS**  

A form control element doesn't call Document::unregisterFormElementWithFormAttribute when its "form" attribute's removed.

This should probably be fixed by adding the line  

document()->unregisterFormElementWithFormAttribute(this);  

after  

void HTMLFormControlElement::attributeChanged(Attribute\* attr, bool preserveDecls)  

{  

if (attr->name() == formAttr) {  

if (!fastHasAttribute(formAttr)) {

There's also a bit more complicated version of the attack. You can create a container element and append an input element to it; then append the container to another document's element. By this you also create a reference in Document::m\_formElementsWithFormAttribute which won't be removed after deletion of the input element.

I think this may be solved by overriding the willMoveToNewOwnerDocument method.

**VERSION**  

Chromium 10.0.603.0 (68309). Doesn't affect stable.

## Attachments

- [65577.html](attachments/65577.html) (text/html; charset=us-ascii, 678 B)

## Timeline

### in...@chromium.org (2011-01-13)

merged to m9 in http://trac.webkit.org/changeset/75681. fix revision in 75676.

### sc...@gmail.com (2011-01-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-25)

@serg.glazunov: congrats!! You know the drill by now, but this bug has qualified for a $1000 Chromium Security Reward. We should get the fix out to users and announced next week, hopefully.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-01-25)

Oh, doesn't affect stable I see. So thanks for making sure that Chrome 9 won't be affected either!

### sc...@gmail.com (2011-02-10)

Invoice finalized; payment is in e-payment system.


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

This issue was migrated from crbug.com/chromium/68641?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086664)*
