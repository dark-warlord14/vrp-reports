# Security: Creating a loop in the DOM tree (99% a DoS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061847](https://issues.chromium.org/issues/40061847) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink |
| **Reporter** | pa...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2012-07-26 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 20.0.1132.57 m stable  

Operating System: all

Source\WebCore\dom\ContainerNode.cpp

bool ContainerNode::replaceChild(PassRefPtr<Node> newChild, Node\* oldChild, ExceptionCode& ec, bool shouldLazyAttach)  

{  

...

1. checkReplaceChild(newChild.get(), oldChild, ec);  
   
   if (ec)  
   
   return false;
   
   ...
2. removeChild(oldChild, ec);  
   
   if (ec)  
   
   return false;  
   
   ...  
   
   // Add the new child(ren)  
   
   for (NodeVector::const\_iterator it = targets.begin(); it != targets.end(); ++it) {  
   
   ...  
   
   if (next)
3. ```
        insertBeforeCommon(next.get(), child);  
   
   ```
   
   ...
4. ```
    updateTreeAfterInsertion(this, child, shouldLazyAttach);  
   
   ```

1 - check hierarchy and bail if (but not only if) oldChild is a descendant of newChild  

2 - by intercepting the removal event, we mess up the DOM a bit, so that oldChild->next() is  

a descendant of newChild  

3 - this creates a loop in the DOM: newChild is accessible by next->prev() and next->parent()->...  

4 - infinite loop

Program received signal SIGSEGV, Segmentation fault.  

WebCore::Node::typeTag (this=<error reading variable: Cannot access memory at address 0x7fffc0617ff0>) at third\_party/WebKit/Source/WebCore/dom/Node.h:703  

703 NodeTypeTag typeTag() const { return static\_cast<NodeTypeTag>(m\_nodeFlags & NodeTypeTagMask); }

This could be exploitable, if there was a way not to crash inside  

updateTreeAfterInsertion(). I don't see how that could be done, so you decide.

Adding checkReplaceChild just before the for() would solve this problem.

## Attachments

- [replace.html](attachments/replace.html) (text/html; charset=us-ascii, 1.0 KB)
- [new.poc.html](attachments/new.poc.html) (text/html; charset=us-ascii, 866 B)

## Timeline

### js...@chromium.org (2012-07-28)

This is a renderer stack exhaustion. It's not a security issue because we isolate renderers in separate processes. This means that a site can crash its own tab, but does not affect the browser or other tabs.

### pa...@gmail.com (2012-07-29)

This isn't a stack exhaustion caused by, for example, a deeply nested html like "<p>"^n+"</p>"^n. If it's possible to intercept an event raised from updateTreeAfter* (before the stack exhaustion), or avoid crashing inside this procedure in any other way, then manipulating a looped DOM tree from JS could potentially lead to more interesting crashes. Classifying it as a DOS basing only on the stack signature is insufficient, IMO.



### sc...@gmail.com (2012-07-29)

Yeah, we need the opinion of a DOM expert here. cc:ed Dimitri. This sounds similar to some DOM issues noted by Mark Dowd in his audit a couple of years back.

### dg...@chromium.org (2012-07-29)

Ryosuke and Morrita-san have totally stolen the DOM expert title from me :)

### [Deleted User] (2012-07-30)

looking.

### [Deleted User] (2012-07-30)

https://bugs.webkit.org/show_bug.cgi?id=92619

### [Deleted User] (2012-07-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-08-05)

Fixed: http://trac.webkit.org/changeset/124156

No one seemed to have a firm opinion on security impact. I don't see anything obvious, but will flag it low out of an abundance of caution.

### pa...@gmail.com (2012-08-08)

Still crashes -- collectChildrenAndRemoveFromOldParent can fire a mutation event.

### [Deleted User] (2012-08-09)

Upstreamed again - https://bugs.webkit.org/show_bug.cgi?id=93587

### [Deleted User] (2012-08-10)

And fixed https://trac.webkit.org/changeset/125237

### in...@chromium.org (2012-08-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-10)

@morrita @rniwa: thanks for the two fixes! Now that you understand it further, did you have any thoughts on whether this tree inconsistency could lead to any bad conditions such as a use-after-free? I want to make sure we reward pawlkt under our reward program if that were the case.

### [Deleted User] (2012-08-10)

These bad topologies tend to result in script-contextless execution of scripts (i.e. cross origin bug).

### sc...@gmail.com (2012-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

@pawlkt: we don't know of any bad impact from this bug / situation, but we'd like to award you a $500 Chromium Security Reward out of an abundance of caution.

### pa...@gmail.com (2012-08-20)

Thanks.

### sc...@gmail.com (2012-08-25)

M22: https://trac.webkit.org/changeset/125237 -> https://trac.webkit.org/changeset/126668 (older CL already in M22)

### sc...@gmail.com (2012-09-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/139168?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061847)*
