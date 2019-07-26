import wptools

so = wptools.page('Stack Overflow').get_parse()

print(so.infobox)
