# Crash by form controls with form attributes under orphan nodes

| Field | Value |
|-------|-------|
| **Issue ID** | [40087039](https://issues.chromium.org/issues/40087039) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | st...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2011-01-19 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 9.0.597.67 beta  

**URLs (if applicable) :**  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Opera 11: OK  

Safari 5: OK  

Firefox 3.x: OK  

Firefox 4.x: OK  

Chrome 8.0.552.237 (Mac OS X / Windows XP): OK  

Chrome 9.0.597.67 (Mac OS X / Windows XP (several systems) / Windows 7): FAIL  

Chrome 10.x (Mac OS X): FAIL  

IE 7/8: OK

**What steps will reproduce the problem?**

1. Login on <https://login.yes-co.com/> (username "[stefanvanzanden@gmail.com](mailto:stefanvanzanden@gmail.com)" and password "test123")
2. Hover de tab called "Projecten";
3. Click on the project "(BBvk) Lammertkamp 40";
4. Click on the category "Algemeen" (it is crashing the most on this one, but you can also try other tabs as long as it is containing forms);
5. Refresh this tab (press F5 when window is focused) until the crash happens (often within the first 10 refreshes);

**What is the expected result?**  

Well.. that it stops crashing :).

**What happens instead?**  

Getting an "Aw Snap" BWOD (Blue Window Of Death :)) message without detailed information on what goes wrong;

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

1. From my own Javascript logs it seems to crash alot on and stops on random logs, but mostly the problems occur when destroying an item

(where I first disconnect events from DomElements before destroying the DomElement). But beside this I also see it crash when adding a  

class or applying a style (using Dojo 1.4);  

2. I thought the problems occured because due to the legacy code I am doing alot some evalling of inline generated Javascript, but I am

currently removing all this on another development environment but all it does is make it crash just a bit less.  

3. All crashes should have been send to Google (it is enabled) so maybe that could help.  

4. This problem is occuring on several systems using Google Chrome 9 beta;  

5. I hope this can be fixed, we currently have an average of 49% of our users using Chrome and after our efforts to convince them using it  

would be rather bad to have them move to either Firefox;

Thanks in advanced for any reply / fix or more information for me to debug the problem :).

Stefan van Zanden

## Timeline

### st...@gmail.com (2011-01-19)

Not sure if this is helpfull (not sure what is send to Google using the crash reports), but when I disable the webdeveloper console and turn on the logging in Chrome, the last thing my "chrome_debug.log" reports are messages about "OnResponseCompleted", and this is every time (checked for 10 crashes), a dump of the different ones:


[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1345)] Resuming: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7
[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1393)] OnReadCompleted: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7
[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1345)] Resuming: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7
[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1393)] OnReadCompleted: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7
[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1345)] Resuming: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7
[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1393)] OnReadCompleted: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7
[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1345)] Resuming: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7
[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1393)] OnReadCompleted: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7
[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1393)] OnReadCompleted: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7
[5016:4068:198427718:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1461)] OnResponseCompleted: https://yispro-prod.devel.redbus.yes-co.nl/project/16/edit/7


[5016:4068:198333250:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1345)] Resuming: https://yispro-prod.devel.redbus.yes-co.nl/main/search/googlemaps.php?action=getGoogleMapsImage&geolatitude=52.3478175&geolongitude=5.6486385&projectid=16
[5016:4068:198333250:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1393)] OnReadCompleted: https://yispro-prod.devel.redbus.yes-co.nl/main/search/googlemaps.php?action=getGoogleMapsImage&geolatitude=52.3478175&geolongitude=5.6486385&projectid=16
[5016:4068:198333250:VERBOSE1:.\browser\renderer_host\resource_dispatcher_host.cc(1461)] OnResponseCompleted: https://yispro-prod.devel.redbus.yes-co.nl/main/search/googlemaps.php?action=getGoogleMapsImage&geolatitude=52.3478175&geolongitude=5.6486385&projectid=16




Is there a way for me to see what is actually send to Google when a crash occurs?




### th...@chromium.org (2011-01-19)

