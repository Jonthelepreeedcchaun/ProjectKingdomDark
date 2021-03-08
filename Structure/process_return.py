def process_return(input):
    if input.shift and input.escape:
        return True
    if input.q and input.u and input.i and input.t:
        return True
