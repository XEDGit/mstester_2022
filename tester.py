from asyncio.subprocess import DEVNULL
from genericpath import exists
import readline
import subprocess
import sys
import os

def send_cmd(prog, test):
	p = subprocess.Popen(prog, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=DEVNULL)
	p.stdin.write(test.encode())
	p.stdin.close()
	p_res = p.stdout.read()
	p.stdout.close()
	p.terminate()
	p.wait()
	return p.returncode, p_res.decode().rstrip("\n")

def test_cmd(exe_path, test, noout, i):
	mini_code, mini_res = send_cmd(exe_path, test)
	bash_code, bash_res = send_cmd("bash", test)
	diff = col("Fail", "31")
	success = 0
	if mini_res == bash_res:
		success = 1
		diff = col("Success!", "32")
	if mini_code != bash_code:
		diff += " - " + col("Wrong exit code", "33")
	test = test.rstrip("\n")
	if noout:
		out = f"{col(f'Line {i + 1}: ', '1;31')}{test} {diff}"
	else:
		out = f"{col(f'Line {i + 1}: ', '1;31')}{test}\n{col('minishell: ', '31')}\n'{mini_res}'\n{col('exit code: ', '31')}{mini_code}\n{col('bash: ', '31')}\n'{bash_res}'\n{col('exit code: ', '31')}{bash_code}\n{diff}"
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
	noout = True
	interactive = False
	file_path = "new_minishell_tester/tests"
	exe_path = "./minishell"
	help_msg = "Usage: python3 tester.py [-io] [-exe executable_path] [tests_file] [file_line]\n -i:\t\tInteractive mode\n -o:\t\tPrint output of tests\n -exe path:\tPath to your minishell executable\n tests_file:\tPath to the text file containing the tests, one per line (default: \"./new_minishell_tester/tests\")\n file_line:\tTests only the specified line of the file specified by file path\n\nArguments don't have a specific order"
	if argc < 2:
		print(help_msg)
		exit(0)
	while i != argc:
		arg = str(sys.argv[i])
		if arg == "-h":
			print(help_msg)
			exit(0)
		elif arg == "-o":
			noout = False
		elif arg == "-i":
			interactive = True
		elif arg == "-exe":
			i += 1
			if i >= argc:
				error("Error: -exe flag requires one positional argument(path)")
			exe_path = str_to_path(sys.argv[i])
		elif arg.isdigit():
			single = int(arg) - 1
		else:
			file_path = str_to_path(arg)
		i += 1
	if not exists(file_path) or os.path.isdir(file_path) or os.access(file_path, os.X_OK):
		error("Error: '" + file_path + "' isn't a valid file")
	if not exists(exe_path) or os.path.isdir(exe_path) or not os.access(exe_path, os.X_OK):
		error("Error: '" + exe_path + "' isn't a valid file")
	print(file_path, exe_path)
	return noout, interactive, single, file_path, exe_path

def main():
	passed = 0
	tot = 0
	noout, interactive, single, file_path, exe_path = catch_args()
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
			passed += test_cmd(exe_path, test, noout, tot)
			tot += 1
	elif single != -1:
		passed = test_cmd(exe_path, tests[single], noout, single)
		tot += 1
	else:
		for i, test in enumerate(tests):
			passed += test_cmd(exe_path, test, noout, i)
			tot += 1
	print("\n" + col(str(passed) + "/" + str(tot) + " successful tests!", "35;1"))

if __name__ == "__main__":
	main()