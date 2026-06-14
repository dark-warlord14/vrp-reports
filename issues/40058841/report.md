# Security: libxml2 growBuffer integer overflow on 64-bit machines

| Field | Value |
|-------|-------|
| **Issue ID** | [40058841](https://issues.chromium.org/issues/40058841) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2012-2807 |
| **Reporter** | as...@ut.ee |
| **Assignee** | [Deleted User] |
| **Created** | 2012-05-27 |
| **Bounty** | $3,000.00 |

## Description

Here is the growBuffer macro at parser.c:

#define growBuffer(buffer, n) { \  

xmlChar \*tmp; \  

buffer##\_size \*= 2; \  

buffer##\_size += n; \  

printf("growBuffer new\_size=%08x\n", buffer##\_size); \  

fflush(stdout); \  

tmp = (xmlChar \*) \  

xmlRealloc(buffer, buffer##\_size \* sizeof(xmlChar)); \  

if (tmp == NULL) goto mem\_error; \  

buffer = tmp; \  

}

and some of the code from xmlStringLenDecodeEntities:

```
int buffer_size = 0;  
int nbchars = 0;  

...  

if (nbchars > buffer_size - i - XML_PARSER_BUFFER_SIZE) {  
    growBuffer(buffer, i + XML_PARSER_BUFFER_SIZE);  
}  
if (nbchars > buffer_size) {  
    printf("copying %d bytes to index=%08x, buffer_size=%08x\n",  
           i, nbchars, buffer_size);  
    fflush(stdout);  
}  
for (;i > 0;i--)  
    buffer[nbchars++] = \*cur++;  

```

(I added the printf-s for debugging.)

An integer overflow can occur in the calculation of new buffer##\_size. But a 2GB malloc() has to succeed first, so only 64-bit machines are affected.  

The steps for triggering the overflow are:

1. grow the buffer up to buffer\_size=0x7fffffff and fill it
2. add another i=0x1000 bytes to buffer
3. growBuffer(buffer, 0x1000 + 0x64) is called
4. 0x7fffffff \* 2 = -2 (sign goes negative)
5. -2 + 0x1000 + 0x64 = 0x1062 (back to positive)
6. 0x1062 byte buffer is allocated
7. newly allocated buffer is written to out of range

If it wasn't for step 5, realloc(-2) would fail, which would be harmless. This is the case for most realloc-s that only multiply size by 2. But I think there  

are more cases like this one.

I think a possible solution would be to use ssize\_t (64-bit signed) instead of int (32-bit signed) for buffer\_size and nbchars.

**VERSION**  

Chrome Version: 18.0.969.0 (Developer Build 113953 Linux)  

Operating System: Arch linux, x86\_64

**REPRODUCTION CASE**  

Open bad.xml in chrome.

It will take quite a long time to process the file, ~5-10 minutes for my computer that has enough (>2GB) of free RAM. I tried it on a 1GB RAM  

computer with swap and it took hours.

It prints out:

...  

growBuffer new\_size=03ffff83  

growBuffer new\_size=07ffff87  

growBuffer new\_size=0fffff8f  

growBuffer new\_size=1fffff9f  

growBuffer new\_size=3fffffbf  

tcmalloc: large alloc 1073741824 bytes == 0x7f2c859fb000 @ 0x7f36bef6667f 0x7f36bef66791 0x7f36bef678ec 0x7f36bef6647c 0x7f36bef67009 0x7f36bef670dc 0x7f36c356cf67 0x7f36c0e1b097 0x7f36c0e1b5b3 0x7f36c0e1e718 0x7f36c0e2d2a9 0x7f36c0e2d408 0x7f36c0e2d98b 0x7f36c0e34359 0x7f36c0e3692f 0x7f36c172c1a7 0x7f36c172993e 0x7f36c306ce18 0x7f36c15e052e 0x7f36c15d2281 0x7f36c0c1378c 0x7f36c0c77c58 0x7f36c15d1fc9 0x7f36c15d232d 0x7f36c16065c5 0x7f36c1619cd4 0x7f36c1607a67 0x7f36c161a5d5 0x7f36c31ddaea 0x7f36c211311e 0x7f36c08c95af  

growBuffer new\_size=7fffffff  

tcmalloc: large alloc 2147487744 bytes == 0x7f2c057fa000 @ 0x7f36bef6667f 0x7f36bef66791 0x7f36bef678ec 0x7f36bef6647c 0x7f36bef67009 0x7f36bef670dc 0x7f36c356cf67 0x7f36c0e1b097 0x7f36c0e1b5b3 0x7f36c0e1e718 0x7f36c0e2d2a9 0x7f36c0e2d408 0x7f36c0e2d98b 0x7f36c0e34359 0x7f36c0e3692f 0x7f36c172c1a7 0x7f36c172993e 0x7f36c306ce18 0x7f36c15e052e 0x7f36c15d2281 0x7f36c0c1378c 0x7f36c0c77c58 0x7f36c15d1fc9 0x7f36c15d232d 0x7f36c16065c5 0x7f36c1619cd4 0x7f36c1607a67 0x7f36c161a5d5 0x7f36c31ddaea 0x7f36c211311e 0x7f36c08c95af  

growBuffer new\_size=00001062  

copying 4096 bytes to index=7fffff9b, buffer\_size=00001062

## Attachments

- [bad.xml.gz](attachments/bad.xml.gz) (application/x-gzip; charset=binary, 203.9 KB)
- [buffer.patch](attachments/buffer.patch) (text/x-diff; charset=us-ascii, 9.3 KB)

## Timeline

### sc...@gmail.com (2012-05-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-30)

cc:ing upstream.

### sc...@gmail.com (2012-05-30)

https://crash.corp.google.com/reportdetail?reportid=add9f90deaf5250c

Thread 0 *CRASHED* ( SIGSEGV @ 0x7fc3807e539b )

0x7fc3eefa5448	 [chrome]	 - third_party/libxml/src/parser.c:2594]	xmlStringLenDecodeEntities
0x7fc3eefa5ef8	 [chrome]	 - third_party/libxml/src/parser.c:2675]	xmlStringDecodeEntities
0x7fc3eefa6664	 [chrome]	 - third_party/libxml/src/parser.c:3723]	xmlParseAttValueInternal
0x7fc3eefa7046	 [chrome]	 - third_party/libxml/src/parser.c:8636]	xmlParseStartTag2
0x7fc3eefad8ad	 [chrome]	 - third_party/libxml/src/parser.c:10847]	xmlParseTryOrFinish
0x7fc3eefaecca	 [chrome]	 - third_party/libxml/src/parser.c:11625]	xmlParseChunk
0x7fc3ef58f933	 [chrome]	 - third_party/WebKit/Source/WebCore/xml/parser/XMLDocumentParserLibxml2.cpp:657]	WebCore::XMLDocumentParser::doWrite

