import os
import sys
import re
import hashlib
import shutil

_DST = 'old' # 오래된 파일들이 이동할 디렉토리
_EXTENSION = '.var' # 찾을 확장자
_EXCLUDE_DIRECTORIES = [_DST, r'default'] # 검색에서 제외할 디렉토리

dst = os.path.join(os.getcwd(), _DST)

def scan(path, include_subdirectories=False, exclude_directories=[]):
	with os.scandir(path) as it:
		for entry in it:
			p = os.path.normpath(entry.path)
			if entry.is_dir():
				if include_subdirectories and not p in exclude_directories:
					yield from scan(p, include_subdirectories)
			else:
				yield p

def sha1(filename):
	sha1 = hashlib.sha1()
	with open(filename, 'rb') as f:
		while True:
			b = f.read(8192)
			if(not b):
				break
			sha1.update(b)
	return(sha1.hexdigest().upper())
	
def move(src, dst, mkdir_creator=False):
	if os.path.isdir(dst):
		if mkdir_creator:
			creator = os.path.basename(src)
			dst = os.path.join(dst, creator[:creator.find('.')])
			if not os.path.exists(dst):
				os.mkdir(dst)
			elif not os.path.isdir(dst):
				print(f'이동 실패: {os.path.join(dst, creator)} 경로가 폴더가 아닙니다')
				return False
		dst = os.path.join(dst, os.path.basename(src))
		if os.path.exists(dst):
			if os.path.isfile(dst):
				src_size = os.stat(src).st_size
				src_hash = ''
				dst_size = os.stat(dst).st_size
				dst_hash = ''
				if src_size == dst_size:
					src_hash = sha1(src)
					dst_hash = sha1(dst)
					if src_hash == dst_hash:
						os.remove(src)
						print(f'\t중복 파일 제거: {src}')
						return True
				print(f'충돌: 같은 파일명이지만 파일 내용이 다릅니다')
				print(f'\t{src}\t{src_size} bytes\t{src_hash}')
				print(f'\t{dst}\t{dst_size} bytes\t{dst_hash}')
				return False
			else:
				print(f'이동 실패: 이동할 폴더에 대상 파일명과 같은 폴더가 존재 합니다')
				print(f'\t{dst}')
				return False
		else:
			shutil.move(src, dst)
			print(f'\t이동: {src} -> {dst}')
			return True
	return False

print()

if not os.path.exists(dst):
	os.mkdir(dst)
elif not os.path.isdir(dst):
	print(f'오류: 옮길 대상 경로가 폴더가 아닙니다 {dst}')
	sys.exit(1)

all_packages = {}
latests = {}

for f in scan('.', True, _EXCLUDE_DIRECTORIES):
	file = os.path.splitext(f)
	if(file[1] == _EXTENSION):
		filename = os.path.basename(file[0])
		if re.match(r'^.+\..+\.\d+$', filename):
			package_name = filename[:filename.rfind('.')]
			if not all_packages.get(package_name):
				all_packages[package_name] = []
			all_packages[package_name].append(f)
		else:
			print(f'파일명이 형식에 맞지 않습니다: {f}')

for i, (group, packages) in enumerate(all_packages.items()):
	if len(packages) > 1:
		latests[group] = ['', '']
		latest_version = 0
		latest_size = -1
		latest_package = ''
		latest_hash = ''
		max_depth = -1
		print(f'\n패키지: {group}')
		for p in packages:
			v = int(p[p.rfind('.', 0, len(p) - len(_EXTENSION)) + 1:len(p) - len(_EXTENSION)])
			if v > latest_version:
				s = os.stat(p).st_size
				if s == latest_size:
					if not latest_hash:
						latest_hash = sha1(latest_package)
					h = sha1(p)
					if h == latest_hash:
						print('비교 충돌: 파일명이 다르지만 같은 파일입니다')
						print(f'\t{p}')
						print(f'\t{latest_package}')
						continue
					else:
						latest_hash = h
				if latest_package:
					move(latest_package, dst, True)
				d = p.count(os.sep)
				if d < max_depth:
					latests[group][0] = p
				else:
					max_depth = d
					latests[group][0] = ''
					latests[group][1] = os.path.dirname(p)
				latest_version = v
				latest_size = s
				latest_package = p
				continue
			elif v == latest_version:
				s = os.stat(p).st_size
				if s == latest_size:
					if not latest_hash:
						latest_hash = sha1(latest_package)
					h = sha1(p)
					if h == latest_hash:
						d = p.count(os.sep)
						t = p
						if d > max_depth:
							t = latest_package
							latest_package = p
							max_depth = d
						os.remove(t)
						print(f'\t중복 파일 제거: {t}')
						continue
				print('비교 충돌: 파일명은 같지만 다른 파일입니다')
				print(f'\t{p}')
				print(f'\t{latest_package}')
				continue
			else:
				s = os.stat(p).st_size
				if s == latest_size:
					if not latest_hash:
						latest_hash = sha1(latest_package)
					h = sha1(p)
					if h == latest_hash:
						print('비교 충돌: 파일명이 다르지만 같은 파일입니다')
						print(f'\t{p}')
						print(f'\t{latest_package}')
						continue
				d = p.count(os.sep)
				if d > max_depth:
					latests[group][0] = latest_package
					latests[group][1] = os.path.dirname(p)
					max_depth = d
				move(p, dst, True)
				continue

if len(latests) > 0:
	for l in latests:
		if latests[l][0]:
			move(latests[l][0], latests[l][1])
