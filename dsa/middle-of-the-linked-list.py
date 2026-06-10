# Middle of the Linked List — https://leetcode.com/problems/middle-of-the-linked-list/
# Approach: slow/fast (tortoise and hare) pointers. fast advances two nodes for
#   every one of slow; when fast runs off the end, slow sits at the middle. For
#   even length this returns the second of the two middles, as the problem asks.
# Time: O(n)   Space: O(1)
#
# from typing import Optional
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = head
        fast = head
        while(fast and fast.next):
            slow = slow.next
            fast = fast.next.next
        return slow
