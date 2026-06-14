# css parsing issue in calc

| Field | Value |
|-------|-------|
| **Issue ID** | [40089480](https://issues.chromium.org/issues/40089480) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mi...@chromium.org |
| **Created** | 2011-03-31 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

invalid read with css containing bad character

**VERSION**  

Chrome Version:  

Chromium 12.0.720.0 (Developer Build 79946) Ubuntu 10.10  

WebKit 534.27 (trunk@82507)

Operating System:  

Linux 2.6.35-28-generic #49-Ubuntu SMP Tue Mar 1 14:39:03 UTC 2011 x86\_64 GNU/Linux

**REPRODUCTION CASE**

<div style="A:-webkit-calc(((1)^[))"></div>

or

<div style="width: -webkit-calc((((1px)^[))"></div>

that's a control-left-square-bracket in there (0x1b)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

(gdb) x/i $rip  

=> 0x7ffff62ad54c [WebCore::CSSParserValueList::~CSSParserValueList()+60](javascript:void(0);): cmpl $0x100001,0x18(%rax)  

p/x $rax  

$8 = 0x610063002d0074

(gdb) x/i $rip  

=> 0x7ffff62ad07a <WebCore::CSSParserValueList::insertValueAt(unsigned int, WebCore::CSSParserValue const&)+90>: mov (%rdi),%r8  

(gdb) p/x $rdi  

$11 = 0x60b046207a50d57  

(gdb)

--

## Attachments

- [css3.html](attachments/css3.html) (text/plain; charset=us-ascii, 51 B)
- [css.html](attachments/css.html) (text/plain; charset=us-ascii, 43 B)
- [css2.html](attachments/css2.html) (text/plain; charset=us-ascii, 50 B)
- [valgrind_78071.txt](attachments/valgrind_78071.txt) (text/plain; charset=us-ascii, 17.0 KB)

## Timeline

### mi...@gmail.com (2011-03-31)

vg log

### in...@chromium.org (2011-03-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-31)

webkit bug
https://bugs.webkit.org/show_bug.cgi?id=57581

### in...@chromium.org (2011-03-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-31)

[Empty comment from Monorail migration]

### ts...@chromium.org (2011-03-31)

Looks to be a missing "else branch" in CSSGrammar.y:1525 to set $$ = 0 when the input is already 0.  Otherwise, it looks like $$ will be left unassigned.  In other words, try updating the rule for calc_func_paren_expr to:

calc_func_paren_expr:
    '(' maybe_space calc_func_expr maybe_space ')' maybe_space {
        if ($3) {
            $$ = $3;
            CSSParserValue v;
            v.id = 0;
            v.unit = CSSParserValue::Operator;
            v.iValue = '(';
            $$->insertValueAt(0, v);
            v.iValue = ')';
            $$->addValue(v);
        }
        else
          $$ = 0;
    }


### ts...@chromium.org (2011-03-31)

(possibly same issue with selector_list: rule at line 824).

### in...@chromium.org (2011-03-31)

Patch reverted in http://trac.webkit.org/changeset/82636. I discussed with Mike, he will make sure to land these three regression tests alongwith the next fix in -webkit-calc.


### mi...@chromium.org (2011-03-31)

Thanks for the analysis Tom - that looks like the culprit. I'll make sure to test your fix in the next patch.

### ma...@google.com (2011-04-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-01)

Nice trunk regression catch, @miaubiz :)

### sc...@gmail.com (2011-04-19)

@miaubiz, yes, nice regression catch indeed. It did not take you long at all to flatten this new feature shortly after landing :) Looking at the bug notes, we didn't dupe this ourselves for once, so this is a definite $1000 Chromium Security Reward -- congrats!

### sc...@gmail.com (2011-05-04)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

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

This issue was migrated from crbug.com/chromium/78071?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089480)*