Please get a crash report id:
http://www.chromium.org/for-testers/bug-reporting-guidelines/reporting-crash-bug

Crash reports contain backtraces for all the threads in the crashing process, values in the cpu registers at the time of the crash, the DLLs loaded in the process, and some generic system information like what OS you are running and how long Chrome has been running. All of this is open source: http://code.google.com/p/google-breakpad/

### st...@gmail.com (2011-01-20)

[Comment Deleted]

### st...@gmail.com (2011-01-20)

Hello,

Thanks for the fast response, I looked through the eventvwr.msc on my Windows XP and Windows 7, but all I see is a bunch of warnings and errors registered, but they are giving crash uploaded id's, so hope these came through, else I have to send the ones generated from Mac OS X at home...

From Windows XP I got the following ones:
Crash uploaded. Id=dcf7562eb988a479..
Crash uploaded. Id=7a2b7ea9d6dce7a2..
Crash uploaded. Id=8ecdf09d50024857..
Crash uploaded. Id=a35b5378344d7017..
Crash uploaded. Id=d671c59ae3632f6a..

From a Windows 7 machine I got:
Crash uploaded. Id=e5ef48e40c88a64c..

Oh and the Crash report dump directories on both systems seem to be empty.

Hope it helps.

Grz,
Stefan

### th...@chromium.org (2011-01-20)

Thread 0 *CRASHED* ( EXCEPTION_ACCESS_VIOLATION_READ @ 0x00000000 )
			
0x024230d7 	[chrome.dll 	- htmlformcontrolelement.cpp:477] 	WebCore::HTMLFormControlElement::resetFormOwner(WebCore::HTMLFormElement *)
0x02166fcf 	[chrome.dll 	- document.cpp:4419] 	WebCore::Document::resetFormElementsOwner(WebCore::HTMLFormElement *)
0x0242780f 	[chrome.dll 	- htmlformelement.cpp:151] 	WebCore::HTMLFormElement::removedFromDocument()
0x021ba33e 	[chrome.dll 	- containernode.cpp:442] 	WebCore::ContainerNode::removeChild(WebCore::Node *,int &)
0x0215ae23 	[chrome.dll 	- node.cpp:561] 	WebCore::Node::removeChild(WebCore::Node *,int &)
0x022c03b9 	[chrome.dll 	- v8nodecustom.cpp:105] 	WebCore::V8Node::removeChildCallback(v8::Arguments const &)

### st...@gmail.com (2011-01-20)

And here is a client_id generated from Mac OS X on Chrome 9 beta:

      "client_id": "1DF007FB-15A2-BBC3-4AF8-AAB81165A65E",

### st...@gmail.com (2011-01-20)

@5

Not sure if that information is meant for me, nor do I know anything about the Chrome inside code :)

But does that mean that it goes somewhere wrong when I am removing a HTMLDomElement from the tree, which might be already destroyed or still has events attached to it, just guessing over here :).

What I basically do in our web application is disconnect attached events on HTMLDomElement before destroying the HTMLDomElement itself, so that the Garbage collection can do it's work better (since it's a full Javascript based web application else it would pile up used memory on some browsers :)). 
 

### [Deleted User] (2011-01-26)

[Empty comment from Monorail migration]

### tk...@chromium.org (2011-01-26)

[Empty comment from Monorail migration]

### tk...@chromium.org (2011-01-27)

HTMLFormControlElement.cpp:477 is
http://trac.webkit.org/browser/branches/chromium/597/WebCore/html/HTMLFormControlElement.cpp?rev=76406#L477
>         document()->checkedRadioButtons().addButton(this);

document() never returns NULL.  So "this" might be NULL?


### ba...@google.com (2011-01-27)

Hi Kent-san,

Yes, as far as I briefly investigated, Document::m_formElementsWithFormAttribute contains pointers to HTMLFormControlElement which are no longer valid in that case. There might be resource leak so I'll investigate the cause more detail.

Regards,

### in...@chromium.org (2011-01-27)

Kent confirmed over email that this is a use after free. Adding the security tags.

### js...@chromium.org (2011-01-27)

