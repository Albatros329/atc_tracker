from colorama import init, Style

init(autoreset=True)

def gradient_text(text, start_color, end_color):
    """
    Generates a gradient-colored text string for terminal output.
    Args:
        text (str): The text to be colored.
        start_color (tuple): The RGB color tuple (R, G, B) for the start of the gradient.
        end_color (tuple): The RGB color tuple (R, G, B) for the end of the gradient.
    Returns:
        str: The text with gradient colors applied, formatted for terminal output.
    """


    if len(text) == 0: 
        return ""
    
    result = ""
    length = len(text)
    
    r_step = (end_color[0] - start_color[0]) / length
    g_step = (end_color[1] - start_color[1]) / length
    b_step = (end_color[2] - start_color[2]) / length
    
    for i, char in enumerate(text):
        r = int(start_color[0] + (r_step * i))
        g = int(start_color[1] + (g_step * i))
        b = int(start_color[2] + (b_step * i))
        
        result += f"\033[38;2;{r};{g};{b}m{char}"
    
    return result + Style.RESET_ALL