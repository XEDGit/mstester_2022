#!/usr/bin/env python3
from genericpath import exists
from locale import getpreferredencoding
from collections import Counter
import subprocess
import sys
import os

def send_cmd(prog, test):
	test = test.replace(";", "\n")
	p = subprocess.Popen(prog, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.stdin.write(test.encode(getpreferredencoding(), 'replace'))
	p.stdin.close()
	p_res = p.stdout.read()
	p.stdout.close()
	p_err = p.stderr.read()
	p.stderr.close()
	p.terminate()
	p.wait()
	return p.returncode, p_res.decode(getpreferredencoding(), 'replace').rstrip("\n"), p_err.decode(getpreferredencoding(), 'replace').rstrip("\n")

def make_output(i, test, mini_res, mini_err, mini_code, bash_res, bash_err, bash_code, diff, out, err):
	output = f"{col(f'Line {i + 1}: ', '1;31')}{test} {diff}\n"
	if out:
		output += f"{col('minishell:', '31')}\n'{mini_res}'\n"
		if err:
			output += f"{col('minishell stderr:', '31')}\n{mini_err}\n"
		output += f"{col('exit code: ', '31')}{mini_code}\n"
		output += f"{col('bash: ', '31')}\n'{bash_res}'\n"
		if err:
			output += f"{col('bash stderr:', '31')}\n{bash_err}\n"
		output += f"{col('exit code: ', '31')}{bash_code}\n"
	if out and err:
		output += f"\n{col('minishell stderr:', '31')}\n{mini_err}\n"
		output += f"{col('bash stderr:', '31')}\n{bash_err}\n"
	output += "_________________________________________________________________"
	return output

def test_cmd(exe_path, test, out, err, i):
	mini_code, mini_res, mini_err = send_cmd(exe_path, test)
	bash_code, bash_res, bash_err = send_cmd("bash", test)
	diff = col("Fail", "31")
	success = 0
	if mini_res == bash_res:
		success = 1
		diff = col("Success!", "32")
	if mini_code != bash_code:
		diff += " - " + col("Wrong exit code", "33")
	test = test.rstrip("\n")
	out = make_output(i, test, mini_res, mini_err, mini_code, bash_res, bash_err, bash_code, diff, out, err)
	print(out)
	return success

def str_to_path(string):
	if not "./" in string[:2] and not "/" in string[:1] and not ".." in string[:2] and not "~/" in string[:2]:
			string = "./" + string
	return string

def col(str, col):
	return f"\033[{col}m{str}\033[0m"

def error(msg):
	print(msg)
	exit(1)

def catch_args():
	argc = len(sys.argv)
	i = 1
	single = -1
	out = False
	err = False
	interactive = False
	file_path = "mstester_2022/tests"
	if not exists(file_path) or os.path.isdir(file_path):
		file_path = "tests"
	if not exists(file_path) or os.path.isdir(file_path):
		print("warning: the file containing tests has not been found automatically")
		file_path = "Undefined"
	exe_path = "./minishell"
	if not exists(exe_path) or os.path.isdir(exe_path):
		exe_path = "../minishell"
	if not exists(exe_path) or os.path.isdir(exe_path):
		print("warning: the minishell executable has not been found automatically")
		exe_path = "Undefined"
	help_msg = "Usage: python3 tester.py [-err -o -exe executable_path] tests_file [file_line] | -i [-o -e]\n"
	flags_msg =  "Flags:\n -i:\t\tInteractive mode\n -o:\t\tPrint stdout of both minishell and bash\n -e:\t\tPrint stderr of both minishell and bash\n -x path:\tPath to your minishell executable\n tests_file:\tPath to the text file containing the tests, one per line (default: \"./mstester_2022/tests\")\n file_line:\tTests only the specified line of the file specified by file path\n\nArguments don't have a specific order"
	while i != argc:
		arg = str(sys.argv[i])
		if arg == "-h":
			print(f"{help_msg}\n{flags_msg}")
			exit(0)
		elif arg[0] == '-':
			if 'o' in arg:
				out = True
			if 'i' in arg:
				interactive = True
			if 'e' in arg:
				err = True
			if "x" in arg:
				i += 1
				if i >= argc:
					error("Error: flag requires one positional argument -x <path to minishell executable>")
				exe_path = str_to_path(sys.argv[i])
		elif arg.isdigit():
			single = int(arg) - 1
			out = True
		else:
			file_path = str_to_path(arg)
		i += 1
	if not interactive and not exists(file_path) or os.path.isdir(file_path) or os.access(file_path, os.X_OK):
		error("Error: '" + file_path + "' isn't a valid file")
	if not exists(exe_path) or os.path.isdir(exe_path) or not os.access(exe_path, os.X_OK):
		error("Error: '" + exe_path + "' isn't a valid file")
	return out, interactive, single, file_path, exe_path, err

def main():
	passed = 0
	tot = 0
	out, interactive, single, file_path, exe_path, err = catch_args()
	pre = Counter(os.listdir('.'))
	if not interactive:
		fd = open(file_path, "r")
		tests = fd.readlines()
		fd.close()
	if not interactive and single >= len(tests):
		error("Error: specified line " + str(single + 1) + " is not present in " + file_path)
	print(col("Welcome to the tester for the new 42 minishell!\n\t\tby XEDGit\n", "36;1"))
	if interactive:
		print(col("Enter a command line to test (exit with Ctrl+C):", "31"))
		while True:
			try:
				test = input(">")
			except:
				break
			passed += test_cmd(exe_path, test, False, err, tot)
			tot += 1
	elif single != -1:
		passed = test_cmd(exe_path, tests[single], out, err, single)
		tot += 1
	else:
		for i, test in enumerate(tests):
			passed += test_cmd(exe_path, test, out, err, i)
			tot += 1
	print("\n" + col(str(passed) + "/" + str(tot) + " successful tests!", "35;1"))
	post = Counter(os.listdir('.'))
	newfiles = list(post - pre)
	if not newfiles:
		exit(0)
	print("Cleaning up generated files:")
	for f in newfiles:
		os.remove(f)
		print(f"\t'./{f}' removed")

if __name__ == "__main__":
	main()