---
                int i = xmlStrlen(ent->name);
                const xmlChar *cur = ent->name;

                buffer[nbchars++] = '&';
                if (nbchars > buffer_size - i - XML_PARSER_BUFFER_SIZE) {
                    growBuffer(buffer, i + XML_PARSER_BUFFER_SIZE);
                }
                for (;i > 0;i--)
                    buffer[nbchars++] = *cur++;
                buffer[nbchars++] = ';';       <---- crash here
---

Probably crashes at the line indicated due to incorrect type for strlen (int), which would be negative for a >2GB string and therefore the for loop would not run.

### sc...@gmail.com (2012-05-30)

BTW, FWIW: size_t is almost always the correct type for lengths, buffer sizes, counts, indexes etc. signed types just add headache / complexity / bugs.

### sc...@gmail.com (2012-05-31)

Ok. For Chromium, I'm sorely tempted to land the following patch. I will explain in a subsequent comment.


Index: /stuff/chrome/src/third_party/libxml/src/parser.c
===================================================================
--- /stuff/chrome/src/third_party/libxml/src/parser.c	(revision 139644)
+++ /stuff/chrome/src/third_party/libxml/src/parser.c	(working copy)
@@ -39,6 +39,7 @@
 #define XML_DIR_SEP '/'
 #endif
 
+#include <limits.h>
 #include <stdlib.h>
 #include <string.h>
 #include <stdarg.h>
@@ -2461,11 +2462,16 @@
  */
 #define growBuffer(buffer, n) {						\
     xmlChar *tmp;							\
-    buffer##_size *= 2;							\
-    buffer##_size += n;							\
+    size_t new_size = buffer##_size;					\
+    if (new_size > INT_MAX / 2) goto mem_error;				\
+    new_size *= 2;							\
+    if (new_size + n < new_size) goto mem_error;			\
+    if (new_size + n > INT_MAX / 2 / sizeof(xmlChar)) goto mem_error;	\
+    new_size += n;							\
     tmp = (xmlChar *)							\
-		xmlRealloc(buffer, buffer##_size * sizeof(xmlChar));	\
+		xmlRealloc(buffer, new_size * sizeof(xmlChar));		\
     if (tmp == NULL) goto mem_error;					\
+    buffer##_size = new_size;						\
     buffer = tmp;							\
 }
 


### sc...@gmail.com (2012-05-31)

Rationale:

1) growBuffer is called in many places so rather than worry about whether each call site is vulnerable and/or uses the correct types or not, this generic approach should be a safe catch-all.

