import json
import sys
import os
import difflib

def compare_str(str1='', str2=''):
	return difflib.SequenceMatcher(None, str1, str2).get_opcodes()

def binary_search(dlist, s, e):
	maxn = len(dlist) - 1
	minn = 0
	if s == e:
		while minn <= maxn:
			midn = (maxn+minn) // 2
			if dlist[midn][1] > s:
				maxn = midn - 1
				continue
			elif dlist[midn][2] < s:
				minn = midn + 1
				continue
			elif dlist[midn][1] == dlist[midn][2]:
				return midn
			else:
				break
	maxn = len(dlist) - 1
	minn = 0
	while minn <= maxn:
		midn = (minn+maxn) // 2
		if dlist[midn][1] > s:
			maxn = midn - 1
			continue
		elif dlist[midn][2] < e:
			minn = midn + 1
			continue
		else:
			return midn
	return -1

def binary_search_idx(alist, idx):
	minn = 0
	maxn = len(alist) - 1
	while minn<=maxn:
		midn = (maxn+minn) // 2
		if alist[midn][1] > idx:
			maxn = midn - 1
		elif alist[midn][2] < idx:
			minn = midn + 1
		else:
			return midn
	return -1

def synch(str1='', str2='', str3=''):
	list1 = compare_str(str2, str1)
	list2 = compare_str(str2, str3)

	for i in list2:
		idx = binary_search_idx(list1, i[1])
		if idx < 0 or list1[idx][1] == i[1] or list1[idx][2] == i[1]:
			continue
		if list1[idx][0] == 'equal':
			list1.append(('equal', list1[idx][1], i[1], list1[idx][3], list1[idx][3]+i[1]-list1[idx][1]))
			list1.append(('equal', i[1], list1[idx][2], list1[idx][4]-list1[idx][2]+i[1], list1[idx][4]))
			list1.pop(idx)
		elif list1[idx][0] == 'replace':
			list1.append(('replace', list1[idx][1], i[1], list1[idx][3], list1[idx][4]))
			list1.append(('delete', i[1], list1[idx][2], list1[idx][4], list1[idx][4]))
			list1.pop(idx)
		elif list1[idx][0] == 'delete':
			list1.append(('delete', list1[idx][1], i[1], list1[idx][3], list1[idx][4]))
			list1.append(('delete', i[1], list1[idx][2], list1[idx][3], list1[idx][4]))
			list1.pop(idx)

	print(list1)
	print(list2)

	clist = []
	for i in range(len(list2)):
		if list2[i][0] == 'equal':
			continue
		idx = binary_search(list1, list2[i][1], list2[i][2])
		if idx >= 0:
			if list1[idx][0] == 'equal':
				clist.append(list2[i])
				continue
			if list2[i][1] == list2[i][2]:
				clist.append([list2[i][0], list1[idx][2], list1[idx][2], list2[i][3], list2[i][4]])


if __name__ == '__main__':
	
	# For test
	a = 'abcdfe'
	b = 'abcdeg'
	print(compare_str(a, b))