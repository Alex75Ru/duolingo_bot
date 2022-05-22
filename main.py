from selenium import webdriver


driver = webdriver.Chrome()
url = 'https://en.duolingo.com/profile/'


def parser(base_url, name):
    """
    This function takes base_url and name user
    returns Total XP of user
    :param base_url:
    :param name:
    :return: {user: Total XP}
    """
    full_url = f"{base_url}{name}"
    driver.get(full_url)
    main_page = driver.page_source
    divs = main_page.split(">")
    for i in range(len(divs)):
        if "Total XP" in divs[i]:
            temp_str = divs[i-2]
            total = int(temp_str[:temp_str.find("<"):])
            print(total)
            return {name: total}


parser(url, "username")

