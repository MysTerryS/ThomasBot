from wikipedia import set_lang, summary, search, DisambiguationError, PageError, page

set_lang("RU")

def GetInfoFromWiki(Query):
    print(Query)
    try:
        Result = summary(Query)
        Result = Result[:Result.find("\n")]
        if len(Result) != 0:
            Result = "{}\n{}".format(Result if Result[len(Result) - 1] == "." or Result[len(Result) - 1] == ":" else Result[:Result.rfind(".") + 1], page(Query).url)
        else:
            Result = "{}".format(page(Query).url)
        Result = Result if "{\displaystyle" not in Result else "{}".format(page(Query).url)
    except DisambiguationError:
        Search = search(Query)
        Search = Search if Query not in Search else Search[:Search.index(Query)] + Search[Search.index(Query) + 1:]
        Result = "По вашему запросу найдено:\n{}".format("\n".join(Search))
    except PageError:
        Result = "По вашему запросу ничего не найдено."
    return Result