2) Since "int" is used a lot for lengths etc., the maximum permitted buffer growth will be 2GB (INT_MAX). We could handle more on 64-bit certainly, but for now it seems like any 2GB buffer is pathological and can be supported at a later date via conversion of "int" types to "size_t" in the callers.

3) Internally to growBuffer, a wide and unsigned type is used so that integer overflow can be checked reliably.

4) Also note that previously, buffer##_size was modified prior to the realloc succeeding. We've hit that pattern in libxml in the past and it has caused real vulnerabilities. This is fixed. The new size is only stored after the realloc succeeds.

### sc...@gmail.com (2012-05-31)

Daniel, what do you think of the patch?

### ve...@gmail.com (2012-05-31)

Okay looked at it. The growBuffer macro is used only in 
xmlParseAttValueComplex and xmlStringLenDecodeEntities
and it seems to me that we could just change the declaration of

buffer_size, nbchars in xmlStringLenDecodeEntities
and
buffer_size, nbchars in xmlStringLenDecodeEntities
to size_t

and that seem to work based purely on code analysis (I didn't try to change
this yet and run the test), buffer_size is only used for growing and comparison
to nbchars (both initialized to 0) so that change should be safe, and nbchars
is then used as 3rd argument of COPY_BUF() (an array index, so fine) and second
argument of xmlParserEntityCheck which is an unsigned long too so should be safe too.

There is also in entities.c a simpler macro using buffer_size as int, and
I will certainly clean the two up together.
I will provide an upstream-ready patch later today, once I code this, change
a few comparisons using - to + on the opposite side and use the provided test
case.
Do you have a CVE and an ETA for going public ?

Daniel

### ve...@gmail.com (2012-05-31)

Ah, also your point #4 is taken, that still need to be change in the macro
no matter what :-) 

### sc...@gmail.com (2012-05-31)

Happy to review and test any alternate patch. I think the return value from strlen() should also be stored in a size_t, not an int.
We should also still address the potential integer overflows in growBuffer() -- size_t is still only 32-bits on 32-bit platforms so any of the "multiple by 2", "add n" and "multiply by sizeof(xmlChar)" might overflow in various circumstances (including future ones).

### sc...@gmail.com (2012-05-31)

I should go into more detail about why this is bad:

int len = strlen(buf);

In 64-bit, a string in the range 2GB - 4GB will leave "len" negative. If the code then does this:

other_buf[len] = '\0';

len will be sign-extended, leading to a wild write before the beginning of other_buf.


Issues like these are why I'm scared to simply upgrade the types to "size_t". I'm not sure the code is 64-bit clean enough to handle 2GB+ strings without truncation and signedness issues. It's one of the reasons to perhaps consider the conservative changes to growBuffer() which never permit the buffer to get larger than 2GB, even on 64-bit.


### sc...@gmail.com (2012-05-31)

@veillard: CVE assigned as requested.

CVE-2012-2807

### ve...@gmail.com (2012-05-31)

Okay, I could not reproduce the issue here, trying parsing 
/usr/bin/xmllint --noout --noent bad.xml

I get some error messages and
bad.xml:12: parser error : Memory allocation failed
  <body attrib="&e;"></body>
                   ^
though I see many "failed to load external entity "b" and 
failed to load external entity "c" messages maybe those are needed
aside bad.xml  I tried under valgrind but failed to reach the problem
by lack of memeory and time. So no crash for me at the xmllint level
 (Fedora 16 x86_64, libxml2-2.8.0).

Attached is what I would be tempted to push upstream, your above patch
is correct but I would rather fix things more generally in the parser.
Also include a small hunk for entities.c which is unrelated to the bug itself.

Daniel

### ve...@gmail.com (2012-05-31)

W.r.t. problem of not being ready for strings of more than 2G sure,
there is possibly
many issues like this in the code (shows its age), so I definitely
understand your point.
xmlStrlen is certainly a bit scary from this perspective ...

Daniel

### in...@chromium.org (2012-06-01)

Looks like we have another m19.

### sc...@gmail.com (2012-06-01)

Some notes on the patch:

1) The strlen() I was worried about still needs its return type changed int -> size_t

