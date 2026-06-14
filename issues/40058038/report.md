# Security: Arbitrary memory read in libxslt

| Field | Value |
|-------|-------|
| **Issue ID** | [40058038](https://issues.chromium.org/issues/40058038) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Internals |
| **Reporter** | ni...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-05-09 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

When parsing a XSLT stylesheet containing a DTD, a structure of type xmlEntity is accessed as another type. The value of cur->ns->href is then compared with a string. Given that this value is controlled by the attacker, it can access arbitrary memory locations.

**VERSION**

Chrome: 18.0.1025.162  

Chromium: 18.0.1025.151 (Build de développement 130497 Linux) Ubuntu 10.04

$ xsltproc --version  

Using libxml 20706, libxslt 10126 and libexslt 815  

xsltproc was compiled against libxml 20706, libxslt 10126 and libexslt 815  

libxslt 10126 was compiled against libxml 20706  

libexslt 815 was compiled against libxml 20706

BACKTRACE

#0 xmlStrEqual\_\_internal\_alias (str1=0x2a2a2a2a <Address 0x2a2a2a2a out of bounds>,  

str2=0x1cf444 "<http://www.w3.org/1999/XSL/Transform>") at xmlstring.c:162  

#1 0x001aa384 in xsltParseTemplateContent (style=0x805cc58, templ=0x80598e8) at xslt.c:4849  

#2 0x001ac824 in xsltParseStylesheetProcess (ret=0x805cc58, doc=0x80598e8) at xslt.c:6456  

#3 0x001acd2c in xsltParseStylesheetImportedDoc (doc=0x80598e8, parentStyle=0x0) at xslt.c:6627  

#4 0x001acddf in xsltParseStylesheetDoc (doc=0x80598e8) at xslt.c:6666  

#5 0x0804a7f4 in main (argc=4, argv=0xbffff7e4) at xsltproc.c:830

**REPRODUCTION CASE**

When magic.xml is opened in a browser, it will load magic.xsl, trigger the bug and crash the current tab.

POC CODE

<!DOCTYPE whatever [
<!ATTLIST magic blabla CDATA "anything">
```
<!ENTITY foobar "abcd_efg\*\*\*\*kl_mnop_qrst_uvwx_yzAB_CDEF_GHIK_KLMN_OPQR_STUV_WXYZ">  

```

]>  

<magic xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"/>

ANALYSIS

Once the XSL document is parsed, we get the following layout:

XML\_DOCUMENT\_NODE  

type: xmlDoc  

name: magic.xsl

```
       +  
       | children  
       v  
                       next  
  XML_DTD_NODE  +---------------->  XML_ELEMENT_NODE  
   type: xmlDtd                       type: xmlNode  
   name: whatever                     name: magic  

       +  
       |  children  
       v  
                       next  

```

XML\_ATTRIBUTE\_DECL +-------------> XML\_ENTITY\_DECL  

type: xmlAttribute type: xmlEntity  

name: blabla name: foobar

function xsltParseTemplateContent() at libxslt-1.1.26/libxslt/xslt.c:4830

4837 cur = templ->children;  

=> "cur" points to a XML\_DTD\_NODE structure

