def parse_input(user_input):
    """
    The function splits the input string into words, using a space as a separator.

    Parameters:
        user_input: entered string by user

    Returns:
        str, list: command and list of other arguments
    Raises:
        ValueError: if entered incorrect command
    """

    # try:
    #     cmd, *args = user_input.split()
    #     cmd = cmd.strip().lower()
    #     return cmd, args

    # except ValueError:
    #     return f'Enter correct command'
    
    try:
        if not user_input.strip():
            return "Enter correct command", []
        
        parts = user_input.strip().split()
        cmd = parts[0].strip().lower()
        args = parts[1:] if len(parts) > 1 else []
        
        return cmd, args

    except Exception:
        return "Enter correct command", []
    
   