2) This paradigm:
-        if (out - buffer > buffer_size - 100) {
+        if ((out - buffer) + 100 > buffer_size) {

I think I prefer the old one to be honest. buffer_size is statically set to a larger value just about so it's easier to reason about "buffer_size - 100" being safe with respect to integer overflows.

3) growBuffer:
+    size_t buffer##new_size = buffer##_size * 2 + n;                    \

I still think we should guard against integer overflow here. Both on the *2 and +n. On 32-bit it's not inconceiveably that we could have trouble here.

4) growBuffer:
+               xmlRealloc(buffer, buffer##new_size * sizeof(xmlChar)); \

sizeof(xmlChar) seems to be 1 for me, but there's definite overflow opportunity on other platforms?


5) Possible additional overflow?
-               if (nbchars > buffer_size - i - XML_PARSER_BUFFER_SIZE) {
+               if (nbchars + i + XML_PARSER_BUFFER_SIZE > buffer_size) {

Looks like we should guard against an unexpectedly large "i" here, just to be safe.


Permit me to propose an alternate patch that is sort of a hybrid / subset of the two proposals and that targets the vulnerability specifically. Working on it.

### as...@ut.ee (2012-06-01)

There seem to be more issues like this, as Daniel noted.

Chris, should I just list here what I think is a vulnerability or try to create a PoC and a separate issue for each one?

### sc...@gmail.com (2012-06-02)

I don't think we should create new issues for each similar bug (don't worry, we'll scale up the reward if it makes sense).

More PoCs sounds awesome though, it'll give us definite things to address.

It's difficult to work out which bugs might be realistically reachable via a bad XML file. Did you have any particularly promising leads?

### as...@ut.ee (2012-06-02)

Here are some of the things that look interesting to me.

In libxml/src/tree.c function xmlBufferGrow:
	if (len + buf->use < buf->size) return(0);

The operations are 32-bit unsigned, so a possible overflow in addition?
In this case, the buffer is not grown, while it should.


In tree.c function xmlBufferGrow:
	int size;
	...
	if (buf->size > len)
		size = buf->size * 2;
	else
		size = buf->use + len + 100;
	...
	if ((buf->alloc == XML_BUFFER_ALLOC_IO) && (buf->contentIO != NULL)) {
		...
		newbuf = (xmlChar *) xmlRealloc(buf->contentIO, start_buf + size);
		...
	} else {
		newbuf = (xmlChar *) xmlRealloc(buf->content, size);
		...
	}

Possible overflow in the calculation of size, leading to faulty realloc?


In libxml/src/tree.c function xmlBufferResize:
	unsigned int newSize;
	...
	newSize = (buf->size ? buf->size*2 : size + 10);
	...
	rebuf = (xmlChar *) xmlRealloc(buf->contentIO, start_buf + newSize);

Looks similar to the original issue: realloc(buf->size * 2 + start_buf).


In libxml/src/tree.c function xmlBufferAdd:
	unsigned int needSize;
	...
	if (len < 0)
		len = xmlStrlen(str);
	
	if (len < 0) return -1;
	...
	needSize = buf->use + len + 2;
	if (needSize > buf->size){
		if (!xmlBufferResize(buf, needSize)){

A possible overflow in the calculation of needSize leading to buf not being resized?


In libxslt/libxslt/transform.c function xsltAddTextString:
	if (ctxt->lasttuse + len >= ctxt->lasttsize) {
		...
		int size;

		size = ctxt->lasttsize + len + 100;
		size *= 2;
		newbuf = (xmlChar *) xmlRealloc(target->content,size);
A possible overflow in lastuse + len or in the calculation of size leading to no
realloc or a faulty realloc?


I will try to create some PoC-s. I need to find a 64-bit computer with enough
RAM though. I had to borrow my friend's computer to test the original report,
but I can't do that anymore.


### as...@ut.ee (2012-06-03)

Here is a PoC for xsltAddTextString function. Vulnerable code is:

	if (ctxt->lasttuse + len >= ctxt->lasttsize) {
		...
		int size;

		size = ctxt->lasttsize + len + 100;
		size *= 2;
		newbuf = (xmlChar *) xmlRealloc(target->content,size);
		...
		target->content = newbuf;
		...
		memcpy(&(target->content[ctxt->lasttuse]), string, len);

The PoC builds a buffer of lasttsize=0x7ffeff9c and adds another len=0x10001 bytes.
Then 0x7ffeff9c+0x10001+0x64=0x80000001 and 0x80000001*2=2, so buffer is resized to 2 bytes. Then a wild write is performed to newbuf + 2GB.

Here is the link for the PoC: http://www.ut.ee/~asd/xslt/poc1/bad.xml

It uses XSLT for-each loop to create 2GB of data.

Crash dump:

tcmalloc: large alloc 2147418112 bytes == 0x7ffeea30e000 @  0x555556689b96 0x555556689ca8 0x55555668adf9 0x555556689999 0x55555668a51a 0x55555668a5ed 0x55555abb65ff 0x55555a7382b2 0x55555a738ad4 0x55555a73b5a9 0x55555a7410b7 0x55555a73b27c 0x55555a74170b 0x55555a73b27c 0x55555a73c249 0x55555a73aae6 0x55555a742622 0x55555a742d5e 0x555558e0054c 0x55555839c838 0x555558397edf 0x555558398a17 0x555558397951 0x555558397800 0x555558431f01 0x555558dfce95 0x55555843241b 0x5555584322de 0x555558cf5112 0x555558cf5059 0x555558ccda0f

Program received signal SIGSEGV, Segmentation fault.
0x00007ffff214e7d7 in ?? () from /lib/x86_64-linux-gnu/libc.so.6
(gdb) bt
#0  0x00007ffff214e7d7 in ?? () from /lib/x86_64-linux-gnu/libc.so.6
#1  0x000055555a73833f in xsltAddTextString (ctxt=0x7ffff7e7f600, 
    target=0x7ffff7ec5380, string=0x7fffead4df8b 'b' <repeats 200 times>..., 
    len=65537) at third_party/libxslt/libxslt/transform.c:686
#2  0x000055555a738ad4 in xsltCopyText (ctxt=0x7ffff7e7f600, 
    target=0x7fffea995280, cur=0x7ffff7ec5700, interned=1)
    at third_party/libxslt/libxslt/transform.c:898
#3  0x000055555a73b5a9 in xsltApplySequenceConstructor (ctxt=0x7ffff7e7f600, 
    contextNode=0x7fffea994b00, list=0x7ffff7ec5700, templ=0x0)
    at third_party/libxslt/libxslt/transform.c:2658
#4  0x000055555a7410b7 in xsltIf (ctxt=0x7ffff7e7f600, 
    contextNode=0x7fffea994b00, inst=0x7fffea995f80, castedComp=0x7fffeb4e6c80)
    at third_party/libxslt/libxslt/transform.c:5354
#5  0x000055555a73b27c in xsltApplySequenceConstructor (ctxt=0x7ffff7e7f600, 
    contextNode=0x7fffea994b00, list=0x7fffea995d80, templ=0x0)
    at third_party/libxslt/libxslt/transform.c:2595
#6  0x000055555a74170b in xsltForEach (ctxt=0x7ffff7e7f600, 
    contextNode=0x7fffeb49e840, inst=0x7fffea995c00, castedComp=0x7fffeb4e6a00)
    at third_party/libxslt/libxslt/transform.c:5628
