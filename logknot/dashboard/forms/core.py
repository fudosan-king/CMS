def double(choices, *args):
    if len(args) == 0 and isinstance(choices, (list, tuple)):
        choices = choices
    else:
        choices = (choices,) + args

    return [(x, x) for x in choices]
