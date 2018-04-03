#!/usr/bin/env python

import unittest

class Node:

    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next


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

    def add(self, x):
        self.length += 1
        if not self.first:
            self.last = self.first = Node(x)
        else:
            self.last.next = self.last = Node(x)

    def reverse(self):
        if self.first is None or self.first.next is None:
            return
        self.last = self.first
        new_root = None
        while self.first:
            next_node, self.first.next = self.first.next, new_root
            if next_node is None:
                break
            new_root, self.first = self.first, next_node

    def print_reversed(self):
        self.reverse()
        print(self)
        self.reverse()

    def has_loop(self):
        ''' Returns True if list has loop'''

        if self.first is None or self.first.next is None:
            return False

        slow_pointer = self.first
        fast_pointer = self.first.next
        while True:
            if fast_pointer == slow_pointer:
                return True

            try:
                fast_pointer = fast_pointer.next.next
                slow_pointer = slow_pointer.next
            except AttributeError:
                return False

    def loop_set(self):
        if self.first is None or self.first.next is None:
            return None
        node_set = set()

        pointer = self.first
        while True:
            if pointer in node_set:
                return pointer
            node_set.add(pointer)
            try:
                pointer = pointer.next
            except AttributeError:
                return None

    def  loop_start(self):
        if not self.has_loop():
            return
        current = self.first
        while True:
            if not current.next:
                return current
            temp = current
            current = current.next
            temp.next = None

    def copy_list(self):
        new_list = self.__class__()
        current = self.first

        while current:
            new_list.add(current.value)
            current = current.next

        return new_list


class TestLinkedList(unittest.TestCase):

    def setUp(self):
        self.l = l = LinkedList()

	for i in range(6):
	    l.add(i)

    def test_has_loop(self):
        self.assertFalse(self.l.has_loop())
        self.l.first.next.next.next.next.next = self.l.first.next.next
        self.assertTrue(self.l.has_loop())

    def test_loop_start(self):
        self.assertIsNone(self.l.loop_start())
        loop_start = self.l.first.next.next
        self.l.first.next.next.next.next.next.next = loop_start
        self.assertIs(self.l.loop_start().value, loop_start.value)


if __name__ == '__main__':
    unittest.main()