#7  0x000055555a73b27c in xsltApplySequenceConstructor (ctxt=0x7ffff7e7f600, 
    contextNode=0x7fffeb49e840, list=0x7fffea995b00, templ=0x7fffea995200)
    at third_party/libxslt/libxslt/transform.c:2595
#8  0x000055555a73c249 in xsltApplyXSLTTemplate (ctxt=0x7ffff7e7f600, 
---Type <return> to continue, or q <return> to quit---q
Quit
(gdb) x/10i $rip
=> 0x7ffff214e7d7:      movaps %xmm1,-0x10(%rdi)
   0x7ffff214e7db:      movaps %xmm5,%xmm1
   0x7ffff214e7de:      movaps %xmm2,-0x20(%rdi)
   0x7ffff214e7e2:      lea    -0x40(%rdi),%rdi
   0x7ffff214e7e6:      movaps %xmm3,0x10(%rdi)
   0x7ffff214e7ea:      jb     0x7ffff214e7f4
   0x7ffff214e7ec:      movaps %xmm4,(%rdi)
   0x7ffff214e7ef:      jmpq   *%r9
   0x7ffff214e7f2:      ud2    
   0x7ffff214e7f4:      movaps %xmm4,(%rdi)
(gdb) info reg
rax            0x80006b4ced63   140739288558947
rbx            0x7ffff7e8c000   140737352613888
rcx            0x4000   16384
rdx            0xff7d   65405
rsi            0x7fffead5df48   140737133272904
rdi            0x80006b4ded60   140739288624480
rbp            0x7fffffffad30   0x7fffffffad30
rsp            0x7fffffffacf8   0x7fffffffacf8
r8             0x80006b4ded54   140739288624468
r9             0x7ffff214e7a0   140737254844320
r10            0x0      0
r11            0x7ffff2190110   140737255112976
r12            0x1      1
r13            0x7ffff7e7c478   140737352549496
r14            0x0      0
r15            0x0      0
rip            0x7ffff214e7d7   0x7ffff214e7d7
eflags         0x10206  [ PF IF RF ]
cs             0x33     51
ss             0x2b     43
ds             0x0      0
es             0x0      0
fs             0x0      0


### as...@ut.ee (2012-06-03)

I'm thinking maybe malloc() size in libxml should be limited until it is more safe for 64-bit platforms?

### sc...@gmail.com (2012-06-04)

Another test case! You are awesome.
With these very-long-string integer overflows, it's very hard to know which ones are purely theoretical and which ones are actually reachable by a web page. Nothing beats a repro :)

I agree we probably want a generic approach to block all of these potential problems. At least for Chromium. Let me think on it a bit more.

### ve...@gmail.com (2012-06-06)

Okay, that one is really tied to libxslt, completely different part of
the code but
fairly similar in spirit.

