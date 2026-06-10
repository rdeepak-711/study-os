# Reverse Linked List — https://leetcode.com/problems/reverse-linked-list/
# Approach: iterative in-place reversal with two pointers. x = previous node
#   (starts None), y = current node. Each step: save y.next, point y.next back
#   to x, then advance x and y. The old tail becomes the new head.
# Time: O(n)   Space: O(1)
#
# from typing import Optional
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head==None:
            return None
        x=None
        y=head
        while(y.next!=None):
            z=y.next
            y.next=x
            x=y
            y=z
        y.next=x
        return y
