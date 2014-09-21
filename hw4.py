
# This is the main of the program.
if __name__ == "__main__":
    import urllib

    # Get article from web
    link = "http://en.wikipedia.org/wiki/Quantum_field_theory"
    f = urllib.urlopen(link)
    page = f.read()

    # process with Beautiful Soup 4
    # Note that I'm purposely ignoring headers of the wikipedia article
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page)

    str = ""
    def textOf(soup):
        return str.join(soup.findAll(text=True)).encode('ascii', 'ignore')

    visible_texts = [textOf(n) for n in soup.findAll(["p"])]
    visible_texts.pop() #trim off some junk at the end.  Could do with Beautiful soup patterns but this is just as easy

    #create one long string
    allimportanttext = "".join(visible_texts)

    #create alchemy reference and pass in our string representation of the article
    from alchemyapi import AlchemyAPI
    alchemyapi = AlchemyAPI()
    response = alchemyapi.keywords("text", allimportanttext)

    print('')
    print('## Top 10 Keywords ##')

    ## results come back ordered by relevance.  Print the top 10.
    index = 1;
    for keyword in response['keywords'][:10]:
        print(index)
        print('text: ', keyword['text'].encode('utf-8'))
        print('relevance: ', keyword['relevance'].encode('ascii', 'ignore'))
        print('')
        index = index+1

#         ## Top 10 Keywords ##
# 1
# ('text: ', 'quantum field theory')
# ('relevance: ', '0.961181')
#
# 2
# ('text: ', 'quantum field theories')
# ('relevance: ', '0.581799')
#
# 3
# ('text: ', 'quantum mechanics')
# ('relevance: ', '0.517841')
#
# 4
# ('text: ', 'electromagnetic field')
# ('relevance: ', '0.496985')
#
# 5
# ('text: ', 'classical field theory')
# ('relevance: ', '0.47389')
#
# 6
# ('text: ', 'particles')
# ('relevance: ', '0.440638')
#
# 7
# ('text: ', 'particle')
# ('relevance: ', '0.431834')
#
# 8
# ('text: ', 'quantum electromagnetic field')
# ('relevance: ', '0.431186')
#
# 9
# ('text: ', 'quantum states')
# ('relevance: ', '0.42829')
#
# 10
# ('text: ', 'relativistic quantum field')
# ('relevance: ', '0.42766')