This looks like the first half of https://crbug.com/chromium/65577. It had two separate patches, and it seems that the following one was not merged to m9: http://trac.webkit.org/changeset/75676


### in...@chromium.org (2011-01-27)

Filed as a security bug to WebKit.
https://bugs.webkit.org/show_bug.cgi?id=53223

### js...@chromium.org (2011-01-27)

Re: https://crbug.com/chromium/70078#c13 - On second thought, it looks different. It's hard to tell with the code churn and recent file moves.

### ba...@google.com (2011-01-27)

Hi jschuh,

Thank you for your comment.
Kent-san found out the cause and I'm working on fixing it.

### tk...@chromium.org (2011-01-31)

[Empty comment from Monorail migration]

### tk...@chromium.org (2011-01-31)

bashi@ fixed the problem in WebKit.
http://trac.webkit.org/changeset/77114


### in...@chromium.org (2011-01-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-31)

Needs merge to M9 and M10

### st...@gmail.com (2011-01-31)

Hey All,

Thanks alot for taking a look into and fixing my issue, could someone maybe answer some question to clarify the problem(s) causing it?

1. Is the fixed problem the problem for ALL my crashes from the last weeks?
2. Where or when can I check if the problem will be gone in Chrome 9 beta (are fixes going through Chrome 10 Dev channel first)?
3. Is this related to some bad coding on our part and if so where should I start looking for it?
4. Is there a situation possible where Chrome 9 will be release as "stable" without fixing this issue (because of the new 6 week shedule for new version Google introduced)?

Sorry for all the n00b questions, I am kinda new to this reporting process :).

Thanks alot in advanced.

Stefan van Zanden


### tk...@chromium.org (2011-02-01)

> 1. Is the fixed problem the problem for ALL my crashes from the last weeks?

We hope so.  I think all of crashes of which you provided crash IDs were caused by a single bug, and we fixed it.

> 2. Where or when can I check if the problem will be gone in Chrome 9 beta (are fixes going through Chrome 10 Dev channel first)?

I think the build on http://build.chromium.org/f/chromium/continuous/win/2011-01-31/73223/ already has the fix.

> 3. Is this related to some bad coding on our part and if so where should I start looking for it?

Your code has no problem.
This bug was triggered by form controls with form= attributes.  We can avoid the bug by using no form= attributes.

> 4. Is there a situation possible where Chrome 9 will be release as "stable" without fixing this issue (because of the new 6 week shedule for new version Google introduced)?

I'm afraid the first Chrome 9 stable release won't have the fix.  It'll be released soon and the fix was too late.



### st...@gmail.com (2011-02-01)

> We hope so.  I think all of crashes of which you provided crash IDs were caused by a single bug, and we fixed it.

Ok, I am not entirely familiar with the report system but if I am correct there should be around 200 crashes reported with those id's.

> I think the build on http://build.chromium.org/f/chromium/continuous/win/2011-01-31/73223/ already has the fix.

Hmm.. the mini installer doesn't seem to do anything for me, is it suppose to patch the files of my current Chrome installation?

> Your code has no problem.
> This bug was triggered by form controls with form= attributes.  We can avoid the bug by using no form= attributes.

Ok I find this hard to believe, apparently I am doing something in my code that makes it crash and I am doing something noeone else seems 

to be doing since it isn't important enough to stall the release nor does it crash ever on other webapplications I often use.

> I'm afraid the first Chrome 9 stable release won't have the fix.  It'll be released soon and the fix was too late.
 
Ok.. thats a bit disappointing, because since this will cause a crash every few requests this will create an unworkable situation in our 

application, do you have any workarounds for us?
I hope I can do something in my code to prevent the crash, else we will have to instruct our customers (49% of our current users is 

currently using Chrome) to prevent the Chrome updates, or even worse... recommend a slower browser like IE8 / Firefox :(.

I have already cleaned out any use of legacy code in our next version (use of eval is gone) but that didn't help, Ill check if it helps if 

I don't help the garbage collector by cleaning up events before destroying stuff (will create memory problems in this almost full Ajax 

based Webapplication, but I rather have it crash over a long period of time then every few requests :( ).

Thanks again for all the help :).


