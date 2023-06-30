# New Minishell Tester (2022 subject)
Welcome to the minishell tester, this script will make you test your minishell in a very fast and comprehensive manner with the standard mode, or in a more dynamic way, thanks to the interactive mode (-i).

## Run
To run this script you have to use the Python3 interpreter

    python3 new_minishell_tester/tester.py [-o -err] tests_file [file_line] | -i [-o -err]
    
    tests_file:    Path to the text file containing the tests, one per line (default: "./new_minishell_tester/tests")
    file_line:     Tests only the specified line of the file specified byt file path [optional]

## Flags (optional)
    -h:            Display help text
    -i:            Interactive mode
    -o:            Print stdout of both minishell and bash
    -err:          Print stderr of both minishell and bash
    -exe 'path':   Path to your minishell executable

## Troubleshooting
If the script reports any error, make sure you're using the `-exe path` flag and you're specifying the `tests_file`

## Tests crowdsourcing
The tests file is a crowdsourced collection of command to challenge your minishell, if you have some ideas about what to add feel free to create a pull request
