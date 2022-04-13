def who_deck(function):

    def wrapper(*args):
        print(f'------' + f'{args[1].__class__.__name__}' + f'------')
        function(*args)
        print(f'------' + f'{args[1].__class__.__name__}' + f'------')
    return wrapper
