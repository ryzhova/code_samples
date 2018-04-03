#!/usr/bin/env python
import unittest

class Node:

    def __init__(self, value=None, next=None, rand=None):
        self.value = value
        self.next = next
        self.rand = rand


class LinkedList:

    def __init__(self):
        self.clear()

    def __repr__(self):
        if self.first:
            current = self.first
            out = 'LinkedList [' + str(current.value) + ', '
            while current.next:
                current = current.next
                out += str(current.value) + ', '
            return out + ']'
        return 'LinkedList []'

    def clear(self):
        self.first = None
        self.last = None
        self.length = 0

    def add(self, x, rand=None):
        self.length += 1
        if not self.first:
            self.last = self.first = Node(x, rand=rand)
        else:
            self.last.next = self.last = Node(x, rand=rand)

    def copy_list(self):
        new_list = self.__class__()
        current = self.first

        while current:
            new_list.add(current.value, None)
            current = current.next

        current_oldlist = self.first
        current_newlist = new_list.first

        while current_oldlist:
            current_newlist.rand = current_oldlist.rand
            current_oldlist.rand = current_newlist

            current_oldlist = current_oldlist.next
            current_newlist = current_newlist.next

        current_oldlist = self.first
        current_newlist = new_list.first

        while current_oldlist:

            if current_oldlist.rand.rand is None:
                current_oldlist.rand.next = None
            else:
                current_oldlist.rand.next = current_oldlist.rand.rand.rand

            current_oldlist = current_oldlist.next

        current_oldlist = self.first
        current_newlist = new_list.first

        while current_oldlist:
            current_oldlist.rand = current_newlist.rand
            current_newlist.rand = current_newlist.next
            if current_oldlist.next is None:
                current_newlist.next = None
            else:
                current_newlist.next = current_oldlist.next.rand

            current_oldlist = current_oldlist.next
            current_newlist = current_newlist.next

        return new_list


class TestLinkedList(unittest.TestCase):

    def setUp(self):
        self.l = l = LinkedList()

        l.add(1)
        l.add(2, l.first)
        l.add(3)
        l.add(4, l.first.next)
        l.first.rand = l.first.next.next

    def test_copy_list(self):
        c = self.l.copy_list()
        i = self.l.first
        j = c.first
        while i or j:
            self.assertEqual(i.value, j.value)
            self.assertIsNot(i, j)
            if i.rand is not None or j.rand is not None:
                self.assertEqual(i.rand.value, j.rand.value)
                self.assertIsNot(i.rand, j.rand)
            i = i.next
            j = j.next


if __name__ == '__main__':
    unittest.main()