4839 while (cur != NULL) {  

=> 1st time we enter the "while" loop  

4849 if (IS\_XSLT\_ELEM(cur)) {  

=> neither the "if" or "else if" branchs are taken  

4966 if (cur->children != NULL) {  

4967 if (cur->children->type != XML\_ENTITY\_DECL) {  

4968 cur = cur->children;  

4969 continue;  

4970 }  

4971 }  

=> "cur" now points to a XML\_ATTRIBUTE\_DECL structure

4839 while (cur != NULL) {  

=> 2nd time we enter the "while" loop  

4849 if (IS\_XSLT\_ELEM(cur)) {  

=> neither the "if" or "else if" branchs are taken  

4966 if (cur->children != NULL) {  

=> "cur" has no child  

4973 if (cur->next != NULL) {  

4974 cur = cur->next;  

4975 continue;  

4976 }  

=> "cur" now points to a XML\_ENTITY\_DECL structure

4839 while (cur != NULL) {  

=> 3rd time we enter the "while" loop  

4849 if (IS\_XSLT\_ELEM(cur)) {  

=> "cur" is of type xmlEntity, which hasn't a "ns" entry  

=> "cur->ns->href" points inside the entity value

From libxslt-1.1.26/libxslt/xsltutils.h:  

54 #define IS\_XSLT\_ELEM(n) \  

55 (((n) != NULL) && ((n)->ns != NULL) && \  

56 (xmlStrEqual((n)->ns->href, XSLT\_NAMESPACE)))  

=> crash in xmlStrEqual while dereferencing n->ns->href

PATCH

It could be enough to test near line 4974 if "cur->next->type != XML\_ENTITY\_DECL". This wasn't tested.

## Attachments

- [magic.xsl](attachments/magic.xsl) (text/plain; charset=us-ascii, 232 B)
- [magic.xml](attachments/magic.xml) (application/xml; charset=us-ascii, 66 B)
- [crash_element_decl.xsl](attachments/crash_element_decl.xsl) (text/plain; charset=us-ascii, 280 B)
- [struct_as_xmlNode.png](attachments/struct_as_xmlNode.png) (image/png; charset=binary, 34.4 KB)
- [struct_as_xmlEntity.png](attachments/struct_as_xmlEntity.png) (image/png; charset=binary, 29.1 KB)
- [chromium-127417.patch](attachments/chromium-127417.patch) (text/x-diff; charset=us-ascii, 536 B)

## Timeline

### sc...@gmail.com (2012-05-09)

I'll deal with triage / fix of this.

### ni...@gmail.com (2012-05-09)

The patch I proposed isn't sufficient. The problem occurs with ENTITY declarations (as shown before) but also with ELEMENT ones. However, ELEMENT will crash the program when reading fixed values near NULL (0x8 to 0xC, depending of the type of the element).

mov    eax,DWORD PTR [esi+0x24] => x->ns
...
mov    eax,DWORD PTR [eax+0x8]  => x->ns->href

struct _xmlNode {
    ...
    xmlNs           *ns;        /* pointer to the associated namespace */
    ...
}

struct _xmlNs {
    struct _xmlNs  *next;       /* next Ns link for this node  */
    xmlNsType      type;        /* global or local */
    const xmlChar *href;        /* URL for the namespace */
    const xmlChar *prefix;      /* prefix for the namespace */
    void           *_private;   /* application data */
    struct _xmlDoc *context;    /* normally an xmlDoc */
};

struct _xmlEntity {
    ...
    xmlChar         *orig;       /* content without ref substitution - Easy to control */
    ...
}

struct _xmlElement {
    ...
    xmlElementTypeVal      etype;       /* The type - Crash when dereferencing etype+8 */
    ...
}

### ni...@gmail.com (2012-05-09)

_private and context are controlled by the attacker, but I didn't find any interesting path (like free() or some pointers to functions).

### ni...@gmail.com (2012-05-11)

Using asan-linux-beta-19.0.1084.46.zip (64 bits) and the same PoC => NULL deref in xmlStrEqual

==11454== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc 0x7f2ad81b644a sp 0x7fffc77e3940 bp 0x7fffc77e3940 T0)

    #0  0000000003f4f44a <xmlStrEqual+0x3a>:
 3f4f44a:       8a 00                   mov    (%rax),%al
    #1  xsltParseTemplateContent+0x36a
    #2  xsltParseStylesheetProcess+0x32b5
    #3  xsltParseStylesheetImportedDoc+0x495
    #4  xsltParseStylesheetDoc+0x1c
    #5  _ZN7WebCore13XSLStyleSheet17compileStyleSheetEv+0x28b
    #6  _ZN7WebCore13XSLTProcessor17transformToStringEPNS_4NodeERN3WTF6StringES5_S5_+0x4de
    #7  _ZN7WebCore8Document17applyXSLTransformEPNS_21ProcessingInstructionE+0x2cb
    #8  _ZN7WebCore8Document24collectActiveStylesheetsERN3WTF6VectorINS1_6RefPtrINS_10StyleSheetEEELm0EEE+0x183e
    #9  _ZN7WebCore8Document23updateActiveStylesheetsENS_23StyleSelectorUpdateFlagE+0x1c4
    #10  _ZN7WebCore8Document20styleSelectorChangedENS_23StyleSelectorUpdateFlagE+0x12b
    #11  _ZN7WebCore8Document18removePendingSheetEv+0x43
    #12  _ZN7WebCore21ProcessingInstruction11sheetLoadedEv+0xc3
    #13  _ZN7WebCore13XSLStyleSheet11checkLoadedEv+0xd1
    #14  _ZN7WebCore19CachedXSLStyleSheet11checkNotifyEv+0x21f
    #15  _ZN7WebCore19CachedXSLStyleSheet4dataEN3WTF10PassRefPtrINS_12SharedBufferEEEb+0x40b
    #16  _ZN7WebCore17SubresourceLoader16didFinishLoadingEd+0x23b
    #17  _ZN11webkit_glue16WebURLLoaderImpl7Context18OnCompletedRequestERKN3net16URLRequestStatusERKSsRKN4base9TimeTicksE+0x7f7


### in...@chromium.org (2012-05-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-12)

Chris, please feel to fix the tags. Was doing some tag cleanup :)

### in...@chromium.org (2012-05-12)

Actually i shouldnt assign the severity, that is a bad practice without verifying.

### sc...@gmail.com (2012-05-25)

Sorry I haven't gotten to this yet. It's getting near the top of the list.

@nicolas.gregoire@agarri.fr: did you know that we offer reward "bonuses" for patches to security bugs? It sounds like you're well on top of the issue at a source-code level so perhaps you had a patch to propose?

### sc...@gmail.com (2012-05-31)

Daniel, here's another one. Sorry for taking so long to cc: you.

### ve...@gmail.com (2012-05-31)

The small attached patch should fix this, can you verify. Libxslt was
assuming element nodes at that level. At least this fixes the problem for me :-)

Daniel

### sc...@gmail.com (2012-06-01)

Patch seems to work nicely here. I'll land it to Chromium.

### bu...@chromium.org (2012-06-01)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=140041

------------------------------------------------------------------------
r140041 | cevans@chromium.org | Fri Jun 01 09:47:04 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxslt/libxslt/xsltutils.h?r1=140041&r2=140040&pathrev=140041
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxslt/README.chromium?r1=140041&r2=140040&pathrev=140041

Fix crash with unexpected DTD nodes in XSLT.

BUG=127417
Review URL: https://chromiumcodereview.appspot.com/10441148
------------------------------------------------------------------------

### sc...@gmail.com (2012-06-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-06-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-06-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=140843

------------------------------------------------------------------------
r140843 | cevans@chromium.org | Wed Jun 06 14:41:54 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1132/src/third_party/libxslt/README.chromium?r1=140843&r2=140842&pathrev=140843
 M http://src.chromium.org/viewvc/chrome/branches/1132/src/third_party/libxslt/libxslt/xsltutils.h?r1=140843&r2=140842&pathrev=140843

Merge 140041 - Fix crash with unexpected DTD nodes in XSLT.

BUG=127417
Review URL: https://chromiumcodereview.appspot.com/10441148

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10533035
------------------------------------------------------------------------

### sc...@gmail.com (2012-06-22)

@nicolas.gregoire: thanks for this bug! The arbitrary read might be useful in some exploit scenario therefore we'd be delighted to offer you a $500 Chromium Security Reward.

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

### sc...@gmail.com (2012-06-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-07-13)

CC'ing Debian libxml maintainer.

### sc...@gmail.com (2012-07-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-08-30)

CC'ing Solaris libxml2 maintainer.

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/127417?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058038)*
