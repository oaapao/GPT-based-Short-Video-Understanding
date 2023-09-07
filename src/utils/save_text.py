def save_text_to_txt(content,filepath):
    with open(filepath,'w') as f:
        f.write(content)
    return 'ok'