I don't know how to best handle the issue. When both libraries were developped
the idea of a 2GB XML file was somehow insane. I guess that will need some
refactoring left and right. The immediate way to fix this is probably as Chris
is suggesting to spot the areas where we have a signed int 2G limit and error
out when we reach it (as long as we don't prevent parsing of XML
instances > 4G).
Then as a second step removing those limitations after making sure we don't
break API/ABI except maybe for some structure that ought to be allocated by the
libraries themselves.
So I'm leaning down on Chris original patch at the moment even for
upstream (unless
you think it's not the proper way to handle the whole issue), but I'
starting to be
concerned by the amount of changes needed and the associated testing, which is
why a 2 step approach sounds the best way for me now.

  chris what do you think ?

Daniel

### as...@ut.ee (2012-06-09)

Here is a PoC for xmlBufferAdd function. Vulnerable code is:

	unsigned int needSize;
	...
	if (len < 0)
		len = xmlStrlen(str);
	
	if (len < 0) return -1;
	...
	needSize = buf->use + len + 2;
	if (needSize > buf->size){
		if (!xmlBufferResize(buf, needSize)){
	...
	memmove(&buf->content[buf->use], str, len*sizeof(xmlChar));

The PoC builds 3GB of data and adds another 1GB. The calculation of needSize will
overflow: needSize = 0xc0000000 + 0x40000000 + 2 = 2. This results in the buffer
not being resized, while it should. Then a wild write of 1GB of data is performed.

Here is the link for the PoC: http://www.ut.ee/~asd/xslt/poc2/bad.xml

It has 4 text nodes that contain a total of 4GB (16 invocations of a 256MB entity).
Then an XSLT string() function called on those nodes to concatenate them. The PoC
is quite inefficient though. It took me 4GB RAM and 12GB swap and ran for an hour.

It resulted in a memory corruption detected by TCMalloc:

third_party/tcmalloc/chromium/src/tcmalloc.cc:1760] Memory corrupted 

Program received signal SIGSEGV, Segmentation fault.
0x000055555667f970 in tcmalloc::Abort ()
    at third_party/tcmalloc/chromium/src/base/abort.h:28
28        *reinterpret_cast<volatile int*>(NULL) = 0x2001;
(gdb) bt
#0  0x000055555667f970 in tcmalloc::Abort ()
    at third_party/tcmalloc/chromium/src/base/abort.h:28
#1  0x000055555669fb3e in tcmalloc::Log (mode=tcmalloc::kCrash, 
    filename=0x55555abb97e8 "third_party/tcmalloc/chromium/src/tcmalloc.cc", 
    line=1760, a=..., b=..., c=..., d=...)
    at third_party/tcmalloc/chromium/src/internal_logging.cc:120
#2  0x000055555668b1b6 in DieFromMemoryCorruption ()
    at third_party/tcmalloc/chromium/src/tcmalloc.cc:1760
#3  0x000055555668b453 in ValidateAllocatedRegion (ptr=0x7ff14e857000, cl=0)
    at third_party/tcmalloc/chromium/src/tcmalloc.cc:1853
#4  0x0000555556689ff4 in (anonymous namespace)::do_free_with_callback (
    ptr=0x7ff14e857000, 
    invalid_free_fn=0x55555668818c <(anonymous namespace)::InvalidFree(void*)>)
    at third_party/tcmalloc/chromium/src/tcmalloc.cc:1168
#5  0x000055555668a360 in (anonymous namespace)::do_free (ptr=0x7ff14e857000)
    at third_party/tcmalloc/chromium/src/tcmalloc.cc:1196
#6  0x000055555abb69f6 in tc_free (ptr=0x7ff14e857000)
    at third_party/tcmalloc/chromium/src/tcmalloc.cc:1558
#7  0x00005555585aca07 in xmlXPathReleaseObject (ctxt=0x7fffeb51ea80, 
    obj=0x7fffeb4ca1e0) at third_party/libxml/src/xpath.c:5446
#8  0x00005555585c09b7 in xmlXPathCompOpEvalToBoolean (ctxt=0x7ffff7ebb300, 
    op=0x7fffeb4df140, isPredicate=0) at third_party/libxml/src/xpath.c:14069
#9  0x00005555585c10ff in xmlXPathRunEval (ctxt=0x7ffff7ebb300, toBool=1)
---Type <return> to continue, or q <return> to quit---
    at third_party/libxml/src/xpath.c:14373
#10 0x00005555585c1a72 in xmlXPathCompiledEvalInternal (comp=0x7fffe5d79e80, 


### as...@ut.ee (2012-06-09)

