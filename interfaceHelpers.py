def homepage(new=True):
    print(f"{'-'*80}\n\t\tWelcome to Boogle!\n{'-'*80}")
    userResponse = input("Search:\n")
    searchOut = search(userResponse)
    try:
        renderTemplate(result.html, searchOut)
    except:
        raise ValueError("html render error")

def returnHome(token):
    userDB.remove(token)
    renderTemplate(homepage())
