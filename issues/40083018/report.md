# Security: properly escaped href attribute leading to offline XSS upon saving a page

| Field | Value |
|-------|-------|
| **Issue ID** | [40083018](https://issues.chromium.org/issues/40083018) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Editing |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2015-6790 |
| **Reporter** | in...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2015-10-11 |
| **Bounty** | $500.00 |

## Description

NOTE: This is a split of issue #503217 I previously reported

**VULNERABILITY DETAILS**  

Upon saving a page with a crafted anchor tag, escaped HTML characters followed after "#" in the href attribute will render as regular HTML entities. This makes it possible to steal content or CSRF tokens by making a victim save and open a page that includes this link.

**VERSION**  

Chrome Version: 45.0.2454.101 m stable, 48.0.2533.0 canary  

Operating System: Windows 10 64 bit

**REPRODUCTION CASE**

1. Save this page (CTRL + S)
2. Open
3. A popup box will appear

- Link used for this PoC:  
  
  <http://www.example.com/#&quot;&gt;&lt;script&gt;alert(0)&lt;/script>>

ATTACK SCENARIO

I found a way to abuse this behavior on Facebook:

1. Attacker posts: "Share this post, save the page and see what happens!"
2. Attacker commented the following link: [http://www.example.com/#&quot;&gt;&lt;script&gt;alert&#40;'Thanks,'+document.getElementsByClassName&#40;'\_2dpb'&#41;[0].innerText&#41;&lt;/script&gt;a](http://www.example.com/#&quot;&gt;&lt;script&gt;alert&)
3. Upon opening the saved page, the victim will see a popup box containing "Thanks", followed by his or hers personal name. Obviously we can steal a lot more interesting stuff other than their name.

I added some screenshots of the PoC in actions (PoC is not made public)

## Attachments

- [href1.PNG](attachments/href1.PNG) (image/png, 38.0 KB)
- [href2.PNG](attachments/href2.PNG) (image/png, 12.3 KB)

## Timeline

### in...@gmail.com (2015-10-11)

Sorry, forgot to add the link to the actual PoC. My bad!
http://ceukelai.re/href/

But this may a well work
http://www.google.com#"><script>alert(0)</script>

### oc...@chromium.org (2015-10-12)

Thanks for the report.

Assigning yosin. yosin, please take a look or find a more appropriate owner.

### oc...@chromium.org (2015-10-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-12)

[Empty comment from Monorail migration]

### yo...@chromium.org (2015-10-13)

Ctrl+C/execCommand("copy") works correctly.

### yo...@chromium.org (2015-10-13)

It is caused by WebPageSerializerImpl::openTagToString() which append URL parameter
without escaping:

            if (element->hasLegalLinkAttribute(attrName)) {
                // For links start with "javascript:", we do not change it.
                if (attrValue.startsWith("javascript:", TextCaseInsensitive)) {
DANGER~~~~~~~~~~~~~> result.append(attrValue);
                } else {
                    // Get the absolute link
                    WebLocalFrameImpl* subFrame = WebLocalFrameImpl::fromFrameOwnerElement(element);
                    String completeURL = subFrame ? subFrame->frame()->document()->url() :
                                                    param->document->completeURL(attrValue);
                    // Check whether we have local files for those link.
                    if (m_localLinks.contains(completeURL)) {
                        if (!param->directoryName.isEmpty()) {
                            result.appendLiteral("./");
                            result.append(param->directoryName);
                            result.append('/');
                        }
DANGER ~~~~~~~~~~~~~~~~> result.append(m_localLinks.get(completeURL));
                    } else {
HERE ~~~~~~~~~~~~~~~~~~> result.append(completeURL);
                    }
                }


### yo...@chromium.org (2015-10-13)

In review: http://crrev.com/1398453005

Note: other than having URL attribute value, WebPageSerializerImpl escapes them:
  if (param->isHTMLDocument)
    result.append(m_htmlEntities.convertEntitiesInString(attrValue));
  else
    result.append(m_xmlEntities.convertEntitiesInString(attrValue));


### bu...@chromium.org (2015-10-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b770d85e37b2d0e248f04cf20606a2f3871ef039

commit b770d85e37b2d0e248f04cf20606a2f3871ef039
Author: yosin <yosin@chromium.org>
Date: Tue Oct 13 10:00:14 2015

Make WebPageSerializerImpl to escape URL attribute values in result.

This patch makes |WebPageSerializerImpl| to escape URL attribute values rather
than directly output URL attribute values into result.

BUG=542054
TEST=webkit_unit_tests --gtest_filter=WebPageSerializerTest.URLAttributeValues

Review URL: https://codereview.chromium.org/1398453005

Cr-Commit-Position: refs/heads/master@{#353712}

[modify] http://crrev.com/b770d85e37b2d0e248f04cf20606a2f3871ef039/third_party/WebKit/Source/web/WebPageSerializerImpl.cpp
[modify] http://crrev.com/b770d85e37b2d0e248f04cf20606a2f3871ef039/third_party/WebKit/Source/web/tests/WebPageSerializerTest.cpp
[add] http://crrev.com/b770d85e37b2d0e248f04cf20606a2f3871ef039/third_party/WebKit/Source/web/tests/data/pageserialization/url_attribute_values.html


### aa...@google.com (2015-10-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-11-28)

Requesting Merge for M47 (post-stable patch)

### ti...@google.com (2015-11-28)

[Automated comment] Less than 2 weeks to go before stable on M47, manual review required.

### ti...@google.com (2015-11-28)

Let's take this to the panel as a separate issue from https://crbug.com/chromium/503217

### in...@gmail.com (2015-11-28)

Cool! You can credit me for both issues as "Inti De Ceukelaire" (plus @securinti if we can add our tweet handle). Thanks for the fixes!

### ss...@google.com (2015-12-01)

Adding OS label, please change if incorrect

### ss...@google.com (2015-12-02)

Merge approved for M47 (branch 2526)

### bu...@chromium.org (2015-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/947b9d85a5e06ad7f3d658682db39443d2028c08

commit 947b9d85a5e06ad7f3d658682db39443d2028c08
Author: Yoshifumi Inoue <yosin@chromium.org>
Date: Wed Dec 02 08:43:46 2015

Make WebPageSerializerImpl to escape URL attribute values in result.

This patch makes |WebPageSerializerImpl| to escape URL attribute values rather
than directly output URL attribute values into result.

BUG=542054
TEST=webkit_unit_tests --gtest_filter=WebPageSerializerTest.URLAttributeValues

Review URL: https://codereview.chromium.org/1398453005

Cr-Commit-Position: refs/heads/master@{#353712}
(cherry picked from commit b770d85e37b2d0e248f04cf20606a2f3871ef039)

Review URL: https://codereview.chromium.org/1487273003 .

Cr-Commit-Position: refs/branch-heads/2526@{#496}
Cr-Branched-From: cb947c0153db0ec02a8abbcb3ca086d88bf6006f-refs/heads/master@{#352221}

[modify] http://crrev.com/947b9d85a5e06ad7f3d658682db39443d2028c08/third_party/WebKit/Source/web/WebPageSerializerImpl.cpp
[modify] http://crrev.com/947b9d85a5e06ad7f3d658682db39443d2028c08/third_party/WebKit/Source/web/tests/WebPageSerializerTest.cpp
[add] http://crrev.com/947b9d85a5e06ad7f3d658682db39443d2028c08/third_party/WebKit/Source/web/tests/data/pageserialization/url_attribute_values.html


### ti...@google.com (2015-12-07)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-08)

Congrats Inte - $500 for this report. There's a patch to M47 that is likely to roll out tomorrow that this fix will ship with. We'll credit you in the release notes and the CVE ID is CVE-2015-6790. 

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-19)

Bulk update: removing view restriction from closed bugs.

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

### lo...@redblink.com (2019-04-05)

stealing content or CSRF tokens by making a victim save and open a page that includes this link could have many adverse effects for webmasters . A detailed explaination by security experts at WPHH is worth mentioning here https://secure.wphackedhelp.com/blog/wordpress-xss-attack/ As we know, cookies help us to connect automatically. Therefore, with stolen cookies, we can login with other identities. And that’s one of the reasons why this attack is considered one of the most serious attacks.

An XSS attack is in progress on the client side. It can be run with different client-side programming languages. However, most often, this attack is done with Javascript and HTML.

The XSS cross site scripting attack allows to execute scripts on the client side. This means that you can only run JAVASCRIPT, HTML and other languages that will only run in the one who starts the script and not on the server directly, I let your imagination give you ideas.

### is...@google.com (2019-04-05)

This issue was migrated from crbug.com/chromium/542054?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083018)*