With slight modifications to poc2, overflow occurs in xmlstring.c:xmlStrncat.
Vulnerable code is:

	size = xmlStrlen(cur);
	ret = (xmlChar *) xmlRealloc(cur, (size + len + 1) * sizeof(xmlChar));
	if (ret == NULL) {
		xmlErrMemory(NULL, NULL);
		return(cur);
	}
	memcpy(&ret[size], add, len * sizeof(xmlChar));

The PoC concats 1GB string to a 3GB string. Overflow occurs in the calculation
of the new size for xmlRealloc: 0xc0000000 + 0x40000000 + 1 = 1. One byte
buffer is allocated for the result and a wild write of 1GB is performed to
ret - 1GB.

Here is the link for the PoC: http://www.ut.ee/~asd/xslt/poc3/bad.xml

Again, it has nodes that contain a total of 4GB (16 invocations of 256MB entity).
At first 3GB and 1GB strings are created with the XPath string() function. Then
they are concatenated with the XPath concat() function.

Crash dump:

Program received signal SIGSEGV, Segmentation fault.
0x00007ffff21501bf in ?? () from /lib/x86_64-linux-gnu/libc.so.6
(gdb) x/10i $rip
=> 0x7ffff21501bf:      movntdq %xmm6,-0x70(%rdi)
   0x7ffff21501c4:      movntdq %xmm7,-0x80(%rdi)
   0x7ffff21501c9:      lea    -0x80(%rdi),%rdi
   0x7ffff21501cd:      jae    0x7ffff215016e
   0x7ffff21501cf:      cmp    $0xffffffffffffffc0,%rdx
   0x7ffff21501d3:      lea    0x80(%rdx),%rdx
   0x7ffff21501da:      jl     0x7ffff2150210
   0x7ffff21501dc:      movdqu -0x10(%rsi),%xmm0
   0x7ffff21501e1:      movdqu -0x20(%rsi),%xmm1
   0x7ffff21501e6:      movdqu -0x30(%rsi),%xmm2
(gdb) info reg
rax            0x7fffa7ccae70   140736008597104
rbx            0x7ffff7e90000   140737352630272
rcx            0x180000 1572864
rdx            0x3f9de0f0       1067311344
rsi            0x7feac0aba170   140646231548272
rdi            0x7fffe76a9060   140737075908704
rbp            0x7fffffffb150   0x7fffffffb150
rsp            0x7fffffffb118   0x7fffffffb118
r8             0x7fffe7ccae60   140737082338912
r9             0x7feac10dc000   140646237978624
r10            0x0      0
r11            0x7ffff218ff90   140737255112592
r12            0x1      1
r13            0x7ffff7e7ad78   140737352543608
r14            0x0      0
r15            0x0      0
rip            0x7ffff21501bf   0x7ffff21501bf
eflags         0x10206  [ PF IF RF ]
cs             0x33     51
ss             0x2b     43
ds             0x0      0
es             0x0      0
fs             0x0      0
---Type <return> to continue, or q <return> to quit---q
Quit
(gdb) bt
#0  0x00007ffff21501bf in ?? () from /lib/x86_64-linux-gnu/libc.so.6
#1  0x000055555859a901 in xmlStrncat (cur=0x7fe8ac62d000 "", 
    add=0x7fea810dc000 'a' <repeats 200 times>..., len=1073741824)
    at third_party/libxml/src/xmlstring.c:466
#2  0x000055555859aa97 in xmlStrcat (cur=0x7fe8ac62d000 "", 
    add=0x7fea810dc000 'a' <repeats 200 times>...)
    at third_party/libxml/src/xmlstring.c:527
#3  0x00005555585b2f58 in xmlXPathConcatFunction (ctxt=0x7ffff7ecf0c0, nargs=1)
    at third_party/libxml/src/xpath.c:8887
#4  0x00005555585bef1d in xmlXPathCompOpEval (ctxt=0x7ffff7ecf0c0, 
    op=0x7ffff7e74a00) at third_party/libxml/src/xpath.c:13425
#5  0x00005555585c091e in xmlXPathCompOpEvalToBoolean (ctxt=0x7ffff7ecf0c0, 
    op=0x7ffff7e74a00, isPredicate=0) at third_party/libxml/src/xpath.c:14041
#6  0x00005555585c10ff in xmlXPathRunEval (ctxt=0x7ffff7ecf0c0, toBool=1)
    at third_party/libxml/src/xpath.c:14373
#7  0x00005555585c1a72 in xmlXPathCompiledEvalInternal (comp=0x7fffe1876c40, 
    ctxt=0x7fffeb51cc00, resObj=0x0, toBool=1)
    at third_party/libxml/src/xpath.c:14736
#8  0x00005555585c1c12 in xmlXPathCompiledEvalToBoolean (comp=0x7fffe1876c40, 
    ctxt=0x7fffeb51cc00) at third_party/libxml/src/xpath.c:14818
