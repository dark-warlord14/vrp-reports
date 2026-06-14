# UNKNOWN in v8::internal::FixedArray::get

| Field | Value |
|-------|-------|
| **Issue ID** | [40080854](https://issues.chromium.org/issues/40080854) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@chromium.org |
| **Assignee** | [Deleted User] |
| **Created** | 2014-11-14 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5205335303258112

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8

Crash Type: UNKNOWN
Crash Address: 0x7f41d1643b20
Crash State:
  v8::internal::FixedArray::get
  v8::internal::TypeFeedbackOracle::GetInfo
  v8::internal::TypeFeedbackOracle::CallIsMonomorphic
  

Minimized Testcase (7.52 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94NjnM6Q4C2iwpAqQKE8fUqxJwsEZ3m807CaJU1vitXXH9selXBKWLZOiD4_pJuADJen8bqjlLpaN5ZM9FqrkO9QlnfJjRNhnuTsLBfpTqZjMhr-g2-S5kLKJo1RKlfg3HzF0zQkDmKVZfYWAQ58uBONkZTsw

Filer: mbarbella

## Timeline

### mb...@chromium.org (2014-11-14)

titzer, could you please help find an owner for this?

### mb...@chromium.org (2014-11-14)

Including the repro so that you don't have to dig it out of the archive:

gW=gH=175;
g=[];

for(var n=0; n<gW; n++){
 var l=[];
 for(var p=0; p<gH; p++){
   l.push(1)
 }
 g.push(l)
}

function k(a,b){
 if(a<(/\u0065\u0062\u00b2/ )||b<0||a>=gW||b>=gH)
   return 0;
 return g[a][b];
}

function f(){
 for(var a=[],f=0; f<gW; f++){
   const f = this                              ;    
   for(var h=0; h<gH; h++){
     var e=0;
     for(var i=-1; i<=1; i++)
       for(var j=-1; j<=1; j++)
          e+=k(f+i,h+j);
     e=k((new Array    . abstract        ),h)==1?1:0;
     b.push(((function  (  )  {  }  )   . p      --    ))
   }
   a.push(b)
 }
}

f();
%OptimizeFunctionOnNextCall(f);
f();

### cl...@chromium.org (2014-11-14)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-15)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-11-17)

Michael, can you take a look?

### mv...@chromium.org (2014-11-17)

[Empty comment from Monorail migration]

### mv...@chromium.org (2014-11-17)

Smaller repro:
-----------------
gW=175;

for(var n=0; n<gW; n++){
 var l=[];
 for(var p=0; p<gW; p++){
   l.push(1)
 }
}

function f(){
 var a = [];
 for(var f=0; f<gW; f++){
   const f = 3;
   k(a,a);
 }
}

f();
------

The reason is that the type feedback vector for function f is not initialized, it is the empty array. We decide to optimize in the loop at the start of the program, and attempt to inline f(). But we are surprised to discover we can't peek in the feedback vector at this point (crash).

### mv...@chromium.org (2014-11-17)

Okay, bisected to Andy's recent change https://chromium.googlesource.com/v8/v8/+/910711a16963aebccef59a2f6bf8c7371d985596

Andy, could you take a look asap? The repro in https://crbug.com/chromium/433445#c8 is enough to bring it about.



### cl...@chromium.org (2014-11-24)

wingo@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-01)

ClusterFuzz has detected this issue as fixed in range 25501:25502.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5205335303258112

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8

Crash Type: UNKNOWN
Crash Address: 0x7f9de9343e00
Crash State:
  v8::internal::FixedArray::get
  v8::internal::TypeFeedbackOracle::GetInfo
  v8::internal::TypeFeedbackOracle::CallIsMonomorphic
  
Regressed: V8: r25344:25348
Fixed: V8: r25501:25502

Minimized Testcase (7.51 Kb): https://cluster-fuzz.appspot.com/download/AMIfv974nMpCTsjGFz7yGAOGXGLoGPG3jlcFiJ9xKrD3N2CWYhH1QBXWkNPVYaTC-Jyn5HlG4SPhTuE4gfwQsdW2tr5jUNAN5FFeUUUlx-OAmdk80qCCrOE1-x8MNiC8kDZKeJyMb5nyFZd7P4ZWnI830EHVJxJANg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-02)

wingo@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-09)

wingo@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### mv...@chromium.org (2014-12-10)

I believe this one is fixed now.

### cl...@chromium.org (2014-12-10)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

$1000 for this report, +$500 ClusterFuzz bonus.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-18)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-04-06)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/433445?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/433769, crbug.com/chromium/434375]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080854)*