### st...@gmail.com (2011-02-01)

Ok.. not an ideal situation but I disabled all the event cleaning up prior destroying the HTMLDomElement in case of any Chrome browser and it now seems to be no longer crashing (hurray! :)), only downside is that Chrome can't clean up all the used memory anymore so it is slowly climbing until the tab is closed.

### sc...@gmail.com (2011-02-03)

@stefanvanzanden: thanks for catching this regression. Since it's a security bug, it qualifies for a $500 Chromium Security Reward, if you'd like to accept?

---
NOTE: normally we do not reward security bugs unless initially filed with the
security template. Sometimes we make an exception for the first time an individual
files a security bug as a non-security issues.
For full guidelines on filing security bugs, see:
http://www.chromium.org/Home/chromium-security/reporting-security-bugs
---

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

### st...@gmail.com (2011-02-09)

@scarybea

Wow, cool, didn't know I would qualify for an actual reward since I only reported / workedaround the crashes without knowing it had to do anything with security :).

Since this was partly done in time of the company I work at (Yes-co Nederland B.V.) we decided to accept it and take our development team for some teambuilding.

Do I need to send You our bank details?

Thanks in advanced.
Stefan van Zanden



### in...@chromium.org (2011-02-09)

There is no FormAssociatedLement in m9, @tkent - does this issue exists in m9 ?

Merged to m10 in r78155.

### tk...@chromium.org (2011-02-09)

m9 ?

I think M9 also has this bug.  The changes to FormAssociatedElement should
be applied to HTMLFormControlElement.

BTW, I can't access crbug.com/70078 with a browser.

### sc...@gmail.com (2011-02-10)

@inferno: original bug report is a user-reported regression against M9 beta, so seems like it should affect M9 yeah.
The functionality regression aspect seems like another reason to merge.

@stefanvanzanden: great idea for use of the reward! Sounds like you guys deserve a nice meal and a beer or two for having to devise a work around this bug.
We'll ping this bug with instructions on how to collect the reward once we've released the fix.

### in...@chromium.org (2011-02-10)

@tkent emailed me and will handle this merge for m9.

### tk...@chromium.org (2011-02-10)

Merged to 597 (M9) branch as r78166.


### in...@chromium.org (2011-02-10)

Thanks a lot Kent.

### in...@chromium.org (2011-02-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-10)

sorry status was not getting updated, so had to play this game.

### ch...@gmail.com (2011-02-11)

we had to roll this out of m9 as it broke devtools, history, and google

### sc...@gmail.com (2011-02-12)

@cdn: is that all?

### tk...@chromium.org (2011-02-14)

> we had to roll this out of m9 as it broke devtools, history, and google

What problems did we have? Crash?



### in...@chromium.org (2011-02-14)

google.com search box -> press enter key and form does not submit, instead the input field works like a multi line box and cursor moves to new lines in the seach text box.

devtools -> blank, just two grey strips, no text, no button, no input.

NO crash.

### tk...@chromium.org (2011-02-14)

Ah, I have found I made a mistake in WebKit 78166.  I'll retry it.


### tk...@chromium.org (2011-02-14)

Merged to M9 branch as WebKit 78455.


### in...@chromium.org (2011-02-14)

Fingers crossed, still checking :)

### sc...@gmail.com (2011-03-01)

@stefanvanzanden: this is now fixed in stable with release 9.0.597.107
Sorry for the stability issues and thanks again for the report!
E-mail me, cevans@chromium.org and I can help get you set up to collect the reward.

### st...@gmail.com (2011-03-01)

@scarybea

Thanks alot, I have removed the hack that prevents the crashing and it seem to be stopped (Tested on the Mac OS X version), also memory leaks caused by circular reference are now under control again :).

### st...@gmail.com (2011-03-01)

Ok, also tested on a Windows XP machine and the crashing is gone there asswel :).

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-11)

Reward to be upped to $1337 and donated to charity.

### sc...@gmail.com (2012-05-26)

$1337 paid to American Red Cross.

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

This issue was migrated from crbug.com/chromium/70078?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087039)*