#9  0x000055555a7414a7 in xsltIf (ctxt=0x7ffff7e77800, 
    contextNode=0x7fffeb470d80, inst=0x7fffeb478180, castedComp=0x7fffeb4bfc80)
    at third_party/libxslt/libxslt/transform.c:5334


### sc...@gmail.com (2012-06-16)

@asd@ut.ee: I'm still thinking about this one. Would anything get past if xmlMalloc() was limited to 1GB in Chromium?

I think it would depend on whether concatenations are done one at a time or if multiple chunks can be concatenated at once? In the former case, we'd catch them all, I believe. In the latter case, we'd get in to trouble with 4 chunks: 1GB + 1GB + 1GB + 1GB -> overflow.


### as...@ut.ee (2012-06-17)

@chris: Indeed the 1GB limit wouldn't solve all our problems. I can't think of any places where multiple chunks are concatenated at once, but take a look at xsltAddTextString:

	size = ctxt->lasttsize + len + 100;
	size *= 2;
	newbuf = (xmlChar *) xmlRealloc(target->content,size);

If lasttsize == 1GB and len == 1GB then size = (1GB + 1GB + 100) * 2, which overflows. I think I have seen some more places where it might be possible to blow 1GB up to 4GB.

Also, with signed int-s it is sufficient to add just 1GB + 1GB to flip a sign, which might be dangerous.

A 1GB limit should block most of the overflows though.


### sc...@gmail.com (2012-06-18)

@asd@ut.ee: thanks, I will land a 512MB limit in Chromium as a defensive measure. Please let us know if you find a way to concatenate multiple chunks together in a single place (i.e. any repro that bypasses this defense. If you find one, please file a new bug).

### sc...@gmail.com (2012-06-18)

@veillard: for upstream, maybe it makes sense to start a massive code-level conversion to change any length / size variables to be a size_t ? That would have stopped most of these issues on 64-bit.

### bu...@chromium.org (2012-06-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=142822

------------------------------------------------------------------------
r142822 | cevans@chromium.org | Mon Jun 18 14:35:51 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/src/globals.c?r1=142822&r2=142821&pathrev=142822
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/README.chromium?r1=142822&r2=142821&pathrev=142822

Attempt to address libxml crash.

BUG=129930
Review URL: https://chromiumcodereview.appspot.com/10458051
------------------------------------------------------------------------

### sc...@gmail.com (2012-06-18)

[Empty comment from Monorail migration]

### ve...@gmail.com (2012-06-19)

C.f. https://crbug.com/chromium/129930#c29 . Yes but that's a rather massive work I'm afraid due to the
fact I can't break binary compatibility. So my take is that I may need to
develop a new class of buffers which are properly 64 bits clean, and probably
an API at the parser and XSLT level to define arbitrary limits for maximum
string size manipulated but the parser or transformation process. In any case
not trivial, I am starting to make room for such coming work. In the meantime
patching your copy of the library to impose a size limit sounds fine but let's
keep track of where you're adding this so I can provide the equivalent in a clean
way once I get on the upstream work.

  thanks !

Daniel

### sc...@gmail.com (2012-06-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-06-19)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=143067

------------------------------------------------------------------------
r143067 | cevans@chromium.org | Tue Jun 19 15:35:31 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1132/src/third_party/libxml/README.chromium?r1=143067&r2=143066&pathrev=143067
 M http://src.chromium.org/viewvc/chrome/branches/1132/src/third_party/libxml/src/globals.c?r1=143067&r2=143066&pathrev=143067

Merge 142822 - Attempt to address libxml crash.

BUG=129930
Review URL: https://chromiumcodereview.appspot.com/10458051

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10572025
------------------------------------------------------------------------

### sc...@gmail.com (2012-06-22)

@Juri: thanks for working backwards from the code to real test cases, that was awesome.

And three separate bugs so a $3000 reward.

### as...@ut.ee (2012-06-22)

Thank you :)

### sc...@gmail.com (2012-07-09)

Payment for this one is in the system.

### js...@chromium.org (2012-07-13)

CC'ing Debian libxml maintainer.

### ve...@gmail.com (2012-07-18)

I just pushed the following upstream which is a way to fix the problem very close to
my first patch here, but trying to incorporate the feedback:

http://git.gnome.org/browse/libxml2/commit/?id=459eeb9dc752d5185f57ff6b135027f11981a626

as well as 

http://git.gnome.org/browse/libxml2/commit/?id=4f9fdc709c4861c390cd84e2ed1fd878b3442e28

As pointed out something more dramatic is needed, i'm working on it, i have
already some relatively intrusive changes on around 20 patches and still more
to come.

Daniel

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

This issue was migrated from crbug.com/chromium/129930?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058841)*
