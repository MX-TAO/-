import json
import sys
import os
import difflib
import time

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

	#print(1, list1)
	#print(2, list2)

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

	#print(3, list1)
	#print(4, list2)

	clist1 = [i for i in list1 if i[0]!='equal']
	clist2 = []
	for i in range(len(list2)):
		if list2[i][0] == 'equal':
			continue
		if list2[i][0] == 'delete':
			clist2.append(list2[i])
			continue
		idx = binary_search(list1, list2[i][1], list2[i][2])
		if idx >= 0:
			if list1[idx][0] == 'equal':
				clist2.append(list2[i])
				continue
			if list2[i][1] == list2[i][2]:
				clist2.append((list2[i][0], list1[idx][2], list1[idx][2], list2[i][3], list2[i][4]))
				continue
			clist2.append(list2[i])
	#print(5, clist1)
	#print(6, clist2)

	del_list = [(i[1], i[2]) for i in clist1 if i[0]=='delete' or i[0]=='replace'] + \
		[(i[1], i[2]) for i in clist2 if i[0]=='delete' or i[0]=='replace']

	ins_list = [(i[2], i[3], i[4], 1) for i in clist1 if i[0]=='insert'] + \
		[(i[2], i[3], i[4], 1) for i in clist1 if i[0]=='replace'] + \
		[(i[2], i[3], i[4], 2) for i in clist2 if i[0]=='insert'] + \
		[(i[2], i[3], i[4], 2) for i in clist2 if i[0]=='replace']

	#print(del_list)
	#print(ins_list)
	str2_tmp = str2
	for i in del_list:
		str2_tmp = str2_tmp[:i[0]] + '\b'*(i[1]-i[0]) + str2_tmp[i[1]:]
		#print(str2_tmp)

	ins_list = sorted(ins_list, key=lambda x:x[0], reverse=False)

	#print(ins_list)

	idx = [0] + [i[0] for i in ins_list] + [len(str2)]
	str_list = [str2_tmp[idx[i]:idx[i+1]] for i in range(len(idx)-1)]
	#print(str_list)

	str_tmp = ''
	for i in range(len(ins_list)):
		if ins_list[i][3] == 1:
			str_tmp = str_tmp + str_list[i] + str1[ins_list[i][1]:ins_list[i][2]]
		else:
			str_tmp = str_tmp + str_list[i] + str3[ins_list[i][1]:ins_list[i][2]]
		#print([str_tmp])

	return str_tmp.replace('\b', '')

def synch_for_client(str1='', str2='', str3='', c_idx=0):
	str3 = str3[:c_idx] + '\a' + str3[c_idx:]

	str_tmp = synch(str1, str2, str3)

	c_idx_new = str_tmp.find('\a')

	str_tmp = str_tmp.replace('\a', '')

	if c_idx_new < 0:
		c_idx_new = c_idx

	return max(0, min(len(str_tmp), c_idx_new)), str_tmp

if __name__ == '__main__':
	
	# For test
	a = 'abcdfe'
	b = 'abcdehhhhhhhhhhhhhhhh'
	c = 'abcdeg'
	#print(compare_str(a, c))
	print(synch(a,b,c))

	#第一个参数：服务器的副本
	#第二个参数：客户端传来的旧版
	#第三个参数：客户端传来的新版

	print('\n============\nTo test synch_for_client:\n')
	a = 'abcde'
	b = 'abcf'
	c = 'acf'

	new_str, cur_pos = synch_for_client(a,b,c,1)

	print('new string: ', new_str)
	print('new cur_pos:', cur_pos)

	count = 100000
	start_time = time.time()
	for i in range(count):
		new_str, cur_pos = synch_for_client(a,b,c,1)

	print(count/(time.time()-start_time))