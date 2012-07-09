def clean_language_name(name):
    cleaned_name = name.split('; ')[0].split(', ')[0]
    if cleaned_name.endswith(' languages'):
        cleaned_name = cleaned_name.replace(' languages', '')
    return cleaned_name
