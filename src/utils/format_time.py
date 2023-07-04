def format_time(time_str):
    time_splited = time_str.split(".")
    if len(time_splited) > 2:
        return f"{time_splited[0]}d {time_splited[1]}"
    else:
        return time_splited[0]
