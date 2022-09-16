# New Minishell Tester
Welcome to the minishell tester, this script will make you test your minishell in a very fast and comprehensive manner with the standard mode, or in a more dynamic way, thanks to the interactive mode (-i).

## Run
To run this script you have to use the Python3 interpreter, launch this commands in the terminal to start the program

    git clone https://github.com/XEDGit/new_minishell_tester.git
    python3 new_minishell_tester/tester.py

## Flags (optional)
    -h:            Display help text
    -i:            Interactive mode
    -o:            Print output of tests
    -exe 'path':   Path to your minishell executable
    tests_file:    Path to the text file containing the tests, one per line (default: "./new_minishell_tester/tests")
    file_line:     Tests only the specified line of the file specified byt file path

## Troubleshooting
If the script reports any error, make sure to use the flag '-exe path' or write as a normal argument the path to the tests file
