# Merge Two Sorted Lists — https://leetcode.com/problems/merge-two-sorted-lists/
# Approach: dummy head + tail pointer. Compare the front nodes of both lists,
#   splice the smaller onto the tail, advance that list. When one list runs out,
#   attach the remainder of the other. Reuses existing nodes (only the dummy is
#   allocated).
# Time: O(n + m)   Space: O(1)
#
# from typing import Optional
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        p = list1
        q = list2
        temp = ListNode(None)
        ans = temp

        while(p != None and q != None):
            if(p.val < q.val):
                temp.next = p
                temp=temp.next
                p = p.next
            else:
                temp.next = q
                temp=temp.next
                q = q.next

        if p != None:
            temp.next = p

        if q != None:
            temp.next = q

        return ans